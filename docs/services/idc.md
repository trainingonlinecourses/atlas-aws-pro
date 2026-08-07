# 🎫 IAM Identity Center (SSO) (`idc`)

> SSO for humans — one login to every account, mapped to permission sets.

- **Category:** Security, Identity & Compliance
- **Service id:** `idc`

## Why it exists
Humans shouldn't have IAM users in 30 accounts. Identity Center federates your IdP once and assigns permission sets per group.

## When to use it
Workforce SSO, permission sets, app assignments, machine-to-machine too.

## Learn first

- Permission sets vs IAM roles
- Identity source (built-in / Entra / Okta)
- Account assignments
- MFA enforcement

## Terraform
```hcl
data "aws_ssoadmin_instances" "idc" {}

resource "aws_ssoadmin_permission_set" "platform_admin" {
  instance_arn = tolist(data.aws_ssoadmin_instances.idc.arns)[0]
  name = "PlatformAdmin"
  session_duration = "PT2H"
}

resource "aws_ssoadmin_managed_policy_attachment" "admin" {
  instance_arn = tolist(data.aws_ssoadmin_instances.idc.arns)[0]
  managed_policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
  permission_set_arn = aws_ssoadmin_permission_set.platform_admin.arn
}
```

## AWS CDK
```ts
// Identity Center is configured via console/API + assignments:
// map groups -> permission sets -> accounts. In CDK, manage the IAM
// side (roles) and keep IdP sync in your identity team's tooling.
```

## Boto3 (Python)
```python
import boto3
sso = boto3.client("sso-admin", region_name="us-east-1")
inst = sso.list_instances()["Instances"][0]["InstanceArn"]
for ps in sso.list_permission_sets(InstanceArn=inst)["PermissionSets"]:
    print(ps)
```

## Delete / teardown
```python
sso.delete_permission_set(InstanceArn=inst, PermissionSetArn=ps)
```

## Expert tips

- Permission sets are roles that SSO assumes for you — auditable.
- Short session durations (1-2h) + re-auth beats 12h sessions.

## Real-world example

**Enterprises** — One login, every account, zero shared passwords.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, IAM Identity Center (SSO) is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where IAM Identity Center (SSO) is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production IAM Identity Center (SSO) is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for IAM Identity Center (SSO) means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps IAM Identity Center (SSO) continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **Organizations** (Assigns across all accounts.) — see `organizations`
- **IAM** (Permission sets materialize as roles.) — see `iam`
- **External IdPs** (Entra ID / Okta / Google federation.) — see `external-idps`
