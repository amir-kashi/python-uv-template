# %% Imports
import logging

import streamlit as st

import app
from app.configs.config import DefaultConfig
from app.core.logging import setup_logging
from app.utils.helpers import adder

# %% Configs and Settings
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration settings
CONFIG = DefaultConfig()


def main():
    logger.info("Starting main function")

    st.title("Python Template Project")

    st.write(
        "Welcome to the Python Template project! "
        "This is a sample Streamlit app to demonstrate "
        "the project structure and features."
    )

    st.subheader(f"App Version: {app.__version__}")

    # Display project documentation
    st.header("Project Documentation")
    mds = [
        "README.md",
        "docs/01_quick_start.md",
        "docs/02_project_structure.md",
        "docs/03_dependencies.md",
        "docs/04_pre_commit_hooks.md",
        "docs/05_docker.md",
        "docs/06_cicd.md",
        "docs/07_azure_setup.md",
    ]
    for md in mds:
        logger.info(f"Loading markdown file: {md}")
        with st.expander(f"View {md}"):
            with open(md, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content)

    # Example usage of config and helper function
    logger.info(f"API Key from config: {CONFIG.API_KEY}")
    logger.info(f"Adder function result (1+2+3): {adder(1, 2, 3)}")
    logger.info("Finished main function")


if __name__ == "__main__":
    main()
