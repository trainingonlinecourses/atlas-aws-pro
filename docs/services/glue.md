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

## Next steps

- **S3** (Reads raw zone, writes curated zone.) — see `s3`
- **Athena / Redshift** (Consume the Glue Catalog.) — see `athena---redshift`
- **EventBridge** (Scheduled & event-driven runs.) — see `eventbridge`
