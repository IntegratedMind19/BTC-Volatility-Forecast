from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / ".env"

loaded = load_dotenv(ENV_PATH)

print("Current working directory:", Path.cwd())
print("Expected .env path:", ENV_PATH)
print(".env exists:", ENV_PATH.is_file())
print(".env loaded:", loaded)
print("FRED key available:", bool(os.getenv("FRED_API_KEY")))
print(
    "Alpha Vantage key available:",
    bool(os.getenv("ALPHA_VANTAGE_KEY"))
)
