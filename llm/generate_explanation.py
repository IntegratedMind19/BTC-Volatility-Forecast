def generate_explanation(client: OpenAI, llm_input: str, model: str):
  response = client.responses.create(
    model = model
    input = llm_input
  )
  if not response:
    raise RuntimeError("Failed to generate proper response. Check whether some issues present.")
  return response.output_text.strip()
