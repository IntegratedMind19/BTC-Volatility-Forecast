import os
import requests

def fetch_fed_data(series_id: str):
  api_key = os.getenv("FRED_API_KEY")
  if not api_key:
    raise RuntimeError("FRED API key not found")
  base_url = "https://api.stlouisfed.org/fred/series/observations"
  params = {
    "api_key": api_key,
    "file_type": "json",
    "series_id": series_id,
    "sort_order": "desc",
    "limit": 10
  }
  try:
    response = requests.get(base_url, params = params, timeout = 10)
    response.raise_for_status()
    observations = response.json().get("observations")
    latest = next((observation for observation in observations if observation.get("value") not in {None, "."}), None)
    if latest is None:
      raise RuntimeError("Observation data not found")
    return {
      "status": "available",
      "series_id": series_id,
      "source": "FRED",
      "value": float(latest["value"]),
      "observation_date": latest["date"]
    }
  except (requests.RequestException, TypeError, ValueError) as error:
    return {
            "status": "unavailable",
            "series_id": series_id,
            "source": "FRED",
            "error": str(error),
    }

def retrieve_macro_data():
  FRED_SERIES = {
    "effective_federal_funds_rate": "DFF",
    "ten_year_treasury_yield": "DGS10",
    "market_volatility_index": "VIXCLS",
  }
  return {name: fetch_fed_data(series_id) for name, series_id in FRED_SERIES.items()}
