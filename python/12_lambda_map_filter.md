# Lambda, Map, and Filter

## Simple Explanation

### Lambda
A **lambda** is a tiny, unnamed function — written in just one line.  
Use it for simple, quick operations.

```python
# Normal function
def double(x):
    return x * 2

# Same thing as a lambda
double = lambda x: x * 2
```

### Map
`map()` applies a function to **every item** in a list.

### Filter
`filter()` keeps only items that **pass a condition** (return `True`).

---

## Real-World Example

Think of a **price list processor** for an online store:
- **Map** → Apply 10% discount to every product's price
- **Filter** → Show only products that are under ₹500
- **Lambda** → Write the discount/filter logic in one line

---

## Code Example

```python
prices = [120, 450, 850, 300, 1200, 75, 600]

# Apply 10% discount to all prices (using map + lambda)
discounted = list(map(lambda p: round(p * 0.90, 2), prices))
print("Discounted prices:", discounted)

# Keep only affordable items under ₹500 (using filter + lambda)
affordable = list(filter(lambda p: p < 500, prices))
print("Affordable items (< ₹500):", affordable)

# Combine: affordable items after discount
affordable_after_discount = list(filter(lambda p: p < 500, discounted))
print("Affordable after discount:", affordable_after_discount)
```

**Output:**
```
Discounted prices: [108.0, 405.0, 765.0, 270.0, 1080.0, 67.5, 540.0]
Affordable items (< ₹500): [120, 450, 300, 75]
Affordable after discount: [108.0, 405.0, 270.0, 67.5]
```

---

## Lambda with `sorted()`

Lambda is super useful for custom sorting:

```python
# Sort students by their marks (ascending)
students = [("Rahul", 85), ("Priya", 92), ("Arjun", 70)]
students.sort(key=lambda s: s[1])
print(students)
# [('Arjun', 70), ('Rahul', 85), ('Priya', 92)]
```

---

## Comparison: Lambda vs List Comprehension

Both do the same thing — use whichever feels more readable:

```python
prices = [100, 200, 300, 400]

# Using map + lambda
doubled_map = list(map(lambda p: p * 2, prices))

# Using list comprehension (often cleaner)
doubled_comp = [p * 2 for p in prices]

print(doubled_map)   # [200, 400, 600, 800]
print(doubled_comp)  # [200, 400, 600, 800]
```

---

## When to Use Lambda

✅ **Good for:** Short, simple one-line logic passed to `map()`, `filter()`, or `sorted()`.  
❌ **Avoid for:** Complex logic with multiple steps — use a regular `def` function instead.

---

## Practice Tasks

- **Task 1 (Easy):** Use a lambda to create a function that returns the square of a number.
- **Task 2 (Easy):** Given a list of numbers `[1, 2, 3, 4, 5, 6]`, use `filter()` to keep only even numbers.
- **Task 3 (Medium):** Given a list of names `["alice", "bob", "charlie"]`, use `map()` to capitalize each name.
- **Task 4 (Medium):** Given a list of products with prices `[("Book", 200), ("Pen", 50), ("Bag", 800)]`, filter products costing less than ₹300 using `filter()`.
- **Task 5 (Medium):** Sort a list of employees `[("Rahul", "Dev"), ("Priya", "Manager"), ("Arjun", "QA")]` alphabetically by name using `sorted()` and a lambda.

---

## Interview Questions

- **Q1: What is a lambda function?**  
  A: An anonymous (unnamed), one-line function. Syntax: `lambda args: expression`.

- **Q2: What does `map()` do?**  
  A: It applies a function to every item in an iterable and returns the results.

- **Q3: What does `filter()` do?**  
  A: It keeps only the items from an iterable where the function returns `True`.

- **Q4: Why do we wrap `map()` and `filter()` with `list()`?**  
  A: Because they return lazy iterator objects — `list()` converts them into a usable list.

- **Q5: What is the difference between `map()` and a list comprehension?**  
  A: They do the same thing. List comprehensions are usually more readable. `map()` can be slightly faster for large data.

- **Q6: Can a lambda have multiple arguments?**  
  A: Yes. Example: `lambda x, y: x + y`.

- **Q7: When should you NOT use a lambda?**  
  A: When the logic is complex or needs multiple lines. Use a regular `def` function instead.

---

⬅️ Prev: [Basic OOP](./11_basic_oop.md) | Next ➡️: [Decorators](./13_decorators.md)
