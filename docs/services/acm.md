# 📜 Certificate Manager (`acm`)

> Free TLS certificates, issued and auto-renewed.

- **Category:** Security, Identity & Compliance
- **Service id:** `acm`

## Why it exists
HTTPS is non-negotiable, and hand-managed certs expire at the worst moment. ACM renews automatically.

## When to use it
TLS for domains on CloudFront, ALB and API Gateway.

## Learn first

- DNS vs email validation
- ACM works with AWS services only
- Wildcard certs

## Terraform
```hcl
resource "aws_acm_certificate" "site" {
  domain_name = "*.acme.dev"
  validation_method = "DNS"
  lifecycle { create_before_destroy = true }
}
```

## AWS CDK
```ts
import * as acm from "aws-cdk-lib/aws-certificatemanager";
const cert = new acm.Certificate(this, "Site", {
  domainName: "*.acme.dev",
  validation: acm.CertificateValidation.fromDns(zone),
});
```

## Boto3 (Python)
```python
import boto3
acm = boto3.client("acm", region_name="us-east-1")
for c in acm.list_certificates()["CertificateSummaryList"]:
    print(c["DomainName"], c["CertificateArn"])
```

## Delete / teardown
```python
acm.delete_certificate(CertificateArn=arn)  # must not be in use
```

## Expert tips

- CloudFront certs MUST be issued in us-east-1.
- create_before_destroy avoids downtime during replacement.

## Real-world example

**Every HTTPS site** — Auto-renews the TLS certs powering CloudFront and ALB — free.

## Next steps

- **ALB / CloudFront / API Gateway** (Consumers of certificates.) — see `alb---cloudfront---api-gateway`
- **Route 53** (DNS validation records.) — see `route-53`
