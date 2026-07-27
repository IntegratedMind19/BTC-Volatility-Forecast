import json
from analysis_module import get_analysis_data

def build_llm_inputs(prompt_template: str, knowledge_base: str, analysis_output: dict, market_context: dict):
  analysis_output = get_analysis_data()
  analysis_json = json.dumps(analysis_output, indent = 2)
  market_json = json.dumps(market_context, indent = 2)
  return f'''
  {prompt_template}

  knowledge_base:
  
  {knowledge_base}

  analysis_output:

  {analysis_json}

  Market context:

  {market_json}
  
  Generate a complete report now.
  '''
