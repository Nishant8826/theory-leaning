# Input and Output

## Simple Explanation

Every program needs to **talk to the user**.

- **Output** = your program *speaks* → uses `print()`
- **Input** = your program *listens* → uses `input()`

Think of it like a chat:
> Your program says "What is your name?" → You type it → Your program replies "Hello, Rahul!"

---

## Real-World Example

Think of an **ATM machine**:
- It *shows* your balance on screen → that's **output** (`print`)
- It *asks* you to enter your PIN → that's **input** (`input`)

Without input/output, your program would just run silently and no one would see anything!

---

## Code Example

```python
# Output — show something on screen
print("Welcome to the ATM!")
print("Please follow the instructions.")

# Input — ask the user for information
name = input("Enter your name: ")
pin = input("Enter your 4-digit PIN: ")

# Use the input in output
print(f"Hello, {name}! Your PIN has been accepted.")
```

**Sample Run:**
```
Welcome to the ATM!
Please follow the instructions.
Enter your name: Rahul
Enter your 4-digit PIN: 1234
Hello, Rahul! Your PIN has been accepted.
```

---

## Formatting Output (f-strings)

The cleanest way to mix variables into text is using **f-strings** (Python 3.6+):

```python
name = "Priya"
age = 22
city = "Mumbai"

print(f"My name is {name}, I am {age} years old and I live in {city}.")
```

You can also do math inside f-strings:
```python
price = 500
quantity = 3
print(f"Total: ₹{price * quantity}")  # Total: ₹1500
```

---

## Important: `input()` Always Returns a String

Even if the user types a number, `input()` gives you a **string**. Convert it if needed:

```python
age = input("Enter your age: ")   # "22" ← this is a string!
age = int(age)                     # 22  ← now it's a number

# Or in one line:
age = int(input("Enter your age: "))
```

---

## Practice Tasks

- **Task 1 (Easy):** Print your name, age, and favourite food using `print()`.
- **Task 2 (Easy):** Ask the user their name with `input()` and greet them.
- **Task 3 (Easy):** Ask for a city name and print: `"You live in [city]"`.
- **Task 4 (Medium):** Ask the user for two numbers, add them, and print the result. *(Remember to convert to `int`!)*
- **Task 5 (Medium):** Build a mini profile card — ask for name, age, and job. Print a nice formatted card using f-strings.

---

## Interview Questions

- **Q1: What is the difference between `print()` and `input()`?**  
  A: `print()` shows output to the user. `input()` reads input from the user.

- **Q2: What type does `input()` always return?**  
  A: It always returns a `str` (string), even if the user types a number.

- **Q3: How do you take a number as input from the user?**  
  A: Wrap it with `int()` or `float()`: `age = int(input("Enter age: "))`.

- **Q4: What is an f-string?**  
  A: A formatted string that lets you embed variables directly inside `{}`. Works with Python 3.6+.

- **Q5: How do you print multiple things on one line?**  
  A: `print("Hello", name, "!")` — `print()` separates items with a space by default.

- **Q6: How do you print without a newline at the end?**  
  A: Use `end=""`: `print("Loading...", end="")`.

---

⬅️ Prev: [Variables and Data Types](./00_variables_and_data_types.md) | Next ➡️: [Conditionals](./02_conditionals.md)
