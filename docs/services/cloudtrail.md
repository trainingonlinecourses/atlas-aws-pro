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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS CloudTrail keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS CloudTrail is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS CloudTrail is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS CloudTrail means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **S3** (Trail logs delivered to a locked-down bucket.) — see `s3`
- **Athena** (SQL over the trail.) — see `athena`
- **GuardDuty** (Consumes CloudTrail as a detection source.) — see `guardduty`
