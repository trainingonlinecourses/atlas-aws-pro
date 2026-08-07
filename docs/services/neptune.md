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

## Next steps

- **VPC** (Cluster lives in private subnets.) — see `vpc`
- **IAM** (Database auth via IAM instead of passwords.) — see `iam`
- **Bedrock KB** (Graphs enrich RAG.) — see `bedrock-kb`
