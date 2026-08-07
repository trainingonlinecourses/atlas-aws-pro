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

## Next steps

- **S3** (Snapshots delivered to a bucket.) — see `s3`
- **EventBridge / SNS** (Notify on non-compliance.) — see `eventbridge---sns`
- **Security Hub** (Config findings roll up.) — see `security-hub`
