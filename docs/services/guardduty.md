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

## Next steps

- **CloudTrail / VPC Flow Logs** (Its raw material.) — see `cloudtrail---vpc-flow-logs`
- **EventBridge** (High findings trigger remediation.) — see `eventbridge`
- **Security Hub** (Org-wide aggregation.) — see `security-hub`
