# 🖥️ Elastic Compute Cloud (`ec2`)

> Rent virtual servers by the second — the original building block of the cloud.

- **Category:** Compute
- **Service id:** `ec2`

## Why it exists
You need a machine you fully control: any OS, any software. EC2 launches one in 30 seconds and bills per second.

## When to use it
Web servers, CI runners, batch workers, GPU hosts.

## Learn first

- Linux basics & SSH
- Security groups = firewalls
- AMIs & instance families
- On-Demand vs Spot vs Reserved

## Terraform
```hcl
resource "aws_instance" "web" {
  ami                    = "ami-0c2b8ca1dad44e93a" # Amazon Linux 2023
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.pub_a.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  root_block_device { volume_size = 20; encrypted = true }
  tags = { Name = "web-01" }
}
```

## AWS CDK
```ts
import * as ec2 from "aws-cdk-lib/aws-ec2";
const web = new ec2.Instance(this, "Web", {
  vpc,
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
  machineImage: ec2.MachineImage.latestAmazonLinux2023(),
  vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
});
```

## Boto3 (Python)
```python
import boto3
ec2 = boto3.client("ec2", region_name="us-east-1")
resp = ec2.run_instances(ImageId="ami-0c2b8ca1dad44e93a",
    InstanceType="t3.micro", MinCount=1, MaxCount=1)
print("Launched:", resp["Instances"][0]["InstanceId"])
```

## Delete / teardown
```python
ec2.terminate_instances(InstanceIds=["i-0abc123"])
```

## Expert tips

- Never store keys on the box — use IAM instance profiles.
- Stop ≠ terminate: stopped instances keep billing on EBS + EIP.

## Real-world example

**Netflix** — Streams video and runs chaos experiments across thousands of EC2 instances.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run EC2 at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where Elastic Compute Cloud gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production Elastic Compute Cloud runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the EC2 stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **VPC** (Instances plug ENIs into subnets; SGs are the firewall.) — see `vpc`
- **EBS** (Root & data volumes attach here.) — see `ebs`
- **ALB** (Target groups route to healthy instances.) — see `alb`
- **IAM** (Instance profiles grant permissions.) — see `iam`
