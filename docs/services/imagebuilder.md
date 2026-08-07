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

## Next steps

- **EC2** (The AMIs you bake.) — see `ec2`
- **Systems Manager** (Patch baselines as components.) — see `systems-manager`
- **Inspector** (Scan the baked image.) — see `inspector`
