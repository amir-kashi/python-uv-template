# Project Structure

This project follows the modern **src-layout pattern**, which improves import reliability, testing, and packaging consistency.

```text
python-uv-template/   (sample file names)
├── src/
│   └── app/                     # Main Python package
│       ├── __init__.py
│       ├── main.py              # Application entry point
│       │
│       ├── core/                # Core business logic
│       │   ├── logic.py
│       │   └── logging.py
│       │
│       ├── utils/               # Helper and utility functions
│       │   └── helpers.py
│       │
│       └── configs/             # Application configuration
│           ├── config.py
│           └── logging_config.ini
│
├── tests/                       # Unit and integration tests (pytest)
│   ├── test_logic.py
│   └── test_service_a.py
│
├── scripts/                     # Development and helper scripts
│   └── run_local.sh
│
├── logs/                        # Runtime log files (created at runtime)
│   └── logging.log
│
├── docs/                        # Project documentation
│   ├── quick_start.md
│   ├── docker.md
│   ├── dependencies.md
│   └── architecture.md
│
├── Dockerfile.streamlit         # Container definition for Streamlit UI service
├── Dockerfile.fastapi           # Container definition for FastAPI service
├── .dockerignore                # Files excluded from Docker build
│
├── pyproject.toml               # Project metadata and dependencies
├── uv.lock                      # Locked dependency versions (reproducible builds)
│
├── .pre-commit-config.yaml      # Pre-commit hook configuration
├── .gitignore                   # Git ignore rules
├── .env.example                 # Example environment variables
│
├── README.md                    # High-level project overview
└── LICENSE                      # License file
```

---

## Directory and File Overview

### `src/app/`

Contains the main application code.

* `main.py` — entry point of the application
* `core/` — business logic and core functionality
* `utils/` — reusable helper functions
* `configs/` — configuration files, including logging setup

This layout ensures clean imports such as:

```python
from app.core.logic import my_function
or
from .core.logic import my_function
```

---

### `tests/`

Contains automated tests using `pytest`.

* Tests mirror the structure of the source code
* Automatically discovered when running:

```bash
uv run pytest
```

---

### `scripts/`

Contains helper scripts for development and operational tasks.

Examples:

* Local execution scripts
* Data migration scripts
* Maintenance utilities

---

### `logs/`

Stores application log files.

* Created automatically at runtime if not present
* Controlled via `src/app/configs/logging_config.ini`
* Should not be committed to Git (included in `.gitignore`)

---

### `docs/`

Contains detailed project documentation.

Examples:

* Quick start guide
* Docker usage
* Dependency management
* Architecture explanation

---

### `Dockerfile.streamlit` and `Dockerfile.fastapi`

Define the containerized runtime environments for each service.

Used to:

* Build service-specific production-ready images
* Keep Streamlit and FastAPI startup commands isolated and explicit
* Deploy each service independently to cloud platforms such as Azure

See `docs/docker.md` for usage instructions.

---

### `pyproject.toml`

Defines:

* Project metadata
* Production dependencies
* Development dependencies
* Tool configurations (pytest, black, etc.)

This is the single source of truth for dependencies.

---

### `uv.lock`

Locks exact dependency versions for reproducibility.

Ensures:

* Consistent environments across developers and production
* Deterministic builds

Automatically generated and updated by:

```bash
uv sync
```

---

### `.pre-commit-config.yaml`

Defines automated code quality checks run before commits.

Examples:

* Formatting (Black)
* Linting (Ruff)
* Whitespace cleanup

---

### `.env.example`

Template for environment variables required by the application.

Developers should copy this to `.env` and adjust values as needed.

---

## Why use the `src/` layout?

This prevents accidental imports from the project root and ensures the code behaves the same in development, testing, and production environments.

It is the recommended structure for modern Python projects.
