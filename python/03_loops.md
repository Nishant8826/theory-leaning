# Loops (for and while)

## Simple Explanation

A **loop** lets you repeat code multiple times without writing it again and again.

Python has two types:
- **`for` loop** — repeat a fixed number of times, or go through each item in a list.
- **`while` loop** — keep repeating as long as a condition is `True`.

> Imagine you need to send a "Happy Birthday!" message to 100 friends.  
> Writing `print("Happy Birthday!")` 100 times is crazy — a loop does it in 2 lines!

---

## Real-World Example

Think of a **supermarket billing counter**:
- The cashier scans each item one by one → that's a **loop** going through each item.

Think of a **password prompt**:
- Keep asking for the password until the user enters the correct one → that's a **while loop**.

---

## Code Example — `for` Loop

```python
# Print receipt for shopping cart
items = ["Apple", "Bread", "Milk", "Eggs"]

print("🧾 Your Shopping Receipt:")
for item in items:
    print(f"  - {item}")

print("Thank you for shopping!")
```

**Output:**
```
🧾 Your Shopping Receipt:
  - Apple
  - Bread
  - Milk
  - Eggs
Thank you for shopping!
```

---

## Code Example — `range()` with `for`

```python
# Print table of 5
for i in range(1, 11):
    print(f"5 x {i} = {5 * i}")
```

| `range()` call      | Numbers produced  |
|---------------------|-------------------|
| `range(5)`          | 0, 1, 2, 3, 4     |
| `range(1, 6)`       | 1, 2, 3, 4, 5     |
| `range(0, 10, 2)`   | 0, 2, 4, 6, 8     |

---

## Code Example — `while` Loop

```python
# Keep asking until correct password is entered
correct_password = "python123"

while True:
    entered = input("Enter password: ")
    if entered == correct_password:
        print("✅ Access granted!")
        break
    else:
        print("❌ Wrong password. Try again.")
```

---

## Loop Control: `break` and `continue`

- **`break`** — stop the loop immediately.
- **`continue`** — skip this round and go to the next one.

```python
# Print only odd numbers from 1 to 10, stop at 7
for num in range(1, 11):
    if num == 8:
        break           # stop at 8
    if num % 2 == 0:
        continue        # skip even numbers
    print(num)          # prints: 1, 3, 5, 7
```

---

## Practice Tasks

- **Task 1 (Easy):** Print numbers 1 to 10 using a `for` loop.
- **Task 2 (Easy):** Print all items in a list `["Monday", "Tuesday", "Wednesday"]` using a loop.
- **Task 3 (Medium):** Calculate the sum of numbers from 1 to 100 using a loop.
- **Task 4 (Medium):** Ask the user to enter numbers until they type `0`. Print the total sum.
- **Task 5 (Medium):** Print a multiplication table (1–10) for any number entered by the user.

---

## Interview Questions

- **Q1: What is the difference between a `for` loop and a `while` loop?**  
  A: `for` is used when you know how many times to repeat. `while` is used when you repeat until a condition becomes false.

- **Q2: What does `range(1, 6)` produce?**  
  A: `1, 2, 3, 4, 5` — it stops *before* 6.

- **Q3: What does `break` do in a loop?**  
  A: It stops the loop immediately and exits it.

- **Q4: What does `continue` do?**  
  A: It skips the rest of the current iteration and moves to the next one.

- **Q5: What is an infinite loop? How do you avoid it?**  
  A: A loop that never stops — usually caused by a `while True` with no `break`. Always make sure the loop has an exit condition.

- **Q6: Can you use `else` with a loop?**  
  A: Yes. The `else` block runs *after* the loop finishes normally (not if `break` was used).

- **Q7: How do you loop with index and value together?**  
  A: Use `enumerate()`: `for i, item in enumerate(my_list):`.

---

⬅️ Prev: [Conditionals](./02_conditionals.md) | Next ➡️: [Functions](./04_functions.md)
