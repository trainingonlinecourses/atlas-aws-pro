# 🛢️ Relational Database Service (`rds`)

> Managed SQL databases — patching, backups and failover on autopilot.

- **Category:** Database
- **Service id:** `rds`

## Why it exists
Running Postgres yourself means patch windows and 3am failover drills. RDS does all of it.

## When to use it
Transactional apps needing SQL joins and ACID guarantees.

## Learn first

- Relational modeling & SQL
- Multi-AZ vs read replicas
- Backups & PITR
- Parameter groups

## Terraform
```hcl
resource "aws_db_instance" "orders" {
  identifier = "orders-db"
  engine = "postgres"; engine_version = "16.3"
  instance_class = "db.m6g.large"
  allocated_storage = 100
  db_name = "orders"; username = "appadmin"
  manage_master_user_password = true
  multi_az = true
  db_subnet_group_name = aws_db_subnet_group.data.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  storage_encrypted = true
  backup_retention_period = 14
}
```

## AWS CDK
```ts
import * as rds from "aws-cdk-lib/aws-rds";
const db = new rds.DatabaseInstance(this, "Orders", {
  engine: rds.DatabaseInstanceEngine.postgres({
    version: rds.PostgresEngineVersion.VER_16_3 }),
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.M6G, ec2.InstanceSize.LARGE),
  vpc, multiAz: true, storageEncrypted: true,
});
```

## Boto3 (Python)
```python
import boto3
rds = boto3.client("rds", region_name="us-east-1")
for db in rds.describe_db_instances()["DBInstances"]:
    print(db["DBInstanceIdentifier"], db["DBInstanceStatus"])
```

## Delete / teardown
```python
rds.delete_db_instance(DBInstanceIdentifier="orders-db", SkipFinalSnapshot=True)
```

## Expert tips

- Multi-AZ is for failover, replicas are for reads — don't confuse them.
- Keep final snapshots unless you truly mean delete.

## Real-world example

**Expedia** — Keeps booking transactions on Multi-AZ databases with automated backups.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Relational Database Service runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Relational Database Service gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Relational Database Service is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Relational Database Service is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Relational Database Service disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **VPC** (Lives in private subnets.) — see `vpc`
- **Secrets Manager** (Credentials stored & rotated.) — see `secrets-manager`
- **KMS** (Encryption at rest.) — see `kms`
- **DMS** (Common migration target.) — see `dms`
