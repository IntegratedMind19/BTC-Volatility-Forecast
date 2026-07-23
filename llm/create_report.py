from pathlib import Path

def create_report(
  knowledge_base_dir: str | Path, prompt_template_dir: str | Path, analysis_output: dict,
  client: OpenAI, model: str
) -> str:
  knowledge_base = load_knowledge_base(knowledge_base_dir)
  prompt_template = load_prompt_template(prompt_template_dir)
  llm_input = build_llm_inputs(prompt_template, knowledge_base, analysis_output)
  response = generate_explanation(client, llm_input, model)
  return response
                    
