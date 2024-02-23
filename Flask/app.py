import sys
import os
from datetime import date
import json
from flask import Flask, render_template, request
from functools import lru_cache


main_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
sys.path.append(os.path.dirname(main_py_path))

from main import server_predict

app = Flask(__name__)

@app.route("/")
def index():
    

    return "hello"

@app.route("/predict") 
def predict():
    print("LOL")
    res=server_predict()
    return res

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
