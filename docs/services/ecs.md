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

## Next steps

- **ECR** (Task definitions pull images from your registry.) — see `ecr`
- **ALB** (Services register tasks into target groups.) — see `alb`
- **IAM** (Separate execution vs task roles.) — see `iam`
- **CloudWatch** (Container logs land in log groups.) — see `cloudwatch`
