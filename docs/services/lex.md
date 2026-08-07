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

## Next steps

- **Cognito** (Auth for web chat widgets.) — see `cognito`
- **Lambda** (Fulfillment logic per intent.) — see `lambda`
- **Bedrock** (Hybrid: Lex routes, LLMs elaborate.) — see `bedrock`
