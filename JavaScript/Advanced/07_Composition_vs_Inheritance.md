# 📌 07 — Composition vs Inheritance

## 🌟 Introduction

In software design, there are two main ways to share code between objects: **Inheritance** and **Composition**.

-   **Inheritance:** You design your objects around what they **ARE** (Hierarchy).
-   **Composition:** You design your objects around what they **DO** (Building Blocks).

---

## 🏗️ Inheritance: The "Is-A" Relationship

Inheritance is like a **Family Tree**. A `Dog` is an `Animal`. It inherits everything from `Animal`.

-   **Pros:** Easy to understand at first. Good for small, rigid hierarchies.
-   **Cons:** The "Gorilla/Banana" Problem. You wanted a banana, but you got a gorilla holding the banana and the entire jungle attached to it.

```javascript
class Animal {
  eat() { console.log("Eating..."); }
}

class Dog extends Animal {
  bark() { console.log("Woof!"); }
}

const myDog = new Dog();
myDog.eat(); // Inherited
myDog.bark();
```

---

## 🏗️ Composition: The "Has-A" Relationship

Composition is like a **LEGO Set**. Instead of being a specific type, an object **has** certain abilities.

-   **Pros:** Extremely flexible. You only pick the "blocks" you need.
-   **Cons:** Can require a bit more setup code to "assemble" the object.

```javascript
const canEat = {
  eat: () => console.log("Eating...")
};

const canBark = {
  bark: () => console.log("Woof!")
};

const canFly = {
  fly: () => console.log("Flying...")
};

// Assemble a Robot Dog (It can eat and bark, but not fly)
const robotDog = Object.assign({}, canEat, canBark);

// Assemble a Super Dog (It can do everything!)
const superDog = Object.assign({}, canEat, canBark, canFly);
```

---

## 📐 Visualizing the Difference

```text
INHERITANCE (Hierarchy)
      [ Animal ]
          │
      [ Mammal ]
          │
      [  Dog   ] (Stuck with everything above it)

-----------------------------------------------------------

COMPOSITION (Building Blocks)
[ Eat ]   [ Bark ]   [ Fly ]   [ Swim ]
   │         │          │         │
   └─────────┴────┬─────┴─────────┘
                  ▼
            [ My Custom Object ] (Only takes what it needs)
```

---

## ⚡ Comparison Table

| Feature | Inheritance | Composition |
| :--- | :--- | :--- |
| **Relationship** | "Is-A" (Dog is an Animal) | "Has-A" (Dog has a Barking ability) |
| **Flexibility** | Rigid (Hard to change later) | Flexible (Easy to swap blocks) |
| **Coupling** | Tight (Child depends on Parent) | Loose (Independent modules) |
| **Complexity** | Simple for small apps | Better for large, complex apps |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Prototype Chain Length
In Inheritance, every method call like `myDog.eat()` has to walk up the **Prototype Chain**. If your hierarchy is 10 levels deep, V8 has to check 10 objects before it finds the method. In Composition (using `Object.assign`), the methods are often "own properties" of the object, making the lookup nearly instant.

---

## 💼 Interview Questions

**Q1: Why is Composition often preferred over Inheritance?**
> **Ans:** Inheritance forces you into a rigid hierarchy. If you later need a "Flying Dog," you have to refactor the whole tree. With Composition, you just add the `canFly` block to the object.

**Q2: What is the "Fragile Base Class" problem?**
> **Ans:** In Inheritance, if you change a method in the base class (`Animal`), it might accidentally break hundreds of child classes (`Dog`, `Cat`, `Bird`) that rely on that specific behavior.

**Q3: Can you use both together?**
> **Ans:** Yes! You can have a small inheritance tree for core identity and use composition for specific behaviors/features.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Inheritance** | Very clean syntax with `class` and `extends`. | Leads to deep, confusing "Class Hell" in large apps. |
| **Composition** | Avoids the "Gorilla/Banana" problem entirely. | Harder to see the "type" of an object at a glance. |
| **Mixins** | Reusable pieces of code across different classes. | Possible name collisions (two mixins having the same method name). |

---

## 🔗 Navigation

**Prev:** [06_Currying.md](06_Currying.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_Immutability.md](08_Immutability.md)
