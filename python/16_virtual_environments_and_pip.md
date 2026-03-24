# Virtual Environments and pip

## Simple Explanation

**pip** = Python's package manager. It installs libraries from the internet (PyPI).

**Virtual Environment (venv)** = an isolated workspace for a Python project.  
It has its own Python and its own installed packages — completely separate from your system.

> Think of it like **having a different toolbox for each project**:  
> Your web app project has its own tools.  
> Your data analysis project has its own tools.  
> They don't mix or interfere with each other.

---

## Real-World Example

Imagine you're working on **two projects**:
- **Project A** (old) → needs `django==3.2`
- **Project B** (new) → needs `django==5.0`

If you install both globally on your computer, they'll **conflict**!  
With virtual environments, each project gets its own `django` version and everything works perfectly.

---

## Creating and Activating a Virtual Environment

```bash
# Step 1: Create a virtual environment folder called 'venv'
python -m venv venv

# Step 2: Activate it
# On Windows:
venv\Scripts\activate

# On macOS / Linux:
source venv/bin/activate

# Your terminal prompt will change to show (venv) — now you're inside!
```

---

## Using pip (After Activating venv)

```bash
# Install a package
pip install requests

# Install a specific version
pip install django==5.0

# Upgrade a package
pip install --upgrade requests

# Uninstall a package
pip uninstall requests

# See all installed packages
pip list

# Save all installed packages to a file (for sharing)
pip freeze > requirements.txt

# Install from a requirements file (used by teammates to match your setup)
pip install -r requirements.txt
```

---

## Code Example — Full Workflow

```bash
# Starting a new project → follow these steps every time:

# 1. Create the virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install the packages you need
pip install flask requests python-dotenv

# 4. Save your packages list
pip freeze > requirements.txt

# 5. When done, deactivate
deactivate
```

**Sharing with a teammate:**
```bash
# Teammate clones your repo and runs:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# ✅ Exact same setup in minutes!
```

---

## The `requirements.txt` File

This file lists all your project's dependencies:

```
flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
```

- Generated with `pip freeze > requirements.txt`
- Installed with `pip install -r requirements.txt`
- **Always commit this file** to Git (so teammates can replicate your environment)

---

## What to Add to `.gitignore`

```
venv/
__pycache__/
*.pyc
.env
```

> ⚠️ **Never commit the `venv/` folder** — it's large and machine-specific. Share `requirements.txt` instead.

---

## Quick Tips

- **Always create a venv** for every new project.
- **Always activate** the venv before installing packages.
- Use `pip list` to see what's currently installed.
- Use `pip show flask` to see details about a specific package.

---

## Practice Tasks

- **Task 1 (Easy):** Create a new virtual environment called `myenv`. Activate it. Run `pip list` and note the default packages.
- **Task 2 (Easy):** Install the `requests` library inside your venv and verify with `pip list`.
- **Task 3 (Medium):** Install `flask` and `python-dotenv`. Generate a `requirements.txt` file.
- **Task 4 (Medium):** Deactivate your venv. Create a fresh venv `myenv2`. Install dependencies from the `requirements.txt` you created.
- **Task 5 (Medium):** Write a small Python script that imports `requests` and fetches data from `https://jsonplaceholder.typicode.com/todos/1`. Print the response.

---

## Interview Questions

- **Q1: What is `pip`?**  
  A: Python's package manager. Used to install, update, and uninstall third-party libraries.

- **Q2: What is a virtual environment?**  
  A: An isolated Python environment for a project with its own packages — prevents conflicts between projects.

- **Q3: Why should you use a virtual environment?**  
  A: To avoid version conflicts between projects and keep your global Python clean.

- **Q4: What is `requirements.txt`?**  
  A: A file that lists all installed packages and their versions. Created with `pip freeze > requirements.txt`.

- **Q5: How do you install all dependencies from a `requirements.txt`?**  
  A: Run `pip install -r requirements.txt`.

- **Q6: Should you commit the `venv/` folder to Git?**  
  A: No. Add it to `.gitignore`. Only commit `requirements.txt`.

- **Q7: What is the difference between `pip install` and `pip install -r`?**  
  A: `pip install package` installs a single package. `pip install -r file.txt` installs all packages listed in the file.

---

⬅️ Prev: [*args and **kwargs](./15_args_and_kwargs.md) | Next ➡️: End
