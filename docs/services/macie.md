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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Macie is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Amazon Macie is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Amazon Macie is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Amazon Macie means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Macie continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **S3** (The surface it scans.) — see `s3`
- **Security Hub** (Findings roll up.) — see `security-hub`
- **EventBridge** (Reacts to new sensitive-data findings.) — see `eventbridge`
