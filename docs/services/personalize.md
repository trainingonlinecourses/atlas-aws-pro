# 🎯 Amazon Personalize (`personalize`)

> ML-based recommendations — 'customers also bought' — without a data-science team.

- **Category:** Machine Learning & AI
- **Service id:** `personalize`
- **AI-enabled:** yes

## Why it exists
Recommendation engines are table stakes for ecommerce but hard to build. Personalize trains models on your users' interactions and serves ranked recommendations via API.

## When to use it
Product recommendations, content ranking, personalized emails.

## Learn first

- Interaction datasets (views, clicks, purchases)
- Solutions & campaigns
- Recipes (HRNN, SIMS, etc.)
- Real-time vs batch recommendations

## Terraform
```hcl
# Personalize support in the AWS TF provider is still maturing.
# Model: dataset-group -> dataset -> solution -> campaign.
```

## AWS CDK
```ts
// No first-class CDK construct (L1 only) — manage via the console or SDK.
```

## Boto3 (Python)
```python
import boto3
pr = boto3.client("personalize-runtime", region_name="us-east-1")
resp = pr.get_recommendations(campaignArn="arn:aws:personalize:...:campaign/demo",
    userId="user-42")
for item in resp["itemList"][:5]: print(item["itemId"])
```

## Delete / teardown
```python
# Delete campaign, then solution, then datasets, then the group.
```

## Expert tips

- You need a steady stream of interaction events — no data, no personalization.
- Start with the SIMS recipe for 'related items', HRNN for user recommendations.

## Real-world example

**E-commerce** — 10-30% click-through lifts from personalized feeds.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Personalize runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Personalize against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Personalize is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Personalize is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Pinpoint** (Deliver personalized emails.) — see `pinpoint`
- **Kinesis** (Stream interaction events in.) — see `kinesis`
