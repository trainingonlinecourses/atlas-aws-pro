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

## Next steps

- **RDS / Aurora** (Native rotation of master passwords.) — see `rds---aurora`
- **KMS** (Envelope-encrypted secrets.) — see `kms`
- **ECS / Lambda** (Fetch via role permissions.) — see `ecs---lambda`
