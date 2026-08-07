# 🥾 AWS CloudTrail (`cloudtrail`)

> Who did what, when, from where — every API call, recorded.

- **Category:** Management & Governance
- **Service id:** `cloudtrail`

## Why it exists
'Who deleted that bucket?' must have an answer in seconds. CloudTrail logs every API action.

## When to use it
Compliance evidence, security investigations, change tracking.

## Learn first

- Management vs data events
- Multi-region trails
- Log validation
- Athena over trails

## Terraform
```hcl
resource "aws_cloudtrail" "org" {
  name = "org-trail"
  s3_bucket_name = aws_s3_bucket.trail_logs.id
  include_global_service_events = true
  is_multi_region_trail = true
  enable_log_file_validation = true
}
```

## AWS CDK
```ts
import * as cloudtrail from "aws-cdk-lib/aws-cloudtrail";
const trail = new cloudtrail.Trail(this, "Org", {
  s3Bucket: trailBucket, isMultiRegionTrail: true,
  enableFileValidation: true,
});
```

## Boto3 (Python)
```python
import boto3
ct = boto3.client("cloudtrail", region_name="us-east-1")
events = ct.lookup_events(LookupAttributes=[
    {"AttributeKey": "EventName", "AttributeValue": "DeleteBucket"}])["Events"]
for e in events:
    print(e["EventTime"], "-", e["Username"])
```

## Delete / teardown
```python
ct.delete_trail(Name="org-trail")
```

## Expert tips

- Multi-region + log validation = tamper-evident audit.
- Query trails with Athena before you need them urgently.

## Real-world example

**Auditors** — Reconstruct exactly who deleted a production bucket, from which IP.

## Next steps

- **S3** (Trail logs delivered to a locked-down bucket.) — see `s3`
- **Athena** (SQL over the trail.) — see `athena`
- **GuardDuty** (Consumes CloudTrail as a detection source.) — see `guardduty`
