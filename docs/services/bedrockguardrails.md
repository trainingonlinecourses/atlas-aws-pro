# 🚧 Amazon Bedrock Guardrails (`bedrockguardrails`)

> Policy rails for GenAI — block toxic, off-topic and PII-leaking traffic.

- **Category:** Machine Learning & AI
- **Service id:** `bedrockguardrails`
- **AI-enabled:** yes

## Why it exists
Production GenAI needs rails: denied topics, content filters, PII redaction.

## When to use it
Input/output filtering, PII masking, topic denial, hallucination checks.

## Learn first

- Content filters & strengths
- Denied topics & word filters
- PII: mask vs block
- ApplyGuardrail API & versions

## Terraform
```hcl
resource "aws_bedrock_guardrail" "rails" {
  name = "prod-rails"
  blocked_input_messaging = "Sorry, I can't help with that."
  blocked_outputs_messaging = "I can't share that information."
  content_policy_config {
    filters_config { type = "HATE"; input_strength = "HIGH"; output_strength = "HIGH" }
    filters_config { type = "VIOLENCE"; input_strength = "HIGH"; output_strength = "HIGH" }
  }
  sensitive_information_policy_config {
    pii_entity_config { action = "BLOCK"; type = "EMAIL" }
  }
}
```

## AWS CDK
```ts
import * as bedrock from "aws-cdk-lib/aws-bedrock";
new bedrock.CfnGuardrail(this, "Rails", {
  name: "prod-rails",
  blockedInputMessaging: "Sorry, I can't help with that.",
  blockedOutputsMessaging: "I can't share that information.",
  contentPolicyConfig: { filtersConfig: [
    { type: "HATE", inputStrength: "HIGH", outputStrength: "HIGH" },
    { type: "VIOLENCE", inputStrength: "HIGH", outputStrength: "HIGH" },
  ]},
});
```

## Boto3 (Python)
```python
import boto3
br = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = br.apply_guardrail(
    guardrailIdentifier="arn:aws:bedrock:us-east-1:123:guardrail/rails",
    guardrailVersion="DRAFT", source="INPUT",
    content=[{"text": {"text": "email me at jane@example.com"}}])
print(resp["action"], resp.get("assessments"))
```

## Delete / teardown
```python
boto3.client("bedrock").delete_guardrail(guardrailIdentifier="arn:...")
```

## Expert tips

- Version guardrails like code; audit block metrics weekly.
- Denied topics beat prompt tricks — declare what you won't discuss.

## Real-world example

**AgentOps** — Every agent turn runs through a guardrail; blocked attempts show up in CloudWatch.

## Next steps

- **Bedrock models & Agents** (Attach guardrails at invoke time.) — see `bedrock-models-&-agents`
- **CloudWatch** (Block metrics feed AgentOps dashboards.) — see `cloudwatch`
