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

## Next steps

- **App tier** (Reads cache before ever hitting the DB.) — see `app-tier`
- **VPC** (Cluster sits in private subnets.) — see `vpc`
