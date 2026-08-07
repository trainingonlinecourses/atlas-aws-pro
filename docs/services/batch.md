# 🧮 AWS Batch (`batch`)

> Managed batch computing — thousands of jobs, right-sized and Spot-priced.

- **Category:** Compute
- **Service id:** `batch`

## Why it exists
When the work is 'run N independent jobs', Batch queues them, provisions capacity, leans on Spot.

## When to use it
Media transcoding, simulations, risk calculations, nightly jobs.

## Learn first

- Job definitions & queues
- Compute environments
- Spot strategies
- Dependencies & retries

## Terraform
```hcl
resource "aws_batch_compute_environment" "spot" {
  compute_environment_name = "render-spot"
  type = "MANAGED"
  compute_resources {
    type = "SPOT"; max_vcpus = 256
    instance_type = ["optimal"]
    subnets = [aws_subnet.priv_a.id]
  }
}

resource "aws_batch_job_queue" "render" {
  name = "render-queue"; state = "ENABLED"; priority = 1
  compute_environment_order {
    order = 1
    compute_environment = aws_batch_compute_environment.spot.arn
  }
}
```

## AWS CDK
```ts
import * as batch from "aws-cdk-lib/aws-batch";
new batch.CfnComputeEnvironment(this, "Spot", {
  type: "MANAGED",
  computeResources: { type: "SPOT", maxvCpus: 256,
    instanceTypes: ["optimal"], subnets: [privA.subnetId] },
});
```

## Boto3 (Python)
```python
import boto3
b = boto3.client("batch", region_name="us-east-1")
job = b.submit_job(jobName="render-1042", jobQueue="render-queue",
                   jobDefinition="render-def")
print(job["jobId"])
```

## Delete / teardown
```python
b.delete_job_queue(jobQueue="render-queue")
```

## Expert tips

- Design jobs to be retryable — Spot can reclaim capacity.
- 'optimal' instance type lets Batch pick the best fit.

## Real-world example

**VFX & risk teams** — Render farms scale to thousands of Spot cores, then vanish.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Batch at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where AWS Batch gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production AWS Batch runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Batch stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **ECS** (Batch runs jobs as containers under the hood.) — see `ecs`
- **Spot** (Up to ~70% cost reduction for tolerant jobs.) — see `spot`
- **S3** (Job inputs & outputs.) — see `s3`
