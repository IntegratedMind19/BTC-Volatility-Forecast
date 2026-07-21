# Confidence

The confidence index reflects how reliable the forecast is, by considering multiple internal indicators. It is not a probability such that the forecast is accurate.

Greater confidence index generally indicates:
- Strong agreement within the Random Forest Model
- Stronger persistence of recent volatility

Lower confidence index generally indicates:
- greater disagreement among model components
- less consistent historical volatility (weak volatility persistence)

---

# Model Limitations

The forecasting model has several limitations.

- The model only uses historical market data.
- External news is not directly included in the prediction model.
- Unexpected events may rapidly change market volatility.
- The model predicts volatility rather than future price direction.
- Feature importance indicates model influence rather than causal relationships.

---
