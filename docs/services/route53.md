# 🧭 Amazon Route 53 (`route53`)

> DNS with superpowers: health checks, failover, latency routing.

- **Category:** Networking & Delivery
- **Service id:** `route53`

## Why it exists
Every request starts with DNS. Route 53 also detects unhealthy endpoints and reroutes users.

## When to use it
Domain hosting, alias records, multi-region failover, private DNS.

## Learn first

- Record types & alias records
- Latency vs failover routing
- Health checks
- Private hosted zones

## Terraform
```hcl
resource "aws_route53_zone" "acme" { name = "acme.dev" }

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.acme.zone_id
  name = "www.acme.dev"; type = "A"
  alias {
    name = aws_lb.web.dns_name
    zone_id = aws_lb.web.zone_id
    evaluate_target_health = true
  }
}
```

## AWS CDK
```ts
import * as route53 from "aws-cdk-lib/aws-route53";
import * as targets from "aws-cdk-lib/aws-route53-targets";
const zone = new route53.HostedZone(this, "Zone", { zoneName: "acme.dev" });
new route53.ARecord(this, "Www", {
  zone, recordName: "www",
  target: route53.RecordTarget.fromAlias(new targets.LoadBalancerTarget(alb)),
});
```

## Boto3 (Python)
```python
import boto3
r53 = boto3.client("route53")
for z in r53.list_hosted_zones()["HostedZones"]:
    print(z["Name"], z["Id"])
```

## Delete / teardown
```python
r53.delete_hosted_zone(Id="/hostedzone/Z123...")  # delete records first
```

## Expert tips

- Use ALIAS records to AWS targets, CNAME only for external.
- 100% SLA is why DNS lives here.

## Real-world example

**Global SaaS** — Route users to the nearest healthy region with latency records.

## Next steps

- **CloudFront / ALB** (Alias records point here — no IPs to manage.) — see `cloudfront---alb`
- **ACM** (DNS validation records for certs.) — see `acm`
- **Health checks** (Trigger CloudWatch alarms.) — see `health-checks`
