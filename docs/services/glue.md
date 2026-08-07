# 🧪 AWS Glue (`glue`)

> Serverless Spark ETL + the catalog that makes S3 data queryable.

- **Category:** Analytics
- **Service id:** `glue`
- **AI-enabled:** yes

## Why it exists
Raw files in S3 aren't analytics. Glue crawls them into a catalog, then Spark jobs clean and reshape them.

## When to use it
ETL jobs, data catalog, schema discovery, feeding Athena/Redshift.

## Learn first

- Glue Data Catalog
- Crawlers & classifiers
- Spark jobs & bookmarks

## Terraform
```hcl
resource "aws_glue_crawler" "raw" {
  name = "raw-zone"
  role = aws_iam_role.glue.arn
  database_name = "lake_raw"
  s3_target { path = "s3://acme-lake/raw/" }
}

resource "aws_glue_job" "clean" {
  name = "clean-orders"
  role_arn = aws_iam_role.glue.arn
  command {
    name = "glueetl"
    script_location = "s3://acme-lake/scripts/clean_orders.py"
    python_version = "3"
  }
  glue_version = "4.0"
}
```

## AWS CDK
```ts
import * as glue from "aws-cdk-lib/aws-glue";
new glue.CfnCrawler(this, "Raw", {
  role: glueRole.roleArn, databaseName: "lake_raw",
  targets: { s3Targets: [{ path: "s3://acme-lake/raw/" }] },
});
new glue.CfnJob(this, "Clean", {
  role: glueRole.roleArn,
  command: { name: "glueetl", scriptLocation: "s3://acme-lake/scripts/clean.py" },
  glueVersion: "4.0",
});
```

## Boto3 (Python)
```python
import boto3
glue = boto3.client("glue", region_name="us-east-1")
run = glue.start_job_run(JobName="clean-orders")
print(run["JobRunId"])
```

## Delete / teardown
```python
glue.delete_job(JobName="clean-orders"); glue.delete_crawler(Name="raw-zone")
```

## Expert tips

- The Catalog is the lake's brain — Athena & Redshift both read it.
- Job bookmarks prevent reprocessing old files.

## Real-world example

**Retail lakes** — Nightly Spark ETL turns raw clicks into curated tables.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Glue runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production AWS Glue is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for AWS Glue is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **S3** (Reads raw zone, writes curated zone.) — see `s3`
- **Athena / Redshift** (Consume the Glue Catalog.) — see `athena---redshift`
- **EventBridge** (Scheduled & event-driven runs.) — see `eventbridge`
