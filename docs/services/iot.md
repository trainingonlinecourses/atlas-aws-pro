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

## Next steps

- **S3** (Store raw telemetry.) — see `s3`
- **Kinesis** (High-throughput device streams.) — see `kinesis`
- **IoT Analytics** (Analyze device data.) — see `iot-analytics`
