# 🛡️ Web Application Firewall (`waf`)

> Block SQLi, XSS, bots and brute force before they reach your app.

- **Category:** Security, Identity & Compliance
- **Service id:** `waf`

## Why it exists
Load balancers don't read payloads. WAF inspects HTTP requests — rate limits /login, blocks injection patterns.

## When to use it
Protecting CloudFront, ALB and API Gateway front doors.

## Learn first

- Web ACLs & rules
- Rate-based vs pattern rules
- Managed rule groups (OWASP)

## Terraform
```hcl
resource "aws_wafv2_web_acl" "edge" {
  name = "edge-acl"; scope = "REGIONAL"
  default_action { allow {} }
  rule {
    name = "rate-limit"; priority = 1
    action { block {} }
    statement {
      rate_based_statement { limit = 300; aggregate_key_type = "IP" }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name = "rate-limit"
      sampled_requests_enabled = true
    }
  }
  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name = "edge-acl"
    sampled_requests_enabled = true
  }
}

resource "aws_wafv2_web_acl_association" "alb" {
  resource_arn = aws_lb.web.arn
  web_acl_arn = aws_wafv2_web_acl.edge.arn
}
```

## AWS CDK
```ts
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
new wafv2.CfnWebACL(this, "Edge", {
  scope: "REGIONAL",
  defaultAction: { allow: {} },
  rules: [{
    name: "rate-limit", priority: 1, action: { block: {} },
    statement: { rateBasedStatement: { limit: 300, aggregateKeyType: "IP" } },
    visibilityConfig: { cloudWatchMetricsEnabled: true,
      metricName: "rate-limit", sampledRequestsEnabled: true },
  }],
  visibilityConfig: { cloudWatchMetricsEnabled: true,
    metricName: "edge-acl", sampledRequestsEnabled: true },
});
```

## Boto3 (Python)
```python
import boto3
waf = boto3.client("wafv2", region_name="us-east-1")
for acl in waf.list_web_acls(Scope="REGIONAL")["WebACLs"]:
    print(acl["Name"], acl["Id"])
```

## Delete / teardown
```python
waf.delete_web_acl(Name="edge-acl", Scope="REGIONAL", Id=aclid, LockToken=tok)
```

## Expert tips

- Start in COUNT mode, watch sampled requests, then switch to BLOCK.
- Attach AWS managed rule groups before writing custom rules.

## Real-world example

**E-commerce** — Block credential-stuffing on /login before it reaches the ALB.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Web Application Firewall is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Web Application Firewall is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Web Application Firewall is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Web Application Firewall means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Web Application Firewall continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **CloudFront / ALB / API Gateway** (The three surfaces a Web ACL attaches to.) — see `cloudfront---alb---api-gateway`
- **CloudWatch** (Sampled requests show what got blocked.) — see `cloudwatch`
