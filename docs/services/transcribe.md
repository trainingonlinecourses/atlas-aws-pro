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

## Next steps

- **S3** (Audio in, transcripts out.) — see `s3`
- **Comprehend** (Sentiment over transcripts.) — see `comprehend`
- **Kinesis** (Streaming for live calls.) — see `kinesis`
