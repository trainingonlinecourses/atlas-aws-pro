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

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Connect is a thin pipe: small queues/topics, short retention, and obvious test producers.

- Use a dev-only queue/topic name so dev and prod never cross-deliver.
- Seed the message shape from the schema so consumers fail loudly on changes.
- Clear the dev queue nightly so stale messages don't linger.

### 🧪 Staging / Pre-prod

Staging is where Amazon Connect is load-tested and failure paths (DLQ, redrive, retry) are proven.

- Inject a poison message and confirm it lands on the DLQ with a redrive policy.
- Load-test consumer throughput and back-pressure before prod traffic hits.
- Verify exactly-once/idempotency behavior against staging consumers.

### 🚀 Production

In production Amazon Connect is the reliability backbone: DLQs configured, retries bounded, lag monitored.

- Configure a DLQ with a max-receive count so poisoned messages can't loop forever.
- Monitor age of oldest message and DLQ depth; page the owning team on lag.
- Keep consumers idempotent so retries never double-apply.

### 🌍 Multi-region / DR

DR for Amazon Connect is an alternate path in a second region or account, with a defined loss tolerance.

- Replicate the queue/topic policy and consumer config to the DR region.
- Accept or mitigate the RPO: messages produced during a regional failure are the decision.
- Test that consumers can drain the DR path and reconcile afterwards.

### ♻️ Lifecycle & IaC

Lifecycle treats Amazon Connect as code: schemas versioned, topics registered, consumers owned.

- Manage queues/topics and their policies in Terraform, with the schema in a registry.
- Keep a subscriber manifest so every new consumer is reviewed, not silently added.
- Alert on delivery failures and prune unused topics to cut noise and cost.

## Next steps

- **Lex** (Voice bots for self-service.) — see `lex`
- **Lambda** (Custom flow logic.) — see `lambda`
- **QuickSight** (Live contact analytics.) — see `quicksight`
