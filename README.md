# serverless-python-demo

## Quick‑start workflow

This workflow avoids installing local JARs or standalone emulators; all infrastructure services run inside disposable Docker containers, while Serverless Framework manages the Lambda code and HTTP emulation.

### Install dependencies

```bash
npm install
```

### Spin up Dockerised emulators

```bash
npm run setup:sqs          # ElasticMQ
npm run setup:dynamodb     # DynamoDB Local
npm run dynamodb-admin     # optional UI at http://localhost:8001
```

### Run Serverless Offline

```bash
npm run dev
```

### Run manual tests

#### HTTP→DynamoDB

```bash
curl -X POST http://localhost:3000/create-item \
     -H 'Content-Type: application/json' \
     -d '{"PK":"123"}'
```

#### SQS trigger

```bash
aws --endpoint-url http://localhost:9324 \
    sqs send-message \
    --queue-url http://localhost:9324/000000000000/main-queue-offline \
    --message-body "hello from sqs"
```

#### S3 trigger

```bash
echo "demo" > demo.txt
aws --endpoint-url http://localhost:4569 \
    s3 cp demo.txt s3://main-bucket-offline/
```

### Tear everything down when finished

```bash
npm run teardown
```
