# CI / CD

This document describes the project's CI and CD pipelines.

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
uv run safety check --json
uv run pytest tests/ -v --tb=short
uv run pytest tests/ --cov=src/ --cov-report=xml --cov-report=term
```

## Continuous Deployment (CD)

Source: [.github/workflows/cd.yaml](../.github/workflows/cd.yaml)

Summary:
- Triggers: automatically after the **CI Pipeline** workflow completes successfully on the `main` branch (`workflow_run` event).
- Deploys to Azure App Service using an image pushed to Azure Container Registry (ACR).

Jobs:

- **build-docker** — Build & push Docker image to ACR
	- Extracts the version from `pyproject.toml`.
	- Sets up Docker Buildx and logs in to ACR using repository secrets.
	- Builds and pushes the image with two tags: `latest` and the extracted version number.
	- Uses ACR-based build cache (`buildcache` tag) to speed up subsequent builds.

- **deploy** — Deploy to production
	- Depends on: `build-docker`.
	- Runs in the `production` GitHub environment (can be configured with required reviewers/protection rules).
	- Logs in to Azure using a service principal credential secret.
	- Deploys the versioned Docker image to Azure Web App using `azure/webapps-deploy`.
	- Restarts the Web App after deployment.

## Required GitHub Secrets

The following secrets must be configured in your GitHub repository (Settings → Secrets and variables → Actions) before the workflows will run correctly.

### CI Secrets (optional)

| Secret | Description |
|--------|-------------|
| `CODECOV_TOKEN` | Token for authenticated Codecov uploads. The CI workflow includes the upload step but the token is commented out by default. Add this secret and uncomment the `token` line in `ci.yaml` if you want authenticated uploads or need to enforce upload failures. |

### CD Secrets (required)

| Secret | Description |
|--------|-------------|
| `ACR_LOGIN_SERVER` | The login server URL of your Azure Container Registry (e.g. `myregistry.azurecr.io`). |
| `ACR_USERNAME` | The username used to authenticate with ACR (e.g. the registry name or a service principal client ID). |
| `ACR_PASSWORD` | The password or service principal client secret used to authenticate with ACR. |
| `AZURE_CREDENTIALS` | A JSON object containing Azure service principal credentials used by `azure/login`. Create a service principal with `az ad sp create-for-rbac --name github-cd-sp --sdk-auth`, then manually construct the JSON with: `clientId`, `clientSecret`, `subscriptionId`, `tenantId`. **Note**: the `--sdk-auth` flag is deprecated. Alternatively, use federated credentials (OIDC) with `azure/login` for a secretless setup. |
| `AZURE_WEBAPP_NAME` | The name of the Azure Web App to deploy to. |
| `AZURE_RESOURCE_GROUP` | The Azure resource group that contains the Web App (used when restarting the app). |
