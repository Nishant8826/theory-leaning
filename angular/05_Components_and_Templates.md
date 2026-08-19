# Components and Templates

## What is it?
A Component is the fundamental building block of an Angular application. It encapsulates three core pillars:
1. **UI Presentation**: The HTML template defining the view structure.
2. **Styling**: Component-scoped CSS/SCSS rules.
3. **Behavioral Logic**: A TypeScript class handling user interactions, properties, and methods.

Templates are written in HTML augmented with Angular's expressive template syntax to bind and render dynamic data.

## Why do we need it?
In traditional web development, keeping JavaScript variables synchronized with the UI requires verbose and manual DOM querying (e.g., `document.getElementById('title').innerText = value`). 

Angular components and templates solve this by providing declarative, automated data binding. When the TypeScript class state updates, Angular automatically and efficiently synchronizes the UI without manual DOM manipulation.

```
┌─────────────────────────────────────────────────────────┐
│                    Component Class                      │
│                  username: 'Developer'                  │
└──────────────────────────┬──────────────────────────────┘
                           │ 
                           │ (Data Binding)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    HTML Template                        │
│             <p>Welcome, {{ username }}</p>              │
└─────────────────────────────────────────────────────────┘
```

## How does it work?
1. **Interpolation & Property Binding**: Data flows unidirectionally from the component TypeScript class to the HTML template (One-Way: Class -> View).
2. **Event Binding**: User interactions (such as clicks, input changes, and keystrokes) trigger methods defined in the TypeScript class (One-Way: View -> Class).
3. **Two-Way Binding**: Simultaneously synchronizes form input controls with TypeScript class variables using the `[(ngModel)]` syntax.
4. **Change Detection**: When an asynchronous event occurs (such as a click or HTTP response), Angular checks if data has changed and updates the corresponding DOM nodes.

## Impact
* **Application Architecture**: Encourages a modular, component-driven UI architecture composed of isolated, reusable visual widgets.
* **Performance**: The Ivy compiler transforms templates into compact, optimized JavaScript instructions, bypassing the need for a heavy runtime Virtual DOM diffing engine.
* **Maintainability**: Clear separation between visual layout (HTML), styles (CSS), and component behavior (TypeScript) makes code easy to test and refactor.

## Real World Example
In a user profile settings page, as the user types a new username in a text input, the profile header dynamically updates in real time, and the "Save Changes" button automatically enables as soon as form validation rules are satisfied.

## Syntax
Angular data binding syntax cheat sheet:
* **Interpolation**: `{{ expression }}` (Embeds evaluated string values).
* **Property Binding**: `[target]="expression"` (Binds data to a DOM element property or component `@Input()`).
* **Event Binding**: `(target)="statement()"` (Listens for DOM events and calls methods).
* **Two-Way Binding**: `[(ngModel)]="property"` (Two-way data synchronization via `FormsModule`).
* **Template Reference Variable**: `#refName` (Creates a local reference to a DOM node or child component).

## Code Examples
Below is a complete standalone component demonstrating all major binding types:

```typescript
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="profile-card">
      <!-- 1. Interpolation -->
      <h2>User: {{ name.toUpperCase() }}</h2>
      <p>Status: {{ isLoggedIn ? 'Active' : 'Offline' }}</p>

      <!-- 2. Property Binding -->
      <img [src]="avatarUrl" [alt]="name + ' Avatar'" class="avatar" />

      <!-- 3. Event Binding -->
      <div class="actions">
        <button (click)="toggleStatus()">Toggle Online Status</button>
      </div>

      <!-- 4. Two-Way Data Binding (requires FormsModule) -->
      <div class="edit-section">
        <label for="username-input">Edit Name: </label>
        <input id="username-input" [(ngModel)]="name" placeholder="Enter name" />
      </div>

      <!-- 5. Template Reference Variable -->
      <div class="ref-section">
        <input #phoneInput type="text" placeholder="Enter phone number" />
        <button (click)="logPhone(phoneInput.value)">Log Phone Value</button>
      </div>
    </div>
  `,
  styles: [`
    .profile-card { 
      border: 1px solid #ccc; 
      padding: 16px; 
      border-radius: 8px; 
      max-width: 320px; 
    }
    .avatar { 
      width: 100px; 
      height: 100px; 
      border-radius: 50%; 
      display: block; 
      margin: 10px 0; 
    }
    .edit-section, .ref-section { 
      margin-top: 15px; 
    }
    input { 
      padding: 6px; 
      border: 1px solid #aaa; 
      border-radius: 4px; 
      margin-right: 5px;
    }
    button {
      padding: 6px 12px;
      cursor: pointer;
    }
  `]
})
export class UserProfileComponent {
  name: string = 'Alex Developer';
  isLoggedIn: boolean = true;
  avatarUrl: string = 'https://api.dicebear.com/7.x/bottts/svg?seed=Alex';

  toggleStatus(): void {
    this.isLoggedIn = !this.isLoggedIn;
  }

  logPhone(value: string): void {
    console.log('Phone number entered:', value);
  }
}
```

## Best Practices
1. **Avoid Expensive Computations in Templates**: Never invoke methods that perform heavy loops, calculations, or API calls directly inside `{{ }}` or property bindings, as they re-execute on every change detection cycle. Use pure pipes or Signals/computed values instead.
2. **Use Two-Way Binding Only Where Necessary**: Reserve `[(ngModel)]` for form controls. For general component data flow, prefer unidirectional inputs and outputs.
3. **Encapsulate Component Styles**: Leverage Angular's default style encapsulation (`ViewEncapsulation.Emulated`) to keep CSS rules scoped to their component without leaking into the global application.

## Common Mistakes
* **Missing Property Binding Brackets**: Writing `<img src="avatarUrl">` instead of `<img [src]="avatarUrl">`. Without square brackets, the literal string `"avatarUrl"` is assigned rather than the component property value.
* **Binding to Non-Pure Function Calls**: Writing `[disabled]="calculateIsDisabled()"` in templates can cause severe UI lag because the function is re-evaluated constantly during change detection.

## Interview Questions & Answers
### Q: What is the difference between Property Binding and Interpolation?
**A**: Interpolation (`{{ }}`) is syntactic sugar that evaluates expressions and converts the result into a string inserted into the template text. Property binding (`[property]="value"`) directly sets a DOM property or `@Input()` with its native type (boolean, array, object, or number), avoiding string conversion.

### Q: What is a Template Reference Variable and how is it used?
**A**: A template reference variable (declared using `#varName`) is a reference to a DOM element, component instance, or directive within the template. It allows you to read element properties (e.g., `#inputField` -> `inputField.value`) and pass them into event handlers without writing boilerplate component logic.

## Summary
Components unite TypeScript logic, HTML templates, and scoped CSS into modular UI building blocks. Template bindings (interpolation, property, event, two-way, and template reference variables) establish clean, declarative connections between application state and the rendered UI.

---

Previous : [Angular Architecture](./04_Angular_Architecture.md) | Index : [Home](./00_index.md) | Next : [Pipes](./06_Pipes.md)
