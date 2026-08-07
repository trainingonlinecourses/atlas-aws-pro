# 🏗️ AWS CloudFormation (`cloudformation`)

> AWS-native infrastructure-as-code — the engine under CDK itself.

- **Category:** Management & Governance
- **Service id:** `cloudformation`

## Why it exists
Console clicks don't scale. Templates make infrastructure versionable — and CDK compiles straight into CloudFormation.

## When to use it
Org baselines, service catalog, drift-managed stacks, CDK output.

## Learn first

- Resources, parameters, outputs
- Change sets
- Nested stacks / StackSets
- Drift detection

## Terraform
```hcl
# From Terraform you can deploy a CFN stack:
resource "aws_cloudformation_stack" "quick_vpc" {
  name = "quick-vpc"
  template_body = file("vpc.yaml")
  parameters = { Env = "prod" }
}
# ...or write YAML and run:
#   aws cloudformation deploy --template-file vpc.yaml --stack-name quick-vpc
```

## AWS CDK
```ts
// CDK *is* a CloudFormation generator:
import * as cdk from "aws-cdk-lib";
const app = new cdk.App();
const stack = new cdk.Stack(app, "QuickVpc", { env: { region: "us-east-1" } });
// ...add constructs to the stack...
app.synth();   // cdk synth -> template, cdk deploy -> CloudFormation
```

## Boto3 (Python)
```python
import boto3
cfn = boto3.client("cloudformation", region_name="us-east-1")
cfn.create_stack(StackName="quick-vpc",
    TemplateBody=open("vpc.yaml").read(), Capabilities=["CAPABILITY_IAM"])
print(cfn.describe_stacks(StackName="quick-vpc")["Stacks"][0]["StackStatus"])
```

## Delete / teardown
```python
cfn.delete_stack(StackName="quick-vpc")
```

## Expert tips

- Change sets = terraform plan for CFN — always preview.
- CAPABILITY_NAMED_IAM is required when templates name IAM resources.

## Real-world example

**NASA JPL** — Provisions mission-support infrastructure with CloudFormation.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS CloudFormation keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS CloudFormation is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS CloudFormation is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS CloudFormation means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **CDK** (Synthesizes to CloudFormation templates.) — see `cdk`
- **Terraform** (Pick one per repo — both hit the same APIs.) — see `terraform`
- **SSM** (Change sets & drift detection.) — see `ssm`
