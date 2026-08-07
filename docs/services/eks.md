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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run EKS at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where Elastic Kubernetes Service gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production Elastic Kubernetes Service runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the EKS stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **VPC** (Pods get real VPC IPs via the CNI.) — see `vpc`
- **ECR** (Image source for deployments.) — see `ecr`
- **ALB** (LB controller provisions ALBs from Ingress.) — see `alb`
- **IAM** (IRSA maps service accounts to roles.) — see `iam`
