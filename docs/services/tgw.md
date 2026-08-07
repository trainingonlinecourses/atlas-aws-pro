# 🔀 AWS Transit Gateway (`tgw`)

> One hub that connects every VPC, on-prem network and shared service.

- **Category:** Networking & Delivery
- **Service id:** `tgw`

## Why it exists
Peering 30 VPCs pairwise means 435 connections. TGW replaces that with one hub: every VPC attaches once.

## When to use it
Enterprise multi-account networking, hub-and-spoke, hybrid routing.

## Learn first

- Hub-and-spoke vs mesh
- TGW route tables
- When peering/PrivateLink is simpler

## Terraform
```hcl
resource "aws_ec2_transit_gateway" "hub" {
  description = "hub for regional VPCs"
  amazon_side_asn = 64512
}

resource "aws_ec2_transit_gateway_vpc_attachment" "prod" {
  transit_gateway_id = aws_ec2_transit_gateway.hub.id
  vpc_id = aws_vpc.prod.id
  subnet_ids = [aws_subnet.tgw_a.id]
}
```

## AWS CDK
```ts
const tgw = new ec2.CfnTransitGateway(this, "Hub", {
  description: "hub for regional VPCs", amazonSideAsn: 64512,
});
new ec2.CfnTransitGatewayAttachment(this, "ProdAttach", {
  transitGatewayId: tgw.ref, vpcId: prodVpc.vpcId,
  subnetIds: [tgwSubnetA.subnetId],
});
```

## Boto3 (Python)
```python
import boto3
tgwc = boto3.client("ec2", region_name="us-east-1")
for g in tgwc.describe_transit_gateways()["TransitGateways"]:
    print(g["TransitGatewayId"], g["State"])
```

## Delete / teardown
```python
# detach VPCs first, then:
tgwc.delete_transit_gateway(TransitGatewayId="tgw-0abc")
```

## Expert tips

- Route tables on the TGW decide who can reach whom — segment there.
- It bills hourly per attachment — count before you attach.

## Real-world example

**Enterprises** — Consolidate hundreds of VPCs into a hub-and-spoke with central inspection.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Transit Gateway runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production AWS Transit Gateway is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for AWS Transit Gateway is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **VPC Peering** (Use peering for 2-3 VPCs; TGW when it grows.) — see `vpc-peering`
- **Direct Connect** (On-prem links terminate into the TGW.) — see `direct-connect`
- **RAM** (Share the gateway across accounts.) — see `ram`
