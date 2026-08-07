# 🛰️ AWS Global Accelerator (`globalaccelerator`)

> Two static anycast IPs + AWS backbone routing across regions.

- **Category:** Networking & Delivery
- **Service id:** `globalaccelerator`

## Why it exists
Global users need predictable latency and instant regional failover without DNS TTL delays.

## When to use it
Global apps, game servers, TCP/UDP a CDN can't serve.

## Learn first

- Anycast static IPs
- Listeners & endpoint groups
- GA vs CloudFront

## Terraform
```hcl
resource "aws_global_accelerator_accelerator" "app" { name = "app-accelerator" }

resource "aws_global_accelerator_listener" "https" {
  accelerator_arn = aws_global_accelerator_accelerator.app.id
  protocol = "TCP"
  port_range { from_port = 443; to_port = 443 }
}

resource "aws_global_accelerator_endpoint_group" "use1" {
  listener_arn = aws_global_accelerator_listener.https.id
  endpoint_group_region = "us-east-1"
  endpoint_configuration { endpoint_id = aws_lb.web.arn; weight = 100 }
}
```

## AWS CDK
```ts
import * as ga from "aws-cdk-lib/aws-globalaccelerator";
const accel = new ga.CfnAccelerator(this, "App", { name: "app-accelerator" });
new ga.CfnListener(this, "Https", {
  acceleratorArn: accel.attrAcceleratorArn,
  protocol: "TCP", portRanges: [{ fromPort: 443, toPort: 443 }],
});
```

## Boto3 (Python)
```python
import boto3
ga = boto3.client("globalaccelerator", region_name="us-west-2")
for a in ga.list_accelerators()["Accelerators"]:
    print(a["Name"], a["Status"], a["IpSets"])
```

## Delete / teardown
```python
ga.delete_accelerator(AcceleratorArn=arn)  # disable first
```

## Expert tips

- Static IPs are gold for allowlists and mobile clients.
- GA is TCP/UDP; CloudFront is HTTP caching — different tools.

## Real-world example

**Game studios** — Route players to the nearest healthy region with sub-second failover.

## Next steps

- **ALB / NLB / EIP** (Any of these can be endpoints.) — see `alb---nlb---eip`
- **Route 53** (Alias records at the accelerator.) — see `route-53`
