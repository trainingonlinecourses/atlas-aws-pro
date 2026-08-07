# 🔑 Key Management Service (`kms`)

> The vault for your encryption keys — used by nearly every AWS service.

- **Category:** Security, Identity & Compliance
- **Service id:** `kms`

## Why it exists
Encryption at rest is table stakes. KMS gives central, auditable, rotating keys that S3, RDS, EBS call into.

## When to use it
Envelope encryption, service encryption, compliance.

## Learn first

- KMS keys vs data keys
- Envelope encryption
- Key policies & rotation

## Terraform
```hcl
resource "aws_kms_key" "app" {
  description = "acme application data key"
  enable_key_rotation = true
  deletion_window_in_days = 30
}

resource "aws_kms_alias" "app" {
  name = "alias/acme-app"
  target_key_id = aws_kms_key.app.key_id
}
```

## AWS CDK
```ts
import * as kms from "aws-cdk-lib/aws-kms";
const key = new kms.Key(this, "App", {
  enableKeyRotation: true, alias: "acme-app",
});
```

## Boto3 (Python)
```python
import boto3
kms = boto3.client("kms", region_name="us-east-1")
enc = kms.encrypt(KeyId="alias/acme-app", Plaintext=b"ssn:123-45-6789")
dec = kms.decrypt(CiphertextBlob=enc["CiphertextBlob"])
print("roundtrip:", dec["Plaintext"].decode())
```

## Delete / teardown
```python
kms.schedule_key_deletion(KeyId="alias/acme-app", PendingWindowInDays=7)
```

## Expert tips

- Deletion has a waiting period on purpose — keys can't be un-broken.
- Aliases keep code stable while keys rotate.

## Real-world example

**Healthtech** — Encrypt PHI in RDS + S3 with customer-managed, annually rotated keys.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Key Management Service is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Key Management Service is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Key Management Service is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Key Management Service means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Key Management Service continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **S3 / RDS / EBS / ECR** (All encrypt with KMS keys.) — see `s3---rds---ebs---ecr`
- **CloudTrail** (Every key use is auditable.) — see `cloudtrail`
- **Secrets Manager** (Secrets wrapped with KMS.) — see `secrets-manager`
