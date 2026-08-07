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

## Next steps

- **Personalize** (The recommendation cousin.) — see `personalize`
- **QuickSight** (Plot forecast vs actual.) — see `quicksight`
