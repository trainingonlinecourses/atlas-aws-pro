# 🚨 Amazon GuardDuty (`guardduty`)

> ML-powered threat detection — finds the crypto-miner before finance does.

- **Category:** Security, Identity & Compliance
- **Service id:** `guardduty`

## Why it exists
You can't watch every CloudTrail event. GuardDuty flags anomalies: stolen keys, mining, exfiltration.

## When to use it
SOC alerting, compliance evidence, compromised-instance detection.

## Learn first

- Data sources: CloudTrail, VPC Flow, DNS
- Finding severity
- Auto-remediation via EventBridge

## Terraform
```hcl
resource "aws_guardduty_detector" "main" {
  enable = true
  datasources { s3_logs { enable = true } }
}

resource "aws_cloudwatch_event_rule" "gd_high" {
  name = "guardduty-high-severity"
  event_pattern = jsonencode({
    source = ["aws.guardduty"]
    detail_type = ["GuardDuty Finding"]
    detail = { severity = [{ numeric = [">=", 7] }] }
  })
}
```

## AWS CDK
```ts
import * as guardduty from "aws-cdk-lib/aws-guardduty";
new guardduty.CfnDetector(this, "Main", { enable: true });
// + EventBridge rule -> Lambda remediation for high findings
```

## Boto3 (Python)
```python
import boto3
gd = boto3.client("guardduty", region_name="us-east-1")
det = gd.list_detectors()["DetectorIds"][0]
print(gd.get_detector_statistics(DetectorId=det)["Total"])
```

## Delete / teardown
```python
gd.delete_detector(DetectorId=det)
```

## Expert tips

- Enable at the org level from day one — it's cheap insurance.
- Wire severity ≥7 findings straight into your pager.

## Real-world example

**Fintech SOCs** — Auto-triage 'EC2 mining cryptocurrency' findings to Slack in minutes.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon GuardDuty is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Amazon GuardDuty is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Amazon GuardDuty is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Amazon GuardDuty means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon GuardDuty continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **CloudTrail / VPC Flow Logs** (Its raw material.) — see `cloudtrail---vpc-flow-logs`
- **EventBridge** (High findings trigger remediation.) — see `eventbridge`
- **Security Hub** (Org-wide aggregation.) — see `security-hub`
