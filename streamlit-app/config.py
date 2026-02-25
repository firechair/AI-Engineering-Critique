import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
APP_DIR = Path(__file__).parent
RUBRICS_DIR = APP_DIR / "rubrics"
TECHNIQUES_DIR = BASE_DIR / "prompt_techniques"
CSS_FILE = APP_DIR / "assets" / "style.css"
EVALUATIONS_DIR = APP_DIR / "evaluations"

# Ensure directories exist
EVALUATIONS_DIR.mkdir(exist_ok=True)

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODELS_URL = f"{OPENROUTER_BASE_URL}/models"

# App Settings
APP_TITLE = "AI Engineering Critique"
APP_ICON = "🧐"
