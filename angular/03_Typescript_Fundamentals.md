# TypeScript Fundamentals

## What is it?
TypeScript ek open-source, strongly-typed programming language hai jo JavaScript par hi bani hai. Yeh JavaScript ka ek superset hai, jiska matlab hai ki har valid JavaScript code valid TypeScript hai. Yeh plain JavaScript me compile hoti hai taaki kisi bhi web browser par execute ho sake.

## Why do we need it?
JavaScript dynamically typed hai, jiski wajah se silent errors aate hain aur wo directly application run hone (runtime) par hi pata chalte hain. Jaise ki, kisi function me galat object pass kar dene se app crash ho sakta hai. TypeScript compiler-time par hi type checking add kar dene se code likhte waqt hi IDE errors show kar deta hai, inline APIs documentation de deta hai, aur smart autocomplete provide karta hai.

```
JS Flow:
Write Code ──> Run App ──> User clicks button ──> TypeError: Cannot read properties of undefined (Runtime Crash)

TS Flow:
Write Code ──> Compiler checks types ──> Reports error during coding ──> Fix immediately (Production Safe)
```

## How does it work?
1. **Type Checker**: Compilation ke dauran chalta hai taaki ensure kar sake ki variables, arguments, aur return types declared types ke rules ko follow kar rahe hain.
2. **TSConfig**: Config file (`tsconfig.json`) yeh guidelines batata hai ki TypeScript kitni strictly type checking karega aur kis ECMA version me code compile karega.
3. **Transpilation**: Compilation ke waqt saare type annotations ko remove kar ya strips out kiya jata hai, aur plain JavaScript bachti hai jise browser engines execute kar sakein.

## Impact
* **Application Architecture**: Strict classes, interfaces, aur design patterns ke zariye code architecture ko improve karta hai.
* **Performance**: Runtime par zero overhead hota hai. Saare TypeScript annotations compile ke waqt remove ho jate hain.
* **Maintainability**: Refactoring behad predictable ho jati hai, kyunki ek parameter name change karne par compiler un sabhi places ko point out kar deta hai jahan wo use ho raha hai.

## Real World Example
Checkout form model code karte waqt, TypeScript interface `interface CartItem { id: string; price: number; }` design karne se developer galti se bhi string value ko number calculations me forward nahi kar zeg, jisse mathematical errors se bacha ja sakta hai.

## Syntax
Common TS typings aur syntax elements:
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
TypeScript me Classes, OOP, Generics, aur Async programming ka ek comprehensive example:

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
      resolve([
        new Task('1', 'Learn TypeScript', Priority.High),
        new Task('2', 'Setup Angular CLI', Priority.Medium)
      ]);
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
1. **Avoid `any` Type**: `any` type declare karne se TypeScript compile checks bypass ho jate hain. Agar type dynamic hai toh `unknown` use karein aur use logic se check karein (narrow down).
2. **Use Interfaces for Object Models**: Public APIs aur application data models ke liye `interface` use karein kyunki yeh OOP patterns aur extension (declaration merging) support karta hai.
3. **ReadOnly Modifiers**: Aise variables jinhe object initialize karne ke baad modify nahi karna chahiye, unhe `readonly` set karein.

## Common Mistakes
* **Overusing Enums**: Basic numeric enums ko compiler prevent nahi kar pata compile time me. Unke badle string enums ya literal type unions prefer karein: `type Role = 'admin' | 'user'`.
* **Ignoring strictNullChecks**: Kisi object key ko access karna bina check kiye ki wo value defined hai ya null, jisse runtime error aa sakta hai. Humesha strict config settings enable rakhein.

## Interview Questions & Answers
### Q: What is the difference between an Interface and a Type Alias?
**A**: Interfaces extension ke liye open hoti hain (same name se dubara declare karne par merge ho jati hain), classes me `implements` support karti hain, aur object shapes ke liye best hain. Type aliases (`type`) primitives, unions, tuples, aur intersections ke variables setup me use hote hain, jo complex mapping ke liye powerful hain.

### Q: What does `unknown` mean and how is it different from `any`?
**A**: Dono hi kisi bhi value ko represent kar sakte hain. Lekin `any` use karne par compiler saare checks bypass kar deta hai. Jabki `unknown` type-safe hai; compiler tab tak operations block rakhta hai jab tak aap type checks (jaise `typeof` ya `instanceof`) se variable type narrow nahi kar lete.

## Summary
TypeScript modern web development ka standard hai. Isme types, classes, interfaces, generics, aur async helpers add hone se, developers ko coding time par hi bugs find karne me help milti hai aur enterprise codebase clean aur readable rehta hai.

---

Previous : [Setup and Environment](./02_Setup_and_Environment.md) | Index : [Home](./00_index.md) | Next : [Angular Architecture](./04_Angular_Architecture.md)
