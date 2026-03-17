# Lambda, Map, and Filter

## What is it?

### Lambda
A **lambda** is a tiny, one-line function without a name (also called an *anonymous function*).

```python
# Regular function
def double(x):
    return x * 2

# Same thing as a lambda
double = lambda x: x * 2
```

### Map
`map()` applies a function to **every item** in a list (or other iterable) and returns the results.

### Filter
`filter()` keeps only the items that pass a **condition** (return `True`).

## Why is it useful?

- Write short, clean code for simple transformations.
- Quickly process every item in a list without writing a loop.
- Very common in data processing and functional programming.

## Example

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Double every number using map + lambda
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)   # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Keep only even numbers using filter + lambda
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)     # [2, 4, 6, 8, 10]
```

## Explanation of Example

1. `lambda x: x * 2` — a quick function that takes `x` and returns `x * 2`.
2. `map(func, numbers)` — runs `func` on each number. We wrap it in `list()` to see the result.
3. `filter(func, numbers)` — keeps only items where `func` returns `True`.

## List Comprehension Alternative

You can often use list comprehensions instead:

```python
doubled = [x * 2 for x in numbers]
evens   = [x for x in numbers if x % 2 == 0]
```

Both approaches are fine — use whichever reads better for your situation.

## When to Use Lambda

✅ Great for short, simple operations passed to `map()`, `filter()`, or `sorted()`.  
❌ Avoid for complex logic — use a regular `def` function instead.

```python
# Sorting a list of tuples by the second element
pairs = [(1, "banana"), (3, "apple"), (2, "cherry")]
pairs.sort(key=lambda item: item[1])
print(pairs)
# [(3, 'apple'), (1, 'banana'), (2, 'cherry')]
```
