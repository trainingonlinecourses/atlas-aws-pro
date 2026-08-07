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

## Next steps

- **Bedrock + OpenSearch** (Build a custom RAG pipeline instead.) — see `bedrock-+-opensearch`
- **Textract** (Extract text from PDFs before indexing.) — see `textract`
