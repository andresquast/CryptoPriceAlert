from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Settings
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "price_history.db"

# API Settings
UPDATE_INTERVAL = 10000  # milliseconds
MAX_HISTORY_POINTS = 50

# UI Settings
WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Crypto Price Monitor"