# API conect HTML - GeoRef and Predeict (USE: python -m http.server)

## Dependencies and Setup
import pandas as pd
import numpy as np
import requests
import scipy.stats as stats
import json
from flask import Flask, jsonify, render_template, request, url_for
import joblib
#from geopy.geocoders import Nominatim

# Google developer API key
from api_keys_all import google_api_key
  
## 

app = Flask(__name__)

#Call Models:
model_cdmx = joblib.load('cdmx_72.sav')

model_gdl = joblib.load('gdl_81.sav')

model_mty = joblib.load('mty_80.sav')

#Call Scalers:
X_Scaler_cdmx = joblib.load('X_scaler_cdmx.sav')
y_Scaler_cdmx = joblib.load('y_scaler_cdmx.sav')

X_Scaler_gdl = joblib.load('X_scaler_gdl.sav')
y_Scaler_gdl = joblib.load('y_scaler_gdl.sav')

X_Scaler_mty = joblib.load('X_scaler_mty.sav')
y_Scaler_mty = joblib.load('y_scaler_mty.sav')

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    "Rutas disponibles:"
    "https://wakamol-e-lab-demo-day.herokuapp.com/predict/<room>/<bathroom>/<construction>/<terrain>/<direction>/<casa>/<casa_en_c>/<depto>/<nuevo>/<remate>"
    
    return render_template('index.html')
    
#################################################
#@app.route('/predict/<room>/<bathroom>/<construction>/<terrain>/<direction>/<casa>/<casa_en_c>/<depto>/<nuevo>/<remate>', methods=['GET'])
@app.route('/predict/<room>/<bathroom>/<construction>/<terrain>/<direction>/<casa>/<casa_en_c>/<depto>/<nuevo>/<remate>')
def predict(room, bathroom, construction, terrain, direction, casa, casa_en_c, depto, nuevo, remate):
    print("entró a la ruta")
    # Datos Dummy:
    ###### 
    # http://127.0.0.1:5000/predict/2/1/80/80/Parque%Espa%C3%B1a%20la%Condesa/0/0/1/1/0
    
    # Búsqueda
    ## Function: Locate address
    # Build URL using the Google Maps API
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    print(base_url)
    params = {"address": direction, "key": google_api_key}
    print(params)
    #loop to get all locations from locaitions
    lat = []
    lon = []
    
    try:
        response = requests.get(base_url, params={"address": direction,"key": google_api_key})
        print(response)
        geo      = response.json()
        lat.append(geo["results"][0]["geometry"]["location"]["lat"])
        lon.append(geo["results"][0]["geometry"]["location"]["lng"])
        print(lat)
        print(lon)
        
    except (KeyError, IndexError):
        notfound.append(index)
       
    # Revisamos que coordenadas esten en los tres casos posibles: ZMVM, MTY, GDL
    if (lat[0] > 19.1) & (lat[0] < 19.8) & (lon[0] > - 99.4) & (lon[0] < - 98.8):
        
        # Modelo CDMX + Estado de México
        float_features = [room, bathroom, construction, terrain, lon[0], lat[0], nuevo, remate, casa, casa_en_c, depto]
        print(float_features)
        for i, item in enumerate(float_features):
            float_features[i] = float(item)
        print(float_features)
        float_features = np.array(float_features).reshape(1, -1)
        print(float_features)
        #float_features= X_Scaler_cdmx.fit(float_features)
        #print(float_features)
        #float_features = X_Scaler_cdmx.transform(float_features)
        #float_features1 = X_Scaler_cdmx.fit(float_features).transform(float_features)
        float_features = np.array(np.array(float_features - X_Scaler_cdmx.mean_) / X_Scaler_cdmx.scale_)
        print(float_features)
        prediction = model_cdmx.predict(float_features)
        print(prediction)
        #prediction = y_Scaler_cdmx.inverse_transform(prediction)
        prediction = (prediction * y_Scaler_cdmx.scale_) + y_Scaler_cdmx.mean_
        print(prediction)
        
        output = round(prediction[0], 0)
        print(output)
        
    elif (lat[0] > 20.39) & (lat[0] < 20.82) & (lon[0] > - 103.59) & (lon[0] < - 103.18):
        
        # Modelo GDL
        float_features = [room, bathroom, construction, terrain, lon[0], lat[0], nuevo, remate, casa, casa_en_c, depto]
        for i, item in enumerate(float_features):
            float_features[i] = float(item)
        float_features = np.array(float_features).reshape(1, -1)
        #float_features = X_Scaler_gdl.transform(float_features)
        #float_features = (float_features - X_Scaler_gdl.mean_) / X_Scaler_gdl.scale_
        float_features = np.array(np.array(float_features - X_Scaler_gdl.mean_) / X_Scaler_gdl.scale_)
        prediction = model_gdl.predict(float_features)
        #prediction = y_Scaler_gdl.inverse_transform(prediction)
        prediction = (prediction * y_Scaler_gdl.scale_) + y_Scaler_gdl.mean_
        
        output = round(prediction[0], 0)
        
    elif (lat[0] > 25.51) & (lat[0] < 25.85) & (lon[0] > - 100.53) & (lon[0] < - 100.07):
        
        # Modelo MTY
        float_features = [room, bathroom, construction, terrain, lon[0], lat[0], nuevo, remate, casa, casa_en_c, depto]
        for i, item in enumerate(float_features):
            float_features[i] = float(item)
        float_features = np.array(float_features).reshape(1, -1)
        #float_features = X_Scaler_mty.transform(float_features)
        #float_features = (float_features - X_Scaler_mty.mean_) / X_Scaler_mty.scale_
        float_features = np.array(np.array(float_features - X_Scaler_mty.mean_) / X_Scaler_mty.scale_)
        prediction = model_mty.predict(float_features)
        #prediction = y_Scaler_mty.inverse_transform(prediction)
        prediction = (prediction * y_Scaler_mty.scale_) + y_Scaler_mty.mean_
        
        output = round(prediction[0], 0)
    
    else:
        output = 0
    
    # Return
    
    #return jsonify(output, lon, lat)
    print(output)
    return jsonify(output)

#################################################

if __name__ == "__main__":
    app.run(debug=True)
    
#