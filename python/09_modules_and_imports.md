# Modules and Imports

## What is it?

A **module** is simply a Python file (`.py`) that contains functions, classes, or variables you can reuse.

**Importing** means bringing code from a module into your program so you can use it.

Python comes with a huge **standard library** of built-in modules — you don't need to install anything extra for them.

## Why is it useful?

- **Saves time** — use ready-made code instead of writing everything from scratch.
- **Keeps projects organized** — split your code into separate files/modules.
- **Huge ecosystem** — thousands of third-party packages on PyPI (installed with `pip`).

## Example

```python
# Import the entire module
import math

print(math.sqrt(16))     # 4.0
print(math.pi)           # 3.141592653589793

# Import specific items
from math import ceil, floor

print(ceil(4.2))   # 5
print(floor(4.8))  # 4

# Import with an alias
import datetime as dt

now = dt.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
```

## Explanation of Example

1. `import math` — loads the whole `math` module; access with `math.xxx`.
2. `from math import ceil, floor` — loads only what you need; no prefix required.
3. `import datetime as dt` — gives it a shorter nickname for convenience.

## Some Handy Built-in Modules

| Module      | What it does                          |
|-------------|---------------------------------------|
| `math`      | Math functions (sqrt, pi, ceil …)     |
| `random`    | Generate random numbers               |
| `os`        | Interact with the operating system    |
| `datetime`  | Work with dates and times             |
| `json`      | Read and write JSON data              |
| `pathlib`   | Modern way to work with file paths    |
| `sys`       | System-specific parameters            |

## Creating Your Own Module

1. Create a file called `helpers.py`:

```python
# helpers.py
def greet(name):
    return f"Hello, {name}!"
```

2. Use it in another file:

```python
# main.py
from helpers import greet

print(greet("Alice"))   # Hello, Alice!
```

## Installing Third-Party Packages

```bash
pip install requests   # a popular package for HTTP requests
```

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)   # 200
```
