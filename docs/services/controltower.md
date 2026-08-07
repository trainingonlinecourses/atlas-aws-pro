# 🗼 AWS Control Tower (`controltower`)

> Landing zone as code — guardrails, account vending, baseline security.

- **Category:** Security, Identity & Compliance
- **Service id:** `controltower`

## Why it exists
Control Tower stands up the multi-account baseline (logging, audit, shared network) and enforces guardrails — the enterprise starting line.

## When to use it
Greenfield landing zones, account vending machines, detective/preventive guardrails.

## Learn first

- Landing zone vs guardrails (controls)
- Account Factory
- Mandatory vs strongly-recommended controls
- Home Region concept

## Terraform
```hcl
resource "aws_controltower_landing_zone" "lz" {
  manifest_json = file("landing-zone-manifest.json")
}

# Example guardrail on a workload OU:
resource "aws_controltower_control" "no_root" {
  target_identifier = aws_organizations_ou.workloads.arn
  control_identifier = "arn:aws:controltower:us-east-1::control/AWS-GR_RESTRICT_ROOT_USER"
}
```

## AWS CDK
```ts
import * as controltower from "aws-cdk-lib/aws-controltower";
new controltower.CfnLandingZone(this, "LZ", {
  manifest: JSON.parse(fs.readFileSync("manifest.json", "utf8")),
});
```

## Boto3 (Python)
```python
import boto3
ct = boto3.client("controltower", region_name="us-east-1")
for lz in ct.list_landing_zones()["landingZones"]:
    print(ct.get_landing_zone(landingZoneIdentifier=lz)["landingZone"]["status"])
```

## Delete / teardown
```python
ct.delete_landing_zone(landingZoneIdentifier=lzid)  # rare — usually you evolve it
```

## Expert tips

- Adopt Control Tower BEFORE you have 20 accounts, not after.
- Guardrails beat tribal knowledge — they enforce policy automatically.

## Real-world example

**Global enterprises** — Every new team gets a compliant account in minutes via Account Factory.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, AWS Control Tower is configured but audited: the same controls as prod exist, just scoped to dev accounts.

- Create the service with least-privilege and a dev-only boundary, not admin-by-default.
- Store any keys/secrets in a secrets manager, never in code or env files.
- Enable basic logging so dev behavior is visible and reproducible.

### 🧪 Staging / Pre-prod

Staging is where AWS Control Tower is exercised against realistic policies and evidence starts being collected.

- Run the same Config/Security Hub rules as prod and fix findings before release.
- Test rotation and break-glass access paths here, where mistakes are recoverable.
- Scan the artifact (image/code/package) the same way prod will be scanned.

### 🚀 Production

In production AWS Control Tower is hardened, monitored, and evidence-producing for auditors.

- Enforce least privilege with permission boundaries; audit access with Access Analyzer.
- Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.
- Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.

### 🌍 Multi-region / DR

DR for AWS Control Tower means the control plane answers in the backup region too — logging, KMS, and IAM included.

- Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.
- Test that privileged access, rotation, and alerts all function in the backup region.
- Include the security stack in the DR runbook, not just the workloads.

### ♻️ Lifecycle & IaC

Lifecycle keeps AWS Control Tower continuously compliant: policies as code, rotation automated, findings tracked.

- Define policies (IAM/SCP) in Terraform and review them like application code.
- Automate secret rotation and never let a static key outlive a quarter.
- Close the loop: every security finding becomes a tracked issue with an owner.

## Next steps

- **Organizations** (The substrate Control Tower manages.) — see `organizations`
- **CloudTrail / Config** (Centralized logging accounts.) — see `cloudtrail---config`
- **IAM Identity Center** (Identity baseline.) — see `iam-identity-center`
