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

## Next steps

- **S3** (The most common origin, locked with OAC.) — see `s3`
- **WAF** (Web ACLs attach to distributions.) — see `waf`
- **Lambda@Edge** (Code at 310+ PoPs.) — see `lambda@edge`
