import json
import pandas as pd
import boto3 
from boto3.dynamodb.conditions import Key, Attr
import os
from datetime import datetime, timedelta
from forecast import Forecast

dynamodb = boto3.resource("dynamodb",
                         aws_access_key_id="AKIAQGQSULZCBGXZDZPD",
                         aws_secret_access_key="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")
#aqiTable = dynamodb.Table(os.getenv("TRANSFORMED_TABLE_NAME"))
aqiTable = dynamodb.Table("TransformedDataTable")

def fetchData(startTime, endTime):
    response = aqiTable.scan(
    FilterExpression=Attr('Date-Time').gte(startTime) & Attr('Date-Time').lte(endTime)
    )
    print(response["Items"])
    dataFrame = pd.DataFrame(response["Items"])
    # dataFrame.index = pd.to_datetime(dataFrame['Date-Time'])
    # dataFrame.drop(['Date-Time'],axis=1, inplace=True)
    # dataFrame.sort_index(inplace=True)
    # dataFrame = dataFrame[['PM2.5', 'PM10',	'NO', 'NO2', 'NOx', 'NH3' ,	'CO', 'SO2', 'O3', 'AQI']]
    # dataFrame = dataFrame.astype('float')
    return dataFrame

def lambda_handler():
    endTime = datetime.now().strftime("%Y-%m-%d %H:00:00")
    startTime = (datetime.now() - timedelta(hours=17)).strftime("%Y-%m-%d %H:00:00")
    print(startTime)
    print(endTime)
    data = fetchData(startTime, endTime)
    # model = Forecast(data)
    # model.process_data()
    # forecasts = model.forecast_next()
    # return {
    #     "result":forecasts,
    #     "endTime": endTime
    # }

lambda_handler()

