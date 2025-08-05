import json
import os
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.environ.get("DYNAMODB_ENDPOINT") or None
)
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def health_check(event, context):
    """
    Simple health check endpoint to validate lambda is working
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Lambda is working correctly",
            "status": "healthy",
            "timestamp": context.aws_request_id if context else "local"
        })
    }


def create_item(event, context):
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # Handle both string and dict body formats
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
        
        pk = body.get("PK", "default")
        print(f"Attempting to insert item with PK={pk}")
        
        table.put_item(Item={"PK": pk})
        print(f"Successfully inserted item with PK={pk}")
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Item created", "PK": pk})
        }
    except Exception as e:
        print(f"Error in create_item: {str(e)}")
        print(f"Event was: {json.dumps(event)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },  
            "body": json.dumps({"error": str(e)})
        }


def queue_handler(event, context):
    """
    Handle SQS messages
    """
    try:
        print(f"SQS event received: {json.dumps(event)}")
        
        if 'Records' not in event:
            print("No Records found in event")
            return {"statusCode": 400, "body": "No Records found"}
        
        processed_messages = []
        for record in event["Records"]:
            try:
                message_body = record.get('body', '')
                message_id = record.get('messageId', 'unknown')
                receipt_handle = record.get('receiptHandle', 'unknown')
                
                print(f"Processing SQS message ID: {message_id}")
                print(f"Message body: {message_body}")
                
                # Process the message here - you can add your business logic
                # For example, parse JSON if the message is JSON
                try:
                    if message_body:
                        parsed_body = json.loads(message_body)
                        print(f"Parsed message: {parsed_body}")
                except json.JSONDecodeError:
                    print(f"Message body is not valid JSON: {message_body}")
                
                processed_messages.append({
                    "messageId": message_id,
                    "status": "processed"
                })
                
            except Exception as e:
                print(f"Error processing individual SQS record: {str(e)}")
                processed_messages.append({
                    "messageId": record.get('messageId', 'unknown'),
                    "status": "failed",
                    "error": str(e)
                })
        
        print(f"Processed {len(processed_messages)} messages")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Processed {len(processed_messages)} SQS messages",
                "processed": processed_messages
            })
        }
        
    except Exception as e:
        print(f"Error in queue_handler: {str(e)}")
        print(f"Event was: {json.dumps(event)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def s3_handler(event, context):
    """
    Handle S3 events
    """
    try:
        print(f"S3 event received: {json.dumps(event)}")
        
        if 'Records' not in event:
            print("No Records found in event")
            return {"statusCode": 400, "body": "No Records found"}
        
        processed_objects = []
        for record in event["Records"]:
            try:
                # Extract S3 event information
                event_name = record.get('eventName', 'unknown')
                s3_info = record.get('s3', {})
                bucket_info = s3_info.get('bucket', {})
                object_info = s3_info.get('object', {})
                
                bucket_name = bucket_info.get('name', 'unknown')
                object_key = object_info.get('key', 'unknown')
                object_size = object_info.get('size', 0)
                
                print(f"S3 Event: {event_name}")
                print(f"Bucket: {bucket_name}")
                print(f"Object Key: {object_key}")
                print(f"Object Size: {object_size} bytes")
                
                # Process the S3 event here - you can add your business logic
                # For example, process uploaded files, trigger other workflows, etc.
                
                processed_objects.append({
                    "bucket": bucket_name,
                    "key": object_key,
                    "event": event_name,
                    "size": object_size,
                    "status": "processed"
                })
                
            except Exception as e:
                print(f"Error processing individual S3 record: {str(e)}")
                processed_objects.append({
                    "bucket": "unknown",
                    "key": "unknown",
                    "status": "failed",
                    "error": str(e)
                })
        
        print(f"Processed {len(processed_objects)} S3 objects")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Processed {len(processed_objects)} S3 events",
                "processed": processed_objects
            })
        }
        
    except Exception as e:
        print(f"Error in s3_handler: {str(e)}")
        print(f"Event was: {json.dumps(event)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
