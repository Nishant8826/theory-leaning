# String Handling

## Simple Explanation

A **string** is text — any sequence of letters, numbers, or symbols wrapped in quotes.

```python
name = "Rahul"
message = 'Hello, World!'
address = """123 Main Street,
Delhi, India"""
```

Strings are used **everywhere** — usernames, email addresses, messages, URLs, file paths.

---

## Real-World Example

Think of a **user registration form**:
- Name: `"Rahul Sharma"` → trim spaces, convert to title case
- Email: `"rahul@email.com"` → check if it contains `@`
- Password: `"pass123"` → check length ≥ 8 characters

All of these operations use **string methods**!

---

## Code Example

```python
# Simulating form data received from user
raw_name = "  rahul sharma  "
email = "Rahul@Email.COM"
password = "pass123"

# Clean up the name
clean_name = raw_name.strip().title()
print(clean_name)          # Rahul Sharma

# Normalize the email
clean_email = email.lower()
print(clean_email)         # rahul@email.com

# Check email format
if "@" in clean_email:
    print("✅ Valid email")
else:
    print("❌ Invalid email")

# Validate password length
if len(password) >= 8:
    print("✅ Password strong enough")
else:
    print("❌ Password too short")

# Replace part of a string
masked_email = clean_email.replace(clean_email.split("@")[0], "****")
print(masked_email)        # ****@email.com
```

---

## Common String Methods

| Method              | What it does                             | Example                          |
|---------------------|------------------------------------------|----------------------------------|
| `strip()`           | Remove spaces from both sides            | `"  hi  ".strip()` → `"hi"`     |
| `lower()`           | Convert to lowercase                     | `"HELLO".lower()` → `"hello"`   |
| `upper()`           | Convert to uppercase                     | `"hello".upper()` → `"HELLO"`   |
| `title()`           | Capitalize each word                     | `"rahul sharma".title()`         |
| `replace(a, b)`     | Replace `a` with `b`                     | `"bad word".replace("bad","good")` |
| `split(sep)`        | Split into a list                        | `"a,b,c".split(",")` → `['a','b','c']` |
| `join(list)`        | Join a list into a string                | `" ".join(["Hi","Rahul"])`       |
| `startswith(x)`     | Check if starts with `x`                | `"Hello".startswith("He")` → `True` |
| `endswith(x)`       | Check if ends with `x`                  | `"file.pdf".endswith(".pdf")`    |
| `find(x)`           | Find index of `x` (-1 if not found)     | `"hello".find("ll")` → `2`      |
| `len(s)`            | Number of characters                     | `len("Python")` → `6`           |

---

## String Concatenation and f-strings

```python
first = "Rahul"
last = "Sharma"

# Using + (not recommended for many variables)
print("Hello, " + first + " " + last + "!")

# Using f-string (recommended ✅)
print(f"Hello, {first} {last}!")

# With calculation
price = 500
qty = 3
print(f"Total: ₹{price * qty}")
```

---

## Accessing Characters

```python
word = "Python"

print(word[0])      # P  (first character)
print(word[-1])     # n  (last character)
print(word[0:3])    # Pyt (slicing — first 3 chars)
print(word[::-1])   # nohtyP (reverse the string)
```

---

## Quick Tips

- Strings are **immutable** — methods don't change the original, they return a new string.
- Use `\\n` for a new line inside a string.
- Use `\\t` for a tab inside a string.

---

## Practice Tasks

- **Task 1 (Easy):** Take a name with extra spaces (`"  John  "`) and print it cleaned and uppercase.
- **Task 2 (Easy):** Check if an email string contains `"@"`. Print valid/invalid.
- **Task 3 (Medium):** Ask user for a sentence. Count how many words it has using `.split()`.
- **Task 4 (Medium):** Ask for a username. Validate: must be 4–15 characters long, print pass/fail.
- **Task 5 (Medium):** Reverse a string entered by the user and check if it's a palindrome (e.g., `"madam"` → same when reversed).

---

## Interview Questions

- **Q1: Are strings mutable in Python?**  
  A: No. Strings are immutable — you cannot change them in place. Methods return new strings.

- **Q2: How do you reverse a string in Python?**  
  A: `text[::-1]` — slicing with step `-1`.

- **Q3: What is the difference between `find()` and `index()`?**  
  A: `find()` returns `-1` if not found. `index()` raises a `ValueError` if not found.

- **Q4: How do you check if a string contains a substring?**  
  A: Use `in`: `if "hello" in text:`.

- **Q5: What is an f-string?**  
  A: A formatted string using `f"..."` syntax where you can embed variables inside `{}`.

- **Q6: How do you split a sentence into words?**  
  A: `sentence.split()` — splits on spaces by default.

- **Q7: How do you join a list of strings into one string?**  
  A: `" ".join(["Hello", "World"])` → `"Hello World"`.

---

⬅️ Prev: [Tuples, Sets, and Dictionaries](./06_tuples_sets_and_dictionaries.md) | Next ➡️: [Error Handling](./08_error_handling.md)
