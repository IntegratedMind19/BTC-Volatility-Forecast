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
analysis_output = {'prediction': {'predicted_volatility': 0.022092328335047644,
  'forecast_relativity': 'higher',
  'risk_level': 'low',
  'volatility_regime': {'vol_regime_level': 'low',
   'vol_regime_percentile': 9.337641357027463}},
 'forecast_inputs': {'today_garch_volatility': 0.021302715001249684,
  'rolling_volatility': 0.01662369500299916,
  'yesterday_volatility': 0.02172172797477164,
  'feature_values': {'return_lag_1': -0.006098209978869562,
   'return_lag_2': 0.019359107363715822,
   'garch_vol_lag_1': 0.02172172797477164,
   'garch_vol_lag_2': 0.021556655153477246,
   'rolling_mean_7': 0.0034935488923221974,
   'rolling_std_3': 0.016349038274966067,
   'rolling_std_7': 0.010951288931215322,
   'rolling_std_14': 0.01662369500299916},
  'feature_importance': {'return_lag_1': 0.15689520170389054,
   'return_lag_2': 0.005974382025318635,
   'garch_vol_lag_1': 76.57938934703193,
   'garch_vol_lag_2': 0.5920769155262353,
   'rolling_mean_7': 0.5232925609554872,
   'rolling_std_3': 1.3335613423202333,
   'rolling_std_7': 1.9128631494530601,
   'rolling_std_14': 18.895947100983832}},
 'historical_analysis': {'monthly_average': 0.023066520282292356,
  'monthly_max': 0.025319614615054803,
  'monthly_min:': 0.0211324775029717,
  'trend': {'trend': 'decreasing', 'trend_strength': 'weak'},
  'persistence': {'persistence_index': 0.8657409702433936,
   'persistence_level': 'strong'}},
 'confidence': {'confidence_level': 'high',
  'confidence_index': 77.13905649399419,
  'volatility_regime_percentile': 9.337641357027463,
  'persistence_percentile': 86.57409702433935,
  'ensemble_uncertainty_percentile': 26.90453230472517},
 'metadata': {'timestamp': '2026-07-24 04:08:29', 'model_version': '1.0'}}

response = create_report.create_report(knowledge_base_dir, prompt_template_dir, analysis_output, client, "gpt-5.5")

print(response)
