# 🧵 AWS X-Ray (`xray`)

> Distributed tracing — follow one request across every service it touched.

- **Category:** Management & Governance
- **Service id:** `xray`

## Why it exists
When latency hides between API Gateway, Lambda and DynamoDB, traces stitch the whole journey with timings.

## When to use it
Latency debugging, service maps, error root-cause.

## Learn first

- Segments & traces
- SDK instrumentation
- Service maps
- Sampling rules

## Terraform
```hcl
resource "aws_xray_sampling_rule" "default_api" {
  rule_name = "api-traces"
  service_name = "public-api"
  resource_arn = "*"
  fixed_rate = 0.05
  reservoir_size = 5
  url_path = "*"
  version = 1
}
# Enable per service: tracing_config { mode = "Active" } on Lambda,
# or tracing_configuration on API Gateway stages.
```

## AWS CDK
```ts
// Lambda: one line enables active tracing via the escape hatch
const cfnFn = fn.node.defaultChild as lambda.CfnFunction;
cfnFn.tracingConfig = { mode: "Active" };
```

## Boto3 (Python)
```python
import boto3, time
xr = boto3.client("xray", region_name="us-east-1")
end = int(time.time()); start = end - 3600
traces = xr.get_trace_summaries(StartTime=start, EndTime=end)
print(len(traces["Traces"]), "traces in the last hour")
```

## Delete / teardown
```python
xr.delete_sampling_rule(RuleName="api-traces")
```

## Expert tips

- Trace errors at 100%, sample success at 1-5%.
- The service map is your live architecture diagram.

## Real-world example

**Microservice teams** — Trace a slow checkout across 9 services to find the one stalled call.

## Next steps

- **Lambda / ECS / ALB** (All can emit segments.) — see `lambda---ecs---alb`
- **CloudWatch** (X-Ray metrics are merged there.) — see `cloudwatch`
- **API Gateway** (Stage-level tracing toggle.) — see `api-gateway`
