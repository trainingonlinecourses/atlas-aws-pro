# 🛡️ AWS Trusted Advisor (`trustedadvisor`)

> AWS's built-in auditor — security, cost, performance and fault-tolerance checks across your account.

- **Category:** Management & Governance
- **Service id:** `trustedadvisor`

## Why it exists
You can't manually check 100+ best practices. Trusted Advisor runs the checklists and flags underutilized instances, open security groups and single-AZ risks.

## When to use it
Well-Architected reviews, cost-savings discovery, security posture checks.

## Learn first

- Cost / security / performance / fault tolerance / limits
- Full checks vs Business+ tier
- Weekly report emails
- Pairing with AWS Config

## Terraform
```hcl
# Nothing to provision — Trusted Advisor audits what already exists.
```

## AWS CDK
```ts
// Nothing to build — it's a managed auditing service.
```

## Boto3 (Python)
```python
import boto3
support = boto3.client("support", region_name="us-east-1")
for c in support.describe_trusted_advisor_checks(language="en")["checks"][:5]:
    print(c["id"], c["name"])
```

## Delete / teardown
```python
# Nothing to delete — built-in console service.
```

## Expert tips

- Business+ plans unlock the full check set — budget for the tier.
- Act on 'idle RDS' and 'unused EC2' checks first: fastest savings.

## Real-world example

**Enterprise accounts** — Central cloud teams run monthly TA reviews.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Trusted Advisor keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS Trusted Advisor is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS Trusted Advisor is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS Trusted Advisor means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **Config** (Custom rules beyond TA's checklist.) — see `config`
- **Cost Explorer** (Verify the cost flags.) — see `cost-explorer`
