# ✉️ Amazon Simple Email Service (`ses`)

> Transactional and bulk email at scale — deliverability handled.

- **Category:** Application Integration
- **Service id:** `ses`

## Why it exists
Sending email reliably means SPF/DKIM/DMARC, bounces, complaints and warmup. SES packages all of it at the lowest per-message price in the market.

## When to use it
Transactional email (receipts, password resets), newsletters, automated alerts.

## Learn first

- Verified identities & domains
- DKIM/SPF/DMARC setup
- Suppression & bounces
- Sending limits & warmup

## Terraform
```hcl
resource "aws_ses_domain_identity" "example" {
  domain = "example.com"
}
resource "aws_ses_domain_dkim" "example" {
  domain = aws_ses_domain_identity.example.domain
}
```

## AWS CDK
```ts
import * as ses from "aws-cdk-lib/aws-ses";
new ses.EmailIdentity(this, "Identity", { identity: ses.Identity.domain("example.com") });
```

## Boto3 (Python)
```python
import boto3
ses = boto3.client("sesv2", region_name="us-east-1")
ses.send_email(FromEmailAddress="noreply@example.com",
    Destination={"ToAddresses": ["user@example.com"]},
    Content={"Simple": {"Subject": {"Data": "Hello"},
             "Body": {"Text": {"Data": "Welcome!"}}}})
```

## Delete / teardown
```python
ses.delete_email_identity(EmailIdentity="example.com")
```

## Expert tips

- Always attach a configuration set with a bounce SNS topic — you will get bounces.
- Auto-suppress hard bounces via SNS + Lambda.

## Real-world example

**SaaS companies** — Send millions of receipts and notifications monthly.

## Next steps

- **SNS** (Push notifications + email fan-out.) — see `sns`
- **Pinpoint** (Marketing campaigns.) — see `pinpoint`
