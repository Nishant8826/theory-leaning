# Decorators

## Simple Explanation

A **decorator** is a function that **wraps another function** to add extra behavior — *without changing the original function*.

> Think of it like gift wrapping:  
> The gift (your function) stays the same.  
> The wrapper (decorator) adds pretty packaging on top.

You apply a decorator using the `@` symbol above a function:

```python
@my_decorator
def my_function():
    ...
```

---

## Real-World Example

Think of a **website with login protection**:
- Some pages are **public** — anyone can visit.
- Some pages **require login** — you must be logged in first.

Instead of checking login inside every function, you create a `@login_required` decorator and just put it on top of protected functions.

Also in real apps, decorators are used for:
- **Logging** — record every time a function is called
- **Timing** — measure how long a function takes
- **Access control** — check if user has permission

---

## Code Example — Basic Decorator

```python
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"📋 [LOG] Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"✅ [LOG] {func.__name__} finished.")
        return result
    return wrapper


@log_action
def transfer_money(sender, receiver, amount):
    print(f"💸 Transferring ₹{amount} from {sender} to {receiver}")


transfer_money("Rahul", "Priya", 500)
```

**Output:**
```
📋 [LOG] Calling: transfer_money
💸 Transferring ₹500 from Rahul to Priya
✅ [LOG] transfer_money finished.
```

---

## Code Example — Timer Decorator

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


@timer
def process_orders(count):
    time.sleep(0.5)   # simulate processing time
    print(f"Processed {count} orders.")


process_orders(100)
```

**Output:**
```
Processed 100 orders.
⏱️ process_orders took 0.5001 seconds
```

---

## How It Works (Step by Step)

```python
@log_action
def transfer_money(...):
    ...

# The above is exactly the same as:
transfer_money = log_action(transfer_money)
```

1. `log_action` receives `transfer_money` as input.
2. It creates a `wrapper` function that runs extra code before/after.
3. `wrapper` is returned and replaces `transfer_money`.
4. When you call `transfer_money(...)`, you're actually calling `wrapper(...)`.

---

## Key Points

- `*args, **kwargs` in `wrapper` makes your decorator work with **any** function signature.
- Always **return the result** from `wrapper` so the original return value isn't lost.
- You can **stack multiple decorators** on one function:

```python
@log_action
@timer
def my_function():
    pass
```

---

## Practice Tasks

- **Task 1 (Easy):** Create a decorator `shout` that converts the return value of any function to uppercase.
- **Task 2 (Easy):** Create a decorator `greet_wrapper` that prints "Good morning!" before calling the function and "Goodbye!" after.
- **Task 3 (Medium):** Create a `@timer` decorator and apply it to a function that calculates the sum of numbers 1 to 1,000,000.
- **Task 4 (Medium):** Create a `@login_required` decorator that checks a variable `is_logged_in`. If `True`, call the function; if `False`, print "Access denied!".
- **Task 5 (Medium):** Create a decorator that counts how many times a function has been called and prints the count each time.

---

## Interview Questions

- **Q1: What is a decorator in Python?**  
  A: A function that wraps another function to add extra behavior without changing the original code.

- **Q2: How do you apply a decorator?**  
  A: Put `@decorator_name` on the line above the function definition.

- **Q3: Why do we use `*args, **kwargs` in the wrapper?**  
  A: So the decorator works with functions that have any number and type of arguments.

- **Q4: What does `@my_decorator` mean under the hood?**  
  A: It's shorthand for `func = my_decorator(func)`.

- **Q5: What is a real-world use of decorators?**  
  A: Logging, timing, authentication checks, caching, rate limiting.

- **Q6: Can you apply multiple decorators to one function?**  
  A: Yes. They apply from bottom to top (innermost first).

- **Q7: What is `functools.wraps` and why is it used?**  
  A: It preserves the original function's name and docstring when using decorators. Used inside `wrapper` as `@functools.wraps(func)`.

---

⬅️ Prev: [Lambda, Map, and Filter](./12_lambda_map_filter.md) | Next ➡️: [Comprehensions](./14_comprehensions.md)
