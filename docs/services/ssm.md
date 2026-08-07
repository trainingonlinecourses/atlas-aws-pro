# 🔧 AWS Systems Manager (`ssm`)

> The remote-control plane for fleets — sessions, patches, parameters.

- **Category:** Management & Governance
- **Service id:** `ssm`

## Why it exists
SSH bastions don't scale. Session Manager gives shell access through IAM (no port 22); Patch Manager keeps fleets current.

## When to use it
Patch compliance, remote debugging, config parameters, runbooks.

## Learn first

- SSM Agent
- Session Manager vs SSH
- Parameter Store tiers

## Terraform
```hcl
resource "aws_ssm_parameter" "stripe_key" {
  name = "/prod/stripe/secret"
  type = "SecureString"
  value = "sk_live_change-me"
}

resource "aws_ssm_parameter" "feature_flags" {
  name = "/prod/flags"
  type = "String"
  value = jsonencode({ new_checkout = true })
}
# Session Manager = IAM + SSM agent. Grant AmazonSSMManagedInstanceCore
# on the instance role and port 22 can stay closed everywhere.
```

## AWS CDK
```ts
import * as ssm from "aws-cdk-lib/aws-ssm";
new ssm.StringParameter(this, "Flags", {
  parameterName: "/prod/flags",
  stringValue: '{"new_checkout": true}',
});
new ssm.StringParameter(this, "StripeKey", {
  parameterName: "/prod/stripe/secret",
  stringValue: "sk_live_change-me",
  type: ssm.ParameterType.SECURE_STRING,
});
```

## Boto3 (Python)
```python
import boto3
ssm = boto3.client("ssm", region_name="us-east-1")
v = ssm.get_parameter(Name="/prod/stripe/secret", WithDecryption=True)
print("fetched:", v["Parameter"]["Value"][:7] + "…")
```

## Delete / teardown
```python
ssm.delete_parameter(Name="/prod/stripe/secret")
```

## Expert tips

- Deleting port 22 from every SG is a rite of passage.
- Parameter Store = config; Secrets Manager = rotating creds.

## Real-world example

**Platform teams** — Patch 500 servers on schedule and 'SSH' via Session Manager — no bastions.

## Next steps

- **IAM** (Session access is just a policy.) — see `iam`
- **EC2 / ECS** (Agents run on every node.) — see `ec2---ecs`
- **CloudWatch** (Runbook outputs.) — see `cloudwatch`
