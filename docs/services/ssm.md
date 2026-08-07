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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Systems Manager keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS Systems Manager is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS Systems Manager is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS Systems Manager means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **IAM** (Session access is just a policy.) — see `iam`
- **EC2 / ECS** (Agents run on every node.) — see `ec2---ecs`
- **CloudWatch** (Runbook outputs.) — see `cloudwatch`
