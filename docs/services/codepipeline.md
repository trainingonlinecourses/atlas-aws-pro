# 🔁 AWS CodePipeline (`codepipeline`)

> CI/CD orchestrator — commit, build, test, deploy on rails.

- **Category:** Management & Governance
- **Service id:** `codepipeline`

## Why it exists
Manual deploys cause Friday outages. Pipelines run source → build → deploy on every merge, with approvals.

## When to use it
Continuous delivery for Lambda, ECS, EC2, static sites.

## Learn first

- Stages, actions, artifacts
- Source providers
- Manual approvals
- Triggers & rollback

## Terraform
```hcl
resource "aws_codepipeline" "ship" {
  name = "ship-api"
  role_arn = aws_iam_role.pipeline.arn
  artifact_store { location = aws_s3_bucket.artifacts.bucket; type = "S3" }

  stage {
    name = "Source"
    action {
      name = "GitHub"; category = "Source"; owner = "AWS"
      provider = "CodeStarSourceConnection"; version = "1"
      output_artifacts = ["src"]
      configuration = {
        ConnectionArn = aws_codestarconnections_connection.gh.arn
        FullRepositoryId = "acme/api"
        BranchName = "main"
      }
    }
  }
  stage {
    name = "Build"
    action {
      name = "Build"; category = "Build"; owner = "AWS"
      provider = "CodeBuild"; version = "1"
      input_artifacts = ["src"]; output_artifacts = ["build"]
      configuration = { ProjectName = aws_codebuild_project.api.name }
    }
  }
}
```

## AWS CDK
```ts
import * as cp from "aws-cdk-lib/aws-codepipeline";
import * as actions from "aws-cdk-lib/aws-codepipeline-actions";
const src = new cp.Artifact();
const pipeline = new cp.Pipeline(this, "Ship");
pipeline.addStage({ stageActions: [
  new actions.CodeStarConnectionsSourceAction({
    actionName: "GitHub", output: src,
    connectionArn: ghConnectionArn, owner: "acme", repo: "api", branch: "main" }),
]});
pipeline.addStage({ stageActions: [
  new actions.CodeBuildAction({ actionName: "Build", project: buildProject, input: src }),
]});
```

## Boto3 (Python)
```python
import boto3
cp = boto3.client("codepipeline", region_name="us-east-1")
cp.start_pipeline_execution(name="ship-api")
print([p["name"] for p in cp.list_pipelines()["pipelines"]])
```

## Delete / teardown
```python
cp.delete_pipeline(name="ship-api")
```

## Expert tips

- Add an approval stage before prod — one click of safety.
- Artifacts live in S3 — lock that bucket down.

## Real-world example

**Shipping teams** — Every merged PR builds, tests and deploys in minutes with auto-rollback.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS CodePipeline keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS CodePipeline is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS CodePipeline is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS CodePipeline means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **CodeBuild** (The build/test stage.) — see `codebuild`
- **ECR + ECS / CodeDeploy** (Deployment targets.) — see `ecr-+-ecs---codedeploy`
- **S3** (Artifact store.) — see `s3`
- **SNS** (Approval notifications.) — see `sns`
