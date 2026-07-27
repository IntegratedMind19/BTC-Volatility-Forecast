import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import create_report

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
  raise RuntimeError("api_key is not defined correctly")

client = OpenAI(api_key = api_key)

knowledge_base_dir = "../knowledge_base"
prompt_template_dir = "../prompt"
analysis_output = {'prediction': {'predicted_volatility': 0.022197382569522563,
  'forecast_relativity': 'higher',
  'risk_level': 'low',
  'volatility_regime': {'vol_regime_level': 'low',
   'vol_regime_percentile': 8.327953518398967}},
 'forecast_inputs': {'today_garch_volatility': 0.020906196209475363,
  'rolling_volatility': 0.017776302237196343,
  'yesterday_volatility': 0.021357200053285653,
  'feature_values': {'return_lag_1': 0.0033224217714327153,
   'return_lag_2': -0.01465555365422766,
   'garch_vol_lag_1': 0.021357200053285653,
   'garch_vol_lag_2': 0.02136443181819715,
   'rolling_mean_7': 0.0019071288902401712,
   'rolling_std_3': 0.016951184865763955,
   'rolling_std_7': 0.014777270600213548,
   'rolling_std_14': 0.017776302237196343},
  'feature_importance': {'return_lag_1': 0.09868492359510679,
   'return_lag_2': 0.0057087145754965,
   'garch_vol_lag_1': 76.78064429585089,
   'garch_vol_lag_2': 0.5267810098147065,
   'rolling_mean_7': 0.6313012519814201,
   'rolling_std_3': 1.165588486994972,
   'rolling_std_7': 1.8578716628342298,
   'rolling_std_14': 18.933419654353187}},
 'historical_analysis': {'monthly_average': 0.022690263428460023,
  'monthly_max': 0.024677513755158392,
  'monthly_min:': 0.020906196209475363,
  'trend': {'trend': 'decreasing', 'trend_strength': 'weak'},
  'persistence': {'persistence_index': 0.8487228620240335,
   'persistence_level': 'strong'}},
 'confidence': {'confidence_level': 'medium',
  'confidence_index': 51.852180401504555,
  'volatility_regime_percentile': 8.327953518398967,
  'persistence_percentile': 84.87228620240334,
  'ensemble_uncertainty_percentile': 62.299293513166354},
 'metadata': {'timestamp': '2026-07-27 06:13:27', 'model_version': '1.0'}}

market_context = {'retrieved_at': '2026-07-27 07:22:28 (UTC)', 'market_data': {'status': 'available', 'price_usd': {'value': 65368, 'unit': 'USD'}, 'price_change_24h_pct': {'value': 1.64, 'unit': '%'}, 'volume_24h_usd': {'value': 17239271929, 'unit': 'USD'}, 'market_cap_usd': {'value': 1311454901786, 'unit': 'USD'}, 'last_updated_at': '2026-07-27 07:22:01', 'source': 'CoinGecko'}, 'macro_data': {'effective_federal_funds_rate': {'status': 'available', 'series_id': 'DFF', 'source': 'FRED', 'data': {'value': 3.63, 'unit': '%'}, 'observation_date': '2026-07-23'}, 'ten_year_treasury_yield': {'status': 'available', 'series_id': 'DGS10', 'source': 'FRED', 'data': {'value': 4.71, 'unit': '%'}, 'observation_date': '2026-07-23'}, 'market_volatility_index': {'status': 'available', 'series_id': 'VIXCLS', 'source': 'FRED', 'data': {'value': 18.7, 'unit': 'points'}, 'observation_date': '2026-07-23'}}, 'news': [{'title': "Clarity Hopes Fade, BitMEX Shuts as Lawsuit Looms: Hodler's Digest, July 26", 'summary': "Despite support from Goldman Sachs, Fidelity and law enforcement bodies, the Clarity Act's chances dim. BitMEX to close as crypto consolidates into five big players.", 'published_at': '20260727T000344', 'source_name': 'Cointelegraph', 'source_url': 'https://cointelegraph.com/magazine/clarity-hopes-fade-bitmex-shuts-as-lawsuit-looms-hodlers-digest-july-27', 'overall_sentiment_label': 'Neutral', 'relevance_score': 0.310004}, {'title': 'Bitcoin OG Selling Eases, Dormant BTC Movement Hits 4-Year Low', 'summary': 'Dormant Bitcoin activity fell to its lowest level since Q3 2022, suggesting long-term holders have slowed distribution after heavy profit-taking.', 'published_at': '20260726T130435', 'source_name': 'Cointelegraph', 'source_url': 'https://cointelegraph.com/markets/bitcoin-og-dormant-btc-movement-thorn', 'overall_sentiment_label': 'Somewhat-Bearish', 'relevance_score': 0.578355}, {'title': "Here's Why I'm Buying Bitcoin Right Now", 'summary': 'Bitcoin may finally be nearing the end of the bearish phase of its four-year cycle.', 'published_at': '20260726T083000', 'source_name': 'Motley Fool', 'source_url': 'https://www.fool.com/investing/2026/07/26/heres-why-im-buying-bitcoin-right-now/', 'overall_sentiment_label': 'Neutral', 'relevance_score': 0.971202}, {'title': 'Nebius vs. Strategy: Comparing Revenue Trends Between an Artificial Intelligence Company and a Bitcoin Giant', 'summary': "Nebius has grown revenue nearly 33-fold in eight quarters, while Strategy's top line has barely budged - a divergence that raises questions about sustainability.", 'published_at': '20260725T211401', 'source_name': 'Motley Fool', 'source_url': 'https://www.fool.com/coverage/charts/2026/07/25/nebius-vs-strategy-comparing-revenue-trends-between-an-artificial-intelligence-company-and-a-bitcoin-giant/', 'overall_sentiment_label': 'Neutral', 'relevance_score': 0.426824}, {'title': "Bitcoin Advocacy Group to Join US State Department's 'Digital Freedom' Program", 'summary': 'The Bitcoin Policy Institute and three partner organizations will be able to send employees to work alongside State Department officials to address issues including digital freedom.', 'published_at': '20260725T181544', 'source_name': 'Cointelegraph', 'source_url': 'https://cointelegraph.com/news/bitcoin-policy-institute-state-department-program', 'overall_sentiment_label': 'Bullish', 'relevance_score': 0.601928}], 'coverage': {'crypto_market': 'available', 'macroeconomics': 'available', 'news': 'available'}, 'disclaimer': 'External market context was not used as an input to the volatility forecasting model.', 'schema_version': '1.0'}

response = create_report.create_report(knowledge_base_dir, prompt_template_dir, analysis_output, market_context, client, "gpt-5.5")

print(response)
