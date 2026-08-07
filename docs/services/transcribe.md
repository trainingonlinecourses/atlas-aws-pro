# 🎙️ Amazon Transcribe (`transcribe`)

> Speech-to-text at scale — calls, meetings, media archives.

- **Category:** Machine Learning & AI
- **Service id:** `transcribe`
- **AI-enabled:** yes

## Why it exists
Audio is dark data. Transcribe turns calls and videos into searchable text with speaker labels.

## When to use it
Contact-center analytics, captioning, meeting notes.

## Learn first

- Batch vs streaming jobs
- Speaker diarization
- Custom vocabularies

## Terraform
```hcl
# Per-call AI service — no infrastructure to provision.
resource "aws_iam_policy" "transcribe_use" {
  name = "transcribe-jobs"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["transcribe:StartTranscriptionJob", "transcribe:GetTranscriptionJob"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
new iam.ManagedPolicy(this, "TranscribeJobs", {
  statements: [new iam.PolicyStatement({
    actions: ["transcribe:StartTranscriptionJob", "transcribe:GetTranscriptionJob"],
    resources: ["*"],
  })],
});
```

## Boto3 (Python)
```python
import boto3
tr = boto3.client("transcribe", region_name="us-east-1")
tr.start_transcription_job(
    TranscriptionJobName="call-2026-08-05",
    Media={"MediaFileUri": "s3://acme-audio/calls/1042.mp3"},
    MediaFormat="mp3", LanguageCode="en-US",
    Settings={"ShowSpeakerLabel": True})
print("job started")
```

## Delete / teardown
```python
tr.delete_transcription_job(TranscriptionJobName="call-2026-08-05")
```

## Expert tips

- Custom vocabularies fix product-name hallucinations.
- Chain into Comprehend for per-speaker sentiment.

## Real-world example

**Contact centers** — Transcribe 100% of calls, then Comprehend scores sentiment.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Transcribe runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Transcribe against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Transcribe is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Transcribe is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **S3** (Audio in, transcripts out.) — see `s3`
- **Comprehend** (Sentiment over transcripts.) — see `comprehend`
- **Kinesis** (Streaming for live calls.) — see `kinesis`
