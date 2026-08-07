# 🌊 Amazon Kinesis (`kinesis`)

> Real-time streaming at scale — ingest millions of events per second.

- **Category:** Analytics
- **Service id:** `kinesis`
- **AI-enabled:** yes

## Why it exists
Some data is worthless five minutes late: clicks, telemetry, live scores. Kinesis ingests and replays events.

## When to use it
Clickstream, IoT telemetry, live dashboards, ML feature feeds.

## Learn first

- Shards & partition keys
- Retention & replay
- Consumers: Lambda, Flink, Firehose

## Terraform
```hcl
resource "aws_kinesis_stream" "clicks" {
  name = "clicks"
  shard_count = 4
  retention_period = 48
  encryption_type = "KMS"
}
```

## AWS CDK
```ts
import * as kinesis from "aws-cdk-lib/aws-kinesis";
const stream = new kinesis.Stream(this, "Clicks", {
  shardCount: 4,
  retentionPeriod: cdk.Duration.hours(48),
  encryption: kinesis.StreamEncryption.KMS,
});
```

## Boto3 (Python)
```python
import boto3, json
kin = boto3.client("kinesis", region_name="us-east-1")
kin.put_record(StreamName="clicks",
    Data=json.dumps({"page": "/pricing", "user": "c-99"}),
    PartitionKey="c-99")   # same key -> same shard, in order
```

## Delete / teardown
```python
kin.delete_stream(StreamName="clicks", EnforceConsumerDeletion=True)
```

## Expert tips

- Retention lets you replay — consumers can re-read history.
- Watch 'hot shards': uneven partition keys skew load.

## Real-world example

**Disney+** — Real-time recommendations and event delivery at streaming scale.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Kinesis runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production Amazon Kinesis is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for Amazon Kinesis is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **Lambda / Flink** (Consumers process records live.) — see `lambda---flink`
- **Firehose → S3/Redshift** (Batch delivery of the same stream.) — see `firehose-→-s3-redshift`
- **CloudWatch** (Shard-level metrics.) — see `cloudwatch`
