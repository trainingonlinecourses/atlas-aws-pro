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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon Aurora runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon Aurora gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon Aurora is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon Aurora is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Aurora disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **RDS family** (Same subnet groups & security groups.) — see `rds-family`
- **Secrets Manager** (Rotates master credentials.) — see `secrets-manager`
- **DMS** (#1 target for Oracle exits.) — see `dms`
