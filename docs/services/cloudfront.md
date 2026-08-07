# 🌍 Amazon CloudFront (`cloudfront`)

> The CDN — your content served from 310+ edge locations worldwide.

- **Category:** Networking & Delivery
- **Service id:** `cloudfront`

## Why it exists
Users in Tokyo shouldn't fetch assets from Virginia. CloudFront caches at the edge and terminates TLS.

## When to use it
Static assets, video streaming, API acceleration.

## Learn first

- Origins, behaviors, cache policies
- TTLs & invalidation
- Signed URLs
- Origin Access Control

## Terraform
```hcl
resource "aws_cloudfront_distribution" "site" {
  enabled = true
  aliases = ["www.acme.dev"]
  origin {
    domain_name = aws_s3_bucket.assets.bucket_regional_domain_name
    origin_id = "s3"
    origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
  }
  default_cache_behavior {
    target_origin_id = "s3"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods = ["GET", "HEAD"]
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }
  restrictions { geo_restriction { restriction_type = "none" } }
  viewer_certificate { cloudfront_default_certificate = true }
}
```

## AWS CDK
```ts
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as origins from "aws-cdk-lib/aws-cloudfront-origins";
const dist = new cloudfront.Distribution(this, "Site", {
  defaultBehavior: {
    origin: origins.S3BucketOrigin.withOriginAccessControl(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
  },
});
```

## Boto3 (Python)
```python
import boto3
cf = boto3.client("cloudfront")
cf.create_invalidation(DistributionId="E1A2B3C4",
    InvalidationBatch={"Paths": {"Quantity": 1, "Items": ["/images/*"]},
                       "CallerReference": "deploy-2026-08-05"})
```

## Delete / teardown
```python
# disable the distribution first, then delete_distribution
```

## Expert tips

- Cache static, don't cache auth'd APIs — split behaviors.
- OAC replaces legacy OAI; always use OAC.

## Real-world example

**Prime Video** — CloudFront was built to deliver Prime Video.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon CloudFront runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production Amazon CloudFront is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for Amazon CloudFront is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **S3** (The most common origin, locked with OAC.) — see `s3`
- **WAF** (Web ACLs attach to distributions.) — see `waf`
- **Lambda@Edge** (Code at 310+ PoPs.) — see `lambda@edge`
