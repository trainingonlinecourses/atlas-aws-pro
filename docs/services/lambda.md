# λ AWS Lambda (`lambda`)

> Run code on events. Zero servers, pay per 128ms slice.

- **Category:** Compute
- **Service id:** `lambda`

## Why it exists
Most glue code doesn't deserve a server. Lambda spins up per request, scales to zero, bills in milliseconds.

## When to use it
API handlers, S3 triggers, cron jobs, stream processors.

## Learn first

- Event-driven model
- Cold starts & memory↔CPU
- Execution role IAM
- Timeouts & concurrency

## Terraform
```hcl
resource "aws_lambda_function" "processor" {
  function_name = "order-processor"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.12"
  handler       = "index.handler"
  filename      = "lambda.zip"
  memory_size   = 256
  timeout       = 30
}
```

## AWS CDK
```ts
import * as lambda from "aws-cdk-lib/aws-lambda";
const fn = new lambda.Function(this, "Processor", {
  runtime: lambda.Runtime.PYTHON_3_12,
  handler: "index.handler",
  code: lambda.Code.fromAsset("lambda.zip"),
  memorySize: 256, timeout: cdk.Duration.seconds(30),
});
```

## Boto3 (Python)
```python
import boto3, json
lam = boto3.client("lambda", region_name="us-east-1")
resp = lam.invoke(FunctionName="order-processor",
    Payload=json.dumps({"order_id": "A-1042"}))
print(json.loads(resp["Payload"].read()))
```

## Delete / teardown
```python
lam.delete_function(FunctionName="order-processor")
```

## Expert tips

- More memory = more CPU — benchmark, don't guess.
- Keep packages small; zip size drives cold starts.

## Real-world example

**Capital One** — Runs security tooling and data pipelines fully serverless.

## Next steps

- **API Gateway** (HTTP routes invoke Lambda directly.) — see `api-gateway`
- **DynamoDB** (Stateless function; state in the table.) — see `dynamodb`
- **EventBridge / SQS** (Async triggers decouple producers.) — see `eventbridge---sqs`
- **CloudWatch** (Every invocation logs here.) — see `cloudwatch`
