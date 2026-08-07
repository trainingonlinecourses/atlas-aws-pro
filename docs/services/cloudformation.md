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

## Next steps

- **CDK** (Synthesizes to CloudFormation templates.) — see `cdk`
- **Terraform** (Pick one per repo — both hit the same APIs.) — see `terraform`
- **SSM** (Change sets & drift detection.) — see `ssm`
