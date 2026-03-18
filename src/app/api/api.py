# %% Imports
import logging

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.utils.helpers import adder

# %% Configs and Settings
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
fastapi_app = FastAPI(title="FastAPI Example", version="0.1.0")
logger.info("FastAPI app initialized")


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
def add_numbers(a: int, b: int):
    logger.info(f"Add endpoint called with a={a}, b={b}")
    return {"result": adder(a, b)}
