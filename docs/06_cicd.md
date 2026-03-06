# CI / CD

This document describes the project's CI pipeline and provides a placeholder for CD (deployment) details.

## Continuous Integration (CI)

Source: [.github/workflows/ci.yaml](../.github/workflows/ci.yaml)

Summary:
- Triggers: `push` and `pull_request` on `main` and `develop`, and `workflow_dispatch`.
- Environment: uses `PYTHON_VERSION` (default `3.13`) and matrix for tests (3.10–3.13).

Jobs:

- **mypy** — Type checking
	- Runs `mypy` against `src/`.
	- Uses `actions/setup-python` and installs dev deps with `uv`.

- **lint** — Lint & format checks
	- Runs `ruff` for linting and `black --check` for formatting on `src/` and `tests/`.

- **security-scan** — Security checks
	- Runs `bandit` (outputs `bandit-report.json`) and `safety` (dependency checks).

- **test** — Unit tests
	- Matrix across Python 3.10, 3.11, 3.12, 3.13.
	- Runs `pytest`, generates coverage XML, and uploads to Codecov (token not configured by default).

- **build-docker** — Build Docker image
	- Uses Docker Buildx and `docker/build-push-action` to build a CI image (does not push).
	- Uploads the image as an artifact (`docker-image` → `/tmp/image.tar`).

- **all-checks-passed** — Gate job
	- Depends on: `mypy`, `lint`, `security-scan`, `test`, `build-docker`.
	- Fails the workflow if any dependency failed.

Artifacts & Reports:
- Coverage XML is generated and expected at `coverage.xml` (uploaded to Codecov when token configured).
- Bandit JSON is produced as `bandit-report.json` in the `security-scan` job.
- Docker image artifact uploaded as `docker-image`.

Running CI steps locally:
- The workflow uses `uv` to install and run tools. To mirror CI locally:

```
python -m pip install --upgrade pip
pip install uv
uv sync --frozen --no-cache --group dev   # installs dev dependencies
uv run mypy src/
uv run ruff check src/ tests/
uv run black --check src/ tests/
uv run bandit -r src/ -f json -o bandit-report.json
uv run safety check --json
uv run pytest tests/ -v --tb=short
uv run pytest tests/ --cov=src/ --cov-report=xml --cov-report=term
```

Configuration notes:
- Codecov token: the workflow includes a Codecov step but the `token` is commented out. Add `CODECOV_TOKEN` to repository secrets if you want uploads to be authenticated and to enforce failures on upload errors.
- The Docker build step currently builds but does not push; adapt `push: true` and provide registry credentials in secrets for a release pipeline.

## Continuous Deployment (CD)

> TODO: CD workflow (`cd.yaml`) is not complete yet — section intentionally left blank.
