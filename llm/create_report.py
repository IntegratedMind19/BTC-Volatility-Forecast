from pathlib import Path
from openai import OpenAI
import load_explanation_engine as kb
import load_prompt_template as pt
import llm_inputs
import generate_explanation as ge

def create_report(
  knowledge_base_dir: str | Path, prompt_template_dir: str | Path, analysis_output: dict, market_context: dict, 
  client: OpenAI, model: str
) -> str:
  knowledge_base = kb.load_knowledge_base(knowledge_base_dir)
  prompt_template = pt.load_prompt_template(prompt_template_dir)
  llm_input = llm_inputs.build_llm_inputs(prompt_template, knowledge_base, analysis_output, market_context)
  response = ge.generate_explanation(client, llm_input, model)
  return {
    "analysis": analysis_output,
    "market_context": market_context,
    "report": response
  }     
