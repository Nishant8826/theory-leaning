# List, Dict, and Set Comprehensions

## Simple Explanation

A **comprehension** is a short, clean way to create a list, dictionary, or set in **one line** — instead of writing a full loop.

> Normal way — 4 lines:
> ```python
> squares = []
> for x in range(1, 6):
>     squares.append(x ** 2)
> ```
> Comprehension way — 1 line:
> ```python
> squares = [x ** 2 for x in range(1, 6)]
> ```

Same result. Shorter code. More "Pythonic"!

---

## Real-World Example

Think of a **product catalog tool** for an e-commerce app:
- **Get all product names in uppercase** → use list comprehension
- **Get only in-stock products** → filter with a condition
- **Map product ID to price** → use dict comprehension
- **Get unique categories** → use set comprehension

---

## Code Example — List Comprehension

```python
# E-commerce: apply 10% discount to all prices
prices = [100, 250, 500, 750, 1000]
discounted = [round(p * 0.90, 2) for p in prices]
print("Discounted:", discounted)

# Keep only expensive items (price > 400)
premium = [p for p in prices if p > 400]
print("Premium items:", premium)

# Get product names in uppercase
products = ["shirt", "pants", "jacket", "shoes"]
upper_products = [p.upper() for p in products]
print("Products:", upper_products)
```

**Output:**
```
Discounted: [90.0, 225.0, 450.0, 675.0, 900.0]
Premium items: [500, 750, 1000]
Products: ['SHIRT', 'PANTS', 'JACKET', 'SHOES']
```

---

## Code Example — Dict Comprehension

```python
# Map product names to their discounted prices
products = {"Shirt": 500, "Pants": 800, "Jacket": 1200}

# Apply 20% discount
sale_prices = {name: round(price * 0.80, 2) for name, price in products.items()}
print(sale_prices)
# {'Shirt': 400.0, 'Pants': 640.0, 'Jacket': 960.0}

# Flip keys and values
id_to_name = {1: "Rahul", 2: "Priya", 3: "Arjun"}
name_to_id = {name: id for id, name in id_to_name.items()}
print(name_to_id)
# {'Rahul': 1, 'Priya': 2, 'Arjun': 3}
```

---

## Code Example — Set Comprehension

```python
# Get unique first letters from a list of tags
tags = ["python", "programming", "pandas", "react", "redux", "ruby"]
first_letters = {tag[0] for tag in tags}
print(first_letters)   # {'p', 'r'} — only unique letters
```

---

## The General Pattern

```
List:   [expression  for item in iterable  if condition]
Dict:   {key: value  for item in iterable  if condition}
Set:    {expression  for item in iterable  if condition}
```

| Part           | What it means           |
|----------------|-------------------------|
| `expression`   | What each new item should be |
| `for item in`  | The loop source          |
| `if condition` | Optional filter          |

---

## When NOT to Use a Comprehension

- When the logic is complex — use a regular `for` loop for clarity.
- When you need side effects (like printing inside the loop).

> **Rule of thumb:** If it doesn't fit comfortably on one line, write a loop instead.

---

## Practice Tasks

- **Task 1 (Easy):** Create a list of squares of numbers from 1 to 10 using a list comprehension.
- **Task 2 (Easy):** From `[1, 2, 3, 4, 5, 6, 7, 8]`, use a comprehension to get only odd numbers.
- **Task 3 (Medium):** Given a list of names `["rahul", "priya", "arjun"]`, create a new list with names capitalized and only those with name length > 4.
- **Task 4 (Medium):** Create a dictionary `{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}` using dict comprehension.
- **Task 5 (Medium):** Given a list of words, create a set of unique word lengths using set comprehension.

---

## Interview Questions

- **Q1: What is a list comprehension?**  
  A: A short one-line way to create a list using a loop and optional condition inside `[]`.

- **Q2: What is the general syntax of a list comprehension?**  
  A: `[expression for item in iterable if condition]`.

- **Q3: Are list comprehensions faster than regular loops?**  
  A: Generally yes — they are optimized internally by Python.

- **Q4: What is the difference between a list and set comprehension?**  
  A: List comprehension uses `[]` and allows duplicates. Set comprehension uses `{}` and gives unique values.

- **Q5: Can you add a condition in a comprehension?**  
  A: Yes. Add `if condition` at the end: `[x for x in list if x > 0]`.

- **Q6: What is a dict comprehension?**  
  A: A one-line way to create a dictionary: `{key: value for item in iterable}`.

- **Q7: When should you avoid comprehensions?**  
  A: When the logic is complex or has nested conditions — a regular loop is more readable.

---

⬅️ Prev: [Decorators](./13_decorators.md) | Next ➡️: [*args and **kwargs](./15_args_and_kwargs.md)
