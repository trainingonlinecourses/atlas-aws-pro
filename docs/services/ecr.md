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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Elastic Container Registry keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where Elastic Container Registry is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production Elastic Container Registry is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for Elastic Container Registry means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **ECS / EKS / Fargate** (Pull with task-execution roles.) — see `ecs---eks---fargate`
- **CodeBuild** (Pushes fresh builds.) — see `codebuild`
- **Inspector** (Scans pushed images.) — see `inspector`
