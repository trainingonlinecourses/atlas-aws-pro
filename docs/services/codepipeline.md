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

## Next steps

- **CodeBuild** (The build/test stage.) — see `codebuild`
- **ECR + ECS / CodeDeploy** (Deployment targets.) — see `ecr-+-ecs---codedeploy`
- **S3** (Artifact store.) — see `s3`
- **SNS** (Approval notifications.) — see `sns`
