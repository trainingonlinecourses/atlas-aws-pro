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

## Next steps

- **Everything** (Lambda→DynamoDB, EC2→S3, CodePipeline→ECS all work via role trust + policies.) — see `everything`
