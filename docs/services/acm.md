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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Certificate Manager is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Certificate Manager is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Certificate Manager is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Certificate Manager means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Certificate Manager continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **ALB / CloudFront / API Gateway** (Consumers of certificates.) — see `alb---cloudfront---api-gateway`
- **Route 53** (DNS validation records.) — see `route-53`
