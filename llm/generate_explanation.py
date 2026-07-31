from openai import OpenAI

def generate_explanation(client: OpenAI, llm_input: str, model: str):
  try:
    response = client.responses.create(
      model = model,
      input = llm_input
    )
    return response.output_text.strip()
  except Exception as exc:
    return "Failed to generate proper response. Check whether some issues present."
