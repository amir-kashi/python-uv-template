# Pre-commit Hooks

This project uses **pre-commit** to enforce code quality and consistency before changes are committed.

Pre-commit automatically runs checks such as:

- Code formatting (Black)
- Linting (Ruff)
- Trailing whitespace removal
- End-of-file fixes

This helps maintain a clean and consistent codebase.

---

## Why Use Pre-commit?

- Prevents poorly formatted code from being committed
- Reduces CI failures
- Enforces team-wide standards
- Automates repetitive checks

---

## Configuration

Hooks are defined in:

```
.pre-commit-config.yaml
```

Example hooks include:

- Black → code formatter
- Ruff → linter
- Trailing whitespace fixer
- End-of-file fixer

You can add or modify hooks in this file.

---

## Installation (Local Development)

After cloning the repository and syncing dependencies:

```bash
uv run pre-commit install
```

This installs Git hooks locally.

From now on, pre-commit will automatically run on every commit.

---

## Running Hooks Manually

To run hooks against all files:

```bash
uv run pre-commit run --all-files
```

To run hooks on staged files only:

```bash
uv run pre-commit run
```

---

## Skipping Hooks (Not Recommended)

If necessary, you can bypass hooks:

```bash
git commit --no-verify
```

This should only be used in exceptional cases.

---

## Updating Hooks

To update hook versions:

```bash
uv run pre-commit autoupdate
```

Then commit the updated `.pre-commit-config.yaml`.

---

## Best Practices

* Install pre-commit immediately after cloning the project
* Never bypass hooks without reason
* Keep hook versions updated
* Ensure CI also runs linting and tests
