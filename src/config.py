from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# settings
settings = {
    "AZURE_OPENAI_API_BASE_URL": os.getenv("AZURE_OPENAI_API_BASE_URL", ""),
    "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY", ""),
    "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION", ""),
    "AZURE_MODEL_PREFIX": os.getenv("AZURE_MODEL_PREFIX", ""),
}
