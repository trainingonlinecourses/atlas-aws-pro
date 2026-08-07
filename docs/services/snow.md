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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Snowball / Snowmobile is used to prove the migration path on a sample: small data, same tooling.

- Set up the replication/migration job in dev against a subset of records.
- Validate checksums and row counts on the sample before widening the net.
- Keep the dev source isolated so trial runs can't touch real systems.

### 🧪 Staging / Pre-prod

Staging is the dress rehearsal: a full dry-run migration with a rollback plan.

- Run the full migration on staging data and compare record counts end-to-end.
- Time it and log throughput; the staging number is your prod forecast.
- Write and test the rollback script before you ever need it.

### 🚀 Production

In production Snowball / Snowmobile executes the cutover: incremental sync, a short frozen window, and verification.

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

- **S3** (Where the boxes empty into.) — see `s3`
- **KMS** (Device-side encryption keys.) — see `kms`
- **DataSync** (Takes over for ongoing syncs after the initial dump.) — see `datasync`
