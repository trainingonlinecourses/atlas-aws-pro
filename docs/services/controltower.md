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

## Next steps

- **Organizations** (The substrate Control Tower manages.) — see `organizations`
- **CloudTrail / Config** (Centralized logging accounts.) — see `cloudtrail---config`
- **IAM Identity Center** (Identity baseline.) — see `iam-identity-center`
