# 🕵️ Amazon Detective (`detective`)

> Graph-based investigation of suspicious activity. Walk the blast radius of a GuardDuty finding.

- **Category:** Security, Identity & Compliance
- **Service id:** `detective`

## Why it exists
A GuardDuty alert says something happened — not who or how. Detective builds a resource graph so you trace related API calls and entities in one view.

## When to use it
Incident investigation, root-cause on findings, forensics.

## Learn first

- Graph: entities, IPs, roles
- Linked GuardDuty findings
- Investigation timelines
- Findings → entity graphs

## Terraform
```hcl
resource "aws_detective_graph" "soc" {}
resource "aws_detective_member" "child" {
  account_id = "123456789012"
  graph_arn  = aws_detective_graph.soc.id
}
```

## AWS CDK
```ts
// L1 only — CfnGraph.
```

## Boto3 (Python)
```python
import boto3
det = boto3.client("detective", region_name="us-east-1")
graphs = det.list_graphs()["GraphList"]
resp = det.get_graph(GraphArn=graphs[0]["Arn"])
print(resp["GraphArn"])
```

## Delete / teardown
```python
# Remove members, then delete the graph.
```

## Expert tips

- Enable Detective before the incident — it ingests ~2 weeks of history.
- Pair with GuardDuty + Security Hub for the full SOC loop.

## Real-world example

**Security teams** — Cutting MTTR from hours to minutes by tracing a finding to its source.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Detective is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where Amazon Detective is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production Amazon Detective is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for Amazon Detective means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps Amazon Detective continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **GuardDuty** (Feeds the findings.) — see `guardduty`
- **Security Hub** (Aggregates alerts.) — see `security-hub`
- **CloudTrail** (API call evidence.) — see `cloudtrail`
