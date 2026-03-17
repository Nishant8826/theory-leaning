# Lists

## What is it?

A **list** is an ordered collection of items.  
Items can be of any type, and you can add, remove, or change them.

Lists are created with square brackets `[]`:

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]
```

## Why is it useful?

Whenever you need to store **multiple values** together — a shopping list, a list of scores, a set of usernames — a list is usually your go-to choice.

## Example

```python
colors = ["red", "green", "blue"]

# Access by index (starts at 0)
print(colors[0])    # red
print(colors[-1])   # blue (last item)

# Change an item
colors[1] = "yellow"

# Add an item
colors.append("purple")

# Remove an item
colors.remove("red")

print(colors)   # ['yellow', 'blue', 'purple']
```

## Explanation of Example

1. `colors[0]` gives the first element (indexing starts at 0).
2. `colors[-1]` gives the last element using a negative index.
3. `.append()` adds an item to the end.
4. `.remove()` deletes the first occurrence of the given value.

## Useful List Methods

| Method              | What it does                          |
|---------------------|---------------------------------------|
| `append(item)`      | Add item to end                       |
| `insert(i, item)`   | Insert item at position `i`           |
| `remove(item)`      | Remove first occurrence of item       |
| `pop(i)`            | Remove & return item at position `i`  |
| `sort()`            | Sort the list in place                |
| `reverse()`         | Reverse the list in place             |
| `len(my_list)`      | Get the number of items               |

## List Slicing

```python
nums = [10, 20, 30, 40, 50]

print(nums[1:4])    # [20, 30, 40]
print(nums[:3])     # [10, 20, 30]
print(nums[2:])     # [30, 40, 50]
```

## List Comprehension

A short way to create lists:

```python
squares = [x ** 2 for x in range(1, 6)]
print(squares)   # [1, 4, 9, 16, 25]
```
