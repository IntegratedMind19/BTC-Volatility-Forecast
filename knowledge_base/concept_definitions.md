File: concept_definitions.md

# Concept Definitions

## Volatility

Volatility measures how much Bitcoin's price is expected to fluctuate over a period of time. High volatility indicates larger price movements, while low volatility indicates more stable prices. Volatility describes the magnitude of price changes, instead of whether prices will increase or decrease.

---

## Predicted Volatility

Predicted volatility is the model's estimate of Bitcoin's volatility for the next trading day. It represents expected market uncertainty rather than expected returns.

---

## GARCH Volatility

GARCH volatility estimates the current market volatility using historical return patterns. It reflects recent market conditions and serves as one of the inputs to the forecasting model.

---

## Rolling Volatility

Rolling volatility measures recent market variability over a fixed historical window. Higher rolling volatility suggests that recent price movements have been more volatile.

---

## Volatility Regime

The volatility regime classifies current market conditions relative to recent history.

- High: above normal historical level
- Medium: around historical average
- Low: below historical average

---

## Trend

Trend describes whether recent volatility has generally been increasing, decreasing, or remaining relatively stable.

---

## Trend strength

Trend strength describes how rapid the change of volatility over the last 30 days. Stronger trend strength indicates more rapid change, meanwhile weaker trend strength indicates slower change.

---

## Persistence

Persistence describes whether recent volatility tends to continue over time. Strong persistence means volatility is likely to remain at similar levels in the near term (e.g., if today's volatility is high, then tomorrow's volatility is likely to be high).

---

## Feature Importance

Feature importance indicates how influential each feature is within the Random Forest model. Higher importance means the model relied more on that feature when making predictions. Feature importance does not imply causation.

---

## Confidence Index

The confidence index estimates how consistent the model's prediction is based on internal indicators. It reflects model reliability rather than prediction accuracy.
