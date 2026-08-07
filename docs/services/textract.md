# 📄 Amazon Textract (`textract`)

> Extract tables, forms and handwriting from any scanned document.

- **Category:** Machine Learning & AI
- **Service id:** `textract`
- **AI-enabled:** yes

## Why it exists
OCR libraries crumble on invoices with tables. Textract understands layout — fields, tables, checkboxes.

## When to use it
Invoice processing, KYC intake, insurance claims.

## Learn first

- Sync vs async APIs
- AnalyzeDocument vs AnalyzeExpense
- Confidence & review loops

## Terraform
```hcl
# Per-call AI service — no infrastructure to provision.
resource "aws_iam_policy" "textract_use" {
  name = "textract-analyze"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["textract:AnalyzeDocument", "textract:StartDocumentAnalysis"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
new iam.ManagedPolicy(this, "TextractAnalyze", {
  statements: [new iam.PolicyStatement({
    actions: ["textract:AnalyzeDocument", "textract:StartDocumentAnalysis"],
    resources: ["*"],
  })],
});
```

## Boto3 (Python)
```python
import boto3
tex = boto3.client("textract", region_name="us-east-1")
resp = tex.analyze_document(
    Document={"S3Object": {"Bucket": "acme-assets-prod", "Name": "invoice-1042.pdf"}},
    FeatureTypes=["TABLES", "FORMS"])
for b in resp["Blocks"][:5]:
    if b["BlockType"] == "LINE":
        print(b["Text"])
```

## Delete / teardown
```python
# Nothing to delete — per-call service.
```

## Expert tips

- Use AnalyzeExpense for invoices — it knows line items.
- Route low-confidence fields to a human review queue.

## Real-world example

**Mortgage lenders** — Extract income documents in seconds instead of manual data entry.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Textract runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Textract against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Textract is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Textract is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **S3** (Documents in, structured JSON out.) — see `s3`
- **Comprehend** (Chained for entities in extracted text.) — see `comprehend`
- **Step Functions** (Human-review loops.) — see `step-functions`
