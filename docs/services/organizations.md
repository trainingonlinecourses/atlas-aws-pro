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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Organizations is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where AWS Organizations is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production AWS Organizations is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for AWS Organizations means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps AWS Organizations continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **Control Tower** (Automates the landing zone on top of Organizations.) — see `control-tower`
- **IAM Identity Center** (SSO across every account.) — see `iam-identity-center`
- **CloudTrail / Config** (Org-wide trails and rules.) — see `cloudtrail---config`
