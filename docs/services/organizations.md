# 🏛️ AWS Organizations (`organizations`)

> Multi-account governance — SCPs, consolidated billing, account factories.

- **Category:** Security, Identity & Compliance
- **Service id:** `organizations`

## Why it exists
Serious companies don't use one account. Organizations gives you account boundaries, SCP guardrails and one bill.

## When to use it
Landing zones, per-env accounts, SCPs, consolidated billing.

## Learn first

- OUs & account hierarchy
- Service Control Policies (SCPs)
- Consolidated billing
- Delegated admin services

## Terraform
```hcl
resource "aws_organizations_organization" "org" {
  feature_set = "ALL"
  enabled_policy_types = ["SERVICE_CONTROL_POLICY", "TAG_POLICY"]
}

resource "aws_organizations_policy" "region_fence" {
  name = "region-fence"
  content = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid = "DenyOutsideApprovedRegions"
      Effect = "Deny"; Action = "*"; Resource = "*"
      Condition = { StringNotEquals = {
        "aws:RequestedRegion" = ["us-east-1", "eu-west-1"] } }
    }]
  })
}
```

## AWS CDK
```ts
import * as organizations from "aws-cdk-lib/aws-organizations";
new organizations.CfnOrganization(this, "Org", {
  featureSet: "ALL",
});
```

## Boto3 (Python)
```python
import boto3
org = boto3.client("organizations", region_name="us-east-1")
for a in org.list_accounts()["Accounts"]:
    print(a["Name"], a["Id"], a["Status"])
```

## Delete / teardown
```python
# Leaving an org is a process, not a delete call — plan it.
```

## Expert tips

- SCPs set the MAXIMUM permissions — IAM still applies inside.
- Deny root user and unencrypted S3 org-wide from day one.

## Real-world example

**Banks & enterprises** — One org, dozens of accounts, SCPs as the outer security wall.

## Next steps

- **Control Tower** (Automates the landing zone on top of Organizations.) — see `control-tower`
- **IAM Identity Center** (SSO across every account.) — see `iam-identity-center`
- **CloudTrail / Config** (Org-wide trails and rules.) — see `cloudtrail---config`
