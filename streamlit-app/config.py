import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
APP_DIR = Path(__file__).parent
RUBRICS_DIR = APP_DIR / "rubrics"
TECHNIQUES_DIR = APP_DIR / "prompt_techniques"
EVALUATIONS_DIR = APP_DIR / "evaluations"

# Ensure directories exist
EVALUATIONS_DIR.mkdir(exist_ok=True)

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# App Settings
APP_TITLE = "AI Engineering Critique"
APP_ICON = "🧐"
