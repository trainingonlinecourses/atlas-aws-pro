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

## Next steps

- **ECS** (Fargate is a launch type of ECS — same APIs.) — see `ecs`
- **ECR** (Image source.) — see `ecr`
- **VPC** (Each task gets its own ENI.) — see `vpc`
