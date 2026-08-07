# ☂️ AWS Shield (`shield`)

> DDoS protection — always-on L3/4 defense; Advanced guards L7.

- **Category:** Security, Identity & Compliance
- **Service id:** `shield`

## Why it exists
Volumetric attacks hit everyone eventually. Standard is free and automatic; Advanced adds L7 rules, response team and cost protection.

## When to use it
Protecting CloudFront, ALB/NLB, Global Accelerator, Route 53.

## Learn first

- Standard (always on) vs Advanced
- L3/4 vs L7 attack vectors
- Shield Response Team (SRT)
- Cost protection

## Terraform
```hcl
resource "aws_shield_protection" "cf" {
  name = "cloudfront-shield"
  resource_arn = aws_cloudfront_distribution.site.arn
}
# Shield Standard (L3/4) is automatic for every account.
```

## AWS CDK
```ts
import * as shield from "aws-cdk-lib/aws-route53"; // Shield via CfnProtection
new shield.CfnProtection(this, "CfShield", {
  name: "cloudfront-shield",
  resourceArn: dist.distributionArn,
});
```

## Boto3 (Python)
```python
import boto3
sh = boto3.client("shield", region_name="us-east-1")
for p in sh.list_protections()["Protections"]:
    print(p["Name"], p["ResourceArn"])
```

## Delete / teardown
```python
sh.delete_protection(ProtectionId=pid)
```

## Expert tips

- Advanced includes 24/7 access to the DDoS Response Team.
- Bundle Advanced with WAF — they're designed together.

## Real-world example

**Ticketing platforms** — Survive sale-day bot floods with Shield Advanced + WAF.

## Next steps

- **WAF** (L7 rules layer on top of Shield.) — see `waf`
- **CloudFront / ALB / GA** (The protected surfaces.) — see `cloudfront---alb---ga`
- **Route 53** (DNS layer protection.) — see `route-53`
