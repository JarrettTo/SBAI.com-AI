import sys
import os
from datetime import date
import json
from flask import Flask, render_template, request
from functools import lru_cache
import subprocess
import re
import time

main_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
sys.path.append(os.path.dirname(main_py_path))

from main import server_predict

def fetch_game_data(sportsbook="fanduel"):
    main_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
    cmd = ["python3", main_py_path, "-xgb", f"-odds={sportsbook}"]
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        stdout = process.stdout
        stderr = process.stderr

        data_re = re.compile(r'\n(?P<home_team>[\w ]+)(\((?P<home_confidence>[\d+\.]+)%\))? vs (?P<away_team>[\w ]+)(\((?P<away_confidence>[\d+\.]+)%\))?: (?P<ou_pick>OVER|UNDER) (?P<ou_value>[\d+\.]+) (\((?P<ou_confidence>[\d+\.]+)%\))?', re.MULTILINE)
        ev_re = re.compile(r'(?P<team>[\w ]+) EV: (?P<ev>[-\d+\.]+)', re.MULTILINE)
        odds_re = re.compile(r'(?P<away_team>[\w ]+) \((?P<away_team_odds>-?\d+)\) @ (?P<home_team>[\w ]+) \((?P<home_team_odds>-?\d+)\)', re.MULTILINE)
        games = {}
        for match in data_re.finditer(stdout):
            game_dict = {'away_team': match.group('away_team').strip(),
                         'home_team': match.group('home_team').strip(),
                         'away_confidence': match.group('away_confidence'),
                         'home_confidence': match.group('home_confidence'),
                         'ou_pick': match.group('ou_pick'),
                         'ou_value': match.group('ou_value'),
                         'ou_confidence': match.group('ou_confidence')}
            for ev_match in ev_re.finditer(stdout):
                if ev_match.group('team') == game_dict['away_team']:
                    game_dict['away_team_ev'] = ev_match.group('ev')
                if ev_match.group('team') == game_dict['home_team']:
                    game_dict['home_team_ev'] = ev_match.group('ev')
            for odds_match in odds_re.finditer(stdout):
                if odds_match.group('away_team') == game_dict['away_team']:
                    game_dict['away_team_odds'] = odds_match.group('away_team_odds')
                if odds_match.group('home_team') == game_dict['home_team']:
                    game_dict['home_team_odds'] = odds_match.group('home_team_odds')

            print(json.dumps(game_dict, sort_keys=True, indent=4))
            games[f"{game_dict['away_team']}:{game_dict['home_team']}"] = game_dict
        
        return games

    except subprocess.CalledProcessError as e:
        # Handle the error, print stderr or raise the exception
        print(f"Error executing command: {e}")
        print(f"Command output (stdout): {e.stdout}")
        print(f"Command error (stderr): {e.stderr}")
        return {}

def get_ttl_hash(seconds=600):
    """Return the same value within `seconds` time period"""
    return round(time.time() / seconds)

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

@lru_cache()
def fetch_fanduel(ttl_hash=None):
    del ttl_hash
    return fetch_game_data(sportsbook="fanduel")

@lru_cache()
def fetch_draftkings(ttl_hash=None):
    del ttl_hash
    return fetch_game_data(sportsbook="draftkings")

@lru_cache()
def fetch_betmgm(ttl_hash=None):
    del ttl_hash
    return fetch_game_data(sportsbook="betmgm")

@app.route("/")
def index():
    return server_predict()

@app.route("/predict", methods=["GET"]) 
def predict():
    return server_predict()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
