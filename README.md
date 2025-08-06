# serverless-python-demo

## Quick-start workflow

All local services run inside Docker containers. Yarn scripts handle setup and teardown.

### Install dependencies

I prefer to use `yarn` because of faster install. `npm` takes much time.

```bash
# if yarn is not installed
npm install -g yarn

yarn install
```

### Start local AWS emulators

```bash
yarn dev:prepare
```

### Run Serverless Offline

```bash
yarn dev:start
```

### Run manual tests

After running the system properly testing is critial to understand the structure.

#### Health Endpoint Handler

```bash
# get api gateway id
aws --endpoint-url=http://localhost:4566 apigateway get-rest-apis | jq '.items[0].id'

curl -X GET "http://localhost:4566/restapis/<api-gateway-id>/dev/_user_request_/health"

curl -X POST "http://localhost:4566/restapis/<api-gateway-id>/dev/_user_request_/" -H "Content-Type: application/json" -d '{"test": "data"}'
```

#### SQS Handler

```bash
aws --endpoint-url=http://localhost:4566 sqs list-queues

aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/main-queue" --message-body "Test message"

npx serverless logs --function sqs_handler --stage dev

for i in {1..100}; do aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/main-queue" --message-body "$i. test message - SQS integration works!"; done

```

```bash
npx serverless logs --function sqs_handler --stage dev --tail
```

#### Scheduled Handler

```bash
npx serverless logs --function scheduled_handler --stage dev
```

#### S3 Handler

```bash
echo "This is a test file for S3 handler" > test-file.txt

aws --endpoint-url=http://localhost:4566 s3 cp test-file.txt s3://main-bucket/

npx serverless logs --function s3_handler --stage dev

rm test-file.txt
```

#### DynamoDB Stream Handler

```bash
aws dynamodb put-item --table-name main-table --item '{"PK":{"S":"USER#stream-test"},"SK":{"S":"PROFILE#stream-test-1"},"data":{"S":"Initial data for stream testing"},"timestamp":{"S":"2025-01-06T02:36:00Z"}}' --endpoint-url http://localhost:4566

aws dynamodb put-item --table-name main-table --item '{"PK":{"S":"USER#stream-test"},"SK":{"S":"PROFILE#stream-test-1"},"data":{"S":"Updated data after stream testing modification"},"timestamp":{"S":"2025-01-06T02:37:00Z"},"lastModified":{"S":"2025-01-06T02:37:00Z"}}' --endpoint-url http://localhost:4566

npx serverless logs --function dynamodb_stream_handler --stage dev
```

```bash
aws dynamodb delete-item --table-name main-table --key '{"PK":{"S":"USER#stream-test"},"SK":{"S":"PROFILE#stream-test-1"}}' --endpoint-url http://localhost:4566

npx serverless logs --function dynamodb_stream_handler --stage dev --tail
```

### Tear everything down when finished

```bash
yarn dev:clean
```
