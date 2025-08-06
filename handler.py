import time
from typing import Any, Dict


def main_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    print("⚙️ main_handler ⚙️")
    print("🙌 event:", event)
    print("📚 context:", context)

    return {
        "statusCode": 200,
        "body": '{"message": "Hello from main handler!", "method": "'
        + event.get("httpMethod", "UNKNOWN")
        + '"}',
        "headers": {"Content-Type": "application/json"},
    }


def health_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    print("⚙️ health_handler ⚙️")
    print("🙌 event:", event)
    print("📚 context:", context)

    return {
        "statusCode": 200,
        "body": '{"status": "healthy", "timestamp": "' + str(int(time.time())) + '"}',
        "headers": {"Content-Type": "application/json"},
    }


def scheduled_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    print("⚙️ scheduled_handler ⚙️")
    print("🙌 event:", event)
    print("📚 context:", context)

    return {"statusCode": 200}


def sqs_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    print("⚙️ sqs_handler ⚙️")
    print("🙌 event:", event)
    print("📚 context:", context)

    for record in event["Records"]:
        message_body = record["body"]
        receipt_handle = record["receiptHandle"]
        queue_name = record["eventSourceARN"].split(":")[-1]

        print(f"📩 Processing message from queue '{queue_name}': {message_body}")
        print(f"🏷️ Receipt Handle: {receipt_handle}")

        time.sleep(2)

    return {"statusCode": 200}


def dynamodb_stream_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    print("⚙️ dynamodb_stream_handler ⚙️")
    print("🙌 event:", event)
    print("📚 context:", context)

    for record in event["Records"]:
        event_name = record["eventName"]  # INSERT, MODIFY, REMOVE
        table_name = record["eventSourceARN"].split("/")[1]
        
        print(f"📝 DynamoDB Event: {event_name} in table '{table_name}'")
        
        if "dynamodb" in record:
            # Print old image (for MODIFY and REMOVE)
            if "OldImage" in record["dynamodb"]:
                print("🔙 Old Image:", record["dynamodb"]["OldImage"])
            
            # Print new image (for INSERT and MODIFY)
            if "NewImage" in record["dynamodb"]:
                print("🆕 New Image:", record["dynamodb"]["NewImage"])
            
            # Print keys
            if "Keys" in record["dynamodb"]:
                print("🔑 Keys:", record["dynamodb"]["Keys"])

    return {"statusCode": 200}


def s3_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    print("⚙️ s3_handler ⚙️")
    print("🙌 event:", event)
    print("📚 context:", context)

    for record in event["Records"]:
        filename = record["s3"]["object"]["key"]
        filesize = record["s3"]["object"]["size"]

        print(f"New object has been created {filename} ({filesize} bytes)")

    return {"statusCode": 200}
