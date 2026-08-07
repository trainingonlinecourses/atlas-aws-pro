# 📈 Amazon Forecast (`forecast`)

> Time-series forecasting with ML — demand, staffing, capacity — without building models.

- **Category:** Machine Learning & AI
- **Service id:** `forecast`
- **AI-enabled:** yes

## Why it exists
Forecasting is a solved problem when you have clean data and the right library. Forecast automates model selection and tuning behind the scenes.

## When to use it
Demand planning, staffing, inventory, energy-load forecasting.

## Learn first

- Dataset groups & time series
- Predictors (models)
- What-if scenarios
- Accuracy metrics

## Terraform
```hcl
resource "aws_forecast_dataset_group" "demand" {
  dataset_group_name = "demand"
  domain             = "RETAIL"
}
```

## AWS CDK
```ts
// No first-class CDK construct (L1 only) — manage with Terraform.
```

## Boto3 (Python)
```python
import boto3
fc = boto3.client("forecast", region_name="us-east-1")
for p in fc.list_predictors()["Predictors"]:
    print(p["PredictorArn"], p["Status"])
```

## Delete / teardown
```python
fc.delete_forecast(ForecastArn="...")
fc.delete_predictor(PredictorArn="...")
```

## Expert tips

- Historical-data quality beats fancy models — clean the spikes first.
- Backtest before trusting a forecast; pick the right horizon.

## Real-world example

**Retailers** — Demand planning across thousands of SKUs.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Amazon Forecast runs on small data and a notebo0k loop, but with the model and eval tracked from the start.

- Use a dev dataset and keep every experiment logged (data, code, metrics).
- Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.
- Write a small eval set (golden questions) before you write the fancy prompt.

### 🧪 Staging / Pre-prod

Staging validates Amazon Forecast against the eval harness and a shadow deployment before real traffic.

- Run the golden eval set and require it to pass a quality gate in CI.
- Shadow-deploy the candidate while the current model serves, and compare outputs.
- Check drift baselines (data and model quality) against staging signals.

### 🚀 Production

In production Amazon Forecast is governed: versioned, guarded, monitored for drift, and rollback-ready.

- Serve a pinned, registered model version behind a stable alias for instant rollback.
- Enable guardrails, content filters, and PII controls on any generative surface.
- Monitor drift + latency + token spend and alert on any regression.

### 🌍 Multi-region / DR

DR for Amazon Forecast is the ability to re-serve the model in a second region and roll back a bad version.

- Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.
- Keep the previous known-good alias deployable in seconds.
- Drill a rollback and a region promotion annually — models rot like everything else.

### ♻️ Lifecycle & IaC

Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.

- Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.
- Log every inference with trace + source so you can audit what the model said and why.
- Close the loop: production feedback becomes new eval cases for the next retrain.

## Next steps

- **Personalize** (The recommendation cousin.) — see `personalize`
- **QuickSight** (Plot forecast vs actual.) — see `quicksight`
