# Virtual Environments and pip

## What is it?

- **pip** is Python's package manager — it installs third-party libraries from PyPI.
- A **virtual environment (venv)** is an isolated folder that has its own Python and installed packages, separate from your system Python.

Think of a venv like a separate workspace:
> Each project gets its own toolbox so tools from one project don't interfere with another.

## Why is it useful?

- **Avoid conflicts** — Project A might need `requests 2.25` while Project B needs `requests 2.31`. Each venv keeps them separate.
- **Reproducible** — You can share a `requirements.txt` so anyone can set up the same environment.
- **Clean uninstall** — Delete the venv folder and everything installed in it is gone.

## Creating a Virtual Environment

```bash
# Create a venv called 'venv'
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Your prompt will change to show (venv)
```

## Using pip

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.31.0

# Upgrade a package
pip install --upgrade requests

# Uninstall
pip uninstall requests

# See what's installed
pip list

# Save current packages to a file
pip freeze > requirements.txt

# Install from a requirements file
pip install -r requirements.txt
```

## Example — Full Workflow

```bash
# 1. Create and activate venv
python -m venv myproject_env
myproject_env\Scripts\activate       # Windows

# 2. Install packages
pip install flask requests

# 3. Save dependencies
pip freeze > requirements.txt

# 4. Share with a teammate — they run:
pip install -r requirements.txt
```

## Key Points

- **Always use a venv** for real projects — never install packages globally.
- Add `venv/` (or your venv folder name) to `.gitignore` so it doesn't get committed.
- `requirements.txt` is the standard way to document your project's dependencies.

---
Previous: [15_args_and_kwargs.md](15_args_and_kwargs.md)
---
