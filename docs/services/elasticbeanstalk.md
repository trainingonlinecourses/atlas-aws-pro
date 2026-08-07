# 🌱 AWS Elastic Beanstalk (`elasticbeanstalk`)

> Paste your app code; AWS provisions the servers, load balancer and scaling for you.

- **Category:** Compute
- **Service id:** `elasticbeanstalk`

## Why it exists
Before containers took over, Beanstalk was how you deployed without a DevOps team — it still handles health checks, rollbacks and capacity automatically.

## When to use it
Prototypes, internal tools, lift-and-shift web apps.

## Learn first

- Prebuilt runtimes (Node, Python, Java...)
- Single vs load-balanced environments
- Deploy = version + configuration
- Health monitoring

## Terraform
```hcl
resource "aws_elastic_beanstalk_application" "app" {
  name = "myapp"
}
resource "aws_elastic_beanstalk_environment" "prod" {
  name                = "myapp-prod"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.0.1 running Python 3.11"
}
```

## AWS CDK
```ts
// No first-class CDK construct — Beanstalk is AWS-managed; manage with TF.
```

## Boto3 (Python)
```python
import boto3
eb = boto3.client("elasticbeanstalk", region_name="us-east-1")
envs = eb.describe_environments()["Environments"]
for e in envs: print(e["EnvironmentName"], e["Status"])
```

## Delete / teardown
```python
eb.terminate_environment(EnvironmentName="myapp-prod")
```

## Expert tips

- Treat it as a bridge, not a destination — modern apps outgrow it.
- Swap to a newer platform version by launching a fresh environment and cutting over.

## Real-world example

**Early-stage startups** — Shipped MVPs in days without hiring DevOps.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Elastic Beanstalk at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where AWS Elastic Beanstalk gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production AWS Elastic Beanstalk runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Elastic Beanstalk stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **ECS** (Container-native replacement when you mature.) — see `ecs`
- **CodePipeline** (Blue/green deploys with Beanstalk.) — see `codepipeline`
