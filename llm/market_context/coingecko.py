import os
import requests
from datetime import datetime, timezone

def retrieve_bitcoin_market_data():
  api_key = os.getenv("CG_API_KEY")
  base_url = "https://api.coingecko.com/api/v3/simple/price"
  params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
  }
  headers = {}
  if api_key:
    headers["x-cg-demo-api-key"] = api_key
  try:
    response = requests.get(base_url, params = params, headers = headers, timeout = 10)
    response.raise_for_status()
    bitcoin = response.json()["bitcoin"]
    return {
            "status": "available",
            "price_usd": {"value": bitcoin.get("usd"), "unit": "USD"},
            "price_change_24h_pct": {"value": round(bitcoin.get("usd_24h_change"), 2), "unit": "%"},
            "volume_24h_usd": {"value": round(bitcoin.get("usd_24h_vol")), "unit": "USD"},
            "market_cap_usd": {"value": round(bitcoin.get("usd_market_cap")), "unit": "USD"},
            "last_updated_at": datetime.fromtimestamp(bitcoin.get("last_updated_at"), tz = timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "CoinGecko",
    }
  except (requests.RequestException, KeyError, TypeError, ValueError) as error:
    return {
            "status": "unavailable",
            "source": "CoinGecko",
            "error": str(error),
    }

retrieve_bitcoin_market_data()
