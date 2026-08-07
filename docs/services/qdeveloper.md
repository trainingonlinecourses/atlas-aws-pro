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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Q Developer keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where Amazon Q Developer is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production Amazon Q Developer is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for Amazon Q Developer means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **IAM Identity Center** (Licensing & access control.) — see `iam-identity-center`
- **CodePipeline** (Q-generated code flows through your normal CI.) — see `codepipeline`
- **Every service** (Q knows the docs — ask it about any of the 80.) — see `every-service`
