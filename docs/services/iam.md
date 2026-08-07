# 🪪 Identity & Access Management (`iam`)

> Who can do what, where. Learn this before literally everything else.

- **Category:** Security, Identity & Compliance
- **Service id:** `iam`

## Why it exists
Every AWS call is authorized by IAM. Roles, policies and least privilege separate a secure platform from a breach.

## When to use it
Human access, service permissions, cross-account roles, CI/CD credentials.

## Learn first

- Users vs groups vs roles
- Policies: Effect/Action/Resource
- Assume-role & STS
- Least privilege

## Terraform
```hcl
resource "aws_iam_role" "app" {
  name = "checkout-app-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"; Action = "sts:AssumeRole"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "orders_access" {
  name = "orders-table-access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"]
      Resource = aws_dynamodb_table.orders.arn
    }]
  })
}

resource "aws_iam_role_policy_attachment" "app" {
  role = aws_iam_role.app.name
  policy_arn = aws_iam_policy.orders_access.arn
}
```

## AWS CDK
```ts
import * as iam from "aws-cdk-lib/aws-iam";
const role = new iam.Role(this, "AppRole", {
  assumedBy: new iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
});
role.addToPolicy(new iam.PolicyStatement({
  actions: ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"],
  resources: [table.tableArn],
}));
```

## Boto3 (Python)
```python
import boto3
sts = boto3.client("sts")
print(sts.get_caller_identity())      # who am I right now?
iam = boto3.client("iam")
print([r["RoleName"] for r in iam.list_roles(MaxItems=20)["Roles"]])
```

## Delete / teardown
```python
iam.detach_role_policy(RoleName=name, PolicyArn=arn)
iam.delete_policy(PolicyArn=arn); iam.delete_role(RoleName=name)
```

## Expert tips

- Roles > users > keys, in that order, always.
- Resource-scoped ARNs beat '*' in every prod policy.

## Real-world example

**Every AWS org** — Least-privilege roles replaced long-lived keys — the biggest security lever.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Identity & Access Management is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Identity & Access Management is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Identity & Access Management is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Identity & Access Management means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Identity & Access Management continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **Everything** (Lambda→DynamoDB, EC2→S3, CodePipeline→ECS all work via role trust + policies.) — see `everything`
