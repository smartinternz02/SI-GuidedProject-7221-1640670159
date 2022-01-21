import pandas as pd
import numpy as np
import pickle
import os
from flask import Flask, request, render_template
import requests
import json

API_KEY = "0g8EEir-JE-uku8GIAglfyzHHydcw4mtwDWEQCxe9Iea"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/pred',methods=['GET'])
def pred():
    return render_template('upload.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    print('[INFO] loading model...')
    print(request.form.values())
    input_features = [[float(x) for x in request.form.values()]]
    payload_scoring = {"input_data": [{"field": [['x1','x2','x3','x4','x5','x6','x7']], "values": input_features}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6446cb28-8507-477a-8ff2-9e594bce31ed/predictions?version=2022-01-21', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    output = predictions['predictions'][0]['values'][0][0]
    print(output)
    return render_template('upload.html', prediction_text=output)

if __name__ == '__main__':
    app.run(debug=False)

