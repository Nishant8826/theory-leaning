# Variables and Data Types

## Simple Explanation

A **variable** is like a labeled box.  
You put something inside the box, give it a name, and later you can open it to use what's inside.

A **data type** tells Python *what kind of thing* is stored — is it a number? Text? Yes/No?

### Common Data Types

| Type    | What it stores       | Example              |
|---------|----------------------|----------------------|
| `int`   | Whole numbers        | `10`, `-3`, `0`      |
| `float` | Decimal numbers      | `3.14`, `-0.5`       |
| `str`   | Text (words/letters) | `"hello"`, `'Alice'` |
| `bool`  | True or False        | `True`, `False`      |
| `None`  | No value / empty     | `None`               |

---

## Real-World Example

Think of a **bank account**:
- Account holder name → stored as `str`
- Account balance → stored as `float`
- Account number → stored as `int`
- Is account active? → stored as `bool`

Just like a bank keeps different types of info about you, Python keeps different types of data in variables.

---

## Code Example

```python
# Bank account details
account_holder = "Rahul Sharma"   # str  - text
account_number = 1234567890       # int  - whole number
balance = 50750.75                # float - decimal number
is_active = True                  # bool - yes/no

print("Name:", account_holder)
print("Account No:", account_number)
print("Balance:", balance)
print("Active?", is_active)

# Check what type a variable is
print(type(balance))    # <class 'float'>
print(type(is_active))  # <class 'bool'>

# You can change a variable's value anytime
balance = 60000.00
print("Updated Balance:", balance)
```

**Output:**
```
Name: Rahul Sharma
Account No: 1234567890
Balance: 50750.75
Active? True
<class 'float'>
<class 'bool'>
Updated Balance: 60000.0
```

---

## Quick Tips

- Variable names **cannot** start with a number (`1name` ❌ → `name1` ✅).
- Use **snake_case** style: `my_name`, `account_balance` ✅
- Python figures out the type automatically — no need to declare it.
- You can reassign a variable to a completely different type anytime.

```python
x = 10        # int
x = "hello"   # now it's a str — Python is totally fine with this
```

---

## Practice Tasks

- **Task 1 (Easy):** Create variables for your name, age, and city. Print them all.
- **Task 2 (Easy):** Create a variable `price = 199.99` and print its type using `type()`.
- **Task 3 (Easy):** Create a `bool` variable `is_logged_in = False` and print it.
- **Task 4 (Medium):** Create variables for a shopping cart item: `item_name`, `quantity`, `price_per_item`. Calculate and print the total price.
- **Task 5 (Medium):** Assign a number to a variable, print it, then reassign it to a string and print again. Verify the type changed.

---

## Interview Questions

- **Q1: What is a variable in Python?**  
  A: A variable is a name that stores a value. It acts like a labeled container.

- **Q2: What are the basic data types in Python?**  
  A: `int`, `float`, `str`, `bool`, and `None` are the most common ones.

- **Q3: Is Python statically or dynamically typed?**  
  A: Dynamically typed — you don't need to declare the type. Python figures it out automatically.

- **Q4: What does `type()` do?**  
  A: It tells you what data type a variable is holding. Example: `type(10)` returns `<class 'int'>`.

- **Q5: Can a variable change its type?**  
  A: Yes. You can assign a new value of any type to an existing variable.

- **Q6: What is `None` in Python?**  
  A: `None` means "no value" or "empty". It's similar to `null` in other languages.

- **Q7: What is the difference between `int` and `float`?**  
  A: `int` stores whole numbers (e.g., `5`). `float` stores decimal numbers (e.g., `5.0` or `3.14`).

---

⬅️ Prev: Start | Next ➡️: [Input and Output](./01_input_and_output.md)
