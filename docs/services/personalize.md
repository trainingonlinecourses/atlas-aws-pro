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

## Next steps

- **Pinpoint** (Deliver personalized emails.) — see `pinpoint`
- **Kinesis** (Stream interaction events in.) — see `kinesis`
