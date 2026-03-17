# Conditionals (if / elif / else)

## What is it?

Conditionals let your program **make decisions**.

> "**If** it's raining, take an umbrella.  
> **Else**, wear sunglasses."

In Python this looks like:

```python
if condition:
    # do this
elif another_condition:
    # do this instead
else:
    # do this if nothing above was true
```

## Why is it useful?

Real programs need to react differently to different situations.  
- Is the password correct? → Let the user in.  
- Is the age under 18? → Show a different message.  
- Is the balance zero? → Don't allow a purchase.

## Example

```python
age = int(input("Enter your age: "))

if age < 13:
    print("You are a child.")
elif age < 18:
    print("You are a teenager.")
elif age < 65:
    print("You are an adult.")
else:
    print("You are a senior citizen.")
```

## Explanation of Example

1. We ask the user for their age and convert it to an integer.
2. Python checks each condition **from top to bottom**.
3. The first condition that is `True` runs its block — the rest are skipped.
4. `else` catches everything that didn't match any condition above.

## Comparison Operators

| Operator | Meaning                  | Example       |
|----------|--------------------------|---------------|
| `==`     | Equal to                 | `x == 5`      |
| `!=`     | Not equal to             | `x != 5`      |
| `>`      | Greater than             | `x > 5`       |
| `<`      | Less than                | `x < 5`       |
| `>=`     | Greater than or equal to | `x >= 5`      |
| `<=`     | Less than or equal to    | `x <= 5`      |

## Combining Conditions

Use `and`, `or`, and `not`:

```python
age = 20
has_id = True

if age >= 18 and has_id:
    print("You may enter.")
```
