# %% Imports
import logging

from app.core.logging import setup_logging

# %% Configs and Settings
setup_logging()
logger = logging.getLogger(__name__)


def adder(*args):
    """A simple function that adds numbers together."""
    result = sum(args)
    logger.info(f"Adder function called with arguments: {args}, result: {result}")
    return result
