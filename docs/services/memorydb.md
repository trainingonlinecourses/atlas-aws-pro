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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon MemoryDB runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon MemoryDB gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon MemoryDB is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon MemoryDB is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon MemoryDB disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **ElastiCache** (Cheaper when you truly only need a cache.) — see `elasticache`
- **DAX** (In-memory acceleration for DynamoDB.) — see `dax`
