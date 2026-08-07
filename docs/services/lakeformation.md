# 🏞️ AWS Lake Formation (`lakeformation`)

> Fine-grained permissions over the lake — column-level security, no IAM acrobatics.

- **Category:** Analytics
- **Service id:** `lakeformation`
- **AI-enabled:** yes

## Why it exists
Bucket policies can't say 'analysts see revenue but not salaries'. Lake Formation grants table/column/cell access on the Glue Catalog.

## When to use it
Lake permissions, column-level masking, cross-account sharing, curated zones.

## Learn first

- LF-tags & data location registration
- Grant/revoke on catalog objects
- Column filters
- Cross-account sharing

## Terraform
```hcl
resource "aws_lakeformation_permissions" "analyst_read" {
  principal = aws_iam_role.analyst.arn
  permissions = ["SELECT", "DESCRIBE"]
  database { name = aws_glue_catalog_database.raw.name }
}
# Column-level: table_with_columns with excluded_column_names = ["ssn", "salary"]
```

## AWS CDK
```ts
import * as lakeformation from "aws-cdk-lib/aws-lakeformation";
new lakeformation.CfnDataLakeSettings(this, "Admins", {
  admins: [{ dataLakePrincipalIdentifier: platformRole.roleArn }],
});
```

## Boto3 (Python)
```python
import boto3
lf = boto3.client("lakeformation", region_name="us-east-1")
for g in lf.list_permissions()["PrincipalResourcePermissions"]:
    print(g["Principal"], g["Permissions"])
```

## Delete / teardown
```python
lf.batch_revoke_permissions(...)  # then deregister locations
```

## Expert tips

- Register S3 locations BEFORE granting on them.
- LF-tags scale better than per-principal grants.

## Real-world example

**Regulated data teams** — Analysts query revenue freely while PII columns stay masked automatically.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Lake Formation runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production AWS Lake Formation is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for AWS Lake Formation is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **Glue** (Catalog objects are what you grant on.) — see `glue`
- **Athena / Redshift / EMR** (Engines enforce LF permissions.) — see `athena---redshift---emr`
- **RAM** (Shares the lake across accounts.) — see `ram`
