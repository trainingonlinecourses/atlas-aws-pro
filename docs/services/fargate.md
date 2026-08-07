# 🛸 AWS Fargate (`fargate`)

> Serverless compute for containers — no hosts, no patching, just tasks.

- **Category:** Compute
- **Service id:** `fargate`

## Why it exists
You want containers but refuse to manage a fleet. Fargate allocates compute per task.

## When to use it
Spiky workloads, batch containers, small microservices.

## Learn first

- Task def CPU/memory combos
- Fargate vs EC2 cost math
- Task networking (ENI per task)

## Terraform
```hcl
resource "aws_ecs_task_definition" "worker" {
  family = "nightly-worker"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = "1024"; memory = "2048"
  execution_role_arn = aws_iam_role.ecs_exec.arn
  container_definitions = jsonencode([{
    name = "worker"
    image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/worker:2.0"
  }])
}

resource "aws_ecs_service" "worker" {
  name = "worker"; cluster = aws_ecs_cluster.apps.id
  task_definition = aws_ecs_task_definition.worker.arn
  launch_type = "FARGATE"; desired_count = 2
  network_configuration { subnets = [aws_subnet.priv_a.id] }
}
```

## AWS CDK
```ts
import * as ecs from "aws-cdk-lib/aws-ecs";
new ecs.FargateService(this, "Worker", {
  cluster, taskDefinition, desiredCount: 2,   // no fleet to manage, ever
});
```

## Boto3 (Python)
```python
import boto3
ecs = boto3.client("ecs", region_name="us-east-1")
task = ecs.run_task(cluster="apps-cluster", taskDefinition="nightly-worker",
    launchType="FARGATE",
    networkConfiguration={"awsvpcConfiguration": {"subnets": ["subnet-0abc"]}})
print(task["tasks"][0]["taskArn"])
```

## Delete / teardown
```python
ecs.stop_task(cluster="apps-cluster", task=task_arn)
```

## Expert tips

- CPU/memory combos are fixed — you can't pick arbitrary sizes.
- Tasks in private subnets need NAT or VPC endpoints to pull images.

## Real-world example

**Vanguard** — Runs regulated batch containers with zero managed hosts.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Fargate at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where AWS Fargate gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production AWS Fargate runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Fargate stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **ECS** (Fargate is a launch type of ECS — same APIs.) — see `ecs`
- **ECR** (Image source.) — see `ecr`
- **VPC** (Each task gets its own ENI.) — see `vpc`
