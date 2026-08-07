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

## Next steps

- **Config** (Rules as controls.) — see `config`
- **CloudTrail** (API evidence.) — see `cloudtrail`
- **Security Hub** (Findings as evidence.) — see `security-hub`
