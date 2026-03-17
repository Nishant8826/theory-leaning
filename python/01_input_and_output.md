# Input and Output

## What is it?

- **Output** means showing something on the screen. Python uses the `print()` function for this.
- **Input** means asking the user to type something. Python uses the `input()` function.

Think of it like a conversation:
> Your program **speaks** with `print()` and **listens** with `input()`.

## Why is it useful?

Almost every program needs to talk to the user.  
A calculator needs to ask for numbers. A greeting app needs to ask for a name.  
Without input/output, your program would just sit there doing nothing visible.

## Example

```python
# Output – showing text
print("Welcome to Python!")
print("Let's learn together.")

# Input – asking for user's name
name = input("What is your name? ")

# Using the input in output
print("Hello, " + name + "! Nice to meet you.")
```

## Explanation of Example

1. `print("Welcome to Python!")` — displays the text on screen.
2. `input("What is your name? ")` — shows the question and waits for the user to type.  
   Whatever the user types gets stored in the variable `name`.
3. We combined (concatenated) strings with `+` to build a greeting.

## Formatting Output

Python gives you cleaner ways to mix variables into text:

```python
age = 20

# f-string (recommended – Python 3.6+)
print(f"I am {age} years old.")

# .format() method
print("I am {} years old.".format(age))
```

## Important Note

`input()` **always returns a string**, even if the user types a number.  
To use it as a number, convert it:

```python
age = input("Enter your age: ")   # "25" ← this is a string
age = int(age)                     # 25  ← now it's an integer
```
