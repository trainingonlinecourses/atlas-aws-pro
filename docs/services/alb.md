# ⚖️ Application Load Balancer (`alb`)

> Layer-7 load balancing — routes by path, host, header; terminates TLS.

- **Category:** Networking & Delivery
- **Service id:** `alb`

## Why it exists
One server is an outage waiting to happen. The ALB spreads traffic, terminates HTTPS, health-checks targets.

## When to use it
Web tiers, ECS/EKS ingress, path-based routing.

## Learn first

- Listeners, target groups, rules
- Health check tuning
- TLS with ACM
- X-Forwarded headers

## Terraform
```hcl
resource "aws_lb" "web" {
  name = "web-alb"
  load_balancer_type = "application"
  subnets = [aws_subnet.pub_a.id, aws_subnet.pub_b.id]
  security_groups = [aws_security_group.alb_sg.id]
}

resource "aws_lb_target_group" "web" {
  name = "web-tg"; port = 8080; protocol = "HTTP"
  vpc_id = aws_vpc.main.id
  health_check { path = "/healthz"; interval = 15 }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.web.arn
  port = 443; protocol = "HTTPS"
  certificate_arn = aws_acm_certificate.site.arn
  default_action { type = "forward"; target_group_arn = aws_lb_target_group.web.arn }
}
```

## AWS CDK
```ts
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
const alb = new elbv2.ApplicationLoadBalancer(this, "Web", { vpc, internetFacing: true });
const listener = alb.addListener("Https", { port: 443, certificates: [cert] });
listener.addTargets("Web", { port: 8080, healthCheck: { path: "/healthz" } });
```

## Boto3 (Python)
```python
import boto3
elb = boto3.client("elbv2", region_name="us-east-1")
tg = elb.describe_target_groups(Names=["web-tg"])["TargetGroups"][0]
print(elb.describe_target_health(TargetGroupArn=tg["TargetGroupArn"]))
```

## Delete / teardown
```python
elb.delete_load_balancer(LoadBalancerArn=arn)
```

## Expert tips

- Health check path should be cheap (/healthz), not /.
- ALB spans 2+ AZs by design — never deploy in one.

## Real-world example

**BuzzFeed** — Absorbs viral spikes by spreading load behind ALBs.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Application Load Balancer runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production Application Load Balancer is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for Application Load Balancer is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **Auto Scaling / ECS** (Register targets dynamically.) — see `auto-scaling---ecs`
- **ACM** (TLS certs attach to listeners.) — see `acm`
- **WAF** (Regional ACLs protect ALBs.) — see `waf`
- **VPC** (ALB public; targets private.) — see `vpc`
