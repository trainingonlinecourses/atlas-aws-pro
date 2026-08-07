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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Database Migration Service is used to prove the migration path on a sample: small data, same tooling.

- Set up the replication/migration job in dev against a subset of records.
- Validate checksums and row counts on the sample before widening the net.
- Keep the dev source isolated so trial runs can't touch real systems.

### 🧪 Staging / Pre-prod

Staging is the dress rehearsal: a full dry-run migration with a rollback plan.

- Run the full migration on staging data and compare record counts end-to-end.
- Time it and log throughput; the staging number is your prod forecast.
- Write and test the rollback script before you ever need it.

### 🚀 Production

In production Database Migration Service executes the cutover: incremental sync, a short frozen window, and verification.

- Use continuous sync to near-zero downtime, then a brief cutover window.
- Verify with a reconciliation query, not vibes, before traffic is re-routed.
- Keep the old system available for rollback until the new one is proven stable.

### 🌍 Multi-region / DR

DR for a migration is the ability to re-run or roll back: source is intact until cutover is complete.

- Snapshot the source before cutover so rollback is instant if verification fails.
- Store the migration plan and runbook in the repo, not in one engineer's head.
- Define the 'abort criteria' — the exact metric that stops the cutover.

### ♻️ Lifecycle & IaC

Lifecycle formalizes the migration as a project: plan, dry-run, execute, decommission.

- Track the migration as an IaC-driven project with the source and target in Terraform.
- After a stable period, decommission the source and archive its final snapshot.
- Post-incident: document what was learned and fold it into the next migration.

## Next steps

- **RDS / Aurora** (The usual targets.) — see `rds---aurora`
- **VPC** (The replication instance sits inside your network.) — see `vpc`
- **CloudWatch** (Migration progress.) — see `cloudwatch`
