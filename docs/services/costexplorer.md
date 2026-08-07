# 📊 AWS Cost Explorer (`costexplorer`)

> See, filter and forecast what you spend on AWS — by service, account, tag or day.

- **Category:** Analytics
- **Service id:** `costexplorer`
- **AI-enabled:** yes

## Why it exists
Cloud bills spiral quietly. Cost Explorer turns billing data into dashboards and forecasts so you notice the runaway cluster before the invoice.

## When to use it
Monthly cost review, anomaly detection, chargeback by team/tag.

## Learn first

- Cost categories & tags
- Forecasting
- Anomaly detection alerts
- RI/SP coverage reports

## Terraform
```hcl
# Nothing to provision — Cost Explorer is a built-in AWS service.
# Tag resources so you can slice spend by project/team.
```

## AWS CDK
```ts
// No construct needed — Cost Explorer is AWS-managed. Tag resources instead.
```

## Boto3 (Python)
```python
import boto3
ce = boto3.client("ce", region_name="us-east-1")
r = ce.get_cost_and_usage(TimePeriod={"Start": "2026-07-01", "End": "2026-08-01"},
    Granularity="MONTHLY", Metrics=["UnblendedCost"])
print(r["ResultsByTime"])
```

## Delete / teardown
```python
# Nothing to delete — built-in console service.
```

## Expert tips

- Tag everything, then report by tag — untagged spend is 'orphan' cost.
- Pair with Budgets for alerting, not just dashboards.

## Real-world example

**Every AWS customer** — FinOps teams run the show on Cost Explorer.

## Next steps

- **Budgets** (Alerts before you overspend.) — see `budgets`
- **CloudWatch** (Resource-level metrics.) — see `cloudwatch`
