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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS CodeDeploy keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS CodeDeploy is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS CodeDeploy is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS CodeDeploy means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **Auto Scaling** (Deployment groups target whole fleets.) — see `auto-scaling`
- **ALB** (Traffic control in blue/green.) — see `alb`
- **CodePipeline** (Deploys as pipeline stages.) — see `codepipeline`
