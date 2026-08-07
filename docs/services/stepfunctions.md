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

## Next steps

- **Lambda / ECS / SageMaker** (Any service can be a state.) — see `lambda---ecs---sagemaker`
- **SageMaker Pipelines** (Built on Step Functions.) — see `sagemaker-pipelines`
