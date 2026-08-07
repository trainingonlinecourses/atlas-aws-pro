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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Cost Explorer runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production AWS Cost Explorer is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for AWS Cost Explorer is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **Budgets** (Alerts before you overspend.) — see `budgets`
- **CloudWatch** (Resource-level metrics.) — see `cloudwatch`
