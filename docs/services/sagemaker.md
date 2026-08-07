# 🤖 Amazon SageMaker (`sagemaker`)

> The full ML workshop: notebooks, training jobs, registries, endpoints.

- **Category:** Machine Learning & AI
- **Service id:** `sagemaker`
- **AI-enabled:** yes

## Why it exists
Training on laptops doesn't reach production. SageMaker covers prepare → train → version → deploy → monitor.

## When to use it
Custom model training, notebooks, real-time & batch inference, MLOps.

## Learn first

- Notebooks → training → endpoints
- Built-in algos vs custom containers
- Model registry
- Blue/green endpoints

## Terraform
```hcl
resource "aws_sagemaker_notebook_instance" "lab" {
  name = "lab-notebook"
  role_arn = aws_iam_role.sagemaker.arn
  instance_type = "ml.t3.medium"
  direct_internet_access = "Disabled"
}
# Prod: aws_sagemaker_model -> endpoint_configuration -> endpoint
```

## AWS CDK
```ts
import * as sagemaker from "aws-cdk-lib/aws-sagemaker";
new sagemaker.CfnNotebookInstance(this, "Lab", {
  instanceType: "ml.t3.medium",
  roleArn: smRole.roleArn,
  directInternetAccess: "Disabled",
});
// prod: CfnModel -> CfnEndpointConfig -> CfnEndpoint (blue/green)
```

## Boto3 (Python)
```python
# pip install sagemaker
import sagemaker
from sagemaker.estimator import Estimator
est = Estimator(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/xgboost:1.7-1",
    role=sagemaker.get_execution_role(),
    instance_count=2, instance_type="ml.m5.xlarge",
    output_path="s3://acme-ml/models")
est.fit({"train": "s3://acme-ml/train"})
```

## Delete / teardown
```python
import boto3
boto3.client("sagemaker").delete_endpoint(EndpointName="churn-v2")
```

## Expert tips

- Endpoints bill while idle — delete lab endpoints nightly.
- Version everything: data, code, model artifacts.

## Real-world example

**Formula 1** — Built the live pit-strategy predictions you see on broadcasts.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon SageMaker runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon SageMaker against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon SageMaker is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon SageMaker is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **S3** (Training data in, artifacts out.) — see `s3`
- **ECR** (Custom training containers.) — see `ecr`
- **Step Functions** (Orchestrates retraining.) — see `step-functions`
- **CloudWatch** (Drift alarms on endpoints.) — see `cloudwatch`
