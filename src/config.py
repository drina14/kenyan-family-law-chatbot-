#A single place that holds settings the rest of the app needs, so nothing is hardcoded twice.

from pathlib import Path 
import os 
from dotenv import load_dotenv 

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw"
MODEL_PATH = BASE_DIR / "data" / "models"
EMBEDDING_PATH = BASE_DIR / "data" / "embeddings"

MODEL_NAME = "claude-sonnet-4-6"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TOP_K_RESULTS = 5