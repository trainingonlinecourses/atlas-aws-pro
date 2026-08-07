# 🗝️ AWS Secrets Manager (`secretsmanager`)

> Credentials live here, not in .env files — with automatic rotation.

- **Category:** Security, Identity & Compliance
- **Service id:** `secretsmanager`

## Why it exists
DB passwords in git are how breaches start. Secrets Manager stores them encrypted and rotates automatically.

## When to use it
RDS credentials, third-party API keys, OAuth tokens.

## Learn first

- Secrets vs Parameter Store
- Rotation with Lambda
- Fetching at runtime

## Terraform
```hcl
resource "aws_secretsmanager_secret" "db_creds" {
  name = "prod/orders-db"
  kms_key_id = aws_kms_key.app.arn
}

resource "aws_secretsmanager_secret_version" "v1" {
  secret_id = aws_secretsmanager_secret.db_creds.id
  secret_string = jsonencode({ username = "appadmin", password = "CHANGE-ME" })
}
```

## AWS CDK
```ts
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
const secret = new secretsmanager.Secret(this, "DbCreds", {
  secretName: "prod/orders-db", encryptionKey: key,
});
```

## Boto3 (Python)
```python
import boto3, json
sm = boto3.client("secretsmanager", region_name="us-east-1")
creds = json.loads(sm.get_secret_value(SecretId="prod/orders-db")["SecretString"])
print("connecting as", creds["username"])
```

## Delete / teardown
```python
sm.delete_secret(SecretId="prod/orders-db", ForceDeleteWithoutRecovery=True)
```

## Expert tips

- Apps fetch secrets at runtime — never bake them into images.
- RDS-native rotation needs zero custom code.

## Real-world example

**Every RDS shop** — Lambda rotates DB credentials monthly; apps fetch fresh creds at runtime.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Secrets Manager is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where AWS Secrets Manager is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production AWS Secrets Manager is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for AWS Secrets Manager means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps AWS Secrets Manager continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **RDS / Aurora** (Native rotation of master passwords.) — see `rds---aurora`
- **KMS** (Envelope-encrypted secrets.) — see `kms`
- **ECS / Lambda** (Fetch via role permissions.) — see `ecs---lambda`
