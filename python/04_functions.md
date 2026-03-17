# Functions

## What is it?

A **function** is a reusable block of code that performs a specific task.  
You "define" it once, then "call" it whenever you need it.

Think of a function like a recipe:
> Write the recipe once → cook the dish any time you want.

```python
def function_name(parameters):
    # body
    return result
```

## Why is it useful?

- **Avoids repetition** — write code once, use it many times.
- **Keeps things organized** — break a big program into small, manageable pieces.
- **Easier to debug** — if something is wrong, you only fix it in one place.

## Example

```python
def greet(name):
    """Print a friendly greeting."""
    print(f"Hello, {name}! Welcome aboard.")

# Calling the function
greet("Alice")
greet("Bob")
```

**Output:**
```
Hello, Alice! Welcome aboard.
Hello, Bob! Welcome aboard.
```

## Explanation of Example

1. `def greet(name):` — defines a function called `greet` that takes one parameter `name`.
2. The body uses an f-string to print a personalized message.
3. We call `greet("Alice")` — Python runs the body with `name = "Alice"`.

## Returning Values

A function can **send a result back** using `return`:

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)   # 7
```

Without `return`, the function gives back `None` by default.

## Default Parameters

You can set a default value for a parameter:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Good morning") # Good morning, Bob!
```

## Multiple Return Values

```python
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7, 2])
print(lo, hi)   # 1 7
```
