# 🧰 AWS Backup (`backup`)

> One central policy engine backing up EC2, RDS, DynamoDB, EFS and S3.

- **Category:** Storage
- **Service id:** `backup`

## Why it exists
Every service has its own backup knob until one fails. Backup centralizes policies, retention and cross-region copies.

## When to use it
Org-wide backup plans, PITR, DR copies.

## Learn first

- Vaults, plans & selections
- Retention & cold tiers
- Cross-account / cross-region copies

## Terraform
```hcl
resource "aws_backup_vault" "main" { name = "acme-vault" }

resource "aws_backup_plan" "daily" {
  name = "daily-everything"
  rule {
    rule_name = "daily"
    target_vault_name = aws_backup_vault.main.name
    schedule = "cron(0 3 * * ? *)"
    lifecycle { delete_after = 35 }
  }
}

resource "aws_backup_selection" "tagged" {
  name = "backup-tagged"
  plan_id = aws_backup_plan.daily.id
  iam_role_arn = aws_iam_role.backup.arn
  selection_tag { type = "STRINGEQUALS"; key = "Backup"; value = "true" }
}
```

## AWS CDK
```ts
import * as backup from "aws-cdk-lib/aws-backup";
import * as events from "aws-cdk-lib/aws-events";
const vault = new backup.BackupVault(this, "Vault");
const plan = new backup.BackupPlan(this, "Daily", {
  backupVault: vault,
  backupPlanRules: [new backup.BackupPlanRule({
    scheduleExpression: events.Schedule.cron({ hour: "3", minute: "0" }),
    deleteAfter: cdk.Duration.days(35),
  })],
});
plan.addSelection("Tagged", {
  resources: [backup.BackupResource.fromTag("Backup", "true")],
});
```

## Boto3 (Python)
```python
import boto3
bk = boto3.client("backup", region_name="us-east-1")
for v in bk.list_backup_vaults()["BackupVaultList"]:
    print(v["BackupVaultName"], v["CreationDate"])
bk.start_backup_job(BackupVaultName="acme-vault",
    ResourceArn="arn:aws:rds:us-east-1:123456789012:db:orders-db")
```

## Delete / teardown
```python
bk.delete_backup_vault(BackupVaultName="acme-vault")  # must be empty
```

## Expert tips

- Tag-based selection scales better than resource lists.
- Restore tests count — backups you've never restored are hopes.

## Real-world example

**DR planning** — Nightly cross-region copies of RDS + EBS, restorable in minutes.

## Next steps

- **RDS / EC2 / DynamoDB / EFS / S3** (All backup sources.) — see `rds---ec2---dynamodb---efs---s3`
- **KMS** (Vaults encrypt everything.) — see `kms`
- **EventBridge** (Job completion notifications.) — see `eventbridge`
