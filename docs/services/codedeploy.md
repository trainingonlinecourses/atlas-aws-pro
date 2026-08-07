# 🚀 AWS CodeDeploy (`codedeploy`)

> Zero-downtime deployments to EC2 fleets — with automatic rollback.

- **Category:** Management & Governance
- **Service id:** `codedeploy`

## Why it exists
scp to servers is over. CodeDeploy rolls revisions across an ASG with health checks and one-click rollback.

## When to use it
EC2 releases, blue/green with ALB, Lambda alias shifting.

## Learn first

- appspec.yml
- In-place vs blue/green
- Deployment configs
- Auto-rollback on alarm

## Terraform
```hcl
resource "aws_codedeploy_app" "web" { name = "web-app" }

resource "aws_codedeploy_deployment_group" "web" {
  app_name = aws_codedeploy_app.web.name
  deployment_group_name = "web-fleet"
  service_role_arn = aws_iam_role.codedeploy.arn
  autoscaling_groups = [aws_autoscaling_group.web.name]
  deployment_style {
    deployment_type = "IN_PLACE"
    deployment_option = "WITH_TRAFFIC_CONTROL"
  }
  auto_rollback_configuration { enabled = true; events = ["DEPLOYMENT_FAILURE"] }
}
```

## AWS CDK
```ts
import * as codedeploy from "aws-cdk-lib/aws-codedeploy";
new codedeploy.ServerDeploymentGroup(this, "WebFleet", {
  application: new codedeploy.ServerApplication(this, "WebApp"),
  autoScalingGroups: [asg],
  deploymentConfig: codedeploy.ServerDeploymentConfig.ONE_AT_A_TIME,
});
```

## Boto3 (Python)
```python
import boto3
cd = boto3.client("codedeploy", region_name="us-east-1")
dep = cd.create_deployment(applicationName="web-app",
    deploymentGroupName="web-fleet",
    revision={"revisionType": "S3",
        "s3Location": {"bucket": "acme-releases", "key": "web-v2.zip", "bundleType": "zip"}})
print(dep["deploymentId"])
```

## Delete / teardown
```python
cd.delete_application(applicationName="web-app")
```

## Expert tips

- ONE_AT_A_TIME keeps capacity during deploys.
- Wire auto-rollback to your CloudWatch alarms.

## Real-world example

**Fleet releases** — New versions roll across ASGs with health-gated traffic shifts.

## Next steps

- **Auto Scaling** (Deployment groups target whole fleets.) — see `auto-scaling`
- **ALB** (Traffic control in blue/green.) — see `alb`
- **CodePipeline** (Deploys as pipeline stages.) — see `codepipeline`
