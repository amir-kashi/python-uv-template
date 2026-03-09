# Python UV Template

A modern Python project template with:

- `src/app` layout for clean imports
- `uv` for dependency and environment management
- Pre-commit hooks (Black, Ruff, trailing-whitespace)
- Logging setup with `configs/logging_config.ini` and `logs/` folder
- Pytest for testing
- Docker-ready for production deployment

This template is designed as a **starting point for any Python project**, whether backend services, scripts, or ML/AI pipelines.

---

## Using as Template

1. Copy this repository as a starting point for your new project.
2. Rename your project in `pyproject.toml`:

```toml
[project]
name = "my-new-project"
```

3. Run `uv sync` to regenerate the lock file.
4. Update `src/app/` package name if desired (also update imports if necessary).
5. Adjust logging, scripts, and configs for your new project.

---

## Documentation

See `docs/` for:

* [Quick Start](docs/01_quick_start.md)
* [Project Structure](docs/02_project_structure.md)
* [Dependency Management](docs/03_dependencies.md)
* [Pre commit Hooks](docs/04_pre_commit_hooks.md)
* [Docker Deployment](docs/05_docker.md)
* [CI/CD Setup](docs/06_cicd.md)
* [Azure Setup](docs/07_azure_setup.md)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
