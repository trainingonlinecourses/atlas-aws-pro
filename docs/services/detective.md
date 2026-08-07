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

## Next steps

- **GuardDuty** (Feeds the findings.) — see `guardduty`
- **Security Hub** (Aggregates alerts.) — see `security-hub`
- **CloudTrail** (API call evidence.) — see `cloudtrail`
