# 🔐 AWS PrivateLink (`privatelink`)

> Consume services across VPCs & accounts over the AWS backbone — no internet.

- **Category:** Networking & Delivery
- **Service id:** `privatelink`

## Why it exists
Need another team's API inside your VPC privately? An interface endpoint gives you a local ENI + DNS name.

## When to use it
Consuming internal/SaaS APIs, exposing your service to customers.

## Learn first

- Interface vs gateway endpoints
- Endpoint services (NLB-backed)
- Private DNS

## Terraform
```hcl
# As the CONSUMER of a service:
resource "aws_vpc_endpoint" "orders_api" {
  vpc_id = aws_vpc.main.id
  service_name = "com.amazonaws.vpce.us-east-1.vpce-svc-0abc123"
  vpc_endpoint_type = "Interface"
  subnet_ids = [aws_subnet.priv_a.id]
  private_dns_enabled = true
}

# As the PROVIDER:
resource "aws_vpc_endpoint_service" "orders" {
  acceptance_required = true
  network_load_balancer_arns = [aws_lb.internal_nlb.arn]
}
```

## AWS CDK
```ts
// consumer side
vpc.addInterfaceEndpoint("OrdersApi", {
  service: new ec2.InterfaceVpcEndpointService("com.amazonaws.vpce.us-east-1.vpce-svc-0abc123"),
  privateDnsEnabled: true,
});
// provider side
new ec2.VpcEndpointService(this, "OrdersSvc", {
  vpcEndpointServiceLoadBalancers: [internalNlb], acceptanceRequired: true,
});
```

## Boto3 (Python)
```python
import boto3
ec2 = boto3.client("ec2", region_name="us-east-1")
for e in ec2.describe_vpc_endpoints()["VpcEndpoints"]:
    print(e["VpcEndpointId"], e["ServiceName"], e["State"])
```

## Delete / teardown
```python
ec2.delete_vpc_endpoints(VpcEndpointIds=["vpce-0abc"])
```

## Expert tips

- Interface endpoints bill per hour — gateway endpoints (S3/DDB) are free.
- Providers never see consumer IPs — clean isolation.

## Real-world example

**Platform teams** — Consume an internal payments API from 40 VPCs with zero routes between them.

## Next steps

- **NLB** (Backs every endpoint service.) — see `nlb`
- **Route 53** (Private DNS resolves locally.) — see `route-53`
- **SGs** (Access control per endpoint.) — see `sgs`
