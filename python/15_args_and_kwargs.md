# *args and **kwargs

## Simple Explanation

`*args` and `**kwargs` let you write functions that accept **any number of inputs**.

- `*args` — collects extra **positional** arguments into a **tuple** (like a list of values)
- `**kwargs` — collects extra **keyword** arguments into a **dictionary** (like `name="Rahul"`)

> Think of `*args` as "give me however many items you want".  
> Think of `**kwargs` as "give me any named settings you want."

---

## Real-World Example

Think of an **order placement function** for a restaurant:

- You might order 1 item or 10 items — the function must handle any number → use `*args`
- You might pass extra preferences like `"spicy=True"`, `"no_onion=True"` → use `**kwargs`

Or think of a **send email function**:
- `to` (required), `subject` (required)
- Extra options: `cc`, `bcc`, `attachment` — not always passed → use `**kwargs`

---

## Code Example — `*args`

```python
def place_order(customer, *items):
    print(f"📦 Order for: {customer}")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    print(f"Total items: {len(items)}")

place_order("Rahul", "Pizza", "Burger")
print()
place_order("Priya", "Pasta", "Salad", "Cold Drink", "Ice Cream")
```

**Output:**
```
📦 Order for: Rahul
  1. Pizza
  2. Burger
Total items: 2

📦 Order for: Priya
  1. Pasta
  2. Salad
  3. Cold Drink
  4. Ice Cream
Total items: 4
```

---

## Code Example — `**kwargs`

```python
def create_user_profile(name, **details):
    print(f"👤 Profile: {name}")
    for key, value in details.items():
        print(f"  {key}: {value}")

create_user_profile("Rahul", age=25, city="Delhi", is_premium=True)
print()
create_user_profile("Priya", age=22, job="Developer")
```

**Output:**
```
👤 Profile: Rahul
  age: 25
  city: Delhi
  is_premium: True

👤 Profile: Priya
  age: 22
  job: Developer
```

---

## Using Both Together

```python
def send_email(to, subject, *cc_list, **options):
    print(f"📧 To: {to}")
    print(f"   Subject: {subject}")
    if cc_list:
        print(f"   CC: {', '.join(cc_list)}")
    for key, value in options.items():
        print(f"   {key}: {value}")

send_email(
    "rahul@email.com",
    "Meeting Update",
    "priya@email.com", "arjun@email.com",
    priority="High",
    has_attachment=True
)
```

**Output:**
```
📧 To: rahul@email.com
   Subject: Meeting Update
   CC: priya@email.com, arjun@email.com
   priority: High
   has_attachment: True
```

---

## Unpacking with `*` and `**`

You can also **spread** a list or dictionary into a function call:

```python
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))    # same as add(1, 2, 3) → 6

def greet(name, city):
    print(f"Hello {name} from {city}!")

info = {"name": "Rahul", "city": "Delhi"}
greet(**info)           # same as greet(name="Rahul", city="Delhi")
```

---

## Order of Parameters

Always keep this order in function definitions:

```python
def my_func(required, *args, **kwargs):
    pass
```

1. Regular parameters first
2. `*args` second
3. `**kwargs` last

---

## Practice Tasks

- **Task 1 (Easy):** Write a function `add_all(*numbers)` that returns the sum of any number of arguments.
- **Task 2 (Easy):** Write a function `print_info(**kwargs)` that prints each key-value pair.
- **Task 3 (Medium):** Write a function `order_pizza(size, *toppings)` — print the size and list all toppings.
- **Task 4 (Medium):** Write a function `register_user(name, email, **optional)` — optional can include `age`, `city`, `phone`.
- **Task 5 (Medium):** Create a shopping cart function `add_to_cart(*items, **discounts)` — add any items and apply any discounts by item name.

---

## Interview Questions

- **Q1: What is `*args` in Python?**  
  A: It collects any number of extra positional arguments into a tuple inside the function.

- **Q2: What is `**kwargs` in Python?**  
  A: It collects any number of extra keyword arguments into a dictionary inside the function.

- **Q3: What is the correct order of parameters?**  
  A: `def func(normal_param, *args, **kwargs):` — always in that order.

- **Q4: Are the names `args` and `kwargs` mandatory?**  
  A: No. The `*` and `**` are what matter. You could write `*items` or `**options`.

- **Q5: What is the difference between `*args` and a regular list parameter?**  
  A: With `*args`, callers don't wrap values in a list — they just pass multiple values directly.

- **Q6: When would you use `**kwargs` in real projects?**  
  A: When building flexible APIs, utility functions, or wrapper/decorator functions.

- **Q7: What does `func(**dict)` do when calling a function?**  
  A: It unpacks the dictionary and passes each key-value pair as a keyword argument.

---

⬅️ Prev: [Comprehensions](./14_comprehensions.md) | Next ➡️: [Virtual Environments and pip](./16_virtual_environments_and_pip.md)
