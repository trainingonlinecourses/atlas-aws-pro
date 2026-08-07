# 🖼️ EC2 Image Builder (`imagebuilder`)

> Build and maintain golden AMIs. Recipes, pipelines, automated patching on a schedule.

- **Category:** Compute
- **Service id:** `imagebuilder`

## Why it exists
Hand-built AMIs drift and rot. Image Builder codifies the bake — base image + components + tests — rebuilt on a schedule so every instance starts hardened and patched.

## When to use it
Golden AMIs, patching pipelines, CIS-hardened bases.

## Learn first

- Recipes & components
- Build/schedule pipelines
- AMI + EC2 tests
- Distributions (regions, accounts)

## Terraform
```hcl
resource "aws_imagebuilder_image_pipeline" "golden" {
  name     = "golden-amazonlinux"
  image_recipe_arn = aws_imagebuilder_image_recipe.al2023.arn
  distribution_configuration_arn = aws_imagebuilder_distribution_configuration.dist.arn
  schedule {
    schedule_expression = "cron(0 3 ? * SUN *)"
  }
}
```

## AWS CDK
```ts
// L1 only — CfnImagePipeline + CfnImageRecipe.
```

## Boto3 (Python)
```python
import boto3
ib = boto3.client("imagebuilder", region_name="us-east-1")
resp = ib.list_image_pipelines()["imagePipelineList"]
print([p["name"] for p in resp])
```

## Delete / teardown
```python
# Delete the image, recipe, then the pipeline.
```

## Expert tips

- Attach EC2 test components so a build that fails smoke tests fails the pipeline.
- Schedule a weekly rebuild so AMIs are never more than a week stale.

## Real-world example

**Platform teams** — Every new EC2 instance booting from a patched, approved golden AMI.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Image Builder at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where EC2 Image Builder gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production EC2 Image Builder runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Image Builder stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **EC2** (The AMIs you bake.) — see `ec2`
- **Systems Manager** (Patch baselines as components.) — see `systems-manager`
- **Inspector** (Scan the baked image.) — see `inspector`
