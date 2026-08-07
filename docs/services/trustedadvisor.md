# 🛡️ AWS Trusted Advisor (`trustedadvisor`)

> AWS's built-in auditor — security, cost, performance and fault-tolerance checks across your account.

- **Category:** Management & Governance
- **Service id:** `trustedadvisor`

## Why it exists
You can't manually check 100+ best practices. Trusted Advisor runs the checklists and flags underutilized instances, open security groups and single-AZ risks.

## When to use it
Well-Architected reviews, cost-savings discovery, security posture checks.

## Learn first

- Cost / security / performance / fault tolerance / limits
- Full checks vs Business+ tier
- Weekly report emails
- Pairing with AWS Config

## Terraform
```hcl
# Nothing to provision — Trusted Advisor audits what already exists.
```

## AWS CDK
```ts
// Nothing to build — it's a managed auditing service.
```

## Boto3 (Python)
```python
import boto3
support = boto3.client("support", region_name="us-east-1")
for c in support.describe_trusted_advisor_checks(language="en")["checks"][:5]:
    print(c["id"], c["name"])
```

## Delete / teardown
```python
# Nothing to delete — built-in console service.
```

## Expert tips

- Business+ plans unlock the full check set — budget for the tier.
- Act on 'idle RDS' and 'unused EC2' checks first: fastest savings.

## Real-world example

**Enterprise accounts** — Central cloud teams run monthly TA reviews.

## Next steps

- **Config** (Custom rules beyond TA's checklist.) — see `config`
- **Cost Explorer** (Verify the cost flags.) — see `cost-explorer`
