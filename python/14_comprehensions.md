# List, Dict, and Set Comprehensions

## What is it?

A **comprehension** is a short, elegant way to create a list, dictionary, or set in a single line.

Instead of writing a full `for` loop, you express the transformation right inside the brackets.

## Why is it useful?

- **Cleaner code** — one line instead of four.
- **Faster** — comprehensions are optimized internally by Python.
- **Pythonic** — it's the "Python way" of doing things.

## List Comprehension

```python
# Traditional loop
squares = []
for x in range(1, 6):
    squares.append(x ** 2)

# Comprehension — same result
squares = [x ** 2 for x in range(1, 6)]
print(squares)   # [1, 4, 9, 16, 25]
```

### With a Condition

```python
# Only even squares
even_squares = [x ** 2 for x in range(1, 11) if x % 2 == 0]
print(even_squares)   # [4, 16, 36, 64, 100]
```

## Dict Comprehension

```python
# Square mapping: {number: square}
sq_map = {x: x ** 2 for x in range(1, 6)}
print(sq_map)   # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
flipped = {v: k for k, v in original.items()}
print(flipped)   # {1: 'a', 2: 'b', 3: 'c'}
```

## Set Comprehension

```python
# Unique first letters from a list of words
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
first_letters = {w[0] for w in words}
print(first_letters)   # {'a', 'b', 'c'}
```

## Explanation of Example

The general pattern is:

```
[expression  for item in iterable  if condition]
{key: value  for item in iterable  if condition}
{expression  for item in iterable  if condition}
```

1. **expression** — what you want each new item to be.
2. **for item in iterable** — the loop.
3. **if condition** (optional) — a filter.

## When NOT to Use a Comprehension

- When the logic is complex or has multiple `if/else` branches — use a regular loop for clarity.
- When you need to perform side effects (like printing) — `for` loop is better.

> **Rule of thumb:** If the comprehension doesn't fit on one comfortable line, use a loop.
