import os
from dotenv import load_dotenv
import requests

def retrieve_bitcoin_news():
  load_dotenv()
  api_key = os.getenv("ALPHA_VANTAGE_KEY")
  if not api_key:
    raise RuntimeError("Alpha Vantage API key not found")
  base_url = "https://www.alphavantage.co/query"
  params = {
    "function": "NEWS_SENTIMENT",
    "tickers": "CRYPTO:BTC",
    "sort": "LATEST",
    "limit": 10,
    "apikey": api_key
  }
  response = requests.get(base_url, params = params, timeout = 10)
  response.raise_for_status()
  data = response.json()
  feeds = data.get("feed")
  articles = list()
  for item in feeds:
    articles.append(
      {
                    "title": item.get("title"),
                    "summary": item.get("summary"),
                    "published_at": item.get("time_published"),
                    "source_name": item.get("source"),
                    "source_url": item.get("url"),
                    "overall_sentiment_label": item.get(
                        "overall_sentiment_label"
                    ),
                    "relevance_score": extract_btc_relevance(item),
                }
    )
  return articles

def extract_btc_relevance(item: dict[str, Any]) -> float | None:
  for ticker in item.get("ticker_sentiment"):
    if ticker.get("ticker") == "CRYPTO:BTC":
      try:
        return float(ticker.get("relevance_score"))
      except (TypeError, ValueError):
        return None
  return None
