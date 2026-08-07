# 🔬 Amazon Macie (`macie`)

> ML that hunts PII inside S3 — finds the secret nobody remembered storing.

- **Category:** Security, Identity & Compliance
- **Service id:** `macie`

## Why it exists
Someone always dumps a CSV of emails into a bucket. Macie continuously classifies S3 data and alerts on sensitive content.

## When to use it
PII discovery, GDPR/HIPAA evidence, bucket hygiene at scale.

## Learn first

- Managed data identifiers (PII types)
- Scheduled vs one-time jobs
- Sensitive data discovery results
- Custom data identifiers

## Terraform
```hcl
resource "aws_macie2_account" "main" {}

resource "aws_macie2_classification_job" "weekly" {
  job_type = "SCHEDULED"
  schedule_frequency { daily_schedule = true }
  # scoping block selects buckets; managed identifiers find PII
}
```

## AWS CDK
```ts
import * as macie2 from "aws-cdk-lib/aws-macie";
new macie2.CfnSession(this, "Macie", {
  findingPublishingFrequency: "FIFTEEN_MINUTES",
});
```

## Boto3 (Python)
```python
import boto3
mac = boto3.client("macie2", region_name="us-east-1")
print(mac.get_macie_session())
for f in mac.list_findings()["ids"][:5]:
    print(f)
```

## Delete / teardown
```python
mac.disable_macie()
```

## Expert tips

- Run a one-time full-account scan before any audit.
- Pair findings with EventBridge → auto-quarantine bucket ACLs.

## Real-world example

**Regulated enterprises** — Weekly PII sweeps across thousands of buckets, results in Security Hub.

## Next steps

- **S3** (The surface it scans.) — see `s3`
- **Security Hub** (Findings roll up.) — see `security-hub`
- **EventBridge** (Reacts to new sensitive-data findings.) — see `eventbridge`
