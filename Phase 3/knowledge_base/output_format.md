# Report structure (always keep this order):
Forecast Summary
Feature Interpretation
Historical Trend Overview
Market Context
Confidence
Model Limitations

---

# Detailed output format

## Forecast Summary

Predicted volatility: analysis_output['prediction']['predicted_volatility'] ('higher' or 'lower' based on analysis_output['prediction']['forecast_relativity'])
(Provide interpretation here, based on analysis_output['prediction']['forecast_relativity']. Refer to ./interpretation_rules.md for each condition.)

Volatility regime: analysis_output['prediction']['volatility_regime'] (Provide interpretation here, enclosed by brackets. Refer to ./interpretation_rules.md for each condition.)

Risk level: analysis_output['prediction']['risk_level'] (Provide interpretation here, enclosed by brackets. Refer to ./interpretation_rules.md for each condition.)

## Feature Interpretation

(Provide brief explanation by adhering to the guideline ./interpretation_rules.md)

## Historical Trend Overview

Monthly average volatility: analysis_output['historical_analysis']['monthly_average']

Monthly maximum volatility: analysis_output['historical_analysis']['monthly_max']

Monthly minimum volatility: analysis_output['historical_analysis']['monthly_min']

Trend direction: analysis_output['historical_analysis']['trend']['trend']

Trend strength: analysis_output['historical_analysis']['trend']['trend_strength'] (only display this if the trend_strength info is available)

(Based on trend direction only, provide explanation here by adhering to the guideline ./interpretation_rules.md)
(If trend strength information is available, provide explanation here by adhering to the guideline ./interpretation_rules.md)

## Market Context

(Provide brief explanation by adhering to the guideline ./interpretation_rules.md)

## Confidence

Confidence index: analysis_output['confidence']['confidence_index'] (put confidence_level here, enclosed by brackets)

(Do not change the wording)
The confidence index reflects how reliable the forecast is, by considering multiple internal indicators. It is not a probability such that the forecast is accurate.

Greater confidence index generally indicates:
- Strong agreement within the Random Forest Model
- Stronger persistence of recent volatility

Lower confidence index generally indicates:
- greater disagreement among model components
- less consistent historical volatility (weak volatility persistence)

## Limitations

(Do not change the wording)
The forecasting model has several limitations.

- The model only uses historical market data.
- External news is not directly included in the prediction model.
- Unexpected events may rapidly change market volatility.
- The model predicts volatility rather than future price direction.
- Feature importance indicates model influence rather than causal relationships.
