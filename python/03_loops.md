# Loops (for and while)

## What is it?

A **loop** lets you repeat a block of code multiple times without writing it over and over.

Python has two main loops:

- **`for` loop** — runs a fixed number of times (or once for each item in a collection).
- **`while` loop** — keeps running as long as a condition is `True`.

## Why is it useful?

Imagine you need to print "Hello" 100 times.  
Writing `print("Hello")` 100 times is crazy — a loop does it in two lines.

Loops are also used to go through lists, read files line by line, retry failed operations, and much more.

## Example — for loop

```python
# Print numbers 1 to 5
for i in range(1, 6):
    print(i)
```

**Output:**
```
1
2
3
4
5
```

### How `range()` works

| Call              | Produces          |
|-------------------|-------------------|
| `range(5)`        | 0, 1, 2, 3, 4    |
| `range(1, 6)`     | 1, 2, 3, 4, 5    |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8    |

## Example — while loop

```python
count = 1

while count <= 5:
    print("Count is:", count)
    count += 1   # increase by 1 each time
```

## Explanation of Example

1. `count` starts at 1.
2. The `while` loop checks: is `count <= 5`? If yes, run the body.
3. Inside the body, we print and then increase `count` by 1.
4. When `count` becomes 6, the condition is `False` and the loop stops.

## Loop Control

- `break` — exit the loop immediately.
- `continue` — skip the rest of this iteration and jump to the next one.

```python
for num in range(1, 11):
    if num == 5:
        break          # stop the loop entirely
    if num % 2 == 0:
        continue       # skip even numbers
    print(num)         # prints 1, 3
```

## Looping Through a List

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")
```

---

> 📁 **Next:** [[Functions]→](./04_functions.md)
