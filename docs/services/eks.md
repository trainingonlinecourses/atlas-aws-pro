# ☸️ Elastic Kubernetes Service (`eks`)

> Managed Kubernetes control plane — the industry standard, minus the ops.

- **Category:** Compute
- **Service id:** `eks`

## Why it exists
Your org standardizes on Kubernetes or needs its ecosystem. EKS runs the control plane across 3 AZs.

## When to use it
Large multi-team platforms and portable k8s workloads.

## Learn first

- Pods, deployments, services
- kubectl & kubeconfig
- CNI networking in a VPC
- IRSA — IAM for service accounts

## Terraform
```hcl
resource "aws_eks_cluster" "core" {
  name = "core"; role_arn = aws_iam_role.eks_role.arn; version = "1.31"
  vpc_config { subnet_ids = [aws_subnet.priv_a.id, aws_subnet.priv_b.id] }
}

resource "aws_eks_node_group" "workers" {
  cluster_name = aws_eks_cluster.core.name
  node_group_name = "general"
  node_role_arn = aws_iam_role.node_role.arn
  subnet_ids = [aws_subnet.priv_a.id, aws_subnet.priv_b.id]
  instance_types = ["m6i.large"]
  scaling_config { desired_size = 3; min_size = 2; max_size = 6 }
}
```

## AWS CDK
```ts
import * as eks from "aws-cdk-lib/aws-eks";
const cluster = new eks.Cluster(this, "Core", {
  version: eks.KubernetesVersion.V1_31,
  defaultCapacity: 3,
  defaultCapacityInstance: ec2.InstanceType.of(ec2.InstanceClass.M6I, ec2.InstanceSize.LARGE),
});
```

## Boto3 (Python)
```python
import boto3
eks = boto3.client("eks", region_name="us-east-1")
print(eks.list_clusters()["clusters"])
print(eks.describe_cluster(name="core")["cluster"]["status"])
```

## Delete / teardown
```python
eks.delete_nodegroup(clusterName="core", nodegroupName="general")
eks.delete_cluster(name="core")
```

## Expert tips

- Pods consume real VPC IPs — size subnets accordingly.
- IRSA beats node-level IAM roles for least privilege.

## Real-world example

**Lyft** — Runs marketplace services on EKS.

## Next steps

- **VPC** (Pods get real VPC IPs via the CNI.) — see `vpc`
- **ECR** (Image source for deployments.) — see `ecr`
- **ALB** (LB controller provisions ALBs from Ingress.) — see `alb`
- **IAM** (IRSA maps service accounts to roles.) — see `iam`
