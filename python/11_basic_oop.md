# Basic OOP (Classes and Objects)

## Simple Explanation

**OOP** = **Object-Oriented Programming** — a way to write code that models real-world things.

- A **class** is a blueprint (like an architectural drawing of a house).
- An **object** is the actual thing built from that blueprint (the actual house).

> A `BankAccount` class is the blueprint.  
> `rahul_account` and `priya_account` are two different objects (actual accounts) made from it.

---

## Real-World Example

Think of a **Bank Account**:
- Every account has: account number, holder name, balance (→ these are **attributes**)
- Every account can: deposit, withdraw, show balance (→ these are **methods**)

Instead of writing separate variables for each customer, OOP lets you create a `BankAccount` class once and make as many accounts as needed!

---

## Code Example

```python
class BankAccount:
    # Constructor — runs when a new account is created
    def __init__(self, holder, account_number, balance=0):
        self.holder = holder
        self.account_number = account_number
        self.balance = balance

    # Method — deposit money
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✅ ₹{amount} deposited. New balance: ₹{self.balance}")
        else:
            print("❌ Invalid deposit amount.")

    # Method — withdraw money
    def withdraw(self, amount):
        if amount > self.balance:
            print("❌ Insufficient balance.")
        else:
            self.balance -= amount
            print(f"✅ ₹{amount} withdrawn. Remaining: ₹{self.balance}")

    # Method — show account info
    def show_info(self):
        print(f"Account: {self.account_number} | Holder: {self.holder} | Balance: ₹{self.balance}")


# Create objects (actual accounts)
rahul_acc = BankAccount("Rahul", "ACC001", 5000)
priya_acc = BankAccount("Priya", "ACC002", 10000)

rahul_acc.show_info()
rahul_acc.deposit(2000)
rahul_acc.withdraw(3000)

priya_acc.show_info()
```

**Output:**
```
Account: ACC001 | Holder: Rahul | Balance: ₹5000
✅ ₹2000 deposited. New balance: ₹7000
✅ ₹3000 withdrawn. Remaining: ₹4000
Account: ACC002 | Holder: Priya | Balance: ₹10000
```

---

## Inheritance — Reuse and Extend

A class can **inherit** from another class — it gets all the parent's features and can add more.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")


class Dog(Animal):
    def speak(self):
        print(f"{self.name} says: Woof! 🐶")


class Cat(Animal):
    def speak(self):
        print(f"{self.name} says: Meow! 🐱")


dog = Dog("Buddy")
cat = Cat("Whiskers")

dog.speak()   # Buddy says: Woof! 🐶
cat.speak()   # Whiskers says: Meow! 🐱
```

---

## Key OOP Terms

| Term            | Meaning                                          |
|-----------------|--------------------------------------------------|
| **Class**       | Blueprint for creating objects                    |
| **Object**      | An actual instance created from a class           |
| **`__init__`**  | Constructor — runs when object is created         |
| **`self`**      | Refers to the current object                      |
| **Attribute**   | A variable that belongs to an object              |
| **Method**      | A function that belongs to a class                |
| **Inheritance** | A child class getting features from a parent      |

---

## Practice Tasks

- **Task 1 (Easy):** Create a `Car` class with attributes `brand`, `model`, `year`. Create two car objects and print their details.
- **Task 2 (Easy):** Add a method `start()` to your `Car` class that prints `"[brand] car started!"`.
- **Task 3 (Medium):** Create a `Student` class with `name` and `marks`. Add a method `grade()` that returns A/B/C/F based on marks.
- **Task 4 (Medium):** Create a `ShoppingCart` class. Add methods to `add_item(name, price)`, `remove_item(name)`, and `show_total()`.
- **Task 5 (Medium):** Create a parent class `Employee` and two child classes `Manager` and `Developer`. Each should have a different `role()` method.

---

## Interview Questions

- **Q1: What is OOP?**  
  A: Object-Oriented Programming — a style of writing code that organizes data and behavior into objects.

- **Q2: What is the difference between a class and an object?**  
  A: A class is a blueprint. An object is a specific instance created from that blueprint.

- **Q3: What does `__init__` do?**  
  A: It's the constructor — it runs automatically when you create a new object, and sets up initial values.

- **Q4: What is `self` in Python?**  
  A: `self` refers to the current object. It's the first parameter of every instance method.

- **Q5: What is inheritance?**  
  A: When a child class gets attributes and methods from a parent class. Reduces code repetition.

- **Q6: What is method overriding?**  
  A: When a child class defines its own version of a method that exists in the parent class.

- **Q7: What are the 4 pillars of OOP?**  
  A: Encapsulation, Abstraction, Inheritance, Polymorphism.

---

⬅️ Prev: [File Handling](./10_file_handling.md) | Next ➡️: [Lambda, Map, and Filter](./12_lambda_map_filter.md)
