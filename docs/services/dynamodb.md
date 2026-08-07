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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon DynamoDB runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon DynamoDB gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon DynamoDB is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon DynamoDB is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon DynamoDB disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **Lambda** (The classic pair: stateless function + ms table.) — see `lambda`
- **API Gateway** (HTTP APIs front DynamoDB-backed Lambdas.) — see `api-gateway`
- **Streams → EventBridge** (Row changes fan out.) — see `streams-→-eventbridge`
