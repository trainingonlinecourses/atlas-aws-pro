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

## Next steps

- **Lambda / Flink** (Consumers process records live.) — see `lambda---flink`
- **Firehose → S3/Redshift** (Batch delivery of the same stream.) — see `firehose-→-s3-redshift`
- **CloudWatch** (Shard-level metrics.) — see `cloudwatch`
