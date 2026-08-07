# 🦾 Agents for Amazon Bedrock (`bedrockagents`)

> Give an LLM tools, knowledge and memory — and ship it with AgentOps.

- **Category:** Machine Learning & AI
- **Service id:** `bedrockagents`
- **AI-enabled:** yes

## Why it exists
Chatbots answer; agents act. An agent plans, calls your APIs (action groups), queries your KB and reports every step.

## When to use it
Support copilots, ops assistants, agentic RAG, task automation.

## Learn first

- Agents, aliases (DRAFT/PROD)
- Action groups = tools (schema → Lambda)
- Knowledge bases for RAG
- Traces + CloudWatch = AgentOps

## Terraform
```hcl
resource "aws_bedrockagent_agent" "loan_support" {
  agent_name = "loan-support"
  foundation_model = "anthropic.claude-3-haiku-20240307-v1:0"
  agent_resource_role_arn = aws_iam_role.agent.arn
  instruction = "Answer loan-status questions using the knowledge base. Escalate refunds to a human."
}

resource "aws_bedrockagent_agent_action_group" "status" {
  agent_id = aws_bedrockagent_agent.loan_support.id
  agent_version = "DRAFT"
  action_group_name = "check-status"
  action_group_executor { lambda = aws_lambda_function.loan_status.arn }
  function_schema {
    member {
      name = "check_loan_status"
      type = "string"
      description = "Returns the status of a loan application"
      parameter { name = "application_id"; type = "string"; required = true }
    }
  }
}
```

## AWS CDK
```ts
import * as bedrockagent from "aws-cdk-lib/aws-bedrockagent";
const agent = new bedrockagent.CfnAgent(this, "LoanSupport", {
  agentName: "loan-support",
  foundationModel: "anthropic.claude-3-haiku-20240307-v1:0",
  agentResourceRoleArn: agentRole.roleArn,
  instruction: "Answer loan-status questions using the knowledge base.",
});
new bedrockagent.CfnAgentActionGroup(this, "Status", {
  agentId: agent.attrAgentId, agentVersion: "DRAFT",
  actionGroupName: "check-status",
  actionGroupExecutor: { lambda: statusFn.functionArn },
});
```

## Boto3 (Python)
```python
import boto3
agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
resp = agent.invoke_agent(agentId="AGENT123", agentAliasId="ALIAS1",
    sessionId="s-001",
    inputText="What is the status of my loan application LA-9901?")
for chunk in resp["completion"]:
    print(chunk["chunk"]["bytes"].decode(), end="")
```

## Delete / teardown
```python
boto3.client("bedrock-agent").delete_agent(agentId="AGENT123")
```

## Expert tips

- Promote via ALIASES — never point prod at DRAFT.
- Keep an evaluation dataset; re-run it before every promotion.

## Real-world example

**AgentOps in practice** — A lender's agent answers status questions via internal APIs — every trace lands in CloudWatch.

## Next steps

- **Bedrock** (The model doing the reasoning.) — see `bedrock`
- **Lambda** (Action-group executors.) — see `lambda`
- **Bedrock KB** (Grounds answers in your docs.) — see `bedrock-kb`
- **CloudWatch** (The AgentOps observability layer.) — see `cloudwatch`
