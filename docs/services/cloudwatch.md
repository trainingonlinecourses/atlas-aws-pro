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

## Next steps

- **Auto Scaling** (Target-tracking reads its metrics.) — see `auto-scaling`
- **SNS** (Alarms notify topics.) — see `sns`
- **Bedrock Agents** (AgentOps traces & metrics land here.) — see `bedrock-agents`
