# 🚌 Amazon EventBridge (`eventbridge`)

> The event bus every AWS service plugs into — rules react to anything.

- **Category:** Application Integration
- **Service id:** `eventbridge`

## Why it exists
'S3 object created', 'GuardDuty finding' — all EventBridge events. Rules route them to targets with zero polling.

## When to use it
Reactive pipelines, cross-account routing, cron via Scheduler.

## Learn first

- Buses, rules, patterns
- Event pattern syntax
- Targets: Lambda, SQS, SFN, ECS
- Archives & replay

## Terraform
```hcl
resource "aws_cloudwatch_event_rule" "upload" {
  name = "s3-object-created"
  event_pattern = jsonencode({
    source = ["aws.s3"]
    detail_type = ["Object Created"]
  })
}

resource "aws_cloudwatch_event_target" "thumbnail" {
  rule = aws_cloudwatch_event_rule.upload.name
  arn = aws_lambda_function.thumbnail.arn
}
```

## AWS CDK
```ts
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
new events.Rule(this, "Upload", {
  eventPattern: { source: ["aws.s3"], detailType: ["Object Created"] },
  targets: [new targets.LambdaFunction(fn)],
});
```

## Boto3 (Python)
```python
import boto3
eb = boto3.client("events", region_name="us-east-1")
eb.put_events(Entries=[{
    "Source": "com.acme.orders", "DetailType": "OrderShipped",
    "Detail": '{"order_id": "A-1042"}', "EventBusName": "default"}])
```

## Delete / teardown
```python
eb.remove_targets(Rule=rule, Ids=[tid]); eb.delete_rule(Name=rule)
```

## Expert tips

- Event patterns are JSON matchers — test with the console tester.
- Scheduler (cron) lives in the EventBridge family now.

## Real-world example

**Photo platforms** — Every S3 upload triggers thumbnail generation — no polling.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon EventBridge is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where Amazon EventBridge is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production Amazon EventBridge is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for Amazon EventBridge is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats Amazon EventBridge as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **S3 / EC2 / GuardDuty** (Built-in AWS event sources.) — see `s3---ec2---guardduty`
- **Lambda / SQS / Step Functions** (The usual targets.) — see `lambda---sqs---step-functions`
- **SNS** (Chained for human notification.) — see `sns`
