# 📡 AWS IoT Core (`iot`)

> Connect millions of devices. MQTT pub/sub, device shadows, rules that route telemetry.

- **Category:** Application Integration
- **Service id:** `iot`

## Why it exists
Devices aren't reliable HTTP clients. IoT Core speaks MQTT, manages device identity with certificates, and routes telemetry to the services that matter.

## When to use it
Device telemetry, fleet OTA updates, smart products, predictive maintenance.

## Learn first

- MQTT vs HTTPS
- Thing registry & certificates
- Device Shadows
- IoT Rules → services

## Terraform
```hcl
resource "aws_iot_thing" "sensor" {
  name = "temp-sensor-01"
}
resource "aws_iot_topic_rule" "route" {
  name     = "temp_to_s3"
  sql      = "SELECT * FROM 'devices/+/temp'"
  sql_version = "2016-03-23"
  s3 {
    role_arn = aws_iam_role.iot_s3.arn
    bucket   = aws_s3_bucket.telemetry.id
    key      = "${topic()}/${timestamp()}"
  }
}
```

## AWS CDK
```ts
// L1 construct only — manage via CfnThing + CfnTopicRule.
```

## Boto3 (Python)
```python
import boto3
iot = boto3.client("iot-data", region_name="us-east-1")
iot.publish(topic="devices/garage-01/temp",
    qos=1, payload=b'{"celsius": 22.4}')
```

## Delete / teardown
```python
# Delete things, certs, and policies; delete rules separately.
```

## Expert tips

- Every device needs its own certificate — a shared key is a fleet-wide breach.
- Device Shadows cache state so a device can report offline and the cloud still serves it.

## Real-world example

**Fleet operators** — Predictive maintenance by streaming engine telemetry to anomaly detection.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS IoT Core is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where AWS IoT Core is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production AWS IoT Core is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for AWS IoT Core is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats AWS IoT Core as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **S3** (Store raw telemetry.) — see `s3`
- **Kinesis** (High-throughput device streams.) — see `kinesis`
- **IoT Analytics** (Analyze device data.) — see `iot-analytics`
