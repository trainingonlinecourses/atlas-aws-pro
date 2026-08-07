# 🛰️ AWS Global Accelerator (`globalaccelerator`)

> Two static anycast IPs + AWS backbone routing across regions.

- **Category:** Networking & Delivery
- **Service id:** `globalaccelerator`

## Why it exists
Global users need predictable latency and instant regional failover without DNS TTL delays.

## When to use it
Global apps, game servers, TCP/UDP a CDN can't serve.

## Learn first

- Anycast static IPs
- Listeners & endpoint groups
- GA vs CloudFront

## Terraform
```hcl
resource "aws_global_accelerator_accelerator" "app" { name = "app-accelerator" }

resource "aws_global_accelerator_listener" "https" {
  accelerator_arn = aws_global_accelerator_accelerator.app.id
  protocol = "TCP"
  port_range { from_port = 443; to_port = 443 }
}

resource "aws_global_accelerator_endpoint_group" "use1" {
  listener_arn = aws_global_accelerator_listener.https.id
  endpoint_group_region = "us-east-1"
  endpoint_configuration { endpoint_id = aws_lb.web.arn; weight = 100 }
}
```

## AWS CDK
```ts
import * as ga from "aws-cdk-lib/aws-globalaccelerator";
const accel = new ga.CfnAccelerator(this, "App", { name: "app-accelerator" });
new ga.CfnListener(this, "Https", {
  acceleratorArn: accel.attrAcceleratorArn,
  protocol: "TCP", portRanges: [{ fromPort: 443, toPort: 443 }],
});
```

## Boto3 (Python)
```python
import boto3
ga = boto3.client("globalaccelerator", region_name="us-west-2")
for a in ga.list_accelerators()["Accelerators"]:
    print(a["Name"], a["Status"], a["IpSets"])
```

## Delete / teardown
```python
ga.delete_accelerator(AcceleratorArn=arn)  # disable first
```

## Expert tips

- Static IPs are gold for allowlists and mobile clients.
- GA is TCP/UDP; CloudFront is HTTP caching — different tools.

## Real-world example

**Game studios** — Route players to the nearest healthy region with sub-second failover.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Global Accelerator runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production AWS Global Accelerator is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for AWS Global Accelerator is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **ALB / NLB / EIP** (Any of these can be endpoints.) — see `alb---nlb---eip`
- **Route 53** (Alias records at the accelerator.) — see `route-53`
