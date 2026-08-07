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

## Next steps

- **ECS** (Container-native replacement when you mature.) — see `ecs`
- **CodePipeline** (Blue/green deploys with Beanstalk.) — see `codepipeline`
