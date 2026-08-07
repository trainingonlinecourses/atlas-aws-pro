# 🔎 Amazon OpenSearch Service (`opensearch`)

> Search + analytics + the vector engine behind most AWS RAG stacks.

- **Category:** Database
- **Service id:** `opensearch`

## Why it exists
Full-text search and log analytics need inverted indexes; GenAI needs a vector store. OpenSearch does both.

## When to use it
App search, log dashboards, vector DB for Bedrock Knowledge Bases.

## Learn first

- Indexes, mappings, shards
- Dashboards
- Serverless collections
- k-NN / vector indexes

## Terraform
```hcl
resource "aws_opensearch_domain" "vectors" {
  domain_name = "vectors"
  engine_version = "OpenSearch_2.15"
  cluster_config { instance_type = "r6g.large.search"; instance_count = 2 }
  ebs_options { ebs_enabled = true; volume_size = 100; volume_type = "gp3" }
  encrypt_at_rest { enabled = true }
  domain_endpoint_options { enforce_https = true }
}
```

## AWS CDK
```ts
import * as opensearch from "aws-cdk-lib/aws-opensearchservice";
new opensearch.Domain(this, "Vectors", {
  version: opensearch.EngineVersion.openSearch("2.15"),
  capacity: { dataNodes: 2, dataNodeInstanceType: "r6g.large.search" },
  ebs: { volumeSize: 100, volumeType: ec2.EbsDeviceVolumeType.GP3 },
  enforceHttps: true,
});
```

## Boto3 (Python)
```python
import boto3
osc = boto3.client("opensearch", region_name="us-east-1")
d = osc.describe_domain(DomainName="vectors")["DomainStatus"]
print(d["Endpoint"], d["EngineVersion"])
```

## Delete / teardown
```python
osc.delete_domain(DomainName="vectors")
```

## Expert tips

- 3 dedicated masters once you pass ~10 data nodes.
- Serverless collections are ideal for KB vector stores.

## Real-world example

**GenAI teams** — Store Bedrock knowledge-base embeddings and serve similarity search for RAG.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev Amazon OpenSearch Service runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.

- Use a tiny instance or a local/containerized equivalent for day-to-day coding.
- Run schema migrations through the same tool as prod so `apply` is boring and tested.
- Seed with sanitized data, never production PII.

### 🧪 Staging / Pre-prod

Staging is where Amazon OpenSearch Service gets the schema migration, index, and query-plan validation that prod demands.

- Apply the migration, then run the top 10 production queries and compare plans.
- Load-test write and read paths; tune parameters before they become a prod page.
- Exercise the backup-and-restore procedure against staging data.

### 🚀 Production

In production Amazon OpenSearch Service is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.

- Enable multi-AZ, automated backups, and Performance Insights from the start.
- Set statement/query timeouts and alarm on CPU, storage, and deadlocks.
- Use read replicas for reporting and right-size before the CPU knee, not after.

### 🌍 Multi-region / DR

DR for Amazon OpenSearch Service is a readable copy in another region with a defined RPO/RTO and a tested promotion.

- Configure cross-region read replicas or continuous backup to a second region.
- Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.
- Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon OpenSearch Service disciplined: IaC-managed, versioned, and with a teardown that removes data.

- Own the instance and all config in Terraform; use a secrets store for the master password.
- Keep migration files in the repo, applied in order by CI, never by hand.
- Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.

## Next steps

- **Bedrock KB** (The default vector store for RAG.) — see `bedrock-kb`
- **VPC** (Domains can sit fully private.) — see `vpc`
- **S3** (Snapshots for backup.) — see `s3`
