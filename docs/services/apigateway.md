# 🚪 Amazon API Gateway (`apigateway`)

> The front door for your APIs — auth, throttling, routing, metering.

- **Category:** Networking & Delivery
- **Service id:** `apigateway`

## Why it exists
You don't expose Lambdas directly. The gateway authenticates, rate-limits, transforms and routes requests.

## When to use it
Public & partner APIs, serverless backends, usage plans.

## Learn first

- REST vs HTTP vs WebSocket APIs
- Stages & deployments
- Usage plans & API keys

## Terraform
```hcl
resource "aws_apigatewayv2_api" "public" {
  name = "public-api"; protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "orders" {
  api_id = aws_apigatewayv2_api.public.id
  integration_type = "AWS_PROXY"
  integration_uri = aws_lambda_function.processor.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "orders" {
  api_id = aws_apigatewayv2_api.public.id
  route_key = "POST /orders"
  target = "integrations/" + aws_apigatewayv2_integration.orders.id
}
```

## AWS CDK
```ts
import * as apigw from "aws-cdk-lib/aws-apigatewayv2";
import { HttpLambdaIntegration } from "aws-cdk-lib/aws-apigatewayv2-integrations";
const api = new apigw.HttpApi(this, "PublicApi");
api.addRoutes({
  path: "/orders", methods: [apigw.HttpMethod.POST],
  integration: new HttpLambdaIntegration("OrdersInt", fn),
});
```

## Boto3 (Python)
```python
import boto3
apigw = boto3.client("apigatewayv2", region_name="us-east-1")
for api in apigw.get_apis()["Items"]:
    print(api["Name"], "->", api["ApiEndpoint"])
```

## Delete / teardown
```python
apigw.delete_api(ApiId="abc123")
```

## Expert tips

- HTTP APIs are cheaper & faster than REST APIs for most cases.
- Set throttling per stage or one bad client sinks you.

## Real-world example

**Partner portals** — Throttled, API-key-gated endpoints while Lambda handles the logic.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon API Gateway runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.

- Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.
- Create security groups from IaC so a peer can read exactly what's open.
- Tear down unused resources at the end of the week to keep dev costs near zero.

### 🧪 Staging / Pre-prod

Staging proves the connectivity model: same topology as prod, smaller and cheaper.

- Mirror prod's subnets/AZs and route table split to catch topology bugs early.
- Test cross-account peering/transit and PrivateLink paths before prod needs them.
- Enable flow logs in staging so you learn to read them where it's cheap to experiment.

### 🚀 Production

In production Amazon API Gateway is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.

- Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).
- Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.
- Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.

### 🌍 Multi-region / DR

DR for Amazon API Gateway is a second region with its own VPC and a DNS failover path, drilled in advance.

- Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.
- Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.
- Include the network in the DR drill: promote DNS, verify connectivity, then flip back.

### ♻️ Lifecycle & IaC

Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.

- Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.
- Put network changes behind review — a wrong SG or route is a security incident.
- Document the CIDR map centrally; overlap is the #1 blocker in future migrations.

## Next steps

- **Lambda / ECS** (Backends the routes forward to.) — see `lambda---ecs`
- **Cognito** (JWT authorizers validate tokens.) — see `cognito`
- **WAF** (ACLs filter traffic.) — see `waf`
- **CloudWatch** (Access logs & 5XX alarms.) — see `cloudwatch`
