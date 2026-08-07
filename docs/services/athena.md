# 🦉 Amazon Athena (`athena`)

> SQL straight against S3 — no cluster, no loading, pay per query.

- **Category:** Analytics
- **Service id:** `athena`
- **AI-enabled:** yes

## Why it exists
Sometimes you just need an answer from files in S3. Athena runs standard SQL over Parquet using the Glue Catalog.

## When to use it
Log analysis, ad-hoc BI, querying CloudTrail/ALB logs.

## Learn first

- External tables via Glue
- Partitioning for cost
- Parquet + compression
- Workgroups

## Terraform
```hcl
resource "aws_athena_workgroup" "bi" {
  name = "bi"
  configuration {
    enforce_workgroup_configuration = true
    result_configuration { output_location = "s3://acme-lake/athena-results/" }
  }
}

resource "aws_glue_catalog_database" "raw" { name = "lake_raw" }
```

## AWS CDK
```ts
import * as athena from "aws-cdk-lib/aws-athena";
new athena.CfnWorkGroup(this, "Bi", {
  name: "bi",
  workGroupConfiguration: {
    resultConfiguration: { outputLocation: "s3://acme-lake/athena-results/" },
  },
});
```

## Boto3 (Python)
```python
import boto3, time
ath = boto3.client("athena", region_name="us-east-1")
q = ath.start_query_execution(
    QueryString="SELECT status, count(*) c FROM orders GROUP BY status",
    QueryExecutionContext={"Database": "lake_raw"}, WorkGroup="bi")
time.sleep(3)
print(ath.get_query_execution(QueryExecutionId=q["QueryExecutionId"])
      ["QueryExecution"]["Status"]["State"])
```

## Delete / teardown
```python
ath.delete_workgroup(WorkGroup="bi", RecursiveDeleteOption=True)
```

## Expert tips

- You pay per data SCANNED — partitioning is a cost lever, not a luxury.
- Parquet + gzip routinely cuts bills 10-100x.

## Real-world example

**BI analysts** — Query a year of CloudFront logs in S3 without spinning up a cluster.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Athena runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production Amazon Athena is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for Amazon Athena is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **S3** (The data lives here.) — see `s3`
- **Glue** (Provides schemas.) — see `glue`
- **QuickSight** (Dashboards run Athena queries.) — see `quicksight`
