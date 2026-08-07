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

## Next steps

- **Auto Scaling / ECS** (Register targets dynamically.) — see `auto-scaling---ecs`
- **ACM** (TLS certs attach to listeners.) — see `acm`
- **WAF** (Regional ACLs protect ALBs.) — see `waf`
- **VPC** (ALB public; targets private.) — see `vpc`
