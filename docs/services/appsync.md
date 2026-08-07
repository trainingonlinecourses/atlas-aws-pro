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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS AppSync is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where AWS AppSync is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production AWS AppSync is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for AWS AppSync is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats AWS AppSync as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **DynamoDB / Lambda** (Resolvers read & call data sources.) — see `dynamodb---lambda`
- **Cognito** (Default auth for user apps.) — see `cognito`
- **EventBridge** (Event data source.) — see `eventbridge`
