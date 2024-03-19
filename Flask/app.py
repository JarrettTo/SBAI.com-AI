import sys
import os
from datetime import date
import json
from flask import Flask, render_template, request
from functools import lru_cache
from threading import Thread
import logging

main_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
sys.path.append(os.path.dirname(main_py_path))
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
from main import server_predict, train_models, update_data

app = Flask(__name__)
def update_data_background():
    logging.info("Starting update_data task")
    update_data()
    logging.info("update_data task finished")


@app.route("/")
def index():
    

    return "hello"

@app.route("/predict") 
def predict():
    print("LOL")
    res=server_predict()
    return res

@app.route("/train") 
def train():
    res1 = update_data()
    res2 = train_models()
    return res1 + res2

@app.route("/update_data") 
def update_data_route():
    thread = Thread(target=update_data_background)
    thread.start()
    return 'Update in progress'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
