from logging.config import fileConfig
from pathlib import Path


def setup_logging():
    base_dir = Path(__file__).resolve().parents[1]  # go to app/
    config_path = base_dir / "configs" / "logging_config.ini"
    fileConfig(config_path, disable_existing_loggers=False)
