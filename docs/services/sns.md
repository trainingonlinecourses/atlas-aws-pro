# 📢 Simple Notification Service (`sns`)

> Publish once, deliver everywhere — fan-out messaging.

- **Category:** Application Integration
- **Service id:** `sns`

## Why it exists
When something happens, many systems care: workers, email, Slack, PagerDuty. SNS publishes to all at once.

## When to use it
Alarms, fan-out architectures, push/SMS/email.

## Learn first

- Topics & subscriptions
- Fan-out to SQS/Lambda/email
- Message filtering

## Terraform
```hcl
resource "aws_sns_topic" "alerts" { name = "alerts" }

resource "aws_sns_topic_subscription" "ops_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol = "email"
  endpoint = "ops@acme.dev"
}

resource "aws_sns_topic_subscription" "worker_queue" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol = "sqs"
  endpoint = aws_sqs_queue.orders.arn
}
```

## AWS CDK
```ts
import * as sns from "aws-cdk-lib/aws-sns";
import * as subs from "aws-cdk-lib/aws-sns-subscriptions";
const topic = new sns.Topic(this, "Alerts");
topic.addSubscription(new subs.EmailSubscription("ops@acme.dev"));
topic.addSubscription(new subs.SqsSubscription(queue));
```

## Boto3 (Python)
```python
import boto3
sns = boto3.client("sns", region_name="us-east-1")
sns.publish(TopicArn="arn:aws:sns:us-east-1:123456789012:alerts",
            Subject="Deploy finished", Message="api v2.4.1 is live")
```

## Delete / teardown
```python
sns.delete_topic(TopicArn=arn)
```

## Expert tips

- SNS pushes (fire & forget); SQS buffers. Pick per need.
- Subscription filters save downstream cost massively.

## Real-world example

**Platform teams** — One publish fans out to Lambda, SQS and PagerDuty simultaneously.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Simple Notification Service is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where Simple Notification Service is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production Simple Notification Service is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for Simple Notification Service is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats Simple Notification Service as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **CloudWatch Alarms** (alarm_actions point at SNS topics.) — see `cloudwatch-alarms`
- **SQS** (The classic fan-out pairing.) — see `sqs`
- **Lambda** (Push invocations.) — see `lambda`
