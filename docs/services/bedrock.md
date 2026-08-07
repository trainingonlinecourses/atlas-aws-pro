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

## Next steps

- **Bedrock Agents** (Use these models as their brain.) — see `bedrock-agents`
- **S3** (Knowledge-base documents.) — see `s3`
- **Lambda / API Gateway** (Typical invocation paths.) — see `lambda---api-gateway`
- **CloudWatch** (Invocation metrics & logging.) — see `cloudwatch`
