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

## Next steps

- **S3 / RDS / EBS / ECR** (All encrypt with KMS keys.) — see `s3---rds---ebs---ecr`
- **CloudTrail** (Every key use is auditable.) — see `cloudtrail`
- **Secrets Manager** (Secrets wrapped with KMS.) — see `secrets-manager`
