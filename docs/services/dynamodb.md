# 🧲 Amazon DynamoDB (`dynamodb`)

> Millisecond NoSQL at any scale — the default for serverless apps.

- **Category:** Database
- **Service id:** `dynamodb`

## Why it exists
Single-digit-ms reads at millions of requests/sec with zero database ops.

## When to use it
Sessions, carts, IoT state, game profiles, key-value patterns.

## Learn first

- Design access patterns FIRST
- Partition + sort keys
- On-demand vs provisioned
- GSIs & Streams

## Terraform
```hcl
resource "aws_dynamodb_table" "orders" {
  name = "orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "customer_id"; range_key = "order_id"
  attribute { name = "customer_id"; type = "S" }
  attribute { name = "order_id"; type = "S" }
  attribute { name = "status"; type = "S" }
  global_secondary_index {
    name = "by-status"; hash_key = "status"; projection_type = "ALL"
  }
  point_in_time_recovery { enabled = true }
}
```

## AWS CDK
```ts
import * as ddb from "aws-cdk-lib/aws-dynamodb";
const table = new ddb.TableV2(this, "Orders", {
  partitionKey: { name: "customer_id", type: ddb.AttributeType.STRING },
  sortKey: { name: "order_id", type: ddb.AttributeType.STRING },
  billing: ddb.Billing.onDemand(),
  pointInTimeRecovery: true,
});
```

## Boto3 (Python)
```python
import boto3
ddb = boto3.resource("dynamodb", region_name="us-east-1")
table = ddb.Table("orders")
table.put_item(Item={"customer_id":"c-99","order_id":"A-1042","status":"paid"})
resp = table.query(KeyConditionExpression="customer_id = :c",
                   ExpressionAttributeValues={":c":"c-99"})
print(resp["Items"])
```

## Delete / teardown
```python
ddb.Table("orders").delete()
```

## Expert tips

- Single-table design is a superpower once it clicks.
- Hot partitions kill performance — choose keys that spread.

## Real-world example

**Duolingo** — Stores tens of billions of learner objects and scales through viral spikes.

## Next steps

- **Lambda** (The classic pair: stateless function + ms table.) — see `lambda`
- **API Gateway** (HTTP APIs front DynamoDB-backed Lambdas.) — see `api-gateway`
- **Streams → EventBridge** (Row changes fan out.) — see `streams-→-eventbridge`
