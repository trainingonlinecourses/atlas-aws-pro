# 📋 AWS Config (`config`)

> Continuous inventory of your infrastructure + compliance rules as code.

- **Category:** Management & Governance
- **Service id:** `config`

## Why it exists
'What did prod look like on Tuesday?' — Config records every resource change and evaluates rules continuously.

## When to use it
Compliance rules, drift visibility, change history, remediation.

## Learn first

- Recorders & snapshots
- Managed vs custom rules
- Conformance packs
- Remediation actions

## Terraform
```hcl
resource "aws_config_configuration_recorder" "main" {
  name = "main-recorder"
  role_arn = aws_iam_role.config.arn
  recording_group {
    all_supported = true
    include_global_resource_types = true
  }
}

resource "aws_config_config_rule" "no_public_buckets" {
  name = "s3-bucket-public-read-prohibited"
  source {
    owner = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }
  depends_on = [aws_config_configuration_recorder.main]
}
```

## AWS CDK
```ts
import * as config from "aws-cdk-lib/aws-config";
new config.CfnConfigurationRecorder(this, "Recorder", {
  recordingGroup: { allSupported: true, includeGlobalResourceTypes: true },
  roleArn: configRole.roleArn,
});
new config.ManagedRule(this, "NoPublicBuckets", {
  identifier: config.ManagedRuleIdentifiers.S3_BUCKET_PUBLIC_READ_PROHIBITED,
});
```

## Boto3 (Python)
```python
import boto3
cfg = boto3.client("config", region_name="us-east-1")
bad = cfg.get_compliance_details_by_config_rule(
    ConfigRuleName="s3-bucket-public-read-prohibited",
    ComplianceTypes=["NON_COMPLIANT"])
print(len(bad["EvaluationResults"]), "non-compliant resources")
```

## Delete / teardown
```python
cfg.delete_configuration_recorder(ConfigurationRecorderName="main-recorder")
```

## Expert tips

- Pair rules with auto-remediation SSM documents.
- Timeline view shows a resource's entire life story.

## Real-world example

**Regulated teams** — A managed rule flags unencrypted buckets in minutes; Lambda fixes them.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Config keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.

- Give each engineer a short-lived environment or namespace, not shared chaos.
- Set a low retention on dev logs and metrics so noise doesn't mask signal.
- Wire the service into CI so a failing check blocks merge early.

### 🧪 Staging / Pre-prod

Staging is where AWS Config is hardened for operations: alerts, dashboards, and runbooks proven.

- Create the real dashboards and alarms here, then copy them to prod unchanged.
- Test the on-call routing and runbook against a deliberately-induced failure.
- Verify the release pipeline promotes through staging with the same approval gates as prod.

### 🚀 Production

In production AWS Config is the observability and governance backbone of every service.

- Standardize on the four golden signals (latency, traffic, errors, saturation) per service.
- Route alerts by severity; page only on actionable, and keep runbooks one click away.
- Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.

### 🌍 Multi-region / DR

DR for AWS Config means the observability and governance stack answers from the backup region too.

- Replicate dashboards, alarms, and log/metrics destinations to the DR region.
- Include the monitoring stack in the failover drill so you can actually see the DR state.
- Keep the incident-response runbook in a second location, not only in the primary tool.

### ♻️ Lifecycle & IaC

Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.

- Maintain cost-allocation tags (team, env, service) enforced by policy.
- Run periodic right-sizing and idle-resource reviews with the owning teams.
- Close the loop: every incident produces a runbook update or a new automated check.

## Next steps

- **S3** (Snapshots delivered to a bucket.) — see `s3`
- **EventBridge / SNS** (Notify on non-compliance.) — see `eventbridge---sns`
- **Security Hub** (Config findings roll up.) — see `security-hub`
