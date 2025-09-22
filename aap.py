import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
aap = application  # For AWS compatibility

# Load the pre-trained model and scaler
#load the regressor and StandardScaler

ridge_model = pickle.load(open('Models/ridge.pkl', 'rb'))
Standard_Scaler_pickle = pickle.load(open('Models/scaler.pkl', 'rb'))


# Route for the home page
@aap.route('/')

def index():
    return render_template('index.html')

@aap.route('/predictdata', methods=['GET','POST'])

def predict_datapoint():
    if request.method == 'POST':
        Temperature = float(request.form['Temperature'])
        RH = float(request.form['RH'])
        Ws = float(request.form['Ws'])
        Rain = float(request.form['Rain'])
        FFMC = float(request.form['FFMC'])
        DMC = float(request.form['DMC'])
        ISI = float(request.form['ISI'])
        Classes = float(request.form['Classes'])
        Region = float(request.form['Region'])

        new_data_scaled = Standard_Scaler_pickle.transform([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]])
        result = ridge_model.predict(new_data_scaled)

        return render_template('home.html',result = result[0])
    else:
        return render_template('home.html')



if __name__ == "__main__":
    aap.run(debug=True)