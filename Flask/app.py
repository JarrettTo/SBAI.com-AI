import sys
import os
from datetime import date
import json
from flask import Flask, render_template, request, jsonify
from flask import current_app
from functools import lru_cache
from threading import Thread
from flask_mysqldb import MySQL
import requests
import json
from datetime import datetime
import logging

main_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
sys.path.append(os.path.dirname(main_py_path))
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
from main import server_predict, train_models, update_data

app = Flask(__name__)
app.config['MYSQL_HOST'] = '54.183.200.189'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jiustudios'
app.config['MYSQL_DB'] = 'sbai'
mysql = MySQL(app)

@app.route("/")
def index():
    return "hello"

def run_prediction():
    # This function will run the long process in the background.
    with app.app_context():
        res = server_predict()
        print("Prediction complete:", res)

@app.route("/predict") 
def predict():
    thread = Thread(target=run_prediction)
    thread.start()
    # Immediately respond to the request indicating that processing has started.
    return "Prediction process started!"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
