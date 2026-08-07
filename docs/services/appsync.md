# 🔗 AWS AppSync (`appsync`)

> Managed GraphQL API — realtime subscriptions, offline sync, many data sources.

- **Category:** Application Integration
- **Service id:** `appsync`

## Why it exists
Mobile apps want one endpoint with exactly the fields they need, plus live updates.

## When to use it
Mobile backends, realtime dashboards, schema aggregation.

## Learn first

- GraphQL schema & resolvers
- Data sources
- Auth modes
- Subscriptions

## Terraform
```hcl
resource "aws_appsync_graphql_api" "mobile" {
  name = "mobile-api"
  authentication_type = "AMAZON_COGNITO_USER_POOLS"
  user_pool_config {
    user_pool_id = aws_cognito_user_pool.users.id
    default_action = "ALLOW"
  }
}

resource "aws_appsync_datasource" "orders" {
  api_id = aws_appsync_graphql_api.mobile.id
  name = "orders"; type = "AMAZON_DYNAMODB"
  service_role_arn = aws_iam_role.appsync_ddb.arn
  dynamodb_config { table_name = aws_dynamodb_table.orders.name }
}
```

## AWS CDK
```ts
import * as appsync from "aws-cdk-lib/aws-appsync";
const api = new appsync.GraphqlApi(this, "Mobile", {
  name: "mobile-api",
  authorizationConfig: { defaultAuthorization: {
    authorizationType: appsync.AuthorizationType.USER_POOL,
    userPoolConfig: { userPool: pool } } },
});
api.addDynamoDbDataSource("Orders", table);
```

## Boto3 (Python)
```python
import boto3
asx = boto3.client("appsync", region_name="us-east-1")
for g in asx.list_graphql_apis()["graphqlApis"]:
    print(g["name"], g["uris"]["GRAPHQL"])
```

## Delete / teardown
```python
asx.delete_graphql_api(apiId=id)
```

## Expert tips

- Subscriptions need WebSocket — test on real devices.
- Multiple auth modes on one API is a feature, use it.

## Real-world example

**Mobile apps** — Live score and price updates to millions of devices via subscriptions.

## Next steps

- **DynamoDB / Lambda** (Resolvers read & call data sources.) — see `dynamodb---lambda`
- **Cognito** (Default auth for user apps.) — see `cognito`
- **EventBridge** (Event data source.) — see `eventbridge`
