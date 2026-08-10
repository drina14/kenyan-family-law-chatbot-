#A single place that holds settings the rest of the app needs, so nothing is hardcoded twice.

from pathlib import Path #library for working with files and folders.
import os #module lets Python interact with the operating system.
from dotenv import load_dotenv #reads .env file and loads environment variables into the program's environment.

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw"
MODEL_PATH = BASE_DIR / "data" / "models"
EMBEDDING_PATH = BASE_DIR / "data" / "embeddings"

MODEL_NAME = "claude-sonnet-4-6"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TOP_K_RESULTS = 5