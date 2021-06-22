import pandas as pd
from datetime import datetime
import json  
from boto3.dynamodb.conditions import Key, Attr

def get_PM25_subindex(x):
    if x <= 30:
        return x * 50 / 30
    elif x <= 60:
        return 50 + (x - 30) * 50 / 30
    elif x <= 90:
        return 100 + (x - 60) * 100 / 30
    elif x <= 120:
        return 200 + (x - 90) * 100 / 30
    elif x <= 250:
        return 300 + (x - 120) * 100 / 130
    elif x > 250:
        return 400 + (x - 250) * 100 / 130
    else:
        return 0
    
def get_PM10_subindex(x):
    if x <= 50:
        return x
    elif x <= 100:
        return x
    elif x <= 250:
        return 100 + (x - 100) * 100 / 150
    elif x <= 350:
        return 200 + (x - 250)
    elif x <= 430:
        return 300 + (x - 350) * 100 / 80
    elif x > 430:
        return 400 + (x - 430) * 100 / 80
    else:
        return 0
    
def get_SO2_subindex(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 380:
        return 100 + (x - 80) * 100 / 300
    elif x <= 800:
        return 200 + (x - 380) * 100 / 420
    elif x <= 1600:
        return 300 + (x - 800) * 100 / 800
    elif x > 1600:
        return 400 + (x - 1600) * 100 / 800
    else:
        return 0
    
def get_NOx_subindex(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 180:
        return 100 + (x - 80) * 100 / 100
    elif x <= 280:
        return 200 + (x - 180) * 100 / 100
    elif x <= 400:
        return 300 + (x - 280) * 100 / 120
    elif x > 400:
        return 400 + (x - 400) * 100 / 120
    else:
        return 0
    

def get_NH3_subindex(x):
    if x <= 200:
        return x * 50 / 200
    elif x <= 400:
        return 50 + (x - 200) * 50 / 200
    elif x <= 800:
        return 100 + (x - 400) * 100 / 400
    elif x <= 1200:
        return 200 + (x - 800) * 100 / 400
    elif x <= 1800:
        return 300 + (x - 1200) * 100 / 600
    elif x > 1800:
        return 400 + (x - 1800) * 100 / 600
    else:
        return 0
    
def get_CO_subindex(x):
    if x <= 1:
        return x * 50 / 1
    elif x <= 2:
        return 50 + (x - 1) * 50 / 1
    elif x <= 10:
        return 100 + (x - 2) * 100 / 8
    elif x <= 17:
        return 200 + (x - 10) * 100 / 7
    elif x <= 34:
        return 300 + (x - 17) * 100 / 17
    elif x > 34:
        return 400 + (x - 34) * 100 / 17
    else:
        return 0
    
def get_O3_subindex(x):
    if x <= 50:
        return x * 50 / 50
    elif x <= 100:
        return 50 + (x - 50) * 50 / 50
    elif x <= 168:
        return 100 + (x - 100) * 100 / 68
    elif x <= 208:
        return 200 + (x - 168) * 100 / 40
    elif x <= 748:
        return 300 + (x - 208) * 100 / 539
    elif x > 748:
        return 400 + (x - 400) * 100 / 539
    else:
        return 0

def transform(rawTable, startTime, endTime):
    
    response = rawTable.scan(
    FilterExpression=Attr('Date-Time').gte(startTime) & Attr('Date-Time').lte(endTime)
    )
    dataFrame = pd.DataFrame(response["Items"])
    dataFrame.index = pd.to_datetime(dataFrame['Date-Time'])
    dataFrame.drop(['Date-Time'],axis=1, inplace=True)
    dataFrame.sort_index(inplace=True)
    dataFrame.rename(columns={"Ozone": "O3"}, inplace=True)
    dataFrame = dataFrame.astype('float')
    

    aqiData = dataFrame.copy()
    aqiData["PM10_24hr_avg"] = aqiData["PM10"].rolling(window = 24, min_periods = 16).mean().values
    aqiData["PM2.5_24hr_avg"] = aqiData["PM2.5"].rolling(window = 24, min_periods = 16).mean().values
    aqiData["SO2_24hr_avg"] = aqiData["SO2"].rolling(window = 24, min_periods = 16).mean().values
    aqiData["NOx_24hr_avg"] = aqiData["NOx"].rolling(window = 24, min_periods = 16).mean().values
    aqiData["NH3_24hr_avg"] = aqiData["NH3"].rolling(window = 24, min_periods = 16).mean().values
    aqiData["CO_8hr_max"] = aqiData["CO"].rolling(window = 8, min_periods = 1).max().values
    aqiData["O3_8hr_max"] = aqiData["O3"].rolling(window = 8, min_periods = 1).max().values


    aqiData["PM2.5_SubIndex"] = aqiData["PM2.5_24hr_avg"].apply(lambda x: get_PM25_subindex(x))
    aqiData["PM10_SubIndex"] = aqiData["PM10_24hr_avg"].apply(lambda x: get_PM10_subindex(x))
    aqiData["SO2_SubIndex"] = aqiData["SO2_24hr_avg"].apply(lambda x: get_SO2_subindex(x))
    aqiData["NOx_SubIndex"] = aqiData["NOx_24hr_avg"].apply(lambda x: get_NOx_subindex(x))
    aqiData["NH3_SubIndex"] = aqiData["NH3_24hr_avg"].apply(lambda x: get_NH3_subindex(x))
    aqiData["CO_SubIndex"] = aqiData["CO_8hr_max"].apply(lambda x: get_CO_subindex(x))
    aqiData["O3_SubIndex"] = aqiData["O3_8hr_max"].apply(lambda x: get_O3_subindex(x))

    aqiData["AQI"] = round(aqiData[["PM2.5_SubIndex", "PM10_SubIndex", "SO2_SubIndex", "NOx_SubIndex",
                                    "NH3_SubIndex", "CO_SubIndex", "O3_SubIndex"]].max(axis = 1))

    transformedData = aqiData[['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'AQI']]
    transformedData.reset_index(level=0, inplace=True)
    transformedData['Date-Time'] = aqiData.index
    transformedData['Date-Time'] = transformedData['Date-Time'].astype(str)

    return transformedData[-10:].to_dict('records')