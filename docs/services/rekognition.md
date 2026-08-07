# 📸 Amazon Rekognition (`rekognition`)

> Vision as an API call: labels, faces, moderation, text in images & video.

- **Category:** Machine Learning & AI
- **Service id:** `rekognition`
- **AI-enabled:** yes

## Why it exists
Building CV in-house takes a team. One API call returns what's in an image.

## When to use it
Media tagging, content moderation, identity flows, visual search.

## Learn first

- Image vs video operations
- Confidence thresholds
- Moderation taxonomies

## Terraform
```hcl
# Per-call AI service — no infrastructure to provision.
resource "aws_iam_policy" "rekognition_read" {
  name = "rekognition-detect"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["rekognition:DetectLabels", "rekognition:DetectModerationLabels"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
new iam.ManagedPolicy(this, "RekognitionDetect", {
  statements: [new iam.PolicyStatement({
    actions: ["rekognition:DetectLabels", "rekognition:DetectModerationLabels"],
    resources: ["*"],
  })],
});
```

## Boto3 (Python)
```python
import boto3
rek = boto3.client("rekognition", region_name="us-east-1")
resp = rek.detect_labels(Image={"S3Object": {
    "Bucket": "acme-assets-prod", "Name": "beach.jpg"}})
print([(l["Name"], round(l["Confidence"], 1)) for l in resp["Labels"][:5]])
```

## Delete / teardown
```python
# Nothing to delete — Rekognition bills per call. Clean up S3 + IAM.
```

## Expert tips

- Tune thresholds per use case; 90% confidence ≠ universal.
- Video jobs are async — poll or use SNS completion.

## Real-world example

**Media companies** — Auto-tag millions of archive photos so editors can search 'sunset, stadium'.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Rekognition runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Rekognition against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Rekognition is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Rekognition is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **S3** (Images come from buckets.) — see `s3`
- **Lambda** (Upload-triggered tagging.) — see `lambda`
- **Textract / Comprehend** (Siblings for text & language.) — see `textract---comprehend`
