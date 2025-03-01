import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGSMITH_TRACING_V2 = os.getenv("LANGSMITH_TRACING_V2", "false")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
