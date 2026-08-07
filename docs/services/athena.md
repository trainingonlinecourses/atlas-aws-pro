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

## Next steps

- **S3** (The data lives here.) — see `s3`
- **Glue** (Provides schemas.) — see `glue`
- **QuickSight** (Dashboards run Athena queries.) — see `quicksight`
