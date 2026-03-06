# Docker

This project includes a Dockerfile for building a reproducible, production-ready container image.

Docker ensures the application runs consistently across environments such as:

- Local machines
- Cloud platforms (Azure, AWS, GCP)
- Kubernetes clusters
- CI/CD pipelines

---

## Overview

The Docker image:

- Uses Python slim base image for smaller size
- Installs dependencies using `uv`
- Installs only production dependencies
- Runs the application using the `src/` layout
- Writes logs to the `/workspace/logs` directory

---

## Build the Image

From the project root:

```bash
docker build -t python-uv-template .
```

This creates a Docker image named `python-uv-template` (replace it with actual name).

---

## Run the Container

```bash
docker run --rm -p 8501:8501 python-uv-template
```

For a Streamlit app, this maps port 8501 from the container to the host. remove `-p 8501:8501` for non-Streamlit apps.

This will start the application by executing:

```bash
uv run streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0
```

---

## Why Install Only Production Dependencies?

This line ensures only runtime dependencies are installed:

```dockerfile
RUN uv sync --no-dev
```

This improves:

* Image size
* Security
* Startup speed

Development tools such as pytest, black, and pre-commit are excluded.

---

## Environment Variables

Environment variables can be passed using:

```bash
docker run --rm \
  -e ENVIRONMENT=production \
  python-uv-template
```

Or using an env file:

```bash
docker run --rm \
  --env-file .env \
  python-uv-template
```

---

## Run with Mounted Logs (Recommended)

To persist logs outside the container:

In Windows PowerShell:

```powershell
docker run --rm `
  -v ${PWD}/logs:/workspace/logs `
  python-uv-template
```

In Unix/Linux/macOS terminal:

```bash
docker run --rm \
  -v $(pwd)/logs:/workspace/logs \
  python-uv-template
```

Logs will be written to the local `logs/` folder.

---

## Using in Cloud Environments

This Docker image can be deployed to:

* Azure Web App for Containers
* Azure Container Apps
* AWS ECS
* AWS Fargate
* Kubernetes

The container is self-contained and ready for production use.

---

## Rebuilding After Dependency Changes

If dependencies change:

```bash
uv lock
docker build -t python-uv-template .
```

---

## Best Practices

* Always use `--no-dev` in Docker builds
* Do not include tests in production images
* Do not include `.venv`
* Use `.dockerignore` to exclude unnecessary files
* Mount logs externally when possible
