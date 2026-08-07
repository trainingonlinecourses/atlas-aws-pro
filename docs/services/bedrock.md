# 🪨 Amazon Bedrock (`bedrock`)

> Foundation models via one API — Claude, Nova & friends, no GPUs to babysit.

- **Category:** Machine Learning & AI
- **Service id:** `bedrock`
- **AI-enabled:** yes

## Why it exists
You want LLM features without GPU fleets. Bedrock serves top foundation models behind a single API.

## When to use it
Chat & copilots, summarization, RAG, embeddings, agent reasoning.

## Learn first

- Model families & IDs
- InvokeModel vs streaming
- Prompting & context windows
- Guardrails & knowledge bases

## Terraform
```hcl
# Models are enabled per region (console/org policy);
# Terraform mostly manages the IAM around Bedrock:
resource "aws_iam_policy" "bedrock_invoke" {
  name = "bedrock-invoke"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
import * as iam from "aws-cdk-lib/aws-iam";
const invoke = new iam.ManagedPolicy(this, "BedrockInvoke", {
  statements: [new iam.PolicyStatement({
    actions: ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
    resources: ["*"],
  })],
});
appRole.addManagedPolicy(invoke);
```

## Boto3 (Python)
```python
import boto3, json
br = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = br.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "messages": [{"role": "user",
                      "content": "Explain VPC peering in one sentence."}]}))
print(json.loads(resp["body"].read())["content"][0]["text"])
```

## Delete / teardown
```python
# Serverless: nothing to delete. For extras:
# bedrock.delete_guardrail(guardrailIdentifier=...)
```

## Expert tips

- Use the Converse API for multi-turn; it standardizes across models.
- Stream long answers — first-token latency is UX.

## Real-world example

**Lonely Planet** — Built an AI trip-planning assistant on Bedrock without managing GPUs.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Bedrock runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Bedrock against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Bedrock is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Bedrock is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Bedrock Agents** (Use these models as their brain.) — see `bedrock-agents`
- **S3** (Knowledge-base documents.) — see `s3`
- **Lambda / API Gateway** (Typical invocation paths.) — see `lambda---api-gateway`
- **CloudWatch** (Invocation metrics & logging.) — see `cloudwatch`
