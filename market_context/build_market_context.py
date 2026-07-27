import market_context
from datetime import datetime

def market_context_builder():
  market_context_dict = market_context.empty_market_context()
  market_context_dict["retrieved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  market_context_dict["market_data"] = market_context.retrieve_bitcoin_market_data()
  market_context_dict["macro_data"] = market_context.retrieve_macro_data()
  
  articles = market_context.retrieve_bitcoin_news()
  market_context_dict["news"] = [article for article in articles if (article["summary"] and article["relevance_score"] > 0.2)][:5]
  
  market_context_dict["coverage"]["crypto_market"] = market_context_dict["market_data"]["status"]
  market_context_dict["coverage"]["macroeconomics"] = ("available" if any(item.get("status") == "available" for item in market_context_dict["macro_data"].values())
                                                      else "unavailable")
  market_context_dict["coverage"]["news"] = ("available" if news)
  
  return market_context_dict
