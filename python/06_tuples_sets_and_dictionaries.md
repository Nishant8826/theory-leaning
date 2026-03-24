# Tuples, Sets, and Dictionaries

## Simple Explanation

Python has 4 main ways to store multiple items:

| Type           | Ordered? | Can Change? | Allows Duplicates? | Syntax          |
|----------------|----------|-------------|---------------------|-----------------|
| **List**       | ✅ Yes   | ✅ Yes      | ✅ Yes              | `[1, 2, 3]`     |
| **Tuple**      | ✅ Yes   | ❌ No       | ✅ Yes              | `(1, 2, 3)`     |
| **Set**        | ❌ No    | ✅ Yes      | ❌ No               | `{1, 2, 3}`     |
| **Dictionary** | ✅ Yes   | ✅ Yes      | Keys: ❌ No         | `{"name": "Rahul"}` |

---

## Tuples — Locked List

A **tuple** is like a list but **locked** — you can't change it after creating it.

### Real-World Example
> Coordinates on a map: `(28.6139, 77.2090)` — latitude and longitude never change.

```python
location = (28.6139, 77.2090)
print(location[0])   # 28.6139

# location[0] = 100  ❌ Error! Tuples can't be changed.
```

**When to use tuples:**
- Data that should never change (e.g., RGB colors, coordinates, config values)
- Returning multiple values from a function

---

## Sets — No Duplicates Allowed

A **set** automatically removes duplicate values and has no fixed order.

### Real-World Example
> A **unique visitors** tracker — if the same user visits twice, count them only once.

```python
visitors = {"Rahul", "Priya", "Arjun", "Rahul", "Priya"}
print(visitors)  # {'Rahul', 'Priya', 'Arjun'} — duplicates removed!

# Add / remove
visitors.add("Neha")
visitors.discard("Arjun")

# Find common users between two sets
set_a = {"Rahul", "Priya", "Neha"}
set_b = {"Priya", "Neha", "Ravi"}

print(set_a & set_b)   # {'Priya', 'Neha'}  — common (intersection)
print(set_a | set_b)   # All unique users    — union
```

---

## Dictionaries — Key-Value Store

A **dictionary** stores data as **key: value** pairs — like a real dictionary where a word → meaning.

### Real-World Example
> A **user profile** in an app: `{ "name": "Rahul", "age": 25, "email": "rahul@email.com" }`

```python
user = {
    "name": "Rahul",
    "age": 25,
    "city": "Delhi",
    "is_premium": True
}

# Access values
print(user["name"])         # Rahul
print(user.get("email", "Not provided"))  # Not provided (safe access)

# Add / update
user["email"] = "rahul@email.com"
user["age"] = 26

# Delete
del user["is_premium"]

# Loop through all key-value pairs
for key, value in user.items():
    print(f"{key}: {value}")
```

**Output:**
```
name: Rahul
age: 26
city: Delhi
email: rahul@email.com
```

---

## Useful Dictionary Methods

| Method            | What it does                             |
|-------------------|------------------------------------------|
| `keys()`          | Returns all keys                         |
| `values()`        | Returns all values                       |
| `items()`         | Returns key-value pairs                  |
| `get(key, default)` | Returns value or default if key missing |
| `update({...})`   | Merge another dict into this one         |
| `pop(key)`        | Remove and return a key's value          |

---

## Practice Tasks

- **Task 1 (Easy):** Create a tuple with 3 city names. Print each one.
- **Task 2 (Easy):** Create a set with repeated numbers `{1, 2, 2, 3, 3, 4}` and print it — notice duplicates are gone.
- **Task 3 (Medium):** Create a dictionary for a student profile (name, marks, grade). Update the grade and print all info.
- **Task 4 (Medium):** Create two sets of students who passed Math and Science. Find students who passed both (`&`).
- **Task 5 (Medium):** Create a dictionary of 5 items with their prices. Print only items that cost more than ₹50.

---

## Interview Questions

- **Q1: What is the difference between a list and a tuple?**  
  A: A list is mutable (changeable). A tuple is immutable (locked after creation).

- **Q2: Why would you use a tuple instead of a list?**  
  A: When data must not change — like coordinates or a function returning multiple values.

- **Q3: What makes a set different from a list?**  
  A: A set has no duplicates and no guaranteed order. A list preserves order and allows duplicates.

- **Q4: How do you safely access a dictionary key without getting an error?**  
  A: Use `.get(key, default)` — returns the default if the key doesn't exist.

- **Q5: What is the difference between `dict["key"]` and `dict.get("key")`?**  
  A: `dict["key"]` raises a `KeyError` if the key is missing. `dict.get("key")` returns `None` instead.

- **Q6: Can dictionary keys be of any type?**  
  A: Keys must be immutable (e.g., `str`, `int`, `tuple`). You can't use a list as a key.

- **Q7: How do you check if a key exists in a dictionary?**  
  A: Use `if "name" in my_dict:`.

---

⬅️ Prev: [Lists](./05_lists.md) | Next ➡️: [String Handling](./07_string_handling.md)
