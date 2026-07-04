import boto3
import time

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChatMessages")

def lambda_handler(event, context):
    route = event["requestContext"]["routeKey"]

    if route == "sendMessage":
        body = json.loads(event.get("body", "{}"))

        table.put_item(Item={
            "room_id": "global",
            "timestamp": int(time.time()),
            "sender": body.get("sender"),
            "message": body.get("message")
        })

    return {"statusCode": 200}
