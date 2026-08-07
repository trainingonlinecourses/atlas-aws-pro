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

## Next steps

- **SES** (Raw email engine underneath.) — see `ses`
- **SNS** (Push + SMS fallback.) — see `sns`
- **QuickSight** (Campaign analytics.) — see `quicksight`
