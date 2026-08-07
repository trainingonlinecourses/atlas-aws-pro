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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Simple Email Service is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where Amazon Simple Email Service is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production Amazon Simple Email Service is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for Amazon Simple Email Service is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats Amazon Simple Email Service as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **SNS** (Push notifications + email fan-out.) — see `sns`
- **Pinpoint** (Marketing campaigns.) — see `pinpoint`
