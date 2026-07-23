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

knowledge_base_dir = "knowledge_base"
prompt_template_dir = "prompt"
analysis_output = {'prediction': {'predicted_volatility': 0.022121417255959584,
  'forecast_relativity': 'higher',
  'risk_level': 'low',
  'volatility_regime': {'vol_regime_level': 'low',
   'vol_regime_percentile': 9.696186166774403}},
 'forecast_inputs': {'today_garch_volatility': 0.021737970578604437,
  'rolling_volatility': 0.016768494355523807,
  'yesterday_volatility': 0.02157319931147268,
  'feature_values': {'return_lag_1': 0.019359107363715822,
   'return_lag_2': 0.008300835886389635,
   'garch_vol_lag_1': 0.02157319931147268,
   'garch_vol_lag_2': 0.02196383685472248,
   'rolling_mean_7': 0.0022620034081704938,
   'rolling_std_3': 0.01563056316569534,
   'rolling_std_7': 0.012559151718585487,
   'rolling_std_14': 0.016768494355523807},
  'feature_importance': {'return_lag_1': 0.16554487481862923,
   'return_lag_2': 0.004307418462346777,
   'garch_vol_lag_1': 76.48024811187543,
   'garch_vol_lag_2': 0.605821037774435,
   'rolling_mean_7': 0.5258526153799825,
   'rolling_std_3': 1.4998738870707358,
   'rolling_std_7': 1.9773534745226733,
   'rolling_std_14': 18.740998580095766}},
 'historical_analysis': {'monthly_average': 0.02319257094791523,
  'monthly_max': 0.0253383589298245,
  'monthly_min:': 0.021150370298049764,
  'trend': {'trend': 'decreasing', 'trend_strength': 'weak'},
  'persistence': {'persistence_index': 0.8651571602828197,
   'persistence_level': 'strong'}},
 'confidence': {'confidence_level': 'high',
  'confidence_index': 75.17979519433668,
  'volatility_regime_percentile': 9.696186166774403,
  'persistence_percentile': 86.51571602828197,
  'ensemble_uncertainty_percentile': 29.67845659163987},
 'metadata': {'timestamp': '2026-07-23 05:33:31', 'model_version': '1.0'}}

response = create_report.create_report(knowledge_base_dir, prompt_template_dir, analysis_output, client, "gpt-5.5")
