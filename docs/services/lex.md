# 🗨️ Amazon Lex (`lex`)

> Managed conversational bots — the engine behind Alexa-style dialog.

- **Category:** Machine Learning & AI
- **Service id:** `lex`
- **AI-enabled:** yes

## Why it exists
Building intent recognition and slot filling from scratch is years of work. Lex gives you ASR + NLU as an API.

## When to use it
Chatbots, voice IVRs, form-like dialogs over chat.

## Learn first

- Intents, slots, utterances
- Dialog flow & confirmations
- Channels (web, Slack, Connect)
- Lex v2 bots & aliases

## Terraform
```hcl
resource "aws_lexv2models_bot" "faq" {
  name = "faq-bot"
  role_arn = aws_iam_role.lex.arn
  data_privacy { child_directed = false }
  idle_session_ttl_in_seconds = 300
}
```

## AWS CDK
```ts
import * as lex from "aws-cdk-lib/aws-lex";
new lex.CfnBot(this, "Faq", {
  name: "faq-bot",
  roleArn: lexRole.roleArn,
  dataPrivacy: { childDirected: false },
  idleSessionTTLInSeconds: 300,
});
```

## Boto3 (Python)
```python
import boto3
lex = boto3.client("lexv2-runtime", region_name="us-east-1")
resp = lex.recognize_text(botId="BOT123", botAliasId="ALIAS1",
    localeId="en_US", sessionId="s1", text="Where is my order?")
print(resp["messages"][0]["content"])
```

## Delete / teardown
```python
boto3.client("lexv2-models").delete_bot(id="BOT123")
```

## Expert tips

- Start with 3 tight intents; expand after real transcripts.
- Pair with Bedrock for open-ended questions, Lex for structured flows.

## Real-world example

**Retail support** — Deflects 60% of 'where is my order?' chats before a human.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Lex runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Lex against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Lex is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Lex is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Cognito** (Auth for web chat widgets.) — see `cognito`
- **Lambda** (Fulfillment logic per intent.) — see `lambda`
- **Bedrock** (Hybrid: Lex routes, LLMs elaborate.) — see `bedrock`
