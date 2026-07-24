File: output_format.md

# Report structure (strictly follow this order):
1. Forecast Summary
2. Feature Interpretation
3. Historical Trend Overview
4. Market Context
5. Confidence
6. Model Limitations
7. Overall Summary
8. Metadata

(maintain the section name)

---

# Detailed output format (strictly follow the formatting)

## Forecast Summary

Predicted volatility: analysis_output ['prediction'] ['predicted_volatility'] (higher or lower based on analysis_output ['prediction'] ['forecast_relativity']. State explicitly whether higher/lower than today's volatility)

(Provide interpretation here, based on analysis_output ['prediction'] ['forecast_relativity']. Refer to interpretation_rules.md for each condition.)

Volatility regime: analysis_output ['prediction'] ['volatility_regime'] (Provide interpretation here, enclosed by brackets. Refer to interpretation_rules.md for each condition.)

Risk level: analysis_output ['prediction'] ['risk_level'] (Provide interpretation here, enclosed by brackets. Refer to interpretation_rules.md for each condition.)

(Provide brief conclusion here, strictly from the obtained result.)

Example:

The predicted volatility of 2.21% is slightly higher than today's estimated volatility (2.17%), but remains below the recent monthly average (2.32%). Consequently, the overall volatility regime and risk level remain classified as Low.)

## Feature Interpretation

(Provide brief explanation by adhering to the guideline interpretation_rules.md. Convert feature importance values to percentage (e.g. 0.64581 becomes 64.58%).
Do not give explanations on individual features)

## Historical Trend Overview

Monthly average volatility: analysis_output ['historical_analysis'] ['monthly_average']

Monthly maximum volatility: analysis_output ['historical_analysis'] ['monthly_max']

Monthly minimum volatility: analysis_output ['historical_analysis'] ['monthly_min']

Trend direction: analysis_output ['historical_analysis'] ['trend'] ['trend']

Trend strength: analysis_output ['historical_analysis'] ['trend'] ['trend_strength'] (only display this if the trend_strength info is available)

(Based on trend direction only, provide explanation here by adhering to the guideline interpretation_rules.md)

(If trend strength information is available, provide explanation here by adhering to the guideline interpretation_rules.md)

Persistence: analysis_output ['historical_analysis'] ['persistence']

(Explain the connection with the resulting forecast, whether the result is consistent or not.)

## Market Context

(Provide brief explanation by adhering to the guideline interpretation_rules.md)

## Confidence

Confidence index: analysis_output ['confidence'] ['confidence_index'] (put confidence_level here, enclosed by brackets)

(Do not change the wording)

The confidence index reflects how reliable the forecast is, by considering multiple internal indicators. It is not a probability such that the forecast is accurate.

Greater confidence index generally indicates:
- Strong agreement among the model's internal estimates
- Stronger persistence of recent volatility

Lower confidence index generally indicates:
- greater disagreement among model components
- less consistent historical volatility (weak volatility persistence)

(Put explanation here, stating whether the confidence is high/medium/low, and briefly explain the implication of the result.

Example:

The current confidence index of 85.12 is classified as high, suggesting relatively strong agreement among the model's internal indicators. Strong volatility persistence further supports the stability of the forecast.)

## Model Limitations

(Do not change the wording)

The forecasting model has several limitations.

- The model only uses historical market data.
- External news is not directly included in the prediction model.
- Unexpected events may rapidly change market volatility.
- The model predicts volatility rather than future price direction.
- Feature importance indicates model influence rather than causal relationships.

## Overall Summary
(Provide a brief summary based on the obtained result and interpretations.

Example: (Change some informations or wordings if appropriate)

Overall, the model forecasts another day of relatively low Bitcoin volatility, with expected market fluctuations remaining close to recent historical levels. Although volatility is forecast to increase slightly compared with today, the increase is modest and remains consistent with the current low-volatility regime. Users should interpret this forecast alongside external market developments, which are not incorporated directly into the prediction model.)

## Metadata
Timestamp: <YYYY-MM-DD HH:MM:SS> (GMT)

Model version: (Use the information from analysis_output)
