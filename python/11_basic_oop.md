# Basic OOP (Classes and Objects)

## What is it?

**OOP** stands for **Object-Oriented Programming**.

- A **class** is a blueprint (like a cookie cutter).
- An **object** is an actual instance made from that blueprint (like a cookie).

A class bundles **data** (attributes) and **behavior** (methods) together.

## Why is it useful?

OOP helps you model real-world things in code:
- A `Car` class can have attributes like `color` and `speed`, and methods like `drive()` and `brake()`.
- You can create many car objects from the same class.

It keeps your code **organized**, **reusable**, and **easier to maintain** as projects grow.

## Example

```python
class Dog:
    # Constructor — runs when you create a new Dog
    def __init__(self, name, breed):
        self.name = name      # attribute
        self.breed = breed    # attribute

    # Method — something the dog can do
    def bark(self):
        print(f"{self.name} says: Woof! Woof!")

    def info(self):
        print(f"{self.name} is a {self.breed}.")


# Creating objects (instances)
dog1 = Dog("Buddy", "Golden Retriever")
dog2 = Dog("Max", "Bulldog")

dog1.bark()    # Buddy says: Woof! Woof!
dog2.info()    # Max is a Bulldog.
```

## Explanation of Example

1. `class Dog:` — defines a new class called `Dog`.
2. `__init__` is the **constructor** — it runs automatically when you create a new `Dog` object. It sets up the initial data.
3. `self` refers to the current object. `self.name` means "this dog's name".
4. `bark()` and `info()` are **methods** — functions that belong to the class.
5. `Dog("Buddy", "Golden Retriever")` creates an object and calls `__init__` with those values.

## Inheritance

A class can **inherit** from another class — it gets all the parent's attributes and methods, and can add its own.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")


class Cat(Animal):
    def speak(self):
        print(f"{self.name} says: Meow!")


class Duck(Animal):
    def speak(self):
        print(f"{self.name} says: Quack!")


animals = [Cat("Whiskers"), Duck("Donald")]

for animal in animals:
    animal.speak()
# Whiskers says: Meow!
# Donald says: Quack!
```

## Key OOP Terms

| Term            | Meaning                                     |
|-----------------|---------------------------------------------|
| **Class**       | A blueprint for creating objects             |
| **Object**      | An instance of a class                       |
| **Attribute**   | A variable inside a class (data)             |
| **Method**      | A function inside a class (behavior)         |
| **Constructor** | `__init__` — sets up new objects             |
| **Inheritance** | A class can get features from a parent class |
| **self**        | Refers to the current instance               |

---

> 📁 **Next:** [[Lambda, Map, and Filter]→](./12_lambda_map_filter.md)

---
Previous: [10_file_handling.md](10_file_handling.md) Next: [12_lambda_map_filter.md](12_lambda_map_filter.md)
---
