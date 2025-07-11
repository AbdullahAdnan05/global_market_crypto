"""
Central place to read environment variables.
Nothing else in the codebase should call os.getenv directly.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env if running locally
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

COINGECKO_BASE_URL = os.getenv("COINGECKO_BASE_URL")
FX_API_KEY         = os.getenv("FX_API_KEY")
EMAIL_SENDER       = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD     = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT    = os.getenv("EMAIL_RECIPIENT")
DB_URL             = os.getenv("DB_URL")
DB_POSTGRES_URL    = os.getenv("DB_POSTGRES_URL")
CHROMEDRIVER_PATH  = os.getenv("CHROMEDRIVER_PATH")
DEPLOYMENT         = os.getenv("DEPLOYMENT", "0")  # Defaults to "0"

# Early fail if critical vars are missing
required = [COINGECKO_BASE_URL, FX_API_KEY, DB_URL]
if not all(required):
    raise RuntimeError("❌ Missing environment variables in .env or host system.")