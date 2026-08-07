# 💡 Amazon Lightsail (`lightsail`)

> Simplest way to launch a VM or container — fixed price, predictable, zero cloud jargon.

- **Category:** Compute
- **Service id:** `lightsail`

## Why it exists
For most small projects you don't need twelve networking services. Lightsail bundles compute + disk + DNS + firewall into one monthly plan a junior can manage.

## When to use it
Personal sites, dev/test boxes, small SaaS, WordPress.

## Learn first

- Monthly plans vs usage-based
- Static IPs & DNS
- Firewall = security group
- Snapshots

## Terraform
```hcl
resource "aws_lightsail_instance" "web" {
  name           = "web"
  availability_zone = "us-east-1a"
  blueprint_id   = "amazon_linux_2023"
  bundle_id      = "small_2_0"
}
```

## AWS CDK
```ts
// CDK's Lightsail support is thin — manage via Terraform or the console.
// The bundles (small_2_0 etc.) are the pricing unit; pick one, not specs.
```

## Boto3 (Python)
```python
import boto3
ls = boto3.client("lightsail", region_name="us-east-1")
insts = ls.get_instances()["instances"]
for i in insts: print(i["name"], i["blueprintName"])
```

## Delete / teardown
```python
ls.delete_instance(instanceName="web")
```

## Expert tips

- Blueprints are pre-baked OS/app images — pick 'WordPress', not 'install everything'.
- Snapshots let you clone a whole instance into another region.

## Real-world example

**Indie hackers & small agencies** — Stand up client sites with a fixed, predictable monthly bill.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In development, run Lightsail at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.

- Use spot or the cheapest instance class for throwaway workloads; never the production size.
- Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.
- Secrets in dev come from a dev-only store — never copy prod credentials down.

### 🧪 Staging / Pre-prod

Staging is where Amazon Lightsail gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.

- Run the same instance types and subnets as prod so performance surprises surface here.
- Run a load test that reaches prod's projected peak before every release.
- Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.

### 🚀 Production

In production Amazon Lightsail runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.

- Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.
- Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.
- Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.

### 🌍 Multi-region / DR

For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.

- Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.
- Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.
- Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.

### ♻️ Lifecycle & IaC

Lifecycle is code-first: the Lightsail stack lives in git, deploys through CI, and tears down cleanly.

- One Terraform module or CDK stack per environment; promote the same artifact, don't drift.
- Protect prod with a manual approval + `terraform plan` diff posted to the PR.
- Tag every resource (env, team, cost-center) and alert the owning team on spend.

## Next steps

- **EC2** (Full control when you outgrow the bundles.) — see `ec2`
- **Route 53** (DNS beyond the Lightsail console.) — see `route-53`
- **S3** (Offload files and backups.) — see `s3`
