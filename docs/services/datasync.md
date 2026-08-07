# 🔄 AWS DataSync (`datasync`)

> High-speed mover for on-prem ↔ AWS — NFS/SMB/S3 at up to 10 Gbps.

- **Category:** Migration & Transfer
- **Service id:** `datasync`

## Why it exists
Copying terabytes with rsync takes weeks. DataSync saturates the wire, verifies checksums, and schedules recurring syncs.

## When to use it
NAS → S3 migration, DR replication, inter-bucket moves.

## Learn first

- Agents vs task model
- Locations (NFS/SMB/S3/EFS)
- Bandwidth throttling
- Schedules & filters

## Terraform
```hcl
resource "aws_datasync_location_s3" "dest" {
  s3_bucket_arn = aws_s3_bucket.lake.arn
  subdirectory = "/raw/"
  s3_config { bucket_access_role_arn = aws_iam_role.datasync.arn }
}

resource "aws_datasync_task" "nightly" {
  name = "nas-to-lake"
  source_location_arn = aws_datasync_location_nfs.nas.arn
  destination_location_arn = aws_datasync_location_s3.dest.arn
  options { bytes_per_second = 104857600 }  # 100 MB/s cap
}
```

## AWS CDK
```ts
import * as datasync from "aws-cdk-lib/aws-datasync";
new datasync.CfnLocationS3(this, "Dest", {
  s3BucketArn: lake.bucketArn,
  subdirectory: "/raw/",
  s3Config: { bucketAccessRoleArn: dsRole.roleArn },
});
```

## Boto3 (Python)
```python
import boto3
ds = boto3.client("datasync", region_name="us-east-1")
for t in ds.list_tasks()["Tasks"]:
    print(t["Name"], t["Status"])
```

## Delete / teardown
```python
ds.delete_task(TaskArn=arn)
```

## Expert tips

- Throttle bandwidth during business hours — saturating the WAN hurts everyone.
- Verify with checksums enabled; don't trust blind copies.

## Real-world example

**Media companies** — Nightly 40TB NAS → S3 syncs finish before breakfast.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS DataSync is used to prove the migration path on a sample: small data, same tooling.

- Set up the replication/migration job in dev against a subset of records.
- Validate checksums and row counts on the sample before widening the net.
- Keep the dev source isolated so trial runs can't touch real systems.

### 🧪 Staging / Pre-prod

Staging is the dress rehearsal: a full dry-run migration with a rollback plan.

- Run the full migration on staging data and compare record counts end-to-end.
- Time it and log throughput; the staging number is your prod forecast.
- Write and test the rollback script before you ever need it.

### 🚀 Production

In production AWS DataSync executes the cutover: incremental sync, a short frozen window, and verification.

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

- **S3 / EFS** (Destinations for migrated data.) — see `s3---efs`
- **Direct Connect** (The pipe it saturates.) — see `direct-connect`
- **Snow Family** (When even DataSync is too slow.) — see `snow-family`
