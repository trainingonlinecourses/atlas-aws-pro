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

## Next steps

- **Lambda** (Polls and processes batches.) — see `lambda`
- **SNS** (Fan-out: one topic feeds many queues.) — see `sns`
- **DLQ** (Poison messages land here.) — see `dlq`
