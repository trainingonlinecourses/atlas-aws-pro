# 📊 Amazon Redshift (`redshift`)

> Petabyte-scale data warehouse for the questions joins were born to answer.

- **Category:** Database
- **Service id:** `redshift`

## Why it exists
OLTP databases choke on 'sum 3 years grouped by region'. Columnar engines answer in seconds.

## When to use it
BI dashboards, executive reporting, ML feature aggregations.

## Learn first

- Columnar storage & sort keys
- COPY from S3
- Concurrency scaling
- Spectrum: query S3 directly

## Terraform
```hcl
resource "aws_redshift_cluster" "dw" {
  cluster_identifier = "acme-dw"
  node_type = "ra3.xlplus"; number_of_nodes = 2
  database_name = "analytics"; master_username = "dwadmin"
  manage_master_user_password = true
  cluster_subnet_group_name = aws_redshift_subnet_group.dw.name
  publicly_accessible = false
  encrypted = true
}
```

## AWS CDK
```ts
import * as redshift from "aws-cdk-lib/aws-redshift";
new redshift.CfnCluster(this, "DW", {
  clusterIdentifier: "acme-dw", nodeType: "ra3.xlplus",
  numberOfNodes: 2, dbName: "analytics",
  masterUsername: "dwadmin", encrypted: true,
});
```

## Boto3 (Python)
```python
import boto3
rs = boto3.client("redshift-data", region_name="us-east-1")
q = rs.execute_statement(ClusterIdentifier="acme-dw", Database="analytics",
    Sql="SELECT region, SUM(amount) FROM orders GROUP BY region")
print("query id:", q["Id"])
```

## Delete / teardown
```python
boto3.client("redshift").delete_cluster(ClusterIdentifier="acme-dw", SkipFinalClusterSnapshot=True)
```

## Expert tips

- Load with COPY, never row-by-row inserts.
- RA3 separates compute from storage — scale them independently.

## Real-world example

**Amgen** — Runs petabyte-scale biomedical analytics on Redshift.

## Next steps

- **S3** (COPY loads data; Spectrum queries S3 in place.) — see `s3`
- **Glue** (Cleans data before it lands.) — see `glue`
- **QuickSight** (Consumption layer on top.) — see `quicksight`
