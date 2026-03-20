# *args and **kwargs

## What is it?

`*args` and `**kwargs` let you write functions that accept a **flexible number of arguments**.

- `*args` — collects extra **positional** arguments into a **tuple**.
- `**kwargs` — collects extra **keyword** arguments into a **dictionary**.

The names `args` and `kwargs` are just conventions — `*anything` and `**anything` would work too.

## Why is it useful?

- Write functions that don't need a fixed number of inputs.
- Pass arguments through from one function to another (wrappers, decorators).
- Build flexible APIs and utility functions.

## Example — *args

```python
def total(*args):
    print("Values:", args)      # a tuple
    return sum(args)

print(total(1, 2, 3))          # 6
print(total(10, 20, 30, 40))   # 100
```

## Example — **kwargs

```python
def introduce(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

introduce(name="Alice", age=25, city="Delhi")
# name: Alice
# age: 25
# city: Delhi
```

## Using Both Together

```python
def show_all(title, *args, **kwargs):
    print(f"Title: {title}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

show_all("Demo", 1, 2, 3, color="red", size="large")
# Title: Demo
# Args: (1, 2, 3)
# Kwargs: {'color': 'red', 'size': 'large'}
```

## Explanation of Example

1. `*args` gathers `1, 2, 3` into the tuple `(1, 2, 3)`.
2. `**kwargs` gathers `color="red", size="large"` into a dict.
3. Regular parameters (like `title`) must come **before** `*args` and `**kwargs`.

## Unpacking with * and **

You can also **spread** a list or dict into a function call:

```python
numbers = [1, 2, 3]
print(total(*numbers))   # same as total(1, 2, 3) → 6

info = {"name": "Bob", "age": 30}
introduce(**info)         # same as introduce(name="Bob", age=30)
```

---

> 📁 **Next:** [[Virtual Environments and pip]→](./16_virtual_environments_and_pip.md)
