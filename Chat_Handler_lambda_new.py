import json
import boto3
import time

dynamodb = boto3.resource("dynamodb")
messages = dynamodb.Table("ChatMessages")
connections = dynamodb.Table("ChatConnections")

def lambda_handler(event, context):
    route = event["requestContext"]["routeKey"]
    connection_id = event["requestContext"]["connectionId"]

    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]

    api = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=f"https://{domain}/{stage}"
    )

    if route == "$connect":
        connections.put_item(Item={"connection_id": connection_id})

    elif route == "$disconnect":
        connections.delete_item(Key={"connection_id": connection_id})

    elif route == "sendMessage":
        body = json.loads(event.get("body", "{}"))

        sender = body.get("sender")
        message = body.get("message")

        messages.put_item(Item={
            "room_id": "global",
            "timestamp": int(time.time()),
            "sender": sender,
            "message": message
        })

        all_connections = connections.scan()["Items"]

        for conn in all_connections:
            try:
                api.post_to_connection(
                    ConnectionId=conn["connection_id"],
                    Data=json.dumps({
                        "sender": sender,
                        "message": message
                    }).encode()
                )
            except:
                connections.delete_item(
                    Key={"connection_id": conn["connection_id"]}
                )

    return {"statusCode": 200}
