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

## Next steps

- **S3** (The target of every gateway upload.) — see `s3`
- **DMS** (Related migration paths.) — see `dms`
- **Snowball** (Bulk data transfer for big migrations.) — see `snowball`
