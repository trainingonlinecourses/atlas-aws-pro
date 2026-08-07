# 📉 Amazon QuickSight (`quicksight`)

> Serverless BI dashboards — pay per session, embed anywhere, ask Q.

- **Category:** Analytics
- **Service id:** `quicksight`
- **AI-enabled:** yes

## Why it exists
Analysts need dashboards on lake/warehouse data without BI servers. Q answers natural-language questions.

## When to use it
Exec dashboards, embedded analytics in SaaS, SPICE-fast reports.

## Learn first

- Datasets (Athena/Redshift/RDS)
- SPICE engine
- Analyses vs dashboards
- Embedding + Q

## Terraform
```hcl
# QuickSight is configured mostly in-console; Terraform manages users:
resource "aws_quicksight_user" "analyst" {
  email = "analyst@acme.dev"
  identity_type = "IAM"
  user_role = "AUTHOR"
  namespace = "default"
  aws_account_id = data.aws_caller_identity.current.account_id
}
```

## AWS CDK
```ts
// Dashboards are authored in the console/API;
// in CDK, grant the QuickSight service role query access:
datasetRole.addToPolicy(new iam.PolicyStatement({
  actions: ["athena:StartQueryExecution", "athena:GetQueryExecution"],
  resources: ["*"],
}));
```

## Boto3 (Python)
```python
import boto3
qs = boto3.client("quicksight", region_name="us-east-1")
for d in qs.list_dashboards(AwsAccountId="123456789012")["DashboardSummaryList"]:
    print(d["Name"], d["LastPublishedTime"])
```

## Delete / teardown
```python
qs.delete_dashboard(AwsAccountId=acct, DashboardId=id)
```

## Expert tips

- SPICE = in-memory turbo for dashboards; direct query for freshness.
- Per-session pricing beats per-seat when viewers are occasional.

## Real-world example

**Product teams** — Embed live usage dashboards inside their SaaS apps.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon QuickSight runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production Amazon QuickSight is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for Amazon QuickSight is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **Athena / Redshift / RDS** (Dataset sources.) — see `athena---redshift---rds`
- **S3** (SPICE imports.) — see `s3`
- **Cognito** (Auth for embedded dashboards.) — see `cognito`
