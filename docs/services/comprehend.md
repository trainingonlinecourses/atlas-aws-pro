# 📝 Amazon Comprehend (`comprehend`)

> NLP as an API: sentiment, entities, key phrases, PII, language.

- **Category:** Machine Learning & AI
- **Service id:** `comprehend`
- **AI-enabled:** yes

## Why it exists
Text is your biggest unstructured asset. Comprehend gives sentiment, entities and PII redaction with zero training.

## When to use it
Ticket triage, review analytics, PII redaction pipelines.

## Learn first

- Sync vs batch jobs
- Sentiment / entity APIs
- PII detection & redaction

## Terraform
```hcl
# Per-call AI service — no infrastructure to provision.
resource "aws_iam_policy" "comprehend_use" {
  name = "comprehend-analyze"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["comprehend:DetectSentiment", "comprehend:DetectEntities"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
new iam.ManagedPolicy(this, "ComprehendAnalyze", {
  statements: [new iam.PolicyStatement({
    actions: ["comprehend:DetectSentiment", "comprehend:DetectEntities"],
    resources: ["*"],
  })],
});
```

## Boto3 (Python)
```python
import boto3
comp = boto3.client("comprehend", region_name="us-east-1")
r = comp.detect_sentiment(
    Text="The onboarding was great but billing confused me.", LanguageCode="en")
print(r["Sentiment"], r["SentimentScore"])
```

## Delete / teardown
```python
# Nothing to delete — per-call service. Remove IAM policies when done.
```

## Expert tips

- Batch (async) is far cheaper than sync for large corpora.
- PII redaction output keeps offsets — re-apply safely.

## Real-world example

**Support orgs** — Route angry tickets to senior agents automatically via sentiment.

## Next steps

- **Transcribe** (Calls → text → sentiment.) — see `transcribe`
- **S3** (Batch jobs read/write buckets.) — see `s3`
- **Step Functions** (Chains NLP steps.) — see `step-functions`
