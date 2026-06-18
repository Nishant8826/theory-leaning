# Beginner Interview Prep

## What is it?
Beginner Interview Preparation compiles foundational concepts, syntax conventions, and framework features that developers should know when interviewing for entry-level Angular roles.

## Why do we need it?
Interviewing can be challenging without structured preparation. Reviewing core concepts—like component structure, interpolation, direct bindings, and setup CLI tools—helps developers answer questions confidently and demonstrate solid technical foundations.

```
Preparation Flow:
Review Core Definitions ──> Study Direct Bindings ──> Practice CLI Commands ──> Build Simple Demos ──> Ace the Interview
```

## How does it work?
1. **Foundations Check**: Covers what Angular is, single-page application (SPA) architectures, and setup tools.
2. **Template Binding**: Tests knowledge of interpolation, property/event binding, and directive properties.
3. **TypeScript Integration**: Verifies basic understandings of variables, classes, and interfaces.

## Impact
* **Application Architecture**: Establishes a solid understanding of component-driven code layouts.
* **Performance**: Promotes using the Angular CLI and clean bindings to avoid common performance pitfalls.
* **Scalability**: Helps developers structure basic components correctly, paving the way for larger applications.

## Real World Example
An entry-level candidate is asked to explain the difference between a component and a template during a technical interview. The candidate explains that components manage behavior while templates define layout, demonstrating a clear understanding of the framework's architecture.

## Syntax
A basic component structure:
```typescript
@Component({
  selector: 'app-hello',
  standalone: true,
  template: `<p>Hello, {{ name }}!</p>`
})
export class HelloComponent {
  name = 'World';
}
```

## Code Examples
Below is an implementation of a basic component that covers interpolation, click events, and list directives.

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-greet-box',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="greet-card">
      <h2>Hello, {{ guestName }}!</h2>
      <button (click)="changeName()">Greet Admin</button>
      
      <h4>Core Frameworks:</h4>
      <ul>
        <li *ngFor="let item of frameworks">{{ item }}</li>
      </ul>
    </div>
  `,
  styles: [`
    .greet-card { border: 1px solid #10b981; padding: 15px; border-radius: 6px; max-width: 250px; }
  `]
})
export class GreetBoxComponent {
  guestName = 'Guest';
  frameworks = ['Angular', 'React', 'Vue'];

  changeName() {
    this.guestName = 'Admin';
  }
}
```

## Best Practices
1. **Always Use the Angular CLI**: Use CLI generator commands to scaffold components, services, and directives to ensure standard structures.
2. **Enable Strict TypeScript Mode**: Configure typescript to strict check values to avoid common runtime errors.
3. **Write Thin Component Classes**: Delegate data fetching and business calculations to services, keeping components focused on presentation.

## Common Mistakes
* **Mutating DOM Elements Directly**: Using native DOM APIs (like `document.getElementById`) inside component classes. This bypasses Angular's change detection and can cause rendering bugs.
* **Forgetting Parentheses in Interpolation**: Writing `{{ myProperty }}` without defining the property in the class, which throws compilation errors.

## Interview Questions & Answers

### Q1: What is Angular and what are its main features?
**A**: Angular is a component-based, production-ready frontend framework developed by Google. Its main features include a component-driven architecture, built-in dependency injection, two-way data binding, routing engines, form management, and an HTTP client, providing a complete solution for building Single Page Applications (SPAs).

### Q2: What is the difference between a Component and a Directive?
**A**: A component is structurally a directive that has an associated HTML template and style sheet. A directive is a class without a template that attaches styles or behaviors to existing DOM elements (such as showing a tooltip on hover).

### Q3: What is Interpolation and how is it written?
**A**: Interpolation is a syntax used to display dynamic values from component classes inside HTML templates. It is written using double curly braces, e.g. `{{ variableName }}`, and Angular evaluates the expression and renders the string output in the DOM.

### Q4: What are the main bindings available in templates?
**A**: The main bindings are:
1. **Interpolation**: Renders class values as text: `{{ title }}`.
2. **Property Binding**: Binds class values to DOM element properties: `[src]="imageUrl"`.
3. **Event Binding**: Listens to user interactions and triggers class methods: `(click)="onSave()"`.
4. **Two-Way Binding**: Synchronizes input elements and class properties: `[(ngModel)]="username"`.

### Q5: What is the purpose of the Angular CLI?
**A**: The Angular CLI (Command Line Interface) is a command-line tool used to initialize, develop, test, build, and maintain Angular applications. It automates common tasks like generating components, running local development servers, and compiling production assets.

### Q6: Explain what Standalone Components are.
**A**: Standalone components are components that set `standalone: true` and specify their dependencies directly in their `imports` array, bypassing the legacy module-based container architecture (`NgModule`) and making code easier to reuse and maintain.

## Summary
Beginner interviews focus on core foundations like CLI tools, component setups, interpolation, and template bindings. Reviewing these concepts helps candidates demonstrate solid technical baselines.

---

Previous : [Real World E-Commerce Project](./27_Real_World_ECommerce_Project.md) | Index : [Home](./00_index.md) | Next : [Intermediate Interview Prep](./29_Interview_Prep_Intermediate.md)
