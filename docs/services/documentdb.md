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

## Next steps

- **DynamoDB** (Managed NoSQL if you don't need Mongo semantics.) — see `dynamodb`
- **RDS** (When the data is relational after all.) — see `rds`
