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

## Next steps

- **S3** (Source documents live in buckets.) — see `s3`
- **OpenSearch Serverless** (Default vector store.) — see `opensearch-serverless`
- **Bedrock Agents** (Consume the KB during reasoning.) — see `bedrock-agents`
