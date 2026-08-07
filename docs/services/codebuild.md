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

## Next steps

- **CodePipeline** (Usually invoked as a stage.) — see `codepipeline`
- **ECR** (Pushes built images here.) — see `ecr`
- **S3** (Build caching.) — see `s3`
