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

## Next steps

- **Bedrock KB** (The default vector store for RAG.) — see `bedrock-kb`
- **VPC** (Domains can sit fully private.) — see `vpc`
- **S3** (Snapshots for backup.) — see `s3`
