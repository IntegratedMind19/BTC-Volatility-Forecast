from llm.market_context.coingecko import retrieve_bitcoin_market_data
from llm.market_context.fred import retrieve_macro_data
from llm.market_context.news import retrieve_bitcoin_news
from llm.market_context.market_schema import empty_market_context
from datetime import datetime, timezone

def market_context_builder():
  market_context_dict = empty_market_context()
  market_context_dict["retrieved_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + " (UTC)"
  try:
    market_context_dict["market_data"] = retrieve_bitcoin_market_data()
  except Exception as exc:
    market_context_dict["market_data"] = {"information": "There are some issues in retrieving market data or data is not available at the moment."}
    market_context_dict["coverage"]["crypto_market"] = "unavailable"

  try:
    market_context_dict["macro_data"] = retrieve_macro_data()
  except Exception as exc:
    market_context_dict["macro_data"] = {"information": "There are some issues in retrieving macroeconomics data or data is not available at the moment."}
    market_context_dict["coverage"]["macroeconomics"] = "unavailable"   
    
  try:
    articles = retrieve_bitcoin_news(20)
    market_context_dict["news"] = [article for article in articles if (article["summary"] and article["relevance_score"] > 0.2)][:10]
  except Exception as exc:
    market_context_dict["news"] = ["There are some issues in retrieving market news or news articles are not available at the moment."]
    market_context_dict["coverage"]["news"] = "unavailable"

  market_context_dict["coverage"]["crypto_market"] = market_context_dict["market_data"]["status"]
  market_context_dict["coverage"]["macroeconomics"] = ("available" if any(item.get("status") == "available" for item in market_context_dict["macro_data"].values())
                                                      else "unavailable")
  market_context_dict["coverage"]["news"] = ("available" if market_context_dict["news"] else "unavailable")
  
  return market_context_dict

print(market_context_builder())
