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

## Next steps

- **CloudWatch Alarms** (alarm_actions point at SNS topics.) — see `cloudwatch-alarms`
- **SQS** (The classic fan-out pairing.) — see `sqs`
- **Lambda** (Push invocations.) — see `lambda`
