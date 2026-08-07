# 📉 Amazon QuickSight (`quicksight`)

> Serverless BI dashboards — pay per session, embed anywhere, ask Q.

- **Category:** Analytics
- **Service id:** `quicksight`
- **AI-enabled:** yes

## Why it exists
Analysts need dashboards on lake/warehouse data without BI servers. Q answers natural-language questions.

## When to use it
Exec dashboards, embedded analytics in SaaS, SPICE-fast reports.

## Learn first

- Datasets (Athena/Redshift/RDS)
- SPICE engine
- Analyses vs dashboards
- Embedding + Q

## Terraform
```hcl
# QuickSight is configured mostly in-console; Terraform manages users:
resource "aws_quicksight_user" "analyst" {
  email = "analyst@acme.dev"
  identity_type = "IAM"
  user_role = "AUTHOR"
  namespace = "default"
  aws_account_id = data.aws_caller_identity.current.account_id
}
```

## AWS CDK
```ts
// Dashboards are authored in the console/API;
// in CDK, grant the QuickSight service role query access:
datasetRole.addToPolicy(new iam.PolicyStatement({
  actions: ["athena:StartQueryExecution", "athena:GetQueryExecution"],
  resources: ["*"],
}));
```

## Boto3 (Python)
```python
import boto3
qs = boto3.client("quicksight", region_name="us-east-1")
for d in qs.list_dashboards(AwsAccountId="123456789012")["DashboardSummaryList"]:
    print(d["Name"], d["LastPublishedTime"])
```

## Delete / teardown
```python
qs.delete_dashboard(AwsAccountId=acct, DashboardId=id)
```

## Expert tips

- SPICE = in-memory turbo for dashboards; direct query for freshness.
- Per-session pricing beats per-seat when viewers are occasional.

## Real-world example

**Product teams** — Embed live usage dashboards inside their SaaS apps.

## Next steps

- **Athena / Redshift / RDS** (Dataset sources.) — see `athena---redshift---rds`
- **S3** (SPICE imports.) — see `s3`
- **Cognito** (Auth for embedded dashboards.) — see `cognito`
