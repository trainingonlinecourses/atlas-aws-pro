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

## Next steps

- **ALB** (Health checks come from the target group.) — see `alb`
- **CloudWatch** (Alarm-driven scaling policies.) — see `cloudwatch`
- **CodeDeploy** (Deployment groups target the ASG.) — see `codedeploy`
