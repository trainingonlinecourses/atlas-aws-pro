# 🌌 Amazon Aurora (`aurora`)

> Cloud-native SQL — several times the throughput, storage that never runs out.

- **Category:** Database
- **Service id:** `aurora`

## Why it exists
You love Postgres/MySQL semantics but need faster scaling, up to 15 read replicas, auto-growing storage.

## When to use it
High-traffic transactional systems and SaaS platforms.

## Learn first

- Aurora vs RDS architecture
- Writer + reader endpoints
- Serverless v2
- Global databases for DR

## Terraform
```hcl
resource "aws_rds_cluster" "core" {
  cluster_identifier = "core-aurora"
  engine = "aurora-postgresql"; engine_version = "16.3"
  master_username = "appadmin"
  manage_master_user_password = true
  db_subnet_group_name = aws_db_subnet_group.data.name
  storage_encrypted = true
}

resource "aws_rds_cluster_instance" "writer" {
  identifier = "core-writer"
  cluster_identifier = aws_rds_cluster.core.id
  instance_class = "db.r6g.large"
  engine = aws_rds_cluster.core.engine
}
```

## AWS CDK
```ts
import * as rds from "aws-cdk-lib/aws-rds";
const cluster = new rds.DatabaseCluster(this, "Core", {
  engine: rds.DatabaseClusterEngine.auroraPostgres({
    version: rds.AuroraPostgresEngineVersion.VER_16_3 }),
  writer: rds.ClusterInstance.provisioned("writer", {
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.R6G, ec2.InstanceSize.LARGE) }),
  vpc,
});
```

## Boto3 (Python)
```python
import boto3
rds = boto3.client("rds", region_name="us-east-1")
rds.failover_db_cluster(DBClusterIdentifier="core-aurora")  # DR drill
```

## Delete / teardown
```python
rds.delete_db_cluster(DBClusterIdentifier="core-aurora", SkipFinalSnapshot=True)
```

## Expert tips

- Storage auto-grows to 128TB — but monitor it, it bills.
- Point reads at the reader endpoint, writes at the writer.

## Real-world example

**Airbnb** — Migrated critical metadata to Aurora for multiples of self-managed throughput.

## Next steps

- **RDS family** (Same subnet groups & security groups.) — see `rds-family`
- **Secrets Manager** (Rotates master credentials.) — see `secrets-manager`
- **DMS** (#1 target for Oracle exits.) — see `dms`
