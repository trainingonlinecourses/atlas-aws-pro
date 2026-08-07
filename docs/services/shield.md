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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Shield is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where AWS Shield is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production AWS Shield is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for AWS Shield means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps AWS Shield continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **WAF** (L7 rules layer on top of Shield.) — see `waf`
- **CloudFront / ALB / GA** (The protected surfaces.) — see `cloudfront---alb---ga`
- **Route 53** (DNS layer protection.) — see `route-53`
