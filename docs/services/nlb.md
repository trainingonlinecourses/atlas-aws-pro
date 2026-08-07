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

## Next steps

- **PrivateLink** (Endpoint services sit behind NLBs.) — see `privatelink`
- **EKS** (Service type LoadBalancer provisions NLBs.) — see `eks`
- **Global Accelerator** (Uses NLBs/ALBs as endpoints.) — see `global-accelerator`
