# File Handling (Read and Write)

## Simple Explanation

**File handling** lets your program read data from files and save data to files on your computer.

> If your program stores data only in variables, everything disappears when the program closes.  
> Files let you **save data permanently** on disk.

Python uses the built-in `open()` function for this.

---

## Real-World Example

Think of a **student report card app**:
- When results are ready → **write** them to `report.txt`
- Next day, a teacher opens the app → **read** from `report.txt`
- A new student joins → **append** their data to the file

Also think of an **activity log** for a website:
- Every user login → append a line to `activity_log.txt`
- Admin wants to check logs → read the file

---

## File Modes

| Mode  | Meaning                                      |
|-------|----------------------------------------------|
| `"r"` | Read — open for reading (file must exist)    |
| `"w"` | Write — create new or overwrite existing     |
| `"a"` | Append — add to the end of existing file     |
| `"x"` | Create — error if file already exists        |

---

## Code Example — Writing to a File

```python
# Save student results to a file
students = [
    ("Rahul", 85),
    ("Priya", 92),
    ("Arjun", 78),
]

with open("results.txt", "w") as f:
    f.write("📋 Exam Results\n")
    f.write("=" * 25 + "\n")
    for name, marks in students:
        f.write(f"{name}: {marks}/100\n")

print("Results saved successfully!")
```

---

## Code Example — Reading from a File

```python
# Read and display the results
with open("results.txt", "r") as f:
    content = f.read()
    print(content)
```

---

## Code Example — Reading Line by Line

```python
# Read and process each line
with open("results.txt", "r") as f:
    for line in f:
        print(line.strip())   # strip() removes trailing newline
```

---

## Code Example — Appending to a File

```python
# Add a new student result without deleting old ones
with open("results.txt", "a") as f:
    f.write("Neha: 95/100\n")

print("New result added!")
```

---

## Why Use `with open(...)` ?

`with` automatically **closes the file** when you're done — even if an error occurs.  
Without `with`, you'd have to call `f.close()` manually.

```python
# Always prefer this:
with open("file.txt", "r") as f:
    data = f.read()

# Avoid this (easy to forget close):
f = open("file.txt", "r")
data = f.read()
f.close()
```

---

## Handling Missing Files Safely

```python
try:
    with open("config.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("❌ Config file not found! Creating a new one...")
    with open("config.txt", "w") as f:
        f.write("default=true\n")
```

---

## Practice Tasks

- **Task 1 (Easy):** Write a program that saves your name and age to a file called `profile.txt`.
- **Task 2 (Easy):** Read the `profile.txt` file you just created and print its contents.
- **Task 3 (Medium):** Ask the user to enter 5 grocery items. Save them to `grocery.txt`, one per line.
- **Task 4 (Medium):** Read `grocery.txt` and print each item with a numbered list (1. Apple, 2. Bread...).
- **Task 5 (Medium):** Build a simple diary app — ask the user to write a note and append it with today's date to `diary.txt`.

---

## Interview Questions

- **Q1: How do you open a file in Python?**  
  A: Using `open(filename, mode)`. Example: `open("data.txt", "r")`.

- **Q2: What is the difference between `"w"` and `"a"` mode?**  
  A: `"w"` overwrites the file from scratch. `"a"` adds to the end without deleting existing content.

- **Q3: Why should you use `with open(...)` instead of just `open(...)`?**  
  A: `with` automatically closes the file when done, even if an error occurs. Safer and cleaner.

- **Q4: What does `f.read()` return?**  
  A: The entire file content as a single string.

- **Q5: How do you read a file line by line?**  
  A: Loop over the file object: `for line in f:` or use `f.readlines()`.

- **Q6: What happens if you open a non-existent file in `"r"` mode?**  
  A: Python raises a `FileNotFoundError`. Handle it with `try/except`.

- **Q7: How do you write multiple lines to a file?**  
  A: Use `\n` at the end of each line: `f.write("line1\n")`, or use `f.writelines(list)`.

---

⬅️ Prev: [Modules and Imports](./09_modules_and_imports.md) | Next ➡️: [Basic OOP](./11_basic_oop.md)
