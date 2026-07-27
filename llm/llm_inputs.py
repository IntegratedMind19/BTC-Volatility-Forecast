import json

def build_llm_inputs(prompt_template: str, knowledge_base: str, analysis_output: dict, market_context: dict):
  analysis_json = json.dumps(analysis_output, indent = 2)
  return f'''
  {prompt_template}

  knowledge_base:
  
  {knowledge_base}

  analysis_output:

  {analysis_output}

  Market context:

  {market_context}
  
  Generate a complete report now.
  '''
