# 🍃 Amazon DocumentDB (`documentdb`)

> MongoDB-compatible, fully managed document database.

- **Category:** Database
- **Service id:** `documentdb`

## Why it exists
Teams with MongoDB skills shouldn't have to run MongoDB servers. DocumentDB speaks the MongoDB wire protocol while AWS handles clusters, failover and backups.

## When to use it
Content/catalog systems, user profiles, JSON-heavy workloads.

## Learn first

- MongoDB compatibility level
- Cluster = instance + replicas
- Change streams
- TLS/connection strings

## Terraform
```hcl
resource "aws_docdb_cluster" "app" {
  cluster_identifier = "app-cluster"
  engine             = "docdb"
  master_username    = "admin"
  master_password    = "CHANGE_ME_STRONG"
  skip_final_snapshot = true
}
resource "aws_docdb_cluster_instance" "primary" {
  cluster_identifier = aws_docdb_cluster.app.id
  instance_class     = "db.r5.large"
}
```

## AWS CDK
```ts
import * as docdb from "aws-cdk-lib/aws-docdb";
new docdb.DatabaseCluster(this, "AppDb", {
  vpc, masterUser: { username: "admin", password: "CHANGE_ME_STRONG" },
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
});
```

## Boto3 (Python)
```python
import boto3
docdb = boto3.client("docdb", region_name="us-east-1")
for c in docdb.describe_db_clusters()["DBClusters"]:
    print(c["DBClusterIdentifier"], c["Status"])
```

## Delete / teardown
```python
docdb.delete_db_cluster(DBClusterIdentifier="app-cluster", SkipFinalSnapshot=True)
```

## Expert tips

- Use the driver version matching the engine — compatibility is real but not 1:1.
- Replicas are read-only; all writes go to the primary.

## Real-world example

**Edtech & media companies** — Profiles and catalogs too flexible for SQL.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon DocumentDB runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon DocumentDB gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon DocumentDB is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon DocumentDB is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon DocumentDB disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **DynamoDB** (Managed NoSQL if you don't need Mongo semantics.) — see `dynamodb`
- **RDS** (When the data is relational after all.) — see `rds`
