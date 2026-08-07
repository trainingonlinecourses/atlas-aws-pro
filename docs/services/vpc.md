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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Virtual Private Cloud runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production Virtual Private Cloud is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for Virtual Private Cloud is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **Subnets → everything** (EC2, RDS, EKS pods, Lambda ENIs attach here.) — see `subnets-→-everything`
- **Transit Gateway** (Connects this VPC to every other VPC.) — see `transit-gateway`
- **Config** (Watches for security-group drift.) — see `config`
