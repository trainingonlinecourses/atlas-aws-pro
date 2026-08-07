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

## Next steps

- **S3** (Training data in, artifacts out.) — see `s3`
- **ECR** (Custom training containers.) — see `ecr`
- **Step Functions** (Orchestrates retraining.) — see `step-functions`
- **CloudWatch** (Drift alarms on endpoints.) — see `cloudwatch`
