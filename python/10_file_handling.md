# File Handling (Read and Write)

## What is it?

**File handling** lets your program read data from files and write data to files on your computer.

Python uses the built-in `open()` function for this.

## Why is it useful?

Programs often need to:
- Save results so they aren't lost when the program closes.
- Read configuration or data from a file.
- Generate reports, logs, or exports.

## File Modes

| Mode | Meaning                                    |
|------|--------------------------------------------|
| `"r"`  | Read — open for reading (file must exist)  |
| `"w"`  | Write — create or overwrite the file       |
| `"a"`  | Append — add to the end of the file        |
| `"x"`  | Create — create the file, error if exists  |

## Example — Writing to a File

```python
# 'with' automatically closes the file when done
with open("notes.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("This is line two.\n")

print("File written successfully!")
```

## Example — Reading from a File

```python
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)
```

## Example — Reading Line by Line

```python
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())   # strip() removes the extra newline
```

## Example — Appending to a File

```python
with open("notes.txt", "a") as f:
    f.write("This line was added later.\n")
```

## Explanation of Example

1. `open("notes.txt", "w")` opens (or creates) the file in write mode.
2. The `with` statement makes sure the file is closed automatically — even if an error occurs.
3. `.write()` sends text into the file.
4. `.read()` reads the entire file content as a single string.
5. Looping over the file object reads it one line at a time — memory-friendly for large files.

## Quick Tips

- **Always use `with open(...)`** — it handles closing for you.
- If the file might not exist, wrap the read in a `try/except FileNotFoundError`.
- For CSV files, check out the `csv` module; for JSON, use `json`.

---

> 📁 **Next:** [[Basic OOP (Classes and Objects)]→](./11_basic_oop.md)
