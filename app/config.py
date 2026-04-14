from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

RAW_DATASET_PATH = DATA_DIR / "synthetic_dublin_bus_mixed_routes.csv"
DB_PATH = DATA_DIR / "bus_system.db"
MODEL_PATH = MODEL_DIR / "bunching_logreg.joblib"

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_BASE_URL = os.getenv("API_BASE_URL", f"http://{API_HOST}:{API_PORT}")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

BUNCHING_THRESHOLD_MIN = 8.0
GAP_THRESHOLD_MIN = 18.0
SEED = 42