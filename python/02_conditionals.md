# Conditionals (if / elif / else)

## Simple Explanation

Conditionals let your program **make decisions**.

> "**If** it's raining → take an umbrella.  
> **Else if** it's cloudy → wear a jacket.  
> **Else** → wear a t-shirt."

In Python:
```python
if condition:
    # do this
elif another_condition:
    # do this instead
else:
    # do this if nothing above matched
```

---

## Real-World Example

Think of a **user login system**:
- If the password is correct → "Login successful!"
- Else if the account is locked → "Account is locked."
- Else → "Wrong password. Try again."

Also think of a **shopping cart**:
- If the user has a coupon → apply discount
- Else if total > ₹1000 → give 10% off
- Else → no discount

---

## Code Example

```python
# User login check
username = input("Enter username: ")
password = input("Enter password: ")

if username == "admin" and password == "1234":
    print("✅ Login successful! Welcome, Admin.")
elif username == "admin" and password != "1234":
    print("❌ Wrong password. Please try again.")
else:
    print("❌ Username not found.")
```

**Another Example — Age Category:**
```python
age = int(input("Enter your age: "))

if age < 13:
    print("You are a child.")
elif age < 18:
    print("You are a teenager.")
elif age < 60:
    print("You are an adult.")
else:
    print("You are a senior citizen.")
```

---

## Comparison Operators

| Operator | Meaning                  | Example      |
|----------|--------------------------|--------------|
| `==`     | Equal to                 | `x == 5`     |
| `!=`     | Not equal to             | `x != 5`     |
| `>`      | Greater than             | `x > 5`      |
| `<`      | Less than                | `x < 5`      |
| `>=`     | Greater than or equal to | `x >= 5`     |
| `<=`     | Less than or equal to    | `x <= 5`     |

---

## Combining Conditions

Use `and`, `or`, `not` to combine checks:

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("You can enter the event.")

balance = 0
if balance == 0 or balance < 0:
    print("Insufficient balance.")
```

---

## Practice Tasks

- **Task 1 (Easy):** Ask the user's age. Print "Minor" if below 18, else print "Adult".
- **Task 2 (Easy):** Ask for a number. Print "Positive", "Negative", or "Zero".
- **Task 3 (Medium):** Ask for a student's marks (0–100). Print their grade: A (90+), B (75+), C (60+), D (45+), Fail (below 45).
- **Task 4 (Medium):** Build a shopping discount checker — if total > ₹2000 print "20% off", if total > ₹1000 print "10% off", else print "No discount".
- **Task 5 (Medium):** Ask username and password. Give 3 chances. If all 3 fail, print "Account locked".

---

## Interview Questions

- **Q1: What is the difference between `if`, `elif`, and `else`?**  
  A: `if` checks the first condition, `elif` checks more conditions if the first was false, `else` runs when nothing matched.

- **Q2: Can you have multiple `elif` blocks?**  
  A: Yes, you can have as many `elif` blocks as needed.

- **Q3: What is the difference between `=` and `==`?**  
  A: `=` assigns a value. `==` checks if two values are equal.

- **Q4: What does `and` do in a condition?**  
  A: Both conditions must be `True` for the overall check to be `True`.

- **Q5: What does `or` do in a condition?**  
  A: At least one condition must be `True` for the overall check to be `True`.

- **Q6: What is a one-line `if` (ternary operator) in Python?**  
  A: `result = "Adult" if age >= 18 else "Minor"` — assigns based on condition in one line.

- **Q7: Can you nest `if` statements?**  
  A: Yes. An `if` block can contain another `if` block inside it.

---

⬅️ Prev: [Input and Output](./01_input_and_output.md) | Next ➡️: [Loops](./03_loops.md)
