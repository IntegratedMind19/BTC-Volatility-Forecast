import json

def build_llm_inputs(prompt_template: str, knowledge_base: str, analysis_output: dict):
  analysis_json = json.dumps(analysis_output, indent = 2)
  return f'''
  {prompt_template}

  knowledge_base:
  
  {knowledge_base}

  analysis_output:

  {analysis_output}

  The market_context information is not available yet, so skip the market_context section first in the report.
  Generate a complete report now.
  '''
