# 🧞 Amazon Q Developer (`qdeveloper`)

> AWS's AI pair programmer — code gen, upgrades, chat in the IDE & console.

- **Category:** Management & Governance
- **Service id:** `qdeveloper`

## Why it exists
Q Developer writes IaC, explains errors, upgrades Java versions, and answers 'how do I wire X to Y?' — your always-on senior engineer.

## When to use it
Generating Terraform/CDK, debugging errors, code transformation, AWS Q&A.

## Learn first

- IDE plugin vs console chat
- Code transformation jobs
- Security scans
- Citing sources & trust

## Terraform
```hcl
# Q Developer is enabled per organization/user (IAM Identity Center);
# Terraform manages nothing but access. Typical guardrail:
resource "aws_iam_policy" "q_no_admin" {
  name = "q-suggestions-scoped"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Deny"
      Action = ["iam:CreateUser", "organizations:LeaveOrganization"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
// No infrastructure needed — install the AWS Toolkit / Q extension
// and sign in with IAM Identity Center. Treat its output like a
// junior dev's PR: review, test, then merge.
```

## Boto3 (Python)
```python
# Q lives in the IDE/console, not boto3 — but validate everything it
# generates with the same loop you'd use for any code:
#   terraform plan / cdk diff / pytest before merge.
```

## Delete / teardown
```python
# Disable per user in IAM Identity Center; nothing to delete in AWS.
```

## Expert tips

- Use Q to draft, humans to approve — that's the enterprise pattern.
- Its best trick: generating the IAM/TF boilerplate you'd copy-paste.

## Real-world example

**Platform teams** — Cut boilerplate IaC writing time and onboard juniors faster.

## Next steps

- **IAM Identity Center** (Licensing & access control.) — see `iam-identity-center`
- **CodePipeline** (Q-generated code flows through your normal CI.) — see `codepipeline`
- **Every service** (Q knows the docs — ask it about any of the 80.) — see `every-service`
