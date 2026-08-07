# 🧠 Amazon ElastiCache (`elasticache`)

> Managed Redis / Valkey — sub-millisecond memory in front of everything.

- **Category:** Database
- **Service id:** `elasticache`

## Why it exists
Your DB can't survive every page rendering a query. A cache cuts p99 from 100ms to 1ms.

## When to use it
Sessions, leaderboards, feed caches, rate limiting, pub/sub.

## Learn first

- Redis structures & TTLs
- Cache-aside pattern
- Replication groups & failover

## Terraform
```hcl
resource "aws_elasticache_replication_group" "sessions" {
  replication_group_id = "sessions"
  description = "Redis sessions cache"
  node_type = "cache.r6g.large"
  engine = "redis"; engine_version = "7.1"
  num_cache_clusters = 2
  automatic_failover_enabled = true
  subnet_group_name = aws_elasticache_subnet_group.cache.name
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
}
```

## AWS CDK
```ts
import * as elasticache from "aws-cdk-lib/aws-elasticache";
new elasticache.CfnReplicationGroup(this, "Sessions", {
  replicationGroupDescription: "Redis sessions",
  engine: "redis", cacheNodeType: "cache.r6g.large",
  numCacheClusters: 2, automaticFailoverEnabled: true,
});
```

## Boto3 (Python)
```python
# pip install redis
import redis
r = redis.Redis(host="sessions.xxxx.use1.cache.amazonaws.com", port=6379, ssl=True)
r.setex("session:c-99", 1800, "token-blob")
print(r.get("session:c-99"))
```

## Delete / teardown
```python
import boto3
boto3.client("elasticache").delete_replication_group(ReplicationGroupId="sessions")
```

## Expert tips

- Give every key a TTL — memory leaks are silent.
- Watch cache-hit rate; below 80% means rework keys.

## Real-world example

**Tinder** — Caches sessions and match data to keep latency imperceptible.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon ElastiCache runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon ElastiCache gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon ElastiCache is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon ElastiCache is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon ElastiCache disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **App tier** (Reads cache before ever hitting the DB.) — see `app-tier`
- **VPC** (Cluster sits in private subnets.) — see `vpc`
