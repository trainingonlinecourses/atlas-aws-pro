# 📬 Simple Queue Service (`sqs`)

> A queue between services — spikes land here, workers drain at their pace.

- **Category:** Application Integration
- **Service id:** `sqs`

## Why it exists
Synchronous calls cascade failures. A queue decouples producer and consumer: checkout never waits for inventory.

## When to use it
Work queues, order pipelines, buffering, dead-letter queues.

## Learn first

- Standard vs FIFO
- Visibility timeout
- DLQs & redrive
- Long polling

## Terraform
```hcl
resource "aws_sqs_queue" "orders_dlq" { name = "orders-dlq" }

resource "aws_sqs_queue" "orders" {
  name = "orders"
  visibility_timeout_seconds = 60
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount = 4
  })
}
```

## AWS CDK
```ts
import * as sqs from "aws-cdk-lib/aws-sqs";
const dlq = new sqs.Queue(this, "OrdersDlq");
const queue = new sqs.Queue(this, "Orders", {
  visibilityTimeout: cdk.Duration.seconds(60),
  deadLetterQueue: { queue: dlq, maxReceiveCount: 4 },
});
```

## Boto3 (Python)
```python
import boto3
sqs = boto3.client("sqs", region_name="us-east-1")
url = sqs.get_queue_url(QueueName="orders")["QueueUrl"]
sqs.send_message(QueueUrl=url, MessageBody='{"order_id": "A-1042"}')
msgs = sqs.receive_message(QueueUrl=url, WaitTimeSeconds=5).get("Messages", [])
for m in msgs:
    sqs.delete_message(QueueUrl=url, ReceiptHandle=m["ReceiptHandle"])
```

## Delete / teardown
```python
sqs.delete_queue(QueueUrl=url)
```

## Expert tips

- Visibility timeout must exceed max processing time.
- Every production queue ships with a DLQ — no exceptions.

## Real-world example

**E-commerce** — Orders buffer in SQS so flash sales never break inventory or payments.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Simple Queue Service is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where Simple Queue Service is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production Simple Queue Service is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for Simple Queue Service is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats Simple Queue Service as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **Lambda** (Polls and processes batches.) — see `lambda`
- **SNS** (Fan-out: one topic feeds many queues.) — see `sns`
- **DLQ** (Poison messages land here.) — see `dlq`
