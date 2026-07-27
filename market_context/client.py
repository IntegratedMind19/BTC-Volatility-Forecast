from market_context.build_market_context import market_context_builder
from dotenv import load_dotenv

load_dotenv()

context = market_context_builder()

print(context)
