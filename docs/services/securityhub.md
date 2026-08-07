# 🕵️ AWS Security Hub (`securityhub`)

> One pane of glass: GuardDuty + Inspector + Config findings, scored vs CIS.

- **Category:** Security, Identity & Compliance
- **Service id:** `securityhub`

## Why it exists
Security tools shout separately. Security Hub normalizes every finding and scores posture against standards.

## When to use it
SOC triage, compliance scoring, cross-account aggregation.

## Learn first

- Findings format (ASFF)
- CIS / FSBP standards
- Member accounts

## Terraform
```hcl
resource "aws_securityhub_account" "main" {}

resource "aws_securityhub_standards_subscription" "cis" {
  depends_on = [aws_securityhub_account.main]
  standards_arn = "arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.4.0"
}
```

## AWS CDK
```ts
import * as securityhub from "aws-cdk-lib/aws-securityhub";
new securityhub.CfnHub(this, "Hub", {});
// subscribe standards (CIS v1.4, AWS FSBP) via console/API
```

## Boto3 (Python)
```python
import boto3
sh = boto3.client("securityhub", region_name="us-east-1")
findings = sh.get_findings(Filters={
    "SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}]})
print(len(findings["Findings"]), "critical findings")
```

## Delete / teardown
```python
sh.disable_security_hub()
```

## Expert tips

- The compliance score is the number executives actually read.
- Archive noise; resolve real findings — don't delete evidence.

## Real-world example

**Enterprise SOCs** — Correlate GuardDuty, Inspector and Config findings into one queue.

## Next steps

- **GuardDuty / Inspector / Config** (Finding producers.) — see `guardduty---inspector---config`
- **EventBridge → Lambda** (Auto-remediation.) — see `eventbridge-→-lambda`
