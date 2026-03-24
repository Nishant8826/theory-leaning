# Error Handling (try / except)

## Simple Explanation

An **error** (also called an **exception**) happens when something goes wrong while your code is running — like dividing by zero, or typing text where a number was expected.

Instead of letting your program **crash**, you can **catch** the error and handle it gracefully.

```python
try:
    # code that might fail
except SomeError:
    # what to do when it fails
```

> Think of it like a safety net under a trapeze artist.  
> If they fall → the net catches them and they don't get hurt.

---

## Real-World Example

Think of an **ATM machine**:
- If you enter letters instead of an amount → show "Invalid input" (not crash)
- If your balance is too low → show "Insufficient funds" (not crash)
- If the network is down → show "Service unavailable" (not crash)

Error handling keeps your app running smoothly even when things go wrong!

---

## Code Example

```python
def withdraw(balance, amount):
    try:
        amount = float(amount)

        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        if amount > balance:
            raise ValueError("Insufficient balance.")

        balance -= amount
        print(f"✅ Withdrawn ₹{amount}. Remaining: ₹{balance}")
        return balance

    except ValueError as e:
        print(f"❌ Error: {e}")
        return balance
    
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return balance
    
    finally:
        print("Transaction complete.")

# Test it
withdraw(5000, 2000)   # works fine
withdraw(5000, "abc")  # ValueError — not a number
withdraw(5000, 9000)   # ValueError — insufficient balance
```

**Output:**
```
✅ Withdrawn ₹2000.0. Remaining: ₹3000.0
Transaction complete.
❌ Error: could not convert string to float: 'abc'
Transaction complete.
❌ Error: Insufficient balance.
Transaction complete.
```

---

## Common Exceptions

| Exception             | When it happens                          |
|-----------------------|------------------------------------------|
| `ValueError`          | Wrong type of value (e.g., `int("abc")`) |
| `ZeroDivisionError`   | Dividing by zero                         |
| `FileNotFoundError`   | File doesn't exist                       |
| `IndexError`          | List index out of range                  |
| `KeyError`            | Dictionary key not found                 |
| `TypeError`           | Wrong type in operation                  |
| `AttributeError`      | Calling a method that doesn't exist      |

---

## `finally` Block

The `finally` block **always runs** — whether an error happened or not.  
Use it for cleanup: closing files, logging, showing "done" messages.

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    print("Finished reading attempt.")  # always runs
```

---

## Raising Your Own Errors

```python
def set_age(age):
    if age < 0 or age > 150:
        raise ValueError(f"Invalid age: {age}")
    print(f"Age set to {age}")

try:
    set_age(-5)
except ValueError as e:
    print(e)   # Invalid age: -5
```

---

## Practice Tasks

- **Task 1 (Easy):** Write a program that asks for a number and divides 100 by it. Handle `ZeroDivisionError`.
- **Task 2 (Easy):** Ask the user for their age. Handle the case where they type letters instead of a number.
- **Task 3 (Medium):** Open a file called `"data.txt"`. If it doesn't exist, print a friendly message using `FileNotFoundError`.
- **Task 4 (Medium):** Write a function `get_item(my_list, index)` that returns the item at that index, handling `IndexError`.
- **Task 5 (Medium):** Create a login function that raises `PermissionError` if the username is "banned". Catch and handle it properly.

---

## Interview Questions

- **Q1: What is exception handling in Python?**  
  A: A way to catch and manage runtime errors so the program doesn't crash.

- **Q2: What is the difference between `try` and `except`?**  
  A: `try` contains the code that might fail. `except` contains the code to run if it does fail.

- **Q3: What does the `finally` block do?**  
  A: It always runs, whether an error occurred or not. Used for cleanup tasks.

- **Q4: How do you raise your own exception?**  
  A: Use `raise ExceptionType("message")`. Example: `raise ValueError("Invalid input")`.

- **Q5: What is the difference between `Exception` and specific exceptions like `ValueError`?**  
  A: `Exception` catches all errors. Specific ones like `ValueError` catch only that type. Always prefer specific ones.

- **Q6: Can you have multiple `except` blocks?**  
  A: Yes. Each handles a different type of error.

- **Q7: What is `else` in a try block?**  
  A: `else` runs only if the `try` block succeeded (no error occurred).

---

⬅️ Prev: [String Handling](./07_string_handling.md) | Next ➡️: [Modules and Imports](./09_modules_and_imports.md)
