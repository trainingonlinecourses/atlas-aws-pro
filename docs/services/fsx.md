# 🗂️ Amazon FSx (`fsx`)

> Fully managed, high-performance file systems — Lustre, NetApp ONTAP, OpenZFS, Windows File Server.

- **Category:** Storage
- **Service id:** `fsx`

## Why it exists
High-performance compute (HPC, EDA, video) needs parallel file systems, and Windows shops need SMB. FSx runs those without you operating the infrastructure.

## When to use it
HPC workloads, Windows file shares, replacing on-prem NAS.

## Learn first

- Windows vs Lustre vs OpenZFS types
- SMB/NFS vs POSIX clients
- Backups & replication
- Data compression tier

## Terraform
```hcl
resource "aws_fsx_lustre_file_system" "hpc" {
  storage_capacity = 1200
  deployment_type  = "PERSISTENT_1"
  per_unit_storage_throughput = 200
}
```

## AWS CDK
```ts
import * as fsx from "aws-cdk-lib/aws-fsx";
new fsx.LustreFileSystem(this, "Hpc", {
  vpc, storageCapacityGiB: 1200,
  deploymentType: fsx.LustreDeploymentType.PERSISTENT_1,
});
```

## Boto3 (Python)
```python
import boto3
fsx = boto3.client("fsx", region_name="us-east-1")
for fs in fsx.describe_file_systems()["FileSystems"]:
    print(fs["FileSystemId"], fs["FileSystemType"], fs["Lifecycle"])
```

## Delete / teardown
```python
fsx.delete_file_system(FileSystemId="fs-0abc123")
```

## Expert tips

- Match the type to the workload — Lustre for HPC, Windows for SMB, OpenZFS for NFS at scale.
- Enable the data-compression tier on Lustre to cut storage cost 50%+.

## Real-world example

**Media & VFX studios** — Shared storage for rendering farms.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon FSx holds throwaway data. Versioning and lifecycle are on from day one so bad deletes stay reversible.

- Enable versioning and object-lock from the first bucket — retrofitting is painful.
- Use a dev-only prefix/account; never let dev code write to a prod path.
- Set a short lifecycle rule to expire dev objects automatically and keep the bill near zero.

### 🧪 Staging / Pre-prod

Staging proves the data pipeline end-to-end with realistic volumes and the same policies as prod.

- Mirror prod's bucket names, permissions, and lifecycle — test the policy, not a happy path.
- Run the migration/replication job against staging data before production cutover.
- Verify restore from a versioned snapshot here, where failure costs nothing.

### 🚀 Production

In production Amazon FSx is the durability backbone: versioning, MFA-delete, replication, and access auditing are non-negotiable.

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

- **EFS** (Cheaper network FS for generic Linux.) — see `efs`
- **S3** (Lifecycle cold data off FSx.) — see `s3`
