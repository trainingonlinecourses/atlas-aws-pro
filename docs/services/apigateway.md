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

## Next steps

- **Lambda / ECS** (Backends the routes forward to.) — see `lambda---ecs`
- **Cognito** (JWT authorizers validate tokens.) — see `cognito`
- **WAF** (ACLs filter traffic.) — see `waf`
- **CloudWatch** (Access logs & 5XX alarms.) — see `cloudwatch`
