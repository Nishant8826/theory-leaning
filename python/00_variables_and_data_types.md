# Variables and Data Types

## What is it?

A **variable** is like a labeled box where you can store a value.  
You give it a name, put something inside, and later you can look at it or change it.

A **data type** tells Python what *kind* of value is stored — a number, some text, true/false, etc.

### Common Data Types

| Type      | What it stores        | Example           |
|-----------|-----------------------|-------------------|
| `int`     | Whole numbers         | `10`, `-3`, `0`   |
| `float`   | Decimal numbers       | `3.14`, `-0.5`    |
| `str`     | Text (strings)        | `"hello"`, `'hi'` |
| `bool`    | True or False         | `True`, `False`   |
| `None`    | "No value" / empty    | `None`            |

## Why is it useful?

Variables let you **remember** data so you can use it later.  
Without them, every value would be thrown away the instant the line finishes running.

Data types matter because Python treats numbers and text differently —  
you can add numbers together, but adding a number to a word would cause an error.

## Example

```python
# Creating variables
name = "Alice"          # str  – text
age = 25                # int  – whole number
height = 5.6            # float – decimal number
is_student = True       # bool – True or False

# Printing them
print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Student?", is_student)

# Checking the type
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
```

## Explanation of Example

1. We created four variables: `name`, `age`, `height`, and `is_student`.
2. Each one stores a different type of data.
3. `print()` shows the value on the screen.
4. `type()` tells us what data type a variable is holding.

## Quick Tips

- Variable names **cannot** start with a number (`1name` ❌).
- Use **snake_case** for variable names (`my_name` ✅, `myName` works but isn't Pythonic).
- Python figures out the type automatically — you don't need to declare it.
- You can change a variable's value (and even its type) at any time:

```python
x = 10        # int
x = "hello"   # now it's a str – Python is fine with this
```

---

> 📁 **Next:** [[Input and Output]→](./01_input_and_output.md)
