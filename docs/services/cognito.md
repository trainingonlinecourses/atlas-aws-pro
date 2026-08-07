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

## Next steps

- **API Gateway** (JWT authorizers validate Cognito tokens.) — see `api-gateway`
- **Lambda** (Custom triggers for sign-up & MFA.) — see `lambda`
- **IAM** (Identity pools swap tokens for AWS creds.) — see `iam`
