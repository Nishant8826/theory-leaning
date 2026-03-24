# Modules and Imports

## Simple Explanation

A **module** is just a Python file (`.py`) that has useful functions, classes, or variables inside it.

**Importing** means bringing that code into your file so you can use it.

> Think of modules like apps on your phone.  
> You don't build Calculator from scratch — you just open it.  
> Modules = ready-made tools, you just import and use them.

---

## Real-World Example

Think of building an **e-commerce app**:
- You need math → import `math`
- You need to generate order IDs → import `uuid`
- You need today's date on receipts → import `datetime`
- You need to read product data from JSON → import `json`

All these are **built-in Python modules** — free and ready to use!

---

## Code Example

```python
# Import the entire module
import math
import random
import datetime

# Math — calculate discount price
original_price = 1000
discount = 15  # 15%
final_price = original_price - (original_price * discount / 100)
print(f"Final Price: ₹{final_price}")
print(f"Square root of 144: {math.sqrt(144)}")

# Random — pick a lucky winner from a list
participants = ["Rahul", "Priya", "Arjun", "Neha"]
winner = random.choice(participants)
print(f"🎉 Lucky winner: {winner}")

# Datetime — show today's date on receipt
today = datetime.date.today()
print(f"Receipt Date: {today}")
```

**Output (example):**
```
Final Price: ₹850.0
Square root of 144: 12.0
🎉 Lucky winner: Priya
Receipt Date: 2026-03-24
```

---

## Ways to Import

```python
# Import entire module — access with module.name
import math
print(math.pi)           # 3.14159...

# Import specific items — no prefix needed
from math import sqrt, ceil
print(sqrt(25))          # 5.0
print(ceil(4.2))         # 5

# Import with a shorter alias
import datetime as dt
print(dt.date.today())
```

---

## Handy Built-in Modules

| Module      | What it does                             |
|-------------|------------------------------------------|
| `math`      | Math functions: `sqrt`, `ceil`, `pi`...  |
| `random`    | Random numbers, shuffling, choices       |
| `os`        | Interact with the file system/OS         |
| `datetime`  | Work with dates and times                |
| `json`      | Read/write JSON data                     |
| `time`      | Delays, measuring time                   |
| `sys`       | System info and settings                 |
| `uuid`      | Generate unique IDs                      |

---

## Creating Your Own Module

**Step 1** — Create `helpers.py`:
```python
# helpers.py
def greet(name):
    return f"Hello, {name}! Welcome."

def calculate_tax(amount, rate=18):
    return amount * rate / 100
```

**Step 2** — Use it in `main.py`:
```python
# main.py
from helpers import greet, calculate_tax

print(greet("Rahul"))              # Hello, Rahul! Welcome.
print(calculate_tax(1000))         # 180.0
```

---

## Installing Third-Party Packages with pip

```bash
pip install requests   # for making HTTP calls
pip install flask      # for building web apps
```

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)   # 200
```

---

## Practice Tasks

- **Task 1 (Easy):** Import `math` and print the value of `pi` and the `sqrt` of 81.
- **Task 2 (Easy):** Import `random` and print a random number between 1 and 100.
- **Task 3 (Medium):** Import `datetime` and print today's date in the format `DD/MM/YYYY`.
- **Task 4 (Medium):** Create your own module `calculator.py` with `add`, `subtract`, `multiply`, `divide` functions. Import and use them in `main.py`.
- **Task 5 (Medium):** Use `random.shuffle()` to shuffle a list of 5 names and print the result.

---

## Interview Questions

- **Q1: What is a module in Python?**  
  A: A `.py` file containing reusable functions, classes, or variables that can be imported.

- **Q2: What is the difference between `import math` and `from math import sqrt`?**  
  A: `import math` loads the whole module (use `math.sqrt`). `from math import sqrt` loads only `sqrt` (use directly).

- **Q3: What is the Python Standard Library?**  
  A: A huge collection of built-in modules (math, os, json, etc.) that come with Python — no installation needed.

- **Q4: What is `pip`?**  
  A: Python's package manager. Used to install third-party packages from PyPI.

- **Q5: What does `if __name__ == "__main__":` mean?**  
  A: Code inside this block only runs when the file is executed directly, not when it's imported as a module.

- **Q6: What is PyPI?**  
  A: Python Package Index — the official online store for Python packages.

- **Q7: Can you create your own module?**  
  A: Yes. Just create a `.py` file with functions, then use `import filename` to use it in another file.

---

⬅️ Prev: [Error Handling](./08_error_handling.md) | Next ➡️: [File Handling](./10_file_handling.md)
