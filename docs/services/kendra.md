# 🔍 Amazon Kendra (`kendra`)

> Enterprise search powered by ML — answers from your documents, not a keyword list.

- **Category:** Machine Learning & AI
- **Service id:** `kendra`
- **AI-enabled:** yes

## Why it exists
Keyword search returns 1,000 docs; people want an answer. Kendra indexes your docs, wikis and SharePoint and returns relevant answers with sources.

## When to use it
Internal knowledge bases, help centers, HR/IT self-service search.

## Learn first

- Indexes, data sources, connectors
- Document metadata & access control
- FAQs & question answering
- S3/SharePoint/Confluence connectors

## Terraform
```hcl
resource "aws_kendra_index" "kb" {
  name     = "company-kb"
  edition  = "DEVELOPER_EDITION"
  role_arn = aws_iam_role.kendra.arn
}
resource "aws_kendra_data_source" "s3_docs" {
  index_id = aws_kendra_index.kb.id
  name     = "s3-docs"
  type     = "S3"
  role_arn = aws_iam_role.kendra.arn
}
```

## AWS CDK
```ts
// No first-class CDK construct (L1 only) — manage with Terraform.
```

## Boto3 (Python)
```python
import boto3
kendra = boto3.client("kendra", region_name="us-east-1")
resp = kendra.query(IndexId="<index-id>", QueryText="how to reset my password")
for r in resp["ResultItems"][:3]:
    print(r.get("DocumentTitle", {}).get("Text"), "-", r.get("DocumentURI"))
```

## Delete / teardown
```python
kendra.delete_index(Id="<index-id>")
```

## Expert tips

- Feed it metadata-rich docs; relevance depends on structure.
- Use FAQ + document-answer query modes for better responses.

## Real-world example

**Large enterprises** — Cut support tickets with internal answer search.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Kendra runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Kendra against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Kendra is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Kendra is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Bedrock + OpenSearch** (Build a custom RAG pipeline instead.) — see `bedrock-+-opensearch`
- **Textract** (Extract text from PDFs before indexing.) — see `textract`
