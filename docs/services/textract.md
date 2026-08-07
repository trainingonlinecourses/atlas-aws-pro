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

## Next steps

- **S3** (Documents in, structured JSON out.) — see `s3`
- **Comprehend** (Chained for entities in extracted text.) — see `comprehend`
- **Step Functions** (Human-review loops.) — see `step-functions`
