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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Comprehend runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Comprehend against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Comprehend is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Comprehend is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Transcribe** (Calls → text → sentiment.) — see `transcribe`
- **S3** (Batch jobs read/write buckets.) — see `s3`
- **Step Functions** (Chains NLP steps.) — see `step-functions`
