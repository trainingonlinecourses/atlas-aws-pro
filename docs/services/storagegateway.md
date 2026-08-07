# 🚪 AWS Storage Gateway (`storagegateway`)

> Bridge your on-premises storage to AWS — cache, backup and archive without re-architecting.

- **Category:** Storage
- **Service id:** `storagegateway`

## Why it exists
Hybrid cloud starts here: a virtual appliance gives on-prem apps low-latency cached access to S3 and lands backups in AWS.

## When to use it
NAS migration, tape replacement, disaster recovery, cloud-backed file shares.

## Learn first

- File vs Volume vs Tape gateway
- The on-prem appliance
- SMB/NFS protocol mapping
- Bandwidth throttling

## Terraform
```hcl
resource "aws_storagegateway_gateway" "gw" {
  gateway_name = "site-a-gw"
  gateway_ip_address = "10.0.0.20"
  gateway_type = "FILE_S3"
  gateway_timezone = "GMT"
}
```

## AWS CDK
```ts
// No first-class CDK construct — the gateway is an on-prem appliance.
```

## Boto3 (Python)
```python
import boto3
sgw = boto3.client("storagegateway", region_name="us-east-1")
for g in sgw.list_gateways()["Gateways"]:
    print(g["GatewayARN"], g["GatewayType"])
```

## Delete / teardown
```python
sgw.delete_gateway(GatewayARN="arn:aws:storagegateway:...")
```

## Expert tips

- Files are always eventually in S3 — the gateway is a cache in front.
- Use Tape Gateway to retire physical tapes for backup compliance.

## Real-world example

**Enterprise IT** — Backup tools like Veeam send copies to AWS.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Storage Gateway holds throwaway data. Versioning and lifecycle are on from day one so bad deletes stay reversible.

- Enable versioning and object-lock from the first bucket — retrofitting is painful.
- Use a dev-only prefix/account; never let dev code write to a prod path.
- Set a short lifecycle rule to expire dev objects automatically and keep the bill near zero.

### 🧪 Staging / Pre-prod

Staging proves the data pipeline end-to-end with realistic volumes and the same policies as prod.

- Mirror prod's bucket names, permissions, and lifecycle — test the policy, not a happy path.
- Run the migration/replication job against staging data before production cutover.
- Verify restore from a versioned snapshot here, where failure costs nothing.

### 🚀 Production

In production AWS Storage Gateway is the durability backbone: versioning, MFA-delete, replication, and access auditing are non-negotiable.

- Enable versioning + MFA Delete and cross-region replication to a second bucket.
- Use Object Lock/WORM for anything auditable; block public access at the account level.
- Centralize access with bucket policies + IAM and watch Macie/GuardDuty findings on the data.

### 🌍 Multi-region / DR

DR means a second copy in another region with a tested restore path, not a bucket that only exists once.

- Cross-region replicate critical prefixes; set an RPO you can actually honor.
- Test a full restore from the replica at least quarterly and log the elapsed time.
- Automate promotion: if the primary region degrades, the replica bucket takes over with the same DNS.

### ♻️ Lifecycle & IaC

Lifecycle manages the data class, not just the bucket: hot -> warm -> archive on a policy.

- Define lifecycle rules (S3 -> Glacier -> Expire) so cost shrinks automatically.
- Own the bucket in Terraform with a remote-state lock so two pipelines can't clobber it.
- Add cost-alerting per bucket and a monthly report of the top spenders.

## Next steps

- **S3** (The target of every gateway upload.) — see `s3`
- **DMS** (Related migration paths.) — see `dms`
- **Snowball** (Bulk data transfer for big migrations.) — see `snowball`
