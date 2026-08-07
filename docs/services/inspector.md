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

## Next steps

- **ECR** (Image scan findings per repository.) — see `ecr`
- **Security Hub** (Findings roll up centrally.) — see `security-hub`
- **EventBridge** (React to new critical findings.) — see `eventbridge`
