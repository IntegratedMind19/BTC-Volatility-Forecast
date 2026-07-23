def generate_explanation(client: OpenAI, llm_input: str):
  response = client.responses.create(
    model = "gpt-5.5"
    input = llm_input
  )
  if not response:
    raise RuntimeError("Response undefined")
  return response
