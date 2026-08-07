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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Bedrock Guardrails runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Bedrock Guardrails against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Bedrock Guardrails is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Bedrock Guardrails is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Bedrock models & Agents** (Attach guardrails at invoke time.) — see `bedrock-models-&-agents`
- **CloudWatch** (Block metrics feed AgentOps dashboards.) — see `cloudwatch`
