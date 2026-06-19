# TypeScript Fundamentals

## What is it?
TypeScript is an open-source, strongly-typed programming language that builds on JavaScript. It is a superset of JavaScript, meaning all valid JavaScript code is valid TypeScript. It transpiles to plain JavaScript so it can execute on any web browser.

## Why do we need it?
JavaScript is dynamically typed, which leads to silent errors that only manifest during runtime. For example, passing an incorrect object type into a function can crash an app. TypeScript adds compile-time type checking, allowing IDEs to flag type errors immediately, document APIs inline, and provide intelligent autocomplete.

```
JS Flow:
Write Code ──> Run App ──> User clicks button ──> TypeError: Cannot read properties of undefined (Runtime Crash)

TS Flow:
Write Code ──> Compiler checks types ──> Reports error during coding ──> Fix immediately (Production Safe)
```

## How does it work?
1. **Type Checker**: Runs during compilation to ensure variables, arguments, and return types adhere to declared types.
2. **TSConfig**: The config file (`tsconfig.json`) dictates how strictly typescript checks types and what ECMA version the code compiles to.
3. **Transpilation**: Strips out all type annotations, leaving plain JavaScript that engines like V8 can execute.

## Impact
* **Application Architecture**: Improves structure via strict classes, interfaces, and design patterns.
* **Performance**: Zero runtime overhead. TypeScript annotations are completely compiled away.
* **Maintainability**: Refactoring is highly predictable since changing a parameter or property rename updates/flags all usages.

## Real World Example
When coding a checkout form, using a TypeScript interface like `interface CartItem { id: string; price: number; }` prevents a developer from mistakenly sending a string representation of `price` to a mathematical service.

## Syntax
Common TS typings and syntax elements:
```typescript
let age: number = 28;
let username: string = "Nishant";
let isInstructor: boolean = true;

// Type Aliases vs Interfaces
type ID = string | number;

interface User {
  id: ID;
  name: string;
  email?: string; // Optional property
}

// Enums
enum UserRole {
  Admin = 'ADMIN',
  User = 'USER'
}
```

## Code Examples
A comprehensive example showing Classes, OOP, Generics, and Async programming in TypeScript:

```typescript
// Interfaces and Enums
interface Identifiable {
  id: string;
}

enum Priority {
  Low, Medium, High
}

// Classes and OOP
class Task implements Identifiable {
  constructor(
    public id: string,
    public title: string,
    public priority: Priority = Priority.Medium
  ) {}
}

// Generics
class Repository<T extends Identifiable> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  getById(id: string): T | undefined {
    return this.items.find(x => x.id === id);
  }

  getAll(): T[] {
    return [...this.items];
  }
}

// Async programming
class TaskLoader {
  // Simulate API fetch returning a Promise
  async fetchTasksFromApi(): Promise<Task[]> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          new Task('1', 'Learn TypeScript', Priority.High),
          new Task('2', 'Setup Angular CLI', Priority.Medium)
        ]);
      }, 1000);
    });
  }
}

// Using the classes
async function runDemo() {
  const loader = new TaskLoader();
  const repo = new Repository<Task>();

  const tasks = await loader.fetchTasksFromApi();
  tasks.forEach(t => repo.add(t));

  console.log("Tasks:", repo.getAll());
}
runDemo();
```

## Best Practices
1. **Avoid `any` Type**: Using `any` disables type checking. Use `unknown` if a type is truly dynamic, then narrow it down with type guards.
2. **Use Interfaces for Object Models**: For public APIs, interfaces are preferred because they support inheritance and declaration merging.
3. **ReadOnly Modifiers**: Mark properties as `readonly` if they should not be modified post-initialization.

## Common Mistakes
* **Overusing Enums**: Standard numeric enums can be bypassed with arbitrary numbers in older TS. Prefer string enums or literal type unions: `type Role = 'admin' | 'user'`.
* **Ignoring strictNullChecks**: Not checking if an object is null before reading its properties. Always enable strict configurations.

## Interview Questions & Answers
### Q: What is the difference between an Interface and a Type Alias?
**A**: Interfaces are open to extension (you can redeclare them and they merge), support `implements` in classes, and are suited for object shapes. Type aliases (`type`) can describe primitives, unions, tuples, and intersections, making them highly versatile for complex logical mapping.

* **Hinglish Explanation**: Simple words mein, `interface` kisi object ke layout/shape ko design karne ke liye best hota hai kyunki hum isse extend kar sakte hain (inheritance support) aur isse same name se dubara declare karke features merge kar sakte hain (declaration merging). Jabki `type` alias dynamic types (jaise single types, union types like `string | number`, custom types) ko merge ya modify nahi karta, balki bas unka ek alias (nickname) banata hai. Iska redeclaration ya direct extension possible nahi hota.

### Q: What does `unknown` mean and how is it different from `any`?
**A**: Both represent any value. However, `any` bypasses all static type checks, allowing any method call. `unknown` is type-safe; the compiler prevents you from performing any operations on it until you perform type narrowing (using `typeof`, `instanceof`, or custom type guards).

## Summary
TypeScript is standard in modern web development. By adding types, classes, interfaces, generics, and async utilities, it helps catch bugs early and keeps complex code bases readable and manageable.

---

Previous : [Setup and Environment](./02_Setup_and_Environment.md) | Index : [Home](./00_index.md) | Next : [Angular Architecture](./04_Angular_Architecture.md)
