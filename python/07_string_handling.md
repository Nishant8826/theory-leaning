# String Handling

## What is it?

A **string** is a sequence of characters — basically, text.  
In Python, strings are surrounded by quotes:

```python
single = 'Hello'
double = "Hello"
multi  = """This is
a multi-line string."""
```

All three are valid. Use whichever feels natural; pick `"""triple quotes"""` when you need multiple lines.

## Why is it useful?

Strings are everywhere — usernames, messages, file paths, URLs, emails.  
Knowing how to create, combine, search, and modify strings is essential.

## Example

```python
name = "  Alice Wonder  "

# Common string operations
print(name.strip())        # "Alice Wonder"  — remove extra spaces
print(name.lower())        # "  alice wonder  "
print(name.upper())        # "  ALICE WONDER  "
print(name.replace("Wonder", "Smith"))  # "  Alice Smith  "
print(name.strip().split(" "))          # ['Alice', 'Wonder']
```

## Explanation of Example

| Method        | What it does                              |
|---------------|-------------------------------------------|
| `strip()`     | Removes leading and trailing whitespace   |
| `lower()`     | Converts all characters to lowercase      |
| `upper()`     | Converts all characters to uppercase      |
| `replace(a,b)`| Replaces occurrences of `a` with `b`     |
| `split(sep)`  | Splits the string into a list             |

## String Concatenation

```python
first = "Hello"
last = "World"

# Using +
print(first + " " + last)   # Hello World

# Using f-strings (recommended)
print(f"{first} {last}")    # Hello World

# Using .join()
print(" ".join([first, last]))  # Hello World
```

## Checking Content

```python
msg = "Hello, World!"

print(msg.startswith("Hello"))   # True
print(msg.endswith("!"))         # True
print("World" in msg)            # True
print(msg.find("World"))         # 7  (index where it starts)
```

## Accessing Characters

```python
word = "Python"

print(word[0])      # P
print(word[-1])     # n
print(word[0:3])    # Pyt  (slicing)
print(len(word))    # 6
```

## Quick Tips

- Strings are **immutable** — you can't change them in place. Methods like `.upper()` return a *new* string.
- Use `\n` for a new line inside a string and `\t` for a tab.

---

> 📁 **Next:** [[Error Handling]→](./08_error_handling.md)
