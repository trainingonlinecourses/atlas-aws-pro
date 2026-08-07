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

## Next steps

- **S3 / EFS** (Destinations for migrated data.) — see `s3---efs`
- **Direct Connect** (The pipe it saturates.) — see `direct-connect`
- **Snow Family** (When even DataSync is too slow.) — see `snow-family`
