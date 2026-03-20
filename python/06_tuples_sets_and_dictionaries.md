# Tuples, Sets, and Dictionaries

## What are they?

Python has several built-in collection types beyond lists.  
Each one is good at different things.

| Collection   | Ordered? | Changeable? | Duplicates? | Syntax         |
|--------------|----------|-------------|-------------|----------------|
| **List**     | ✅ Yes   | ✅ Yes      | ✅ Yes      | `[1, 2, 3]`   |
| **Tuple**    | ✅ Yes   | ❌ No       | ✅ Yes      | `(1, 2, 3)`   |
| **Set**      | ❌ No    | ✅ Yes      | ❌ No       | `{1, 2, 3}`   |
| **Dict**     | ✅ Yes*  | ✅ Yes      | Keys: ❌ No | `{"a": 1}`     |

\* Dicts keep insertion order in Python 3.7+.

## Why are they useful?

- **Tuple** — when you want a collection that should never change (like coordinates).
- **Set** — when you care about unique values (like removing duplicates).
- **Dictionary** — when you need to look up values by a key (like a real dictionary).

---

## Tuples

```python
point = (3, 5)
print(point[0])   # 3
# point[0] = 10   # ❌ Error — tuples can't be changed
```

### When to use tuples?
- Returning multiple values from a function.
- Storing data that should stay the same (e.g., RGB colors, coordinates).

---

## Sets

```python
colors = {"red", "green", "blue", "red"}
print(colors)   # {'red', 'green', 'blue'} — duplicates removed!

# Add and remove
colors.add("yellow")
colors.discard("green")

# Set operations
a = {1, 2, 3}
b = {3, 4, 5}
print(a & b)   # {3}       — intersection
print(a | b)   # {1,2,3,4,5} — union
```

---

## Dictionaries

A dictionary stores **key-value pairs**.

```python
student = {
    "name": "Alice",
    "age": 21,
    "grade": "A"
}

# Access a value
print(student["name"])       # Alice
print(student.get("age"))    # 21

# Add / update
student["city"] = "Delhi"
student["age"] = 22

# Loop through a dictionary
for key, value in student.items():
    print(f"{key}: {value}")
```

## Explanation of Example

1. Curly braces `{}` with `key: value` pairs create a dictionary.
2. Access values using `dict["key"]` or `dict.get("key")`.
3. `.items()` returns each key-value pair so you can loop through them.

## Useful Dictionary Methods

| Method          | What it does                              |
|-----------------|-------------------------------------------|
| `keys()`        | Returns all keys                          |
| `values()`      | Returns all values                        |
| `items()`       | Returns key-value pairs                   |
| `get(key, def)` | Returns value or default if key missing   |

---

> 📁 **Next:** [[String Handling]→](./07_string_handling.md)
