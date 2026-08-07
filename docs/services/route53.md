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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Route 53 runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production Amazon Route 53 is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for Amazon Route 53 is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **CloudFront / ALB** (Alias records point here — no IPs to manage.) — see `cloudfront---alb`
- **ACM** (DNS validation records for certs.) — see `acm`
- **Health checks** (Trigger CloudWatch alarms.) — see `health-checks`
