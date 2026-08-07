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

## Next steps

- **ECS** (Batch runs jobs as containers under the hood.) — see `ecs`
- **Spot** (Up to ~70% cost reduction for tolerant jobs.) — see `spot`
- **S3** (Job inputs & outputs.) — see `s3`
