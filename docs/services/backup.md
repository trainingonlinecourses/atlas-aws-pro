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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Backup holds throwaway data. Versioning and lifecycle are on from day one so bad deletes stay reversible.

- Enable versioning and object-lock from the first bucket — retrofitting is painful.
- Use a dev-only prefix/account; never let dev code write to a prod path.
- Set a short lifecycle rule to expire dev objects automatically and keep the bill near zero.

### 🧪 Staging / Pre-prod

Staging proves the data pipeline end-to-end with realistic volumes and the same policies as prod.

- Mirror prod's bucket names, permissions, and lifecycle — test the policy, not a happy path.
- Run the migration/replication job against staging data before production cutover.
- Verify restore from a versioned snapshot here, where failure costs nothing.

### 🚀 Production

In production AWS Backup is the durability backbone: versioning, MFA-delete, replication, and access auditing are non-negotiable.

- Enable versioning + MFA Delete and cross-region replication to a second bucket.
- Use Object Lock/WORM for anything auditable; block public access at the account level.
- Centralize access with bucket policies + IAM and watch Macie/GuardDuty findings on the data.

### 🌍 Multi-region / DR

DR means a second copy in another region with a tested restore path, not a bucket that only exists once.

- Cross-region replicate critical prefixes; set an RPO you can actually honor.
- Test a full restore from the replica at least quarterly and log the elapsed time.
- Automate promotion: if the primary region degrades, the replica bucket takes over with the same DNS.

### ♻️ Lifecycle & IaC

Lifecycle manages the data class, not just the bucket: hot -> warm -> archive on a policy.

- Define lifecycle rules (S3 -> Glacier -> Expire) so cost shrinks automatically.
- Own the bucket in Terraform with a remote-state lock so two pipelines can't clobber it.
- Add cost-alerting per bucket and a monthly report of the top spenders.

## Next steps

- **RDS / EC2 / DynamoDB / EFS / S3** (All backup sources.) — see `rds---ec2---dynamodb---efs---s3`
- **KMS** (Vaults encrypt everything.) — see `kms`
- **EventBridge** (Job completion notifications.) — see `eventbridge`
