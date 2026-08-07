# 🚚 Database Migration Service (`dms`)

> Migrate live databases to AWS with near-zero downtime — including CDC.

- **Category:** Migration & Transfer
- **Service id:** `dms`

## Why it exists
You can't freeze production to move it. DMS copies the data, then streams ongoing changes (CDC) until cutover.

## When to use it
Oracle → Aurora, on-prem → RDS, consolidation.

## Learn first

- Replication instance sizing
- Source & target endpoints
- Full load vs full-load + CDC

## Terraform
```hcl
resource "aws_dms_replication_instance" "mig" {
  replication_instance_id = "mig-01"
  replication_instance_class = "dms.t3.medium"
  allocated_storage = 50
  publicly_accessible = false
}

resource "aws_dms_endpoint" "source_ora" {
  endpoint_id = "source-ora"
  endpoint_type = "source"
  engine_name = "oracle"
  server_name = "ora-hq.acme.local"
  port = 1521
  database_name = "PROD"
  username = "dms_user"
  password = "use-secrets-manager"
}

resource "aws_dms_replication_task" "ora_to_aurora" {
  replication_task_id = "ora-to-aurora"
  migration_type = "full-load-and-cdc"
  replication_instance_arn = aws_dms_replication_instance.mig.replication_instance_arn
  source_endpoint_arn = aws_dms_endpoint.source_ora.endpoint_arn
  target_endpoint_arn = aws_dms_endpoint.target_aurora.endpoint_arn
  table_mappings = jsonencode({
    rules = [{ rule-type = "selection", rule-id = "1", rule-action = "include",
      object-locator = { schema-name = "HR", table-name = "%" } }]
  })
}
```

## AWS CDK
```ts
import * as dms from "aws-cdk-lib/aws-dms";
const inst = new dms.CfnReplicationInstance(this, "Mig", {
  replicationInstanceClass: "dms.t3.medium",
  allocatedStorage: 50, publiclyAccessible: false,
});
new dms.CfnReplicationTask(this, "OraToAurora", {
  migrationType: "full-load-and-cdc",
  replicationInstanceArn: inst.ref,
  sourceEndpointArn: oraEndpoint.ref,
  targetEndpointArn: auroraEndpoint.ref,
  tableMappings: JSON.stringify({ rules: [] }),
});
```

## Boto3 (Python)
```python
import boto3
dms = boto3.client("dms", region_name="us-east-1")
for t in dms.describe_replication_tasks()["ReplicationTasks"]:
    print(t["ReplicationTaskIdentifier"], t["Status"])
```

## Delete / teardown
```python
dms.delete_replication_task(ReplicationTaskArn=arn)
dms.delete_replication_instance(ReplicationInstanceArn=arn)
```

## Expert tips

- Run SCT first for heterogeneous engines (Oracle → Postgres).
- CDC lag is your cutover-readiness metric.

## Real-world example

**Enterprises** — Oracle → Aurora with CDC: cutover in minutes, not a frozen weekend.

## Next steps

- **RDS / Aurora** (The usual targets.) — see `rds---aurora`
- **VPC** (The replication instance sits inside your network.) — see `vpc`
- **CloudWatch** (Migration progress.) — see `cloudwatch`
