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

## Next steps

- **S3 / EC2 / GuardDuty** (Built-in AWS event sources.) — see `s3---ec2---guardduty`
- **Lambda / SQS / Step Functions** (The usual targets.) — see `lambda---sqs---step-functions`
- **SNS** (Chained for human notification.) — see `sns`
