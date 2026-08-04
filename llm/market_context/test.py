import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

print("FRED:", bool(os.getenv("FRED_API_KEY")))
print("Alpha Vantage:", bool(os.getenv("ALPHA_VANTAGE_API_KEY")))

print("Working directory:", Path.cwd())
print("Application file:", Path(__file__).resolve())
