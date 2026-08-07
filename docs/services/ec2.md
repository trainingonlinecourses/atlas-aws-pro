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

## Next steps

- **VPC** (Instances plug ENIs into subnets; SGs are the firewall.) — see `vpc`
- **EBS** (Root & data volumes attach here.) — see `ebs`
- **ALB** (Target groups route to healthy instances.) — see `alb`
- **IAM** (Instance profiles grant permissions.) — see `iam`
