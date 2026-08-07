# 🐞 Amazon Inspector (`inspector`)

> Automated vulnerability scanning for EC2, containers and Lambda.

- **Category:** Security, Identity & Compliance
- **Service id:** `inspector`

## Why it exists
Know about CVEs before attackers do. Inspector continuously scans instances, ECR images and Lambda packages.

## When to use it
Container CVEs, EC2 patch gaps, Lambda dependency risk.

## Learn first

- v2 coverage: EC2 / ECR / Lambda
- Findings & severity
- Suppressions

## Terraform
```hcl
resource "aws_inspector2_enabler" "main" {
  account_ids = [data.aws_caller_identity.current.account_id]
  resource_types = ["EC2", "ECR", "LAMBDA"]
}
```

## AWS CDK
```ts
import * as inspectorv2 from "aws-cdk-lib/aws-inspectorv2";
new inspectorv2.CfnEnabler(this, "InspectorV2", {
  accountIds: [cdk.Aws.ACCOUNT_ID],
  resourceTypes: ["EC2", "ECR", "LAMBDA"],
});
```

## Boto3 (Python)
```python
import boto3
ins = boto3.client("inspector2", region_name="us-east-1")
findings = ins.list_findings(filterCriteria={
    "severity": [{"comparison": "EQUALS", "value": "CRITICAL"}]})
print(len(findings["findings"]), "critical CVE findings")
```

## Delete / teardown
```python
ins.disable(accountIds=[acct], resourceTypes=["EC2","ECR","LAMBDA"])
```

## Expert tips

- Gate deploys: block CRITICAL CVEs in ECR before promotion.
- Scan Lambda too — your pip dependencies are attack surface.

## Real-world example

**Platform security** — Block deploys when ECR images carry critical CVEs.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Inspector is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Amazon Inspector is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Amazon Inspector is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Amazon Inspector means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Inspector continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **ECR** (Image scan findings per repository.) — see `ecr`
- **Security Hub** (Findings roll up centrally.) — see `security-hub`
- **EventBridge** (React to new critical findings.) — see `eventbridge`
