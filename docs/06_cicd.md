# CI / CD

This document describes the project's CI and CD pipelines.

## Continuous Integration (CI)

Source: [.github/workflows/ci.yaml](../.github/workflows/ci.yaml)

Summary:
- Triggers: `push` and `pull_request` on `main` and `develop`, and `workflow_dispatch`.
- Environment: uses `PYTHON_VERSION` (default `3.13`) and a test matrix for Python 3.11, 3.12, and 3.13.

Jobs:

- **mypy** — Type checking
	- Runs `mypy` against `src/`.
	- Uses `actions/setup-python` and installs dev deps with `uv`.

- **lint** — Lint & format checks
	- Runs `ruff` for linting and `black --check` for formatting on `src/` and `tests/`.

- **security-scan** — Security checks
	- Runs `bandit` (outputs `bandit-report.json`) and `safety` (dependency checks).
	- Passes `SAFETY_API_KEY` from GitHub Actions secrets to the Safety step via job environment variables.

- **test** — Unit tests
	- Matrix across Python 3.11, 3.12, 3.13.
	- Runs `pytest`, generates coverage XML, and uploads to Codecov (token not configured by default).

- **all-checks-passed** — Gate job
	- Depends on: `mypy`, `lint`, `security-scan`, `test`.
	- Fails the workflow if any dependency failed.

Artifacts & Reports:
- Coverage XML is generated and expected at `coverage.xml` (uploaded to Codecov when token configured).
- Bandit JSON is produced as `bandit-report.json` in the `security-scan` job.

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
export SAFETY_API_KEY="your-safety-api-key"
uv run safety scan --json
uv run pytest tests/ -v --tb=short
uv run pytest tests/ --cov=src/ --cov-report=xml --cov-report=term
```

## Continuous Deployment (CD)

Source: [.github/workflows/cd.yaml](../.github/workflows/cd.yaml)

Summary:
- Triggers: automatically after the **CI Pipeline** workflow completes successfully on the `main` branch (`workflow_run` event).
- Deploys to Azure App Service using two images pushed to Azure Container Registry (ACR): one for Streamlit and one for FastAPI.

Jobs:

- **build-docker** — Build & push Docker images to ACR
	- Extracts the version from `pyproject.toml`.
	- Sets up Docker Buildx and logs in to ACR using repository secrets.
	- Builds and pushes two images (`Dockerfile.streamlit` and `Dockerfile.fastapi`) with two tags each: `latest` and the extracted version number.
	- Uses ACR-based build cache (`buildcache` tag) for each image to speed up subsequent builds.

- **deploy** — Deploy to production
	- Depends on: `build-docker`.
	- Runs in the `production` GitHub environment (can be configured with required reviewers/protection rules).
	- Logs in to Azure using a service principal credential secret.
	- Deploys the versioned Streamlit image to the Streamlit Web App and FastAPI image to the FastAPI Web App using `azure/webapps-deploy`.
	- Sets app settings per Web App, including `WEBSITES_PORT`.
	- Restarts both Web Apps after deployment.

## Required GitHub Secrets

The following secrets must be configured in your GitHub repository (Settings → Secrets and variables → Actions) before the workflows will run correctly.

### CI Secrets

| Secret | Description |
|--------|-------------|
| `SAFETY_API_KEY` | Required for the `security-scan` job. Add this repository secret in GitHub under Settings → Secrets and variables → Actions so the Safety step can authenticate when running `uv run safety scan --json`. |
| `CODECOV_TOKEN` | Token for authenticated Codecov uploads. The CI workflow includes the upload step but the token is commented out by default. Add this secret and uncomment the `token` line in `ci.yaml` if you want authenticated uploads or need to enforce upload failures. |

### CD Secrets (required)

| Secret | Description |
|--------|-------------|
| `ACR_LOGIN_SERVER` | The login server URL of your Azure Container Registry (e.g. `myregistry.azurecr.io`). |
| `ACR_USERNAME` | The username used to authenticate with ACR (e.g. the registry name or a service principal client ID). |
| `ACR_PASSWORD` | The password or service principal client secret used to authenticate with ACR. |
| `AZURE_RESOURCE_GROUP` | The Azure resource group that contains the Web App (used when restarting the app). |
| `AZURE_CREDENTIALS` | A JSON object containing Azure service principal credentials used by `azure/login`. Create a service principal with `az ad sp create-for-rbac --name github-cd-sp --sdk-auth`, then manually construct the JSON with: `clientId`, `clientSecret`, `subscriptionId`, `tenantId`. **Note**: the `--sdk-auth` flag is deprecated. Alternatively, use federated credentials (OIDC) with `azure/login` for a secretless setup. |
| `AZURE_WEBAPP_NAME_STREAMLIT` | The name of the Azure Web App used for the Streamlit UI container. |
| `AZURE_WEBAPP_NAME_FASTAPI` | The name of the Azure Web App used for the FastAPI container. |
