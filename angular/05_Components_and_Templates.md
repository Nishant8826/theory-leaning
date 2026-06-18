# Components and Templates

## What is it?
A component is the fundamental block of an Angular application. It encapsulates three parts: the UI (HTML template), the layout styling (CSS), and the logical behavior (TypeScript class). Templates are the HTML representation of the view, annotated with special Angular template syntax to bind and render data.

## Why do we need it?
In vanilla web development, syncing JS variables with the DOM requires repetitive `document.getElementById().innerText = value` queries. Angular components and templates solve this by providing automated, declarative data binding. This ensures that the layout updates instantly whenever logic variables change, preventing desynchronization.

```
┌─────────────────────────────────────────────────────────┐
│                    Component Class                      │
│                  username: 'Nishant'                    │
└──────────────────────────┬──────────────────────────────┘
                           │ (Data Binding)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    HTML Template                        │
│             <p>Welcome, {{ username }}</p>              │
└─────────────────────────────────────────────────────────┘
```

## How does it work?
1. **Property Binding & Interpolation**: Values flow from the component class down into the DOM template.
2. **Event Binding**: Interactive actions (clicks, keypresses) flow up from the DOM template to trigger methods in the component class.
3. **Two-Way Binding**: Synchronizes the class variable and the DOM input element automatically.
4. **Change Detection**: When a event occurs, Angular checks for changes in variables and updates the template.

## Impact
* **Application Architecture**: Strongly component-oriented. Promotes reusable, isolated UI widgets.
* **Performance**: Ivy compiles templates into compact JavaScript functions, bypassing slow virtual DOM diff structures.
* **Maintainability**: Clear division between design (HTML/CSS) and presentation behavior (TS).

## Real World Example
On a user settings page, when the user types their new username in a text box, the header text updates in real-time, and a "Save" button becomes enabled as a direct result of data binding.

## Syntax
* **Interpolation**: `{{ expression }}`
* **Property Binding**: `[target]="expression"`
* **Event Binding**: `(target)="statement()"`
* **Two-Way Binding**: `[(ngModel)]="property"`
* **Template Reference Variable**: `#varName`

## Code Examples
Below is a complete standalone component demonstrating all template binding mechanisms.

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

      <!-- 4. Two-Way Binding (requires FormsModule) -->
      <div class="edit-section">
        <label for="username-input">Edit Name: </label>
        <input id="username-input" [(ngModel)]="name" placeholder="Enter name" />
      </div>

      <!-- 5. Template Reference Variable -->
      <div class="ref-section">
        <input #phoneInput type="text" placeholder="Enter phone" />
        <button (click)="logPhone(phoneInput.value)">Log Phone Value</button>
      </div>
    </div>
  `,
  styles: [`
    .profile-card { border: 1px solid #ccc; padding: 16px; border-radius: 8px; max-width: 300px; }
    .avatar { width: 100px; height: 100px; border-radius: 50%; display: block; margin: 10px 0; }
    .edit-section, .ref-section { margin-top: 15px; }
    input { padding: 4px; border: 1px solid #aaa; border-radius: 4px; }
  `]
})
export class UserProfileComponent {
  name: string = 'Nishant';
  isLoggedIn: boolean = true;
  avatarUrl: string = 'https://api.dicebear.com/7.x/bottts/svg?seed=Nishant';

  toggleStatus(): void {
    this.isLoggedIn = !this.isLoggedIn;
  }

  logPhone(value: string): void {
    console.log('Phone number:', value);
  }
}
```

## Best Practices
1. **No Side Effects in Interpolation**: Avoid executing complex computation inside `{{ }}` templates as they execute on every change detection cycle.
2. **Use Two-Way Binding Exclusively for Form Elements**: Limit `[(ngModel)]` to user input controls, utilizing unidirectional bindings elsewhere.
3. **Prefer Component Styles**: Use encapsulated styles (`styles` or `styleUrls`) instead of polluting global style sheets.

## Common Mistakes
* **Syntax Confusions**: Forgetting square brackets for property binding, e.g. `<img src="imageUrl">` will set the source strictly to the literal string `"imageUrl"` instead of binding to the class property.
* **Binding directly to expensive methods**: Calling an expensive method like `[disabled]="calculateTax()"` inside template bindings, degrading user interface responsiveness.

## Interview Questions & Answers
### Q: What is the difference between Property Binding and Interpolation?
**A**: Interpolation is a specialized syntax that converts its contents to a string and inserts them into HTML text. Property binding is more general; it binds a value directly to a DOM element property, allowing you to pass complex types (objects, arrays, booleans) directly to native elements or custom component input fields.

### Q: What is a Template Reference Variable and how do you use it?
**A**: A template reference variable (declared using `#varName`) is a reference to a DOM element, directive, or component within a template. It allows you to access its properties (like value, classes, and native methods) in another part of the same template without writing event handlers or TypeScript logic.

## Summary
Components combine TypeScript logic with HTML templates and styles. Template bindings (interpolation, property, event, two-way, and reference variables) form the reactive connection that links class state to visual markup.

---

Previous : [Angular Architecture](./04_Angular_Architecture.md) | Index : [Home](./00_index.md) | Next : [Pipes](./06_Pipes.md)
