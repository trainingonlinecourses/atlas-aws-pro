# 👁️ Amazon CloudWatch (`cloudwatch`)

> Metrics, logs, alarms and dashboards — the nervous system of AWS.

- **Category:** Management & Governance
- **Service id:** `cloudwatch`

## Why it exists
You can't operate what you can't see. Every service emits metrics here; alarms turn metrics into pages.

## When to use it
Monitoring, autoscaling triggers, log analysis, billing alarms.

## Learn first

- Metrics, dimensions, namespaces
- Alarms → SNS
- Log groups & Logs Insights

## Terraform
```hcl
resource "aws_cloudwatch_log_group" "api" {
  name = "/aws/lambda/order-processor"
  retention_in_days = 30
}

resource "aws_cloudwatch_metric_alarm" "api_5xx" {
  alarm_name = "api-gateway-5xx"
  namespace = "AWS/ApiGateway"
  metric_name = "5XXError"
  statistic = "Sum"; period = 60
  evaluation_periods = 2; threshold = 5
  comparison_operator = "GreaterThanThreshold"
  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

## AWS CDK
```ts
import * as cw from "aws-cdk-lib/aws-cloudwatch";
new cw.Alarm(this, "Api5xx", {
  metric: new cw.Metric({
    namespace: "AWS/ApiGateway", metricName: "5XXError",
    statistic: "Sum", period: cdk.Duration.minutes(1),
  }),
  threshold: 5, evaluationPeriods: 2,
});
```

## Boto3 (Python)
```python
import boto3
cw = boto3.client("cloudwatch", region_name="us-east-1")
cw.put_metric_data(Namespace="Orders", MetricData=[{
    "MetricName": "Processed", "Value": 1, "Unit": "Count"}])
```

## Delete / teardown
```python
cw.delete_alarms(AlarmNames=["api-gateway-5xx"])
```

## Expert tips

- Set retention on every log group — default is forever (and bills).
- A billing alarm is the first alarm you should ever create.

## Real-world example

**Every ops team** — Autoscaling, billing alarms and log insights all hang off CloudWatch.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon CloudWatch keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where Amazon CloudWatch is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production Amazon CloudWatch is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for Amazon CloudWatch means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **Auto Scaling** (Target-tracking reads its metrics.) — see `auto-scaling`
- **SNS** (Alarms notify topics.) — see `sns`
- **Bedrock Agents** (AgentOps traces & metrics land here.) — see `bedrock-agents`
