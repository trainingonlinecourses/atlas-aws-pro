# 📋 AWS Audit Manager (`auditmanager`)

> Automate audit evidence collection. Map controls to resources, get a ready-to-review report.

- **Category:** Security, Identity & Compliance
- **Service id:** `auditmanager`

## Why it exists
SOC 2 / ISO prep means collecting evidence screenshots for weeks. Audit Manager maps AWS resources to control frameworks and continuously gathers the evidence.

## When to use it
Compliance prep, evidence collection, control mapping.

## Learn first

- Frameworks (SOC 2, ISO, CIS)
- Control mappings
- Evidence folders
- Assessment reports

## Terraform
```hcl
resource "aws_auditmanager_account_registration" "reg" {}
resource "aws_auditmanager_control" "enc" {
  name = "encrypt-at-rest"
  control_mapping_sources {
    source_name = "KMS CMK enabled"
    source_set_up_option = "Procedural_Controls_Mapping"
    source_type = "MANUAL"
  }
}
```

## AWS CDK
```ts
// L1 only — CfnAssessment / CfnControl.
```

## Boto3 (Python)
```python
import boto3
am = boto3.client("auditmanager", region_name="us-east-1")
resp = am.create_assessment(
    name="soc2-cycle-1",
    assessment_reports_destination={ "destination": "S3",
        "destination_s3_bucket": "audit-evidence",
        "destination_s3_prefix": "soc2" })
```

## Delete / teardown
```python
# Delete assessments, then controls.
```

## Expert tips

- Run a trial assessment before the real audit window opens.
- Custom controls cover non-AWS evidence.

## Real-world example

**Fintech** — Shrinking SOC 2 evidence gathering from weeks to days.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Audit Manager is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where AWS Audit Manager is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production AWS Audit Manager is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for AWS Audit Manager means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps AWS Audit Manager continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **Config** (Rules as controls.) — see `config`
- **CloudTrail** (API evidence.) — see `cloudtrail`
- **Security Hub** (Findings as evidence.) — see `security-hub`
