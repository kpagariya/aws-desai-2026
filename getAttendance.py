import json
import boto3
from decimal import Decimal

table = boto3.resource('dynamodb').Table('Attendance')

def decimal_to_int(obj):
    if isinstance(obj, list):
        return [decimal_to_int(i) for i in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_int(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj)
    return obj

def lambda_handler(event, context):
    data = table.scan()["Items"]
    clean_data = decimal_to_int(data)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(clean_data)
    }
