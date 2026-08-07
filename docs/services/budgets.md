# 🎯 AWS Budgets (`budgets`)

> Set spend limits and get alerted before the invoice surprises you.

- **Category:** Management & Governance
- **Service id:** `budgets`

## Why it exists
Costs climb daily but invoices come monthly. Budgets watches actual vs forecasted spend and pings you at thresholds — cost control as a safety net.

## When to use it
Monthly cost budgets, RI/SP utilization budgets, usage budgets.

## Learn first

- Cost vs usage budgets
- Thresholds & notifications
- RI & Savings Plans budgets
- Budget actions

## Terraform
```hcl
resource "aws_budgets_budget" "monthly" {
  name         = "monthly-spend"
  budget_type  = "COST"
  limit_amount = "5000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  notification {
    comparison_operator = "GREATER_THAN"
    threshold           = 80
    notification_type   = "ACTUAL"
    subscriber_email_addresses = ["team@example.com"]
  }
}
```

## AWS CDK
```ts
// No first-class CDK construct (L1 only) — manage with Terraform.
```

## Boto3 (Python)
```python
import boto3
bud = boto3.client("budgets", region_name="us-east-1")
bud.describe_budgets(AccountId="123456789012")
```

## Delete / teardown
```python
bud.delete_budget(AccountId="123456789012", BudgetName="monthly-spend")
```

## Expert tips

- Set a 50%/90%/100% threshold chain, not a single alert.
- Budget actions can auto-stop or scale resources when a limit is hit.

## Real-world example

**Finance teams** — Catch runaway spend before month-end.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Budgets keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS Budgets is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS Budgets is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS Budgets means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **Cost Explorer** (Deep-dive the numbers behind the alert.) — see `cost-explorer`
- **CloudWatch** (Alarm on resource metrics too.) — see `cloudwatch`
