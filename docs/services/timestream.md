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

## Next steps

- **Kinesis** (Ingest streams into Timestream.) — see `kinesis`
- **QuickSight** (Dashboards over time series.) — see `quicksight`
