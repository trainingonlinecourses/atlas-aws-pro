# ⚡ Amazon MemoryDB (`memorydb`)

> Redis-compatible, durable in-memory database — for when losing data is not an option.

- **Category:** Database
- **Service id:** `memorydb`

## Why it exists
Plain ElastiCache is a cache: restart and it's empty. MemoryDB keeps a write-ahead log so data survives restarts, making it a true database.

## When to use it
Leaderboards, sessions, real-time counters, durable pub/sub.

## Learn first

- Durable vs ephemeral in-memory
- Cluster + shards + replicas
- Redis data types
- Eviction vs persistence

## Terraform
```hcl
resource "aws_memorydb_cluster" "live" {
  name         = "live-scores"
  node_type    = "db.t4g.small"
  num_shards   = 1
  num_replicas_per_shard = 1
}
```

## AWS CDK
```ts
// No first-class CDK construct (L1 only) — manage with Terraform.
```

## Boto3 (Python)
```python
import boto3
mdb = boto3.client("memorydb", region_name="us-east-1")
for c in mdb.describe_clusters()["Clusters"]:
    print(c["Name"], c["Status"])
```

## Delete / teardown
```python
mdb.delete_cluster(ClusterName="live-scores")
```

## Expert tips

- Pick MemoryDB when the data must survive; ElastiCache when it's just a cache.
- Scale writes with multiple shards.

## Real-world example

**Gaming companies** — Live leaderboards that must not wipe on deploy.

## Next steps

- **ElastiCache** (Cheaper when you truly only need a cache.) — see `elasticache`
- **DAX** (In-memory acceleration for DynamoDB.) — see `dax`
