import json
import pandas as pd
import boto3 
from boto3.dynamodb.conditions import Key, Attr
import os
from datetime import datetime, timedelta
from forecast import Forecast
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")

aqiTable = dynamodb.Table(os.getenv("TRANSFORMED_TABLE_NAME"))
forecastTable = dynamodb.Table("FORECAST_TABLE_NAME")

def fetchData(startTime, endTime):
    response = aqiTable.scan(
    FilterExpression=Attr('Date-Time').gte(startTime) & Attr('Date-Time').lte(endTime)
    )
    
    dataFrame = pd.DataFrame(response["Items"])
    dataFrame.index = pd.to_datetime(dataFrame['Date-Time'])
    dataFrame.drop(['Date-Time'],axis=1, inplace=True)
    dataFrame.sort_index(inplace=True)
    dataFrame = dataFrame[['PM2.5', 'PM10',	'NO', 'NO2', 'NOx', 'NH3' ,	'CO', 'SO2', 'O3', 'AQI']]
    dataFrame = dataFrame.astype('float')
    return dataFrame

def lambda_handler(event, context):
    endTime = datetime.now().strftime("%Y-%m-%d %H:00:00")
    startTime = (datetime.now() - timedelta(hours=17)).strftime("%Y-%m-%d %H:00:00")    
    data = fetchData(startTime, endTime)   
    time = data.index[-1:][0]
    
    model = Forecast(data)
    model.process_data()
    forecasts = model.forecast_next()    
    results = []
    for c,i in enumerate(forecasts):
        res = {}
        res["Date-Time"]=(time + timedelta(hours=c+1)).strftime("%Y-%m-%d %H:00:00")
        res["Forecast-AQI"]=int(round(i))
        results.append(res)
    
    with forecastTable.batch_writer() as batch:
        for item in results:
            #data = json.loads(json.dumps(i), parse_float=Decimal)
            batch.put_item(Item = item)



