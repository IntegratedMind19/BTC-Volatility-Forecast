def empty_market_context():
    return {
        "retrieved_at": None,
        "market_data": {},
        "macro_data": {},
        "news": [],
        "coverage": {
            "crypto_market": "unavailable",
            "macroeconomics": "unavailable",
            "news": "unavailable",
        },
        "disclaimer": "External market context was not used as an input to the volatility forecasting model."
    }
