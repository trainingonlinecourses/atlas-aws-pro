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

## Next steps

- **VPC Peering** (Use peering for 2-3 VPCs; TGW when it grows.) — see `vpc-peering`
- **Direct Connect** (On-prem links terminate into the TGW.) — see `direct-connect`
- **RAM** (Share the gateway across accounts.) — see `ram`
