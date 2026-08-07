# 🪜 AWS Step Functions (`stepfunctions`)

> Visual state machines — orchestrate Lambdas, jobs and humans with retries.

- **Category:** Application Integration
- **Service id:** `stepfunctions`

## Why it exists
Chaining Lambdas with queues gets unmaintainable. Step Functions gives a visible workflow: retries, catch, parallel.

## When to use it
Order workflows, ML pipelines (MLOps), long-running jobs.

## Learn first

- Amazon States Language
- Task/Choice/Parallel/Wait states
- Retry & Catch
- Standard vs Express

## Terraform
```hcl
resource "aws_sfn_state_machine" "order_flow" {
  name = "order-flow"
  role_arn = aws_iam_role.sfn.arn
  definition = jsonencode({
    StartAt = "Charge"
    States = {
      Charge = {
        Type = "Task"
        Resource = aws_lambda_function.charge.arn
        Next = "Reserve"
        Retry = [{ ErrorEquals = ["States.ALL"], MaxAttempts = 3 }]
      }
      Reserve = { Type = "Task", Resource = aws_lambda_function.reserve.arn, End = true }
    }
  })
}
```

## AWS CDK
```ts
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";
const charge  = new tasks.LambdaInvoke(this, "Charge", { lambdaFunction: chargeFn });
const reserve = new tasks.LambdaInvoke(this, "Reserve", { lambdaFunction: reserveFn });
new sfn.StateMachine(this, "OrderFlow", {
  definitionBody: sfn.DefinitionBody.fromChainable(charge.next(reserve)),
});
```

## Boto3 (Python)
```python
import boto3, json
sfn = boto3.client("stepfunctions", region_name="us-east-1")
ex = sfn.start_execution(
    stateMachineArn="arn:aws:states:us-east-1:123456789012:stateMachine:order-flow",
    input=json.dumps({"order_id": "A-1042"}))
print(ex["executionArn"])
```

## Delete / teardown
```python
sfn.delete_state_machine(stateMachineArn=arn)
```

## Expert tips

- Express = cheap/high-rate; Standard = auditable/long-running.
- The execution history IS your audit log.

## Real-world example

**Order platforms** — Charge → reserve → ship with retries, catch blocks and full execution history.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Step Functions is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where AWS Step Functions is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production AWS Step Functions is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for AWS Step Functions is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats AWS Step Functions as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **Lambda / ECS / SageMaker** (Any service can be a state.) — see `lambda---ecs---sagemaker`
- **SageMaker Pipelines** (Built on Step Functions.) — see `sagemaker-pipelines`
