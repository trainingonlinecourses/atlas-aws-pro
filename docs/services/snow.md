# ❄️ Snowball / Snowmobile (`snow`)

> Petabyte-mover by truck — when the network is simply too slow.

- **Category:** Migration & Transfer
- **Service id:** `snow`

## Why it exists
At 1 Gbps, 1 PB takes ~3 months. Snowball Edge carries 80-100 TB per box; Snowmobile is a 40-foot container for exabytes.

## When to use it
One-time bulk migrations, remote/offline sites, tape replacement.

## Learn first

- Snowball vs Edge vs Snowmobile
- Ordering & job workflow
- On-device compute basics
- Chain of custody / encryption

## Terraform
```hcl
# Snow devices are physical — ordered via console/API, not Terraform.
# IaC manages the IAM role the device assumes when shipping into S3:
resource "aws_iam_role" "snow" {
  name = "snow-import-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"; Action = "sts:AssumeRole"
      Principal = { Service = "importexport.amazonaws.com" }
    }]
  })
}
```

## AWS CDK
```ts
// No CDK construct — device jobs are API/console operations.
// Keep the landing bucket + role in CDK, order the device manually.
```

## Boto3 (Python)
```python
import boto3
imp = boto3.client("snowball", region_name="us-east-1")
for j in imp.list_jobs()["JobList"]:
    print(j["JobId"], j["JobState"], j["JobType"])
```

## Delete / teardown
```python
imp.cancel_job(JobId=jid)  # before the device ships
```

## Expert tips

- Encrypt with your KMS key before the device leaves AWS.
- Plan the return logistics — devices have due dates.

## Real-world example

**Film studios** — Ship a season of raw footage on Snowballs instead of frying the uplink.

## Next steps

- **S3** (Where the boxes empty into.) — see `s3`
- **KMS** (Device-side encryption keys.) — see `kms`
- **DataSync** (Takes over for ongoing syncs after the initial dump.) — see `datasync`
