# 📦 Elastic Container Registry (`ecr`)

> Private Docker registry — scan on push, immutable tags, lifecycle policies.

- **Category:** Management & Governance
- **Service id:** `ecr`

## Why it exists
Images need a secure home with scanning and retention rules. ECR is wired natively into ECS, EKS and CodeBuild.

## When to use it
Storing app images, immutable release tags, cross-account sharing.

## Learn first

- Repositories & tags
- Scan-on-push
- Lifecycle policies

## Terraform
```hcl
resource "aws_ecr_repository" "api" {
  name = "api"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration { scan_on_push = true }
}

resource "aws_ecr_lifecycle_policy" "api" {
  repository = aws_ecr_repository.api.name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description = "keep last 30 images"
      selection = { tagStatus = "any", countType = "imageCountMoreThan", countNumber = 30 }
      action = { type = "expire" }
    }]
  })
}
```

## AWS CDK
```ts
import * as ecr from "aws-cdk-lib/aws-ecr";
const repo = new ecr.Repository(this, "Api", {
  imageTagMutability: ecr.TagMutability.IMMUTABLE,
  imageScanOnPush: true,
});
repo.addLifecycleRule({ maxImageCount: 30 });
```

## Boto3 (Python)
```python
import boto3
ecr = boto3.client("ecr", region_name="us-east-1")
token = ecr.get_authorization_token()["authorizationData"][0]
print("docker login at", token["proxyEndpoint"])
```

## Delete / teardown
```python
ecr.delete_repository(repositoryName="api", force=True)
```

## Expert tips

- IMMUTABLE tags = what you tested is what runs in prod.
- Tag by git SHA, not 'latest'.

## Real-world example

**Release pipelines** — Immutable tags guarantee prod runs the exact image that passed CI.

## Next steps

- **ECS / EKS / Fargate** (Pull with task-execution roles.) — see `ecs---eks---fargate`
- **CodeBuild** (Pushes fresh builds.) — see `codebuild`
- **Inspector** (Scans pushed images.) — see `inspector`
