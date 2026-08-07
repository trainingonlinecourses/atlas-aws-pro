# 📞 Amazon Connect (`connect`)

> Cloud contact center — IVR, queues, agent desktops, analytics. Pay per minute.

- **Category:** Application Integration
- **Service id:** `connect`

## Why it exists
Building a call center means PBX, IVR, CTI, and reporting. Connect replaces that hardware with a managed service wired to Lambda and Lex.

## When to use it
Customer support, IVR flows, agent routing, voice analytics.

## Learn first

- Contact flows = the IVR
- Queues & routing profiles
- Lambda integration
- Contact Lens analytics

## Terraform
```hcl
resource "aws_connect_instance" "cc" {
  identity_management_type = "CONNECT_MANAGED"
  inbound_calls_enabled    = true
  outbound_calls_enabled   = true
}
resource "aws_connect_queue" "support" {
  instance_id = aws_connect_instance.cc.id
  name        = "support"
  hours_of_operation_id = aws_connect_hours_of_operation.work.id
}
```

## AWS CDK
```ts
// L1 only — CfnInstance + CfnQueue.
```

## Boto3 (Python)
```python
import boto3
con = boto3.client("connect", region_name="us-east-1")
con.start_outbound_voice_contact(
    DestinationPhoneNumber="+15551234567",
    ContactFlowId="arn:aws:connect:...:contact-flow/main",
    InstanceId="arn:aws:connect:...:instance/cc")
```

## Delete / teardown
```python
# Delete queues, flows, then the instance.
```

## Expert tips

- Contact Lens transcribes + scores every call — turn it on before auditors ask.
- Test flows with the softphone simulator before cutting over.

## Real-world example

**Contact centers** — Cut telephony costs ~60% while adding AI-powered call scoring.

## Next steps

- **Lex** (Voice bots for self-service.) — see `lex`
- **Lambda** (Custom flow logic.) — see `lambda`
- **QuickSight** (Live contact analytics.) — see `quicksight`
