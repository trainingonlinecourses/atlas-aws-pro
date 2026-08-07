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

## Next steps

- **EC2** (Volumes attach to one instance at a time.) — see `ec2`
- **KMS** (Volumes encrypted with your keys.) — see `kms`
- **Backup** (Central plans snapshot fleets.) — see `backup`
