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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS X-Ray keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS X-Ray is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS X-Ray is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS X-Ray means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **Lambda / ECS / ALB** (All can emit segments.) — see `lambda---ecs---alb`
- **CloudWatch** (X-Ray metrics are merged there.) — see `cloudwatch`
- **API Gateway** (Stage-level tracing toggle.) — see `api-gateway`
