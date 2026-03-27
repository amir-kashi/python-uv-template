# %% Imports
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.configs.config import DefaultConfig
from app.core.logging import setup_logging
from app.utils.helpers import adder

# %% Configs and Settings
setup_logging()
logger = logging.getLogger(__name__)
CONFIG = DefaultConfig()

# Initialize FastAPI app
fastapi_app = FastAPI(title="FastAPI Example", version="0.1.1")
logger.info("FastAPI app initialized")

security = HTTPBearer()


# %% Functions and Classes
def _verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Verify the API key from Authorization header"""
    if credentials.credentials != CONFIG.FASTAPI_KEY:
        message = f"Invalid FastAPI key provided: `{credentials.credentials[:3]}***`"
        logger.warning(message)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)
    logger.info("API key (FastAPI) verified successfully")
    return credentials.credentials


# %% API Endpoints
@fastapi_app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@fastapi_app.get("/hello")
def hello():
    logger.info("Hello endpoint called")
    return {"message": "Hello from FastAPI Example hoooo!"}


@fastapi_app.post("/add")
def add_numbers(a: int, b: int, api_key: str = Depends(_verify_api_key)):
    logger.info(f"Add endpoint called with a={a}, b={b}")
    return {"result": adder(a, b)}
