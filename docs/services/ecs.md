# 🐳 Elastic Container Service (`ecs`)

> AWS-native container orchestration — Docker without the Kubernetes tax.

- **Category:** Compute
- **Service id:** `ecs`

## Why it exists
You containerized an app and want it scheduled, load-balanced and self-healing without operating Kubernetes.

## When to use it
Microservices and batch jobs in Docker images.

## Learn first

- Images & registries
- Task def vs service vs cluster
- EC2 vs Fargate launch types

## Terraform
```hcl
resource "aws_ecs_cluster" "apps" { name = "apps-cluster" }

resource "aws_ecs_task_definition" "api" {
  family = "api"; network_mode = "awsvpc"
  requires_compatibilities = ["EC2"]
  cpu = "512"; memory = "1024"
  execution_role_arn = aws_iam_role.ecs_exec.arn
  container_definitions = jsonencode([{
    name = "api"
    image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/api:1.4"
    portMappings = [{ containerPort = 8080 }]
  }])
}

resource "aws_ecs_service" "api" {
  name = "api"; cluster = aws_ecs_cluster.apps.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count = 3
}
```

## AWS CDK
```ts
import * as ecs from "aws-cdk-lib/aws-ecs";
const cluster = new ecs.Cluster(this, "Apps", { vpc });
new ecs.Ec2Service(this, "Api", { cluster, taskDefinition, desiredCount: 3 });
```

## Boto3 (Python)
```python
import boto3
ecs = boto3.client("ecs", region_name="us-east-1")
ecs.create_cluster(clusterName="apps-cluster")
print(ecs.describe_clusters(clusters=["apps-cluster"])["clusters"][0]["status"])
```

## Delete / teardown
```python
ecs.delete_cluster(clusterName="apps-cluster")
```

## Expert tips

- Execution role pulls images; task role is what YOUR code can do.
- Enable container insights from day one.

## Real-world example

**BuzzFeed** — Runs its CI system and microservices on ECS.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run ECS at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where Elastic Container Service gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production Elastic Container Service runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the ECS stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **ECR** (Task definitions pull images from your registry.) — see `ecr`
- **ALB** (Services register tasks into target groups.) — see `alb`
- **IAM** (Separate execution vs task roles.) — see `iam`
- **CloudWatch** (Container logs land in log groups.) — see `cloudwatch`
