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

## Next steps

- **Transit Gateway** (DX plugs into the TGW; every attached VPC becomes reachable.) — see `transit-gateway`
- **Route 53** (Consistent on-prem ↔ cloud DNS.) — see `route-53`
