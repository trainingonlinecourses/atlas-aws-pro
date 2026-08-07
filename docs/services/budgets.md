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

## Next steps

- **Cost Explorer** (Deep-dive the numbers behind the alert.) — see `cost-explorer`
- **CloudWatch** (Alarm on resource metrics too.) — see `cloudwatch`
