import json
import os
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.environ.get("DYNAMODB_ENDPOINT") or None
)
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def create_item(event, context):
    body = json.loads(event.get("body", "{}"))
    pk = body.get("PK", "default")
    table.put_item(Item={"PK": pk})
    print(f"Inserted item with PK={pk}")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Item created", "PK": pk})
    }


def queue_handler(event, context):
    for record in event["Records"]:
        print(f"SQS message body: {record['body']}")
    return {"statusCode": 200}


def s3_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"New object '{key}' uploaded to bucket '{bucket}'")
    return {"statusCode": 200}
