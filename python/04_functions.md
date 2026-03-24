# Functions

## Simple Explanation

A **function** is a reusable block of code that does a specific job.  
You write it once, and then call (use) it whenever you need it.

> Think of a function like a **vending machine**:  
> You press a button (call the function), it does its job, and gives you a result.

```python
def function_name(parameters):
    # code to run
    return result
```

---

## Real-World Example

Think of a **bank's transfer function**:
- You provide: sender, receiver, amount
- It checks the balance, deducts, and sends
- You don't care *how* it works internally — you just call it

```python
transfer(sender="Rahul", receiver="Priya", amount=500)
```

This is exactly what a function does — hide complexity and just give you a result!

---

## Code Example

```python
# Function to check if a user can withdraw money
def can_withdraw(balance, amount):
    if amount > balance:
        return False
    return True

# Function to calculate interest
def calculate_interest(principal, rate, years):
    interest = (principal * rate * years) / 100
    return interest

# Calling the functions
balance = 5000
amount = 3000

if can_withdraw(balance, amount):
    print("✅ Withdrawal successful!")
else:
    print("❌ Insufficient balance.")

interest = calculate_interest(10000, 5, 2)
print(f"Interest earned: ₹{interest}")
```

**Output:**
```
✅ Withdrawal successful!
Interest earned: ₹1000.0
```

---

## Default Parameters

You can set a default value for a parameter — if the caller doesn't pass it, the default is used:

```python
def greet(name, message="Hello"):
    print(f"{message}, {name}!")

greet("Rahul")              # Hello, Rahul!
greet("Priya", "Good morning")  # Good morning, Priya!
```

---

## Returning Multiple Values

```python
def get_min_max(numbers):
    return min(numbers), max(numbers)

lowest, highest = get_min_max([5, 2, 9, 1, 7])
print(f"Min: {lowest}, Max: {highest}")  # Min: 1, Max: 9
```

---

## Practice Tasks

- **Task 1 (Easy):** Write a function `say_hello(name)` that prints `"Hello, [name]!"`.
- **Task 2 (Easy):** Write a function `square(n)` that returns `n * n`.
- **Task 3 (Medium):** Write a function `calculate_bill(items)` that takes a list of prices and returns the total.
- **Task 4 (Medium):** Write a function `is_even(n)` that returns `True` if a number is even, `False` otherwise.
- **Task 5 (Medium):** Write a function `login(username, password)` that returns `"Success"` if both are correct, else `"Failed"`.

---

## Interview Questions

- **Q1: What is a function in Python?**  
  A: A reusable block of code that performs a specific task. Defined with `def`.

- **Q2: What is the difference between a parameter and an argument?**  
  A: A *parameter* is the variable in the function definition. An *argument* is the actual value you pass when calling it.

- **Q3: What does `return` do?**  
  A: It sends a value back from the function to the caller. Without it, the function returns `None`.

- **Q4: What is a default parameter?**  
  A: A parameter with a preset value. If the caller doesn't pass it, the default is used.

- **Q5: Can a function return multiple values?**  
  A: Yes, it returns them as a tuple: `return a, b`.

- **Q6: What happens if a function has no `return` statement?**  
  A: It automatically returns `None`.

- **Q7: What is a docstring?**  
  A: A string just after `def` that describes what the function does. Written with `"""triple quotes"""`.

---

⬅️ Prev: [Loops](./03_loops.md) | Next ➡️: [Lists](./05_lists.md)
