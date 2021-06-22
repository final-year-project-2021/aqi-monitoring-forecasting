import boto3
from datetime import datetime, timedelta
import os
from transform import transform
from decimal import Decimal
import json

dynamodb = boto3.resource("dynamodb")
rawTable = dynamodb.Table(os.getenv("RAW_TABLE_NAME"))
transformedTable = dynamodb.Table(os.getenv("TRANSFORMED_TABLE_NAME"))

def batch_insert(data:list):
    with transformedTable.batch_writer() as batch:
        for d in data:
            d = json.loads(json.dumps(d), parse_float=Decimal)
            batch.put_item(Item=d)

def lambda_handler(event, context):
    endTime = datetime.now().strftime("%d-%b-%Y %H:00:00")
    startTime = (datetime.now() - timedelta(hours=24)).strftime("%d-%b-%Y %H:00:00")
    data = transform(rawTable, startTime, endTime)
    batch_insert(data)