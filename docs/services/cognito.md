# 👤 Amazon Cognito (`cognito`)

> Production sign-up/sign-in without building an auth server.

- **Category:** Security, Identity & Compliance
- **Service id:** `cognito`

## Why it exists
Building auth from scratch is a security trap. Cognito hands you user pools, MFA and JWTs out of the box.

## When to use it
Web & mobile sign-in, social federation, tokens for API Gateway.

## Learn first

- User pools vs identity pools
- JWT flow
- Hosted UI vs custom
- App clients

## Terraform
```hcl
resource "aws_cognito_user_pool" "users" {
  name = "acme-users"
  auto_verified_attributes = ["email"]
  password_policy {
    minimum_length = 10; require_uppercase = true
    require_numbers = true; require_symbols = true
  }
}

resource "aws_cognito_user_pool_client" "web" {
  name = "web-spa"
  user_pool_id = aws_cognito_user_pool.users.id
  generate_secret = false
  explicit_auth_flows = ["ALLOW_USER_SRP_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
}
```

## AWS CDK
```ts
import * as cognito from "aws-cdk-lib/aws-cognito";
const pool = new cognito.UserPool(this, "Users", {
  selfSignUpEnabled: true, autoVerify: { email: true },
  passwordPolicy: { minLength: 10, requireSymbols: true },
});
pool.addClient("WebSpa", { authFlows: { userSrp: true } });
```

## Boto3 (Python)
```python
import boto3
cog = boto3.client("cognito-idp", region_name="us-east-1")
resp = cog.admin_create_user(UserPoolId="us-east-1_XXXXX",
                             Username="ada@example.com")
print("created:", resp["User"]["Username"])
```

## Delete / teardown
```python
cog.delete_user_pool(UserPoolId="us-east-1_XXXXX")
```

## Expert tips

- SPAs get clients WITHOUT secrets; backends get clients WITH them.
- Identity pools exchange tokens for scoped AWS creds.

## Real-world example

**Consumer apps** — Login, MFA and profiles across mobile and web with zero auth servers.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Cognito is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Amazon Cognito is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Amazon Cognito is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Amazon Cognito means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Cognito continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **API Gateway** (JWT authorizers validate Cognito tokens.) — see `api-gateway`
- **Lambda** (Custom triggers for sign-up & MFA.) — see `lambda`
- **IAM** (Identity pools swap tokens for AWS creds.) — see `iam`
