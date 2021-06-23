import json
import sys
import os
from webscrap import scrapper
from decimal import Decimal
import boto3, os


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("RAW_TABLE_NAME"))

def lambda_handler(event, context):
    res_list = scrapper()
    with table.batch_writer() as batch:
        for i in res_list:
            data = json.loads(json.dumps(i), parse_float=Decimal)
            batch.put_item(Item = data)
    
