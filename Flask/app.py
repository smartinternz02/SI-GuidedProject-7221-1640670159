import pandas as pd
import numpy as np
import pickle
import os
from flask import Flask, request, render_template

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
    model = pickle.loads(open('fdemand.pkl','rb').read())
    print(request.form.values())
    input_features = [float(x) for x in request.form.values()]
    feature_values = [np.array(input_features)]
    print(feature_values)

    prediction = model.predict(feature_values)
    output = prediction[0]
    print(output)
    return render_template('upload.html', prediction_text=output)

if __name__ == '__main__':
    app.run(debug=False)

