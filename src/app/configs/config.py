import os

from dotenv import load_dotenv

# Load the .env file
load_dotenv()


class DefaultConfig:
    # Sample parameter from the .env file
    API_KEY = os.environ.get("API_KEY", "")

    # Fast API
    FASTAPI_KEY = os.environ.get("FASTAPI_KEY", "")
