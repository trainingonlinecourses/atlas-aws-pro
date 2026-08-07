# ⏱️ Amazon Timestream (`timestream`)

> Serverless time-series database for IoT, telemetry and metrics.

- **Category:** Database
- **Service id:** `timestream`

## Why it exists
Time-series data grows forever and is queried differently than rows. Timestream separates hot in-memory from cold storage automatically and scales to billions of points.

## When to use it
IoT sensor streams, industrial telemetry, stock tickers, app metrics.

## Learn first

- Time-series vs relational modeling
- Memory vs magnetic store
- Automatic retention tiers
- SQL with time functions

## Terraform
```hcl
resource "aws_timestreamwrite_database" "metrics" {
  database_name = "metrics"
}
resource "aws_timestreamwrite_table" "sensors" {
  database_name = aws_timestreamwrite_database.metrics.database_name
  table_name    = "sensors"
}
```

## AWS CDK
```ts
// No first-class CDK construct (L1 only) — manage with Terraform.
```

## Boto3 (Python)
```python
from boto3.session import Session
w = Session().client("timestream-write", region_name="us-east-1")
recs = [{"Dimensions": [{"Name": "sensor", "Value": "s1"}],
         "MeasureName": "temp", "MeasureValue": "22.5",
         "MeasureValueType": "DOUBLE", "Time": str(int(__import__('time').time()*1000))}]
w.write_records(DatabaseName="metrics", TableName="sensors", Records=recs)
```

## Delete / teardown
```python
# Delete tables first, then the database
w.delete_table(DatabaseName="metrics", TableName="sensors")
w.delete_database(DatabaseName="metrics")
```

## Expert tips

- Model one 'measure' per row with tags — not one column per sensor.
- Use scheduled queries to roll raw ticks up into 5-minute aggregates.

## Real-world example

**Industrial IoT vendors** — Millions of sensor readings per day at low cost.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon Timestream runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon Timestream gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon Timestream is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon Timestream is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Timestream disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **Kinesis** (Ingest streams into Timestream.) — see `kinesis`
- **QuickSight** (Dashboards over time series.) — see `quicksight`
