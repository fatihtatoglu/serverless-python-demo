# serverless-python-demo

## Quick-start workflow

All local services run inside Docker containers. Yarn scripts handle setup and teardown.

### Install dependencies

```bash
npm install -g yarn           # if yarn is not installed
yarn install
```

### Start local AWS emulators

```bash
yarn dev:prepare
```

### Run Serverless Offline

```bash
yarn dev
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
yarn dev:clean
```
