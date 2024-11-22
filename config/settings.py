
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

# API Key and other settings
DEFAULT_API_KEY = os.getenv("TOGETHER_API_KEY", "your_default_api_key") 
DEFAULT_BASE_URL = "https://api.together.xyz/v1"
DEFAULT_MODEL = "meta-llama/Llama-Vision-Free"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 512
DEFAULT_TOKEN_BUDGET = 4096