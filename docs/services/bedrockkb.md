# 📚 Bedrock Knowledge Bases (`bedrockkb`)

> RAG as a service — your documents become a live, searchable knowledge base.

- **Category:** Machine Learning & AI
- **Service id:** `bedrockkb`
- **AI-enabled:** yes

## Why it exists
LLMs don't know your private data. A KB chunks, embeds and indexes your docs into a vector store.

## When to use it
Grounded chatbots, doc Q&A, agent knowledge, semantic search.

## Learn first

- Chunking strategies
- Embedding models
- Vector stores (OpenSearch Serverless)
- Retrieve vs RetrieveAndGenerate

## Terraform
```hcl
resource "aws_bedrockagent_knowledge_base" "docs" {
  name = "policy-docs"
  role_arn = aws_iam_role.kb_role.arn
  knowledge_base_configuration {
    type = "VECTOR"
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock::foundation-model/amazon.titan-embed-text-v1"
    }
  }
  storage_configuration {
    type = "OPENSEARCH_SERVERLESS"
    opensearch_serverless_configuration {
      collection_arn = aws_opensearchserverless_collection.vectors.arn
      vector_index_name = "kb-index"
    }
  }
}

resource "aws_bedrockagent_data_source" "s3_docs" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.docs.knowledge_base_id
  name = "policy-pdfs"
  data_source_configuration {
    type = "S3"
    s3_configuration { bucket_arn = aws_s3_bucket.docs.arn }
  }
}
```

## AWS CDK
```ts
import * as bedrockagent from "aws-cdk-lib/aws-bedrockagent";
const kb = new bedrockagent.CfnKnowledgeBase(this, "Docs", {
  roleArn: kbRole.roleArn,
  knowledgeBaseConfiguration: {
    type: "VECTOR",
    vectorKnowledgeBaseConfiguration: {
      embeddingModelArn: "arn:aws:bedrock::foundation-model/amazon.titan-embed-text-v1",
    },
  },
  storageConfiguration: {
    type: "OPENSEARCH_SERVERLESS",
    opensearchServerlessConfiguration: {
      collectionArn: collection.attrArn, vectorIndexName: "kb-index",
    },
  },
});
```

## Boto3 (Python)
```python
import boto3
rt = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
resp = rt.retrieve(knowledgeBaseId="KB123",
    retrievalQuery={"text": "What is our refund policy?"})
for chunk in resp["retrievalResults"][:3]:
    print(chunk["content"]["text"][:120], "...")
```

## Delete / teardown
```python
boto3.client("bedrock-agent").delete_knowledge_base(knowledgeBaseId="KB123")
```

## Expert tips

- Re-sync after doc changes — retrieval quality decays with stale indexes.
- Chunk size is a quality knob; test 300 vs 800 tokens.

## Real-world example

**Support teams** — Ground answers in 10,000 policy PDFs; agents quote sources instead of hallucinating.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Bedrock Knowledge Bases runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Bedrock Knowledge Bases against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Bedrock Knowledge Bases is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Bedrock Knowledge Bases is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **S3** (Source documents live in buckets.) — see `s3`
- **OpenSearch Serverless** (Default vector store.) — see `opensearch-serverless`
- **Bedrock Agents** (Consume the KB during reasoning.) — see `bedrock-agents`
