# Docker

This project uses one Docker image and Docker Compose to run two services:

- Streamlit UI on port 8501
- FastAPI on port 8000

This keeps one shared codebase and dependency set, while running each app as its own container process.

---

## Files Involved

- `Dockerfile`: shared image definition
- `docker-compose.yml`: orchestrates Streamlit and FastAPI services

---

## Overview

The Docker image:

- Uses `python:3.13-slim`
- Installs dependencies with `uv sync --frozen --no-cache --no-dev`
- Copies project source from `src/`
- Sets `PYTHONPATH=/workspace/src`

Compose then starts:

- `streamlit` service with a Streamlit command on port 8501
- `fastapi` service with Uvicorn (`app.api.main:app`) on port 8000

---

## Prerequisites

Create `.env` from the example before starting Compose:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

---

## Run Both Services (Recommended)

From project root:

```bash
docker compose up --build
```

Access:

- Streamlit UI: `http://localhost:8501`
- FastAPI docs: `http://localhost:8000/docs`
- FastAPI sample endpoint: `http://localhost:8000/hello`

To stop:

```bash
docker compose down
```

---

## Run a Single Service

Streamlit only:

```bash
docker compose up --build streamlit
```

FastAPI only:

```bash
docker compose up --build fastapi
```

---

## Logs And Volumes

Both services mount local `./logs` into `/workspace/logs`:

- Host logs remain available after container restart
- Both apps can write to the same logs directory

---

## About Dockerfile CMD

`Dockerfile` contains a default `CMD` for Streamlit.

In Compose, each service defines its own `command`, so that default `CMD` is overridden and not used.

Keeping a default `CMD` is optional and mainly useful for direct `docker run` usage.

---

## Optional: Run Image Directly (Without Compose)

Build image:

```bash
docker build -t python-uv-template .
```

Run Streamlit from image default:

```bash
docker run --rm -p 8501:8501 --env-file .env python-uv-template
```

Run FastAPI by overriding command:

```bash
docker run --rm -p 8000:8000 --env-file .env python-uv-template \
  uv run uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

---

## Rebuild After Dependency Changes

If dependencies change:

```bash
uv lock
docker compose build --no-cache
docker compose up
```

---

## Common Issues

- `docker compose up --build` fails because `.env` is missing:
  - Create `.env` from `.env.example`
- One port is already in use:
  - Free the port or change host-side mapping in `docker-compose.yml`
- Code changes not reflected:
  - Rebuild with `docker compose up --build`
