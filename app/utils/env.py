import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "./data")
MODEL_DIR = os.getenv("MODEL_DIR", "./artifacts")
FRED_API_KEY = os.getenv("FRED_API_KEY", None)

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
