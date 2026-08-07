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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Elastic File System holds throwaway data. Versioning and lifecycle are on from day one so bad deletes stay reversible.

- Enable versioning and object-lock from the first bucket — retrofitting is painful.
- Use a dev-only prefix/account; never let dev code write to a prod path.
- Set a short lifecycle rule to expire dev objects automatically and keep the bill near zero.

### 🧪 Staging / Pre-prod

Staging proves the data pipeline end-to-end with realistic volumes and the same policies as prod.

- Mirror prod's bucket names, permissions, and lifecycle — test the policy, not a happy path.
- Run the migration/replication job against staging data before production cutover.
- Verify restore from a versioned snapshot here, where failure costs nothing.

### 🚀 Production

In production Elastic File System is the durability backbone: versioning, MFA-delete, replication, and access auditing are non-negotiable.

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

- **EC2 / ECS** (Any fleet mounts the same file system.) — see `ec2---ecs`
- **VPC** (Mount targets live in private subnets.) — see `vpc`
