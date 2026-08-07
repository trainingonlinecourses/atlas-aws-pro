# 🕸️ Virtual Private Cloud (`vpc`)

> Your private network in AWS — the boundary every other service lives inside.

- **Category:** Networking & Delivery
- **Service id:** `vpc`

## Why it exists
Nothing launches without a network. The VPC defines IP space, public vs private subnets, traffic paths. Master this first.

## When to use it
Every workload: multi-tier apps, per-env isolation, shared networks.

## Learn first

- CIDR blocks & subnet math
- Public vs private, IGW vs NAT
- Route tables, NACLs vs SGs
- DNS inside the VPC

## Terraform
```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.20.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "prod-vpc" }
}

resource "aws_internet_gateway" "main" { vpc_id = aws_vpc.main.id }

resource "aws_subnet" "pub_a" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.20.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route { cidr_block = "0.0.0.0/0"; gateway_id = aws_internet_gateway.main.id }
}
```

## AWS CDK
```ts
import * as ec2 from "aws-cdk-lib/aws-ec2";
const vpc = new ec2.Vpc(this, "Main", {
  ipAddresses: ec2.IpAddresses.cidr("10.20.0.0/16"),
  maxAzs: 2, natGateways: 1,   // public+private subnets auto-created
});
```

## Boto3 (Python)
```python
import boto3
ec2 = boto3.resource("ec2", region_name="us-east-1")
vpc = ec2.create_vpc(CidrBlock="10.30.0.0/16")
sub = vpc.create_subnet(CidrBlock="10.30.1.0/24")
print(vpc.id, sub.id)
```

## Delete / teardown
```python
sub.delete(); vpc.delete()   # detach IGW / NAT first
```

## Expert tips

- Plan CIDRs before you peer — overlapping ranges are painful.
- Databases always live in private subnets.

## Real-world example

**Capital One** — Segments hundreds of VPCs by team as its primary security perimeter.

## Next steps

- **Subnets → everything** (EC2, RDS, EKS pods, Lambda ENIs attach here.) — see `subnets-→-everything`
- **Transit Gateway** (Connects this VPC to every other VPC.) — see `transit-gateway`
- **Config** (Watches for security-group drift.) — see `config`
