# 💾 Elastic Block Store (`ebs`)

> Real block storage for EC2 — the hard drive that survives a reboot.

- **Category:** Storage
- **Service id:** `ebs`

## Why it exists
Instance storage is ephemeral; for databases or durability you attach an EBS volume.

## When to use it
Boot disks, database volumes (gp3/io2), low-latency block I/O.

## Learn first

- Volume types: gp3, io2
- IOPS vs throughput
- Snapshots & AMIs
- KMS encryption

## Terraform
```hcl
resource "aws_ebs_volume" "pg_data" {
  availability_zone = "us-east-1a"
  type = "gp3"; size = 200; iops = 6000
  throughput = 350; encrypted = true
  tags = { Name = "postgres-data" }
}

resource "aws_volume_attachment" "pg" {
  device_name = "/dev/sdf"
  volume_id = aws_ebs_volume.pg_data.id
  instance_id = aws_instance.db.id
}
```

## AWS CDK
```ts
const vol = new ec2.Volume(this, "PgData", {
  availabilityZone: "us-east-1a",
  size: cdk.Size.gibibytes(200),
  volumeType: ec2.EbsDeviceVolumeType.GP3,
  iops: 6000, encrypted: true,
});
```

## Boto3 (Python)
```python
import boto3
ec2 = boto3.client("ec2", region_name="us-east-1")
vol = ec2.create_volume(AvailabilityZone="us-east-1a", Size=100,
                        VolumeType="gp3", Encrypted=True)
ec2.create_snapshot(VolumeId=vol["VolumeId"])
```

## Delete / teardown
```python
ec2.detach_volume(VolumeId="vol-0abc")
ec2.delete_volume(VolumeId="vol-0abc")
```

## Expert tips

- Volumes are AZ-bound — replicate snapshots across AZs for DR.
- gp3 gives you baseline performance cheaper than gp2.

## Real-world example

**Any DB on EC2** — io2 volumes give sustained sub-millisecond latency to databases.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Elastic Block Store holds throwaway data. Versioning and lifecycle are on from day one so bad deletes stay reversible.

- Enable versioning and object-lock from the first bucket — retrofitting is painful.
- Use a dev-only prefix/account; never let dev code write to a prod path.
- Set a short lifecycle rule to expire dev objects automatically and keep the bill near zero.

### 🧪 Staging / Pre-prod

Staging proves the data pipeline end-to-end with realistic volumes and the same policies as prod.

- Mirror prod's bucket names, permissions, and lifecycle — test the policy, not a happy path.
- Run the migration/replication job against staging data before production cutover.
- Verify restore from a versioned snapshot here, where failure costs nothing.

### 🚀 Production

In production Elastic Block Store is the durability backbone: versioning, MFA-delete, replication, and access auditing are non-negotiable.

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

- **EC2** (Volumes attach to one instance at a time.) — see `ec2`
- **KMS** (Volumes encrypted with your keys.) — see `kms`
- **Backup** (Central plans snapshot fleets.) — see `backup`
