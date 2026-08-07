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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Security Hub is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where AWS Security Hub is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production AWS Security Hub is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for AWS Security Hub means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps AWS Security Hub continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **GuardDuty / Inspector / Config** (Finding producers.) — see `guardduty---inspector---config`
- **EventBridge → Lambda** (Auto-remediation.) — see `eventbridge-→-lambda`
