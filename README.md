# BTC-Volatility-Forecast

This application gives predictive guidance of the next-day bitcoin price volatility. The aim of this application is to guide BTC investor decision-making processes through the result obtained by the prediction model. This application integrates predictive machine-learning volatility modelling alongside with a comprehensive LLM-based explanation.

**Live Application:** https://btc-volatility-forecast-production.up.railway.app/

---

## Overview

Cryptocurrency markets are highly volatile, making risk estimation an important problem for market participants.

This project forecasts next-day Bitcoin volatility, rather than Bitcoin's future price direction. The objective is to estimate the expected magnitude of future price fluctuations and present the result in an accessible and comprehensive format.

The system combines:

- GARCH-based volatility estimation
- Random Forest regression for next-day volatility forecasting
- Historical volatility and return-based features
- LLM-generated forecast interpretation
- External cryptocurrency and macroeconomic market context
- Scheduled forecast generation
- An interactive Flask and Plotly web interface

The final application provides both the numerical forecast and an explanation of the model's result, historical volatility conditions, relevant market context, model confidence, and limitations.

---

## Live Application

The application provides:

- A 30-day Bitcoin volatility chart
- A 30-day Bitcoin price chart for reference purpose
- The latest next-day volatility forecast
- A detailed forecast report
- A detailed and comprehensive list of terminologies

Forecast reports are generated automatically every four hours.

---

## System Architecture

```text

Historical BTC Data
        |
        v
  GARCH Model
        |
        v
Feature Engineering
        |
        v
 Random Forest
        |
        v
Next-Day Volatility Forecast
        |
        +-----------------------+
        |                       |
        v                       v
Analysis Layer           External Market Data
        |                       |
        |                       v
        |               Market Context Layer
        |                       |
        +-----------+-----------+
                    |
                    v
                   LLM
                    |
                    v
        Structured Forecast Report
                    |
                    v
                PostgreSQL
                    |
                    v
              Flask Web App
