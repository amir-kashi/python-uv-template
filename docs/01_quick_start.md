# Quick Start (for Developers)

This section explains how to **set up and run the project locally for development and testing**.
If you want a production-ready deployment, see the [Docker guide](05_docker.md).

---

### 1. Clone the repository

```bash
git clone <repo-url>
cd python-uv-template
````

---

### 2. Install uv (if not already installed)

```bash
pip install uv
```

`uv` manages dependencies, virtual environments, and reproducible builds.

---

### 3. Sync dependencies

```bash
uv sync
```

This installs **both production and development dependencies** defined in `pyproject.toml` and locked in `uv.lock`.

> For **production-only installs**, use:
>
> ```bash
> uv sync --no-dev
> ```

---

### 4. Run the application locally

> For **Streamlit** app, use:
>
> ```bash
> uv run streamlit run src/app/main.py
> ```

> For **normal Python script**, use:
> ```bash
> uv run python -m app.main
> ```

* `uv run` ensures the correct Python environment is used automatically.
* Logs will be written to the `logs/` folder.
* This is suitable for **development and testing**, not production.

---

### 5. Run tests

```bash
uv run pytest
```

* This will discover tests in the `tests/` folder.

---

### Notes

* This setup is **for developers** working on the project locally.
* For **production or containerized deployments**, see the [Docker guide](05_docker.md) for building and running the app.
