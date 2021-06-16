import json
from webscrap import scrapper
from decimal import Decimal
import boto3, os


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("TABLE_NAME"))

def lambda_handler():
    res_list = scrapper()
    with table.batch_writer() as batch:
        for i in range(4):
            data = json.loads(json.dumps(res_list[i]), parse_float=Decimal)
            batch.put_item(Item = data)
