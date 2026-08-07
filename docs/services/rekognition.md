# 📸 Amazon Rekognition (`rekognition`)

> Vision as an API call: labels, faces, moderation, text in images & video.

- **Category:** Machine Learning & AI
- **Service id:** `rekognition`
- **AI-enabled:** yes

## Why it exists
Building CV in-house takes a team. One API call returns what's in an image.

## When to use it
Media tagging, content moderation, identity flows, visual search.

## Learn first

- Image vs video operations
- Confidence thresholds
- Moderation taxonomies

## Terraform
```hcl
# Per-call AI service — no infrastructure to provision.
resource "aws_iam_policy" "rekognition_read" {
  name = "rekognition-detect"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["rekognition:DetectLabels", "rekognition:DetectModerationLabels"]
      Resource = "*"
    }]
  })
}
```

## AWS CDK
```ts
new iam.ManagedPolicy(this, "RekognitionDetect", {
  statements: [new iam.PolicyStatement({
    actions: ["rekognition:DetectLabels", "rekognition:DetectModerationLabels"],
    resources: ["*"],
  })],
});
```

## Boto3 (Python)
```python
import boto3
rek = boto3.client("rekognition", region_name="us-east-1")
resp = rek.detect_labels(Image={"S3Object": {
    "Bucket": "acme-assets-prod", "Name": "beach.jpg"}})
print([(l["Name"], round(l["Confidence"], 1)) for l in resp["Labels"][:5]])
```

## Delete / teardown
```python
# Nothing to delete — Rekognition bills per call. Clean up S3 + IAM.
```

## Expert tips

- Tune thresholds per use case; 90% confidence ≠ universal.
- Video jobs are async — poll or use SNS completion.

## Real-world example

**Media companies** — Auto-tag millions of archive photos so editors can search 'sunset, stadium'.

## Next steps

- **S3** (Images come from buckets.) — see `s3`
- **Lambda** (Upload-triggered tagging.) — see `lambda`
- **Textract / Comprehend** (Siblings for text & language.) — see `textract---comprehend`
