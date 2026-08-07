# 🗂️ Elastic File System (`efs`)

> One shared NFS mount, readable by hundreds of servers at once.

- **Category:** Storage
- **Service id:** `efs`

## Why it exists
EBS is one-server storage. When many instances need the same files, mount EFS everywhere.

## When to use it
Shared web content, lift-and-shift NAS apps, build caches.

## Learn first

- NFS/POSIX vs object storage
- Mount targets per AZ
- Performance modes
- SG-controlled mounts

## Terraform
```hcl
resource "aws_efs_file_system" "content" {
  creation_token = "acme-content"
  throughput_mode = "elastic"
  encrypted = true
}

resource "aws_efs_mount_target" "a" {
  file_system_id = aws_efs_file_system.content.id
  subnet_id = aws_subnet.priv_a.id
  security_groups = [aws_security_group.efs_sg.id]
}
```

## AWS CDK
```ts
import * as efs from "aws-cdk-lib/aws-efs";
const fs = new efs.FileSystem(this, "Content", {
  vpc, encrypted: true,
  throughputMode: efs.ThroughputMode.ELASTIC,
});
```

## Boto3 (Python)
```python
import boto3
efs = boto3.client("efs", region_name="us-east-1")
fs = efs.create_file_system(CreationToken="demo", Encrypted=True)
print(fs["FileSystemId"])  # on EC2: sudo mount -t efs fs-0abc:/ /mnt
```

## Delete / teardown
```python
efs.delete_file_system(FileSystemId="fs-0abc")
```

## Expert tips

- One mount target per AZ keeps traffic local (cheaper, faster).
- Security groups are the only access control — lock port 2049.

## Real-world example

**CMS fleets** — Hundreds of WordPress nodes share one /wp-content mount.

## Next steps

- **EC2 / ECS** (Any fleet mounts the same file system.) — see `ec2---ecs`
- **VPC** (Mount targets live in private subnets.) — see `vpc`
