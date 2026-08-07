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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Polly runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Polly against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Polly is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Polly is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **S3** (Store generated audio.) — see `s3`
- **Transcribe** (The reverse direction — speech to text.) — see `transcribe`
- **Lex** (Voice input for chatbots.) — see `lex`
