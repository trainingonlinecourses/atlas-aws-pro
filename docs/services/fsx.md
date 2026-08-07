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

## Next steps

- **EFS** (Cheaper network FS for generic Linux.) — see `efs`
- **S3** (Lifecycle cold data off FSx.) — see `s3`
