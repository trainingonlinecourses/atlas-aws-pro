# 🔱 Amazon Neptune (`neptune`)

> Graph database for relationships — fraud rings, social graphs, knowledge.

- **Category:** Database
- **Service id:** `neptune`

## Why it exists
When the question is 'who connects to whom, how many hops away', joins collapse. Graphs traverse in milliseconds.

## When to use it
Fraud detection, recommendations, knowledge graphs.

## Learn first

- Property graph vs RDF
- Gremlin / openCypher
- Graph modeling

## Terraform
```hcl
resource "aws_neptune_cluster" "graph" {
  cluster_identifier = "acme-graph"
  engine = "neptune"
  iam_database_authentication_enabled = true
  storage_encrypted = true
  neptune_subnet_group_name = aws_neptune_subnet_group.graph.name
}

resource "aws_neptune_cluster_instance" "writer" {
  identifier = "graph-writer"
  cluster_identifier = aws_neptune_cluster.graph.id
  instance_class = "db.r6g.large"
}
```

## AWS CDK
```ts
import * as neptune from "aws-cdk-lib/aws-neptune";
const cluster = new neptune.CfnDBCluster(this, "Graph", {
  iamAuthEnabled: true, storageEncrypted: true,
});
new neptune.CfnDBInstance(this, "GraphWriter", {
  dbInstanceClass: "db.r6g.large", dbClusterId: cluster.ref,
});
```

## Boto3 (Python)
```python
# pip install gremlinpython — then walk the graph:
# g.V().has("customer","id","c-99").out("transacted_with").limit(3)
import boto3
nep = boto3.client("neptune", region_name="us-east-1")
print([c["DBClusterIdentifier"] for c in nep.describe_db_clusters()["DBClusters"]])
```

## Delete / teardown
```python
nep.delete_db_cluster(DBClusterIdentifier="acme-graph", SkipFinalSnapshot=True)
```

## Expert tips

- Model the questions first — graphs are query-shaped.
- Depth-limited traversals keep latency flat.

## Real-world example

**Fraud teams** — Detect money-mule rings by walking transaction graphs in real time.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon Neptune runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon Neptune gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon Neptune is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon Neptune is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Neptune disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **VPC** (Cluster lives in private subnets.) — see `vpc`
- **IAM** (Database auth via IAM instead of passwords.) — see `iam`
- **Bedrock KB** (Graphs enrich RAG.) — see `bedrock-kb`
