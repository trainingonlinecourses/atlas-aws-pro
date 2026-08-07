# 🔊 Amazon Polly (`polly`)

> Text-to-speech API — turn content into natural, human-like voices.

- **Category:** Machine Learning & AI
- **Service id:** `polly`
- **AI-enabled:** yes

## Why it exists
Reading content aloud (accessibility, podcasts, IVR) shouldn't need a studio. Polly synthesizes speech in dozens of voices/languages.

## When to use it
Accessibility readers, audiobooks, IVR prompts, voice assistants.

## Learn first

- Standard vs Neural voices
- SSML markup
- Output formats (mp3/ogg)
- Synthesis jobs

## Terraform
```hcl
# Per-call AI service — manage the invoke permission:
resource "aws_iam_policy" "polly_speak" {
  name = "polly-speak"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["polly:SynthesizeSpeech"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
new iam.ManagedPolicy(this, "PollySpeak", {
  statements: [new iam.PolicyStatement({
    actions: ["polly:SynthesizeSpeech"], resources: ["*"],
  })],
});
```

## Boto3 (Python)
```python
import boto3
pol = boto3.client("polly", region_name="us-east-1")
resp = pol.synthesize_speech(Text="Your order has shipped.",
    OutputFormat="mp3", VoiceId="Joanna", Engine="neural")
open("ship.mp3", "wb").write(resp["AudioStream"].read())
```

## Delete / teardown
```python
# Per-call service — nothing to delete. Clean up generated audio + IAM.
```

## Expert tips

- Neural voices cost more but sound dramatically better.
- Use SSML breaks (<break/>) for natural pacing.

## Real-world example

**Publishers** — Auto-narrate daily articles for commuter listening.

## Next steps

- **S3** (Store generated audio.) — see `s3`
- **Transcribe** (The reverse direction — speech to text.) — see `transcribe`
- **Lex** (Voice input for chatbots.) — see `lex`
