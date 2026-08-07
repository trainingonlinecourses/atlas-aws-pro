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

## Next steps

- **Organizations** (Assigns across all accounts.) — see `organizations`
- **IAM** (Permission sets materialize as roles.) — see `iam`
- **External IdPs** (Entra ID / Okta / Google federation.) — see `external-idps`
