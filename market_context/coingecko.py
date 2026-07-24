import os
from dotenv import load_dotenv
import requests

def retrieve_coin_gecko_api():
  load_dotenv()
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
    bitcoin = response.json().["bitcoin"]
    return {
            "status": "available",
            "price_usd": bitcoin.get("usd"),
            "price_change_24h_pct": bitcoin.get("usd_24h_change"),
            "volume_24h_usd": bitcoin.get("usd_24h_vol"),
            "market_cap_usd": bitcoin.get("usd_market_cap"),
            "last_updated_at": bitcoin.get("last_updated_at"),
            "source": "CoinGecko",
    }
  except (requests.RequestException, KeyError, TypeError, ValueError) as error:
    return {
            "status": "unavailable",
            "source": "CoinGecko",
            "error": str(error),
    }
