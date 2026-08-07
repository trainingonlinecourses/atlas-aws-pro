# 📣 Amazon Pinpoint (`pinpoint`)

> Multi-channel engagement — email, SMS, push, in-app. Segment, send, measure.

- **Category:** Application Integration
- **Service id:** `pinpoint`

## Why it exists
Sending a campaign to 100k people across email/SMS/push needs channel plumbing plus deliverability tooling. Pinpoint wraps it all with segmentation and analytics.

## When to use it
Transactional email/SMS, marketing campaigns, push notifications.

## Learn first

- Channels & endpoints
- Segments & journeys
- Deliverability & bounce handling
- Templates

## Terraform
```hcl
resource "aws_pinpoint_app" "campaigns" {
  name = "customer-engagement"
}
resource "aws_pinpoint_sms_channel" "sms" {
  application_id = aws_pinpoint_app.campaigns.application_id
}
```

## AWS CDK
```ts
// L1 only — CfnApp + CfnSmsChannel.
```

## Boto3 (Python)
```python
import boto3
pin = boto3.client("pinpoint", region_name="us-east-1")
pin.send_messages(ApplicationId="app-id",
    MessageRequest={ "Addresses": {"user@example.com": {"ChannelType": "EMAIL"}},
        "MessageConfiguration": {"EmailMessage": {
            "FromAddress": "no-reply@example.com",
            "SimpleEmail": {"Subject": {"Data": "Sale!"}, "HtmlPart": {"Data": "<b>50% off</b>"}}}}})
```

## Delete / teardown
```python
# Delete journeys, campaigns, then the app.
```

## Expert tips

- Track bounces and complaints — providers throttle a bad sending reputation.
- Use journeys for lifecycle campaigns, not raw sends.

## Real-world example

**E-commerce** — Abandoned-cart recovery measurably lifts checkout conversion.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Pinpoint is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where Amazon Pinpoint is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production Amazon Pinpoint is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for Amazon Pinpoint is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats Amazon Pinpoint as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **SES** (Raw email engine underneath.) — see `ses`
- **SNS** (Push + SMS fallback.) — see `sns`
- **QuickSight** (Campaign analytics.) — see `quicksight`
