# TypeScript Fundamentals

## What is it?
TypeScript is an open-source, strongly-typed programming language developed by Microsoft that builds directly on JavaScript. It is a strict syntactical superset of JavaScript, meaning every valid JavaScript program is also valid TypeScript. TypeScript compiles (transpiles) down into clean, standard JavaScript so it can execute in any web browser, runtime environment, or server.

## Why do we need it?
JavaScript is dynamically typed, which means variable types are determined at runtime. This often leads to silent bugs and unexpected errors when the application runs in production—such as passing the wrong object structure into a function and crashing the UI. 

TypeScript introduces compile-time type checking. It catches bugs while you write code in your IDE, delivers rich autocompletion (IntelliSense), and provides built-in documentation for API contracts.

```
JavaScript Workflow:
Write Code ──> Run App ──> User Clicks Button ──> TypeError: Cannot read properties of undefined (Runtime Crash)

TypeScript Workflow:
Write Code ──> Compiler Checks Types ──> Reports Error During Coding ──> Fix Immediately (Production Safe)
```

## How does it work?
1. **Type Checker**: Runs during compilation to ensure variables, function arguments, and return values strictly adhere to declared types.
2. **TSConfig (`tsconfig.json`)**: Configures compiler rules, strictness levels (e.g., `strictNullChecks`, `noImplicitAny`), and ECMAScript target output versions.
3. **Transpilation**: During the build step, the TypeScript compiler strips away all type annotations, interfaces, and type declarations, leaving pure JavaScript for browser execution with zero runtime overhead.

## Impact
* **Application Architecture**: Enforces disciplined software design using strong interfaces, classes, generics, and object-oriented patterns.
* **Performance**: Adds zero runtime overhead because all types are completely removed during compilation.
* **Maintainability**: Makes refactoring fearless and predictable. Renaming a model property immediately highlights every file where that property is referenced across the entire application.

## Real World Example
When defining a shopping cart checkout model, writing a TypeScript interface `interface CartItem { id: string; price: number; }` prevents a developer from accidentally passing a string representation of a price into a mathematical calculation function, avoiding severe billing calculation errors.

## Syntax
Common TypeScript types and declarations:

```typescript
let age: number = 28;
let username: string = "Developer";
let isInstructor: boolean = true;

// Type Aliases vs Interfaces
type ID = string | number;

interface User {
  id: ID;
  name: string;
  email?: string; // Optional property
}

// String Union Types (preferred over basic enums)
type UserRole = 'ADMIN' | 'USER' | 'GUEST';
```

## Code Examples
Below is a comprehensive example demonstrating Interfaces, Classes, Generics, and Async programming in TypeScript:

```typescript
// Interfaces
interface Identifiable {
  id: string;
}

enum Priority {
  Low, 
  Medium, 
  High
}

// Classes and OOP
class Task implements Identifiable {
  constructor(
    public id: string,
    public title: string,
    public priority: Priority = Priority.Medium
  ) {}
}

// Generics: Reusable Repository pattern
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

// Async Programming with Promises
class TaskLoader {
  // Simulate an asynchronous API call returning a Promise
  async fetchTasksFromApi(): Promise<Task[]> {
    return new Promise((resolve) => {
      resolve([
        new Task('1', 'Master TypeScript Fundamentals', Priority.High),
        new Task('2', 'Setup Angular Standalone App', Priority.Medium)
      ]);
    });
  }
}

// Executing the demo
async function runDemo(): Promise<void> {
  const loader = new TaskLoader();
  const repo = new Repository<Task>();

  const tasks = await loader.fetchTasksFromApi();
  tasks.forEach(t => repo.add(t));

  console.log("Loaded Tasks:", repo.getAll());
}

runDemo();
```

## Best Practices
1. **Avoid the `any` Type**: Using `any` disables all type safety and defeats the purpose of TypeScript. When the data structure is truly dynamic or unknown, use `unknown` and narrow the type with type guards (`typeof`, `instanceof`).
2. **Use Interfaces for Object Models**: Use `interface` to define API contracts, domain models, and public object shapes because interfaces support extension (`extends`) and declaration merging.
3. **Use `readonly` for Immutability**: Mark properties that should never change after initialization as `readonly` to prevent accidental mutations.

## Common Mistakes
* **Overusing Numeric Enums**: Numeric enums in TypeScript can allow out-of-bounds numeric assignments without warning. Prefer string literal union types (`type Role = 'admin' | 'editor' | 'viewer';`).
* **Ignoring `strictNullChecks`**: Accessing nested properties without verifying whether the parent object is `null` or `undefined`. Always keep `strict: true` enabled in `tsconfig.json`.

## Interview Questions & Answers
### Q: What is the difference between an Interface and a Type Alias?
**A**: Interfaces are extendable, support declaration merging (multiple declarations with the same name merge their properties), and work seamlessly with OOP `implements`. Type aliases (`type`) are more flexible for defining union types (`string | number`), intersection types, tuples, primitive aliases, and mapped types.

### Q: What is the difference between `any` and `unknown`?
**A**: Both types can represent any JavaScript value. However, `any` turns off all compiler type checking, allowing unsafe property access. On the other hand, `unknown` is type-safe; the compiler refuses to allow any operations on an `unknown` value until you narrow its type using runtime checks (like `typeof` or `instanceof`).

## Summary
TypeScript is the industry standard for modern frontend and backend development. By introducing static types, interfaces, generics, and compile-time validation, it helps developers eliminate entire categories of runtime bugs while keeping enterprise codebases clean, maintainable, and scalable.

---

Previous : [Setup and Environment](./02_Setup_and_Environment.md) | Index : [Home](./00_index.md) | Next : [Angular Architecture](./04_Angular_Architecture.md)
