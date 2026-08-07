# 🔌 AWS Direct Connect (`directconnect`)

> A private fiber line from your data center straight into AWS.

- **Category:** Networking & Delivery
- **Service id:** `directconnect`

## Why it exists
Some traffic must never touch the public internet — regulatory data, huge transfers, predictable latency.

## When to use it
Hybrid cloud, bulk S3 movement, finance & healthcare links.

## Learn first

- Dedicated vs hosted connections
- Virtual interfaces
- BGP basics

## Terraform
```hcl
resource "aws_dx_connection" "hq" {
  bandwidth = "1Gbps"
  location = "EqDC2"   # Equinix Ashburn
  name = "hq-link"
}

resource "aws_dx_gateway" "corp" { name = "corp-gw" }

resource "aws_dx_gateway_association" "hub" {
  dx_gateway_id = aws_dx_gateway.corp.id
  associated_gateway_id = aws_ec2_transit_gateway.hub.id
}
```

## AWS CDK
```ts
import * as dx from "aws-cdk-lib/aws-directconnect";
new dx.CfnConnection(this, "Hq", {
  bandwidth: "1Gbps", location: "EqDC2", connectionName: "hq-link",
});
new dx.CfnGateway(this, "Corp", { gatewayName: "corp-gw" });
```

## Boto3 (Python)
```python
import boto3
dx = boto3.client("directconnect", region_name="us-east-1")
for c in dx.describe_connections()["connections"]:
    print(c["connectionName"], c["connectionState"], c["bandwidth"])
```

## Delete / teardown
```python
dx.delete_connection(connectionId="dxcon-abc")
```

## Expert tips

- Provision a redundant link — single fibers get cut.
- LAG bundles links for aggregated bandwidth.

## Real-world example

**Banks** — Stream market data over dedicated 10 Gbps links.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Direct Connect runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production AWS Direct Connect is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for AWS Direct Connect is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **Transit Gateway** (DX plugs into the TGW; every attached VPC becomes reachable.) — see `transit-gateway`
- **Route 53** (Consistent on-prem ↔ cloud DNS.) — see `route-53`
