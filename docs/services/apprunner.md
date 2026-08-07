# 🚤 AWS App Runner (`apprunner`)

> Container to public HTTPS in one click — the simplest compute on AWS.

- **Category:** Compute
- **Service id:** `apprunner`

## Why it exists
You have a Docker image and just want a public, auto-scaling HTTPS endpoint — zero LB or fleet decisions.

## When to use it
Web apps, APIs, internal tools, prototypes that must survive prod.

## Learn first

- Sources: ECR image vs repo
- Autoscaling min/max
- VPC connector for private access

## Terraform
```hcl
resource "aws_apprunner_service" "web" {
  service_name = "web"
  source_configuration {
    image_repository {
      image_identifier = "123456789012.dkr.ecr.us-east-1.amazonaws.com/api:1.4"
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = false
    authentication_configuration { access_role_arn = aws_iam_role.apprunner_ecr.arn }
  }
  instance_configuration { cpu = "512"; memory = "1024" }
}
```

## AWS CDK
```ts
import * as apprunner from "aws-cdk-lib/aws-apprunner";
new apprunner.CfnService(this, "Web", {
  serviceName: "web",
  sourceConfiguration: {
    imageRepository: {
      imageIdentifier: "123456789012.dkr.ecr.us-east-1.amazonaws.com/api:1.4",
      imageRepositoryType: "ECR",
    },
    authenticationConfiguration: { accessRoleArn: ecrRole.roleArn },
  },
});
```

## Boto3 (Python)
```python
import boto3
ar = boto3.client("apprunner", region_name="us-east-1")
for s in ar.list_services()["ServiceSummaryList"]:
    print(s["ServiceName"], s["Status"], s["ServiceUrl"])
```

## Delete / teardown
```python
ar.delete_service(ServiceArn=arn)
```

## Expert tips

- Perfect first deploy: image in, HTTPS URL out.
- Use a VPC connector before talking to RDS.

## Real-world example

**SaaS startups** — Ship containers to auto-scaling HTTPS endpoints without touching a load balancer.

## Next steps

- **ECR** (Pulls your images via an access role.) — see `ecr`
- **VPC** (Connectors reach RDS/DynamoDB privately.) — see `vpc`
- **Route 53** (CNAME the default domain.) — see `route-53`
