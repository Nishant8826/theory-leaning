# Error Handling (try / except)

## What is it?

Errors (also called **exceptions**) happen when something goes wrong while your program is running — like dividing by zero or opening a file that doesn't exist.

**Error handling** lets you catch these problems and deal with them *gracefully* instead of crashing.

```python
try:
    # code that might fail
except SomeError:
    # what to do if it fails
```

## Why is it useful?

- Prevents your program from crashing unexpectedly.
- Lets you show a friendly message instead of a scary error.
- Helps you handle edge cases (bad user input, missing files, network issues).

## Example

```python
try:
    num = int(input("Enter a number: "))
    result = 100 / num
    print(f"100 / {num} = {result}")

except ValueError:
    print("That's not a valid number!")

except ZeroDivisionError:
    print("You can't divide by zero!")

except Exception as e:
    print(f"Something unexpected happened: {e}")

finally:
    print("This always runs, no matter what.")
```

## Explanation of Example

1. The `try` block contains code that *might* fail.
2. If the user types a letter instead of a number → `ValueError` is caught.
3. If the user types `0` → `ZeroDivisionError` is caught.
4. `Exception as e` is a catch-all for anything else.
5. `finally` runs no matter what — success or failure.  
   It's handy for cleanup tasks (closing files, releasing resources).

## Common Exceptions

| Exception           | When it happens                         |
|---------------------|-----------------------------------------|
| `ValueError`        | Wrong type of value (e.g., `int("abc")`)|
| `ZeroDivisionError` | Dividing by zero                        |
| `FileNotFoundError` | File doesn't exist                      |
| `IndexError`        | List index out of range                 |
| `KeyError`          | Dictionary key not found                |
| `TypeError`         | Wrong type in operation                 |

## Raising Your Own Errors

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    print(f"Age set to {age}")

try:
    set_age(-5)
except ValueError as e:
    print(e)   # Age cannot be negative!
```

---

> 📁 **Next:** [[Modules and Imports]→](./09_modules_and_imports.md)
