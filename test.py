import os
from dotenv import load_dotenv

load_dotenv()

print("FRED:", bool(os.getenv("FRED_API_KEY")))
print("Alpha Vantage:", bool(os.getenv("ALPHA_VANTAGE_API_KEY")))
