# 📈 EC2 Auto Scaling (`autoscaling`)

> Fleets that grow with traffic and replace themselves when they break.

- **Category:** Compute
- **Service id:** `autoscaling`

## Why it exists
Traffic is never flat. Auto Scaling adds machines at 9am, removes them at 2am, swaps unhealthy ones.

## When to use it
Any production EC2 workload; drives ECS capacity and CodeDeploy.

## Learn first

- Launch templates
- Target tracking vs step policies
- Health checks (EC2 + ALB)
- Min / desired / max

## Terraform
```hcl
resource "aws_launch_template" "web" {
  name = "web-lt"; image_id = "ami-0c2b8ca1dad44e93a"; instance_type = "t3.micro"
}

resource "aws_autoscaling_group" "web" {
  name = "web-asg"
  vpc_zone_identifier = [aws_subnet.pub_a.id, aws_subnet.pub_b.id]
  target_group_arns = [aws_lb_target_group.web.arn]
  min_size = 2; max_size = 10
  launch_template { id = aws_launch_template.web.id; version = "$Latest" }
}

resource "aws_autoscaling_policy" "cpu" {
  name = "web-cpu-target"
  autoscaling_group_name = aws_autoscaling_group.web.name
  policy_type = "TargetTrackingScaling"
  target_tracking_configuration {
    target_value = 65.0
    predefined_metric_specification { predefined_metric_type = "ASGAverageCPUUtilization" }
  }
}
```

## AWS CDK
```ts
import * as autoscaling from "aws-cdk-lib/aws-autoscaling";
const asg = new autoscaling.AutoScalingGroup(this, "Web", {
  vpc, instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
  machineImage: ec2.MachineImage.latestAmazonLinux2023(),
  minCapacity: 2, maxCapacity: 10,
});
asg.scaleOnCpuUtilization("Cpu", { targetUtilizationPercent: 65 });
```

## Boto3 (Python)
```python
import boto3
asg = boto3.client("autoscaling", region_name="us-east-1")
asg.set_desired_capacity(AutoScalingGroupName="web-asg", DesiredCapacity=4)
```

## Delete / teardown
```python
asg.delete_auto_scaling_group(AutoScalingGroupName="web-asg", ForceDelete=True)
```

## Expert tips

- Always span 2+ AZs — one AZ is an outage waiting to happen.
- Scale-out should be faster than scale-in (cooldowns).

## Real-world example

**Netflix** — Scales its streaming fleet with global demand curves 24/7.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Auto Scaling at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where EC2 Auto Scaling gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production EC2 Auto Scaling runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Auto Scaling stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **ALB** (Health checks come from the target group.) — see `alb`
- **CloudWatch** (Alarm-driven scaling policies.) — see `cloudwatch`
- **CodeDeploy** (Deployment groups target the ASG.) — see `codedeploy`
