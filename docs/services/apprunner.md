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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run App Runner at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where AWS App Runner gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production AWS App Runner runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the App Runner stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **ECR** (Pulls your images via an access role.) — see `ecr`
- **VPC** (Connectors reach RDS/DynamoDB privately.) — see `vpc`
- **Route 53** (CNAME the default domain.) — see `route-53`
