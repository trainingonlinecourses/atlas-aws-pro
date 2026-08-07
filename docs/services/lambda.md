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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Lambda at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where AWS Lambda gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production AWS Lambda runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Lambda stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **API Gateway** (HTTP routes invoke Lambda directly.) — see `api-gateway`
- **DynamoDB** (Stateless function; state in the table.) — see `dynamodb`
- **EventBridge / SQS** (Async triggers decouple producers.) — see `eventbridge---sqs`
- **CloudWatch** (Every invocation logs here.) — see `cloudwatch`
