from tensorflow.keras.models import load_model
from pickle import load
import numpy as np
import pandas as pd
from tsmoothie.smoother import KalmanSmoother

class ForecastModel: 
    def __init__(self):        
        self.model = load_model("./Artefacts/model-v01.h5")
        self.scalerX = load(open("./Artefacts/scalerX.pkl","rb"))
        self.scalerY = load(open("./Artefacts/scalerY.pkl","rb"))
        self.smoother = KalmanSmoother(component='level_longseason', 
                          component_noise={'level':0.1, 'longseason':0.1}, 
                          n_longseasons=365*24)


    def process_data(self, data):        
        self.smoother.smooth(data.T)
        for i,name in enumerate(data.columns):
            data[name] = self.smoother.smooth_data[i]
        data[data.columns[:-1]] = self.scalerX.transform(data[data.columns[:-1]])
        data[['AQI']] = self.scalerY.transform(data[['AQI']])
        return data.values

    def forecast_next(self, data: np.array):
        data = data[-15:]
        data = np.expand_dims(data, axis=0)   
        forecasts = self.model.predict(data)
        forecasts = self.scalerY.inverse_transform(forecasts)[0]   
        return forecasts.reshape(1,3)[0]