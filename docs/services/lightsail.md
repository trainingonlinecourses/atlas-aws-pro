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

## Next steps

- **EC2** (Full control when you outgrow the bundles.) — see `ec2`
- **Route 53** (DNS beyond the Lightsail console.) — see `route-53`
- **S3** (Offload files and backups.) — see `s3`
