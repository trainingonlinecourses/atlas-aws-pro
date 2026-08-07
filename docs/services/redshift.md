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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon Redshift runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon Redshift gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon Redshift is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon Redshift is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Redshift disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **S3** (COPY loads data; Spectrum queries S3 in place.) — see `s3`
- **Glue** (Cleans data before it lands.) — see `glue`
- **QuickSight** (Consumption layer on top.) — see `quicksight`
