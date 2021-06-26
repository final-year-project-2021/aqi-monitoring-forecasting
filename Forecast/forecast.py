from pickle import load
from tensorflow.keras.models import load_model
from tsmoothie.smoother import KalmanSmoother
import numpy as np



class Forecast:
    def __init__(self, data):
        self.scalerX = load(open("./Artefacts/scalerX.pkl","rb"))
        self.scalerY = load(open("./Artefacts/scalerY.pkl","rb"))        
        self.model = load_model("./Artefacts/model-v01.h5")
        self.smoother = KalmanSmoother(component='level_longseason', 
                          component_noise={'level':0.1, 'longseason':0.1}, 
                          n_longseasons=365*24)
        self.data = data

    def process_data(self):
        self.smoother.smooth(self.data.T)
        for i,name in enumerate(self.data.columns):
            self.data[name] = self.smoother.smooth_data[i]
        self.data[self.data.columns[:-1]] = self.scalerX.transform(self.data[self.data.columns[:-1]])
        self.data[['AQI']] = self.scalerY.transform(self.data[['AQI']])
        

    def forecast_next(self):
        data = self.data.values[-15:]
        data = np.expand_dims(data, axis=0)   
        forecasts = self.model.predict(data)
        forecasts = self.scalerY.inverse_transform(forecasts)[0]   
        return forecasts.reshape(1,3)[0]
        