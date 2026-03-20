# Decorators

## What is it?

A **decorator** is a function that wraps another function to add extra behavior — *without changing the original function's code*.

Think of it like gift wrapping:
> The gift (original function) stays the same, but you add a nice wrapper around it.

In Python, you apply a decorator with the `@` symbol above a function definition.

## Why is it useful?

- Add logging, timing, or access control to functions without modifying them.
- Keep your code clean — separate "what the function does" from "extra stuff around it".
- Very common in web frameworks (Flask, Django) and testing.

## Example

```python
def my_decorator(func):
    def wrapper():
        print("--- Before the function runs ---")
        func()
        print("--- After the function runs ---")
    return wrapper


@my_decorator
def say_hello():
    print("Hello!")


say_hello()
```

**Output:**
```
--- Before the function runs ---
Hello!
--- After the function runs ---
```

## Explanation of Example

1. `my_decorator` is a function that takes another function (`func`) as input.
2. Inside, it defines `wrapper()` — which runs some code before and after `func()`.
3. `@my_decorator` is shorthand for `say_hello = my_decorator(say_hello)`.
4. When we call `say_hello()`, we're actually calling `wrapper()`, which in turn calls the original `say_hello()`.

## Practical Example — Timing a Function

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


@timer
def slow_add(a, b):
    time.sleep(1)
    return a + b


print(slow_add(3, 5))
# slow_add took 1.00xx seconds
# 8
```

## Key Points

- `*args, **kwargs` in `wrapper` make the decorator work with any number of arguments.
- Always return `result` from `wrapper` so the original return value isn't lost.
- You can stack multiple decorators on one function (they apply bottom-up).

---

> 📁 **Next:** [[List, Dict, and Set Comprehensions]→](./14_comprehensions.md)
