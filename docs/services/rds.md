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

## Next steps

- **VPC** (Lives in private subnets.) — see `vpc`
- **Secrets Manager** (Credentials stored & rotated.) — see `secrets-manager`
- **KMS** (Encryption at rest.) — see `kms`
- **DMS** (Common migration target.) — see `dms`
