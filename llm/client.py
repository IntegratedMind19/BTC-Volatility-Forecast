import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import create_report
from analysis_module import get_analysis_data
from market_context.build_market_context import market_context_builder

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
  raise RuntimeError("api_key is not defined correctly")

client = OpenAI(api_key = api_key)

knowledge_base_dir = "../knowledge_base"
prompt_template_dir = "../prompt"

analysis_output = get_analysis_data()
market_context = market_context_builder()

response = create_report.create_report(knowledge_base_dir, prompt_template_dir, analysis_output, market_context, client, "gpt-5.5")

print(response)
