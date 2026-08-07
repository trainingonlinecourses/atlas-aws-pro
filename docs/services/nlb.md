# 🚦 Network Load Balancer (`nlb`)

> Layer-4 load balancer — millions of connections/sec, static IPs, TCP/UDP/TLS.

- **Category:** Networking & Delivery
- **Service id:** `nlb`

## Why it exists
Ultra-high-throughput TCP/UDP, static IPs per AZ, or fronting PrivateLink/EKS services — that's L4 territory.

## When to use it
Game servers, IoT fleets, PrivateLink endpoint services, k8s LoadBalancer services.

## Learn first

- L4 vs L7 (ALB)
- Static IP per AZ
- Target groups: instance/IP modes
- Pairs with PrivateLink & Global Accelerator

## Terraform
```hcl
resource "aws_lb" "tcp" {
  name               = "tcp-nlb"
  load_balancer_type = "network"
  subnets            = [aws_subnet.pub_a.id, aws_subnet.pub_b.id]
}

resource "aws_lb_target_group" "tcp" {
  name = "tcp-tg"; port = 443; protocol = "TLS"
  vpc_id = aws_vpc.main.id
}

resource "aws_lb_listener" "tcp" {
  load_balancer_arn = aws_lb.tcp.arn
  port = 443; protocol = "TLS"
  certificate_arn = aws_acm_certificate.site.arn
  default_action { type = "forward"; target_group_arn = aws_lb_target_group.tcp.arn }
}
```

## AWS CDK
```ts
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
const nlb = new elbv2.NetworkLoadBalancer(this, "Tcp", {
  vpc, internetFacing: true,
});
```

## Boto3 (Python)
```python
import boto3
elb = boto3.client("elbv2", region_name="us-east-1")
for lb in elb.describe_load_balancers()["LoadBalancers"]:
    if lb["Type"] == "network":
        print(lb["LoadBalancerName"], lb["State"]["Code"])
```

## Delete / teardown
```python
elb.delete_load_balancer(LoadBalancerArn=arn)
```

## Expert tips

- NLB preserves the client source IP; ALB doesn't.
- PrivateLink endpoint services REQUIRE an NLB.

## Real-world example

**Game studios** — Absorb millions of concurrent TCP connections with static IPs.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Network Load Balancer runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production Network Load Balancer is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for Network Load Balancer is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **PrivateLink** (Endpoint services sit behind NLBs.) — see `privatelink`
- **EKS** (Service type LoadBalancer provisions NLBs.) — see `eks`
- **Global Accelerator** (Uses NLBs/ALBs as endpoints.) — see `global-accelerator`
