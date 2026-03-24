# Lists

## Simple Explanation

A **list** is like a shopping cart — it holds multiple items in order.  
You can add items, remove items, or change them anytime.

Lists are created with square brackets `[]`:

```python
shopping_cart = ["Apple", "Bread", "Milk"]
```

---

## Real-World Example

Think of your **phone's contact list**:
- It stores multiple names in order
- You can add a new contact
- You can delete or update a contact
- You can search for someone

That's exactly how a Python list works!

---

## Code Example

```python
# Supermarket shopping cart
cart = ["Apple", "Bread", "Milk"]

# Access items by position (starts at 0)
print(cart[0])    # Apple
print(cart[-1])   # Milk (last item)

# Add a new item
cart.append("Eggs")

# Update an item
cart[1] = "Brown Bread"

# Remove an item
cart.remove("Milk")

# Print the final cart
print("Your cart:", cart)

# Loop through all items
for item in cart:
    print(f"  - {item}")

# How many items?
print("Total items:", len(cart))
```

**Output:**
```
Apple
Milk
Your cart: ['Apple', 'Brown Bread', 'Eggs']
  - Apple
  - Brown Bread
  - Eggs
Total items: 3
```

---

## Useful List Methods

| Method              | What it does                            |
|---------------------|-----------------------------------------|
| `append(item)`      | Add item to the end                     |
| `insert(i, item)`   | Insert item at position `i`             |
| `remove(item)`      | Remove first match of item              |
| `pop()`             | Remove and return the last item         |
| `pop(i)`            | Remove and return item at position `i`  |
| `sort()`            | Sort the list (alphabetically/numerically) |
| `reverse()`         | Reverse the order                       |
| `len(list)`         | Get total number of items               |
| `in`                | Check if item exists: `"Milk" in cart`  |

---

## List Slicing

Get a portion of a list:

```python
scores = [10, 20, 30, 40, 50]

print(scores[1:4])   # [20, 30, 40]  — index 1 to 3
print(scores[:3])    # [10, 20, 30]  — first 3 items
print(scores[2:])    # [30, 40, 50]  — from index 2 to end
```

---

## Practice Tasks

- **Task 1 (Easy):** Create a list of 5 fruits. Print each one using a loop.
- **Task 2 (Easy):** Create a list of 3 numbers and print their sum using `sum()`.
- **Task 3 (Medium):** Build a to-do list app: add 3 tasks, mark one as done by removing it, then print remaining tasks.
- **Task 4 (Medium):** Create a list of student marks. Print the highest, lowest, and average mark.
- **Task 5 (Medium):** Take a list `[5, 3, 8, 1, 9, 2]`, sort it, and print the top 3 values.

---

## Interview Questions

- **Q1: What is a list in Python?**  
  A: An ordered, changeable collection of items. Created using `[]`.

- **Q2: How do you access the last item of a list?**  
  A: Use `list[-1]` — negative indexing counts from the end.

- **Q3: What is the difference between `remove()` and `pop()`?**  
  A: `remove(value)` removes by value. `pop(index)` removes by position and returns the removed item.

- **Q4: How do you check if an item is in a list?**  
  A: Use `in`: `if "Apple" in cart:`.

- **Q5: Are lists mutable?**  
  A: Yes — you can change, add, or remove items after creation.

- **Q6: What is list slicing?**  
  A: Getting a sub-part of a list using `list[start:end]`.

- **Q7: What is the difference between `append()` and `insert()`?**  
  A: `append()` always adds to the end. `insert(i, item)` adds at a specific position.

---

⬅️ Prev: [Functions](./04_functions.md) | Next ➡️: [Tuples, Sets, and Dictionaries](./06_tuples_sets_and_dictionaries.md)
