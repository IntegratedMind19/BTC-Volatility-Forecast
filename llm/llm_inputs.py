import json

def build_llm_inputs(prompt_template: str, knowledge_base: str, analysis_output: dict, market_context: dict):
  analysis_json = json.dumps(analysis_output, indent = 2)
  return f'''
  {prompt_template}

  knowledge_base:
  
  {knowledge_base}

  analysis_output:

  {json.dumps(analysis_output, indent = 2)}

  Market context:

  {json.dumps(market_context, indent = 2}
  
  Generate a complete report now.
  '''
