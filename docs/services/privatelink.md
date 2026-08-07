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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS PrivateLink runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production AWS PrivateLink is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for AWS PrivateLink is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **NLB** (Backs every endpoint service.) — see `nlb`
- **Route 53** (Private DNS resolves locally.) — see `route-53`
- **SGs** (Access control per endpoint.) — see `sgs`
