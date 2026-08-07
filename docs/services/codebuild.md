# 🧱 AWS CodeBuild (`codebuild`)

> Serverless build farm — compile, test and containerize on demand.

- **Category:** Management & Governance
- **Service id:** `codebuild`

## Why it exists
Don't keep a build server running 24/7. CodeBuild spins disposable containers per build and exits.

## When to use it
Compiling, tests, Docker images, Terraform plans.

## Learn first

- buildspec.yml
- Pre-baked vs custom images
- Privileged mode for docker

## Terraform
```hcl
resource "aws_codebuild_project" "api" {
  name = "api-build"
  service_role = aws_iam_role.build.arn
  artifacts { type = "CODEPIPELINE" }
  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image = "aws/codebuild/amazonlinux-x86_64-standard:5.0"
    type = "LINUX_CONTAINER"
    privileged_mode = true
  }
  source {
    type = "CODEPIPELINE"
    buildspec = <<-EOT
      version: 0.2
      phases:
        build:
          commands:
            - docker build -t api .
      EOT
  }
}
```

## AWS CDK
```ts
import * as codebuild from "aws-cdk-lib/aws-codebuild";
const project = new codebuild.PipelineProject(this, "ApiBuild", {
  environment: {
    buildImage: codebuild.LinuxBuildImage.STANDARD_7_0,
    privileged: true,   // docker builds
  },
});
```

## Boto3 (Python)
```python
import boto3
cb = boto3.client("codebuild", region_name="us-east-1")
build = cb.start_build(projectName="api-build")["build"]
print(build["id"], build["buildStatus"])
```

## Delete / teardown
```python
cb.delete_project(name="api-build")
```

## Expert tips

- Cache dependencies (S3/local) — builds get 10x faster.
- Privileged mode is only needed for docker builds.

## Real-world example

**CI farms** — Build container images per pull request in isolated environments.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS CodeBuild keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS CodeBuild is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS CodeBuild is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS CodeBuild means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **CodePipeline** (Usually invoked as a stage.) — see `codepipeline`
- **ECR** (Pushes built images here.) — see `ecr`
- **S3** (Build caching.) — see `s3`
