# Template-Driven Forms

## What is it?
Template-Driven Forms in Angular use HTML templates and directives (such as `ngModel`) to create form models, manage input bindings, and handle validation rules directly within the markup. Instead of creating programmatic form structures in TypeScript, form state and validation logic are driven declaratively by HTML attributes and Angular directives.

## Why do we need it?
Almost every web application collects user input through forms (e.g., login screens, search filters, newsletter subscriptions, feedback forms). For simple forms with basic requirements, defining complex programmatic structures in TypeScript can feel verbose. 

Template-Driven Forms allow developers to set up two-way data binding and validation rules directly inside the HTML template quickly and with minimal boilerplate.

```
Template-Driven Form (HTML Centric):
Input Tag (with ngModel) ──> Angular automatically creates an internal FormControl
                         ──> Validations evaluated in HTML (required, email, minlength)
                         ──> Exposes form state to class via #myForm="ngForm"
```

## How does it work?
1. **`FormsModule`**: Must be imported into the standalone component's `imports: [...]` array to enable template-driven form directives.
2. **`ngModel`**: Creates an internal `FormControl` instance, binds the HTML input to a property on the TypeScript component, and manages two-way data synchronization (`[(ngModel)]`).
3. **`ngForm`**: Automatically attaches to any `<form>` element when `FormsModule` is present. It aggregates all child `ngModel` controls into a single form group, tracks the form's validity states (`dirty`, `touched`, `valid`, `invalid`), and intercepts submit events.
4. **HTML Validation Attributes**: Directives parse standard HTML validation attributes (e.g., `required`, `minlength`, `maxlength`, `pattern`, `email`) and update the control's validity state dynamically.

## Impact
* **Application Architecture**: Keeps form validation and data binding declarative and template-centric. Best suited for simple, straightforward forms.
* **Performance**: Lightweight for small forms, but relies heavily on two-way data binding and internal template directives.
* **Maintainability**: Easy to read for simple UI inputs, but becomes harder to manage and test as form requirements grow complex (e.g., dynamic multi-step wizards or cross-field validations).

## Real World Example
A newsletter signup modal or a simple search filter input where a user enters an email address and clicks "Subscribe". The input validation, error message display, and submit button states are managed directly in the template.

## Syntax
* **Two-way input binding**: `<input name="username" [(ngModel)]="user.username" />`
* **Form reference**: `<form #signupForm="ngForm" (ngSubmit)="onSubmit(signupForm)">`
* **Control reference for validation**: `<input #emailRef="ngModel" name="email" required email />`

## Code Examples
Below is a complete implementation of a template-driven newsletter registration form with validation and error messaging:

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';

@Component({
  selector: 'app-signup-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="form-container">
      <h3>Newsletter Signup</h3>
      
      <form #regForm="ngForm" (ngSubmit)="handleSubmit(regForm)" novalidate>
        
        <!-- Username Field -->
        <div class="field">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username"
            name="username" 
            [(ngModel)]="user.username" 
            #userRef="ngModel" 
            required 
            minlength="4" />
          
          <div *ngIf="userRef.invalid && (userRef.dirty || userRef.touched)" class="error-msg">
            <span *ngIf="userRef.errors?.['required']">Username is required.</span>
            <span *ngIf="userRef.errors?.['minlength']">Must be at least 4 characters.</span>
          </div>
        </div>

        <!-- Email Field -->
        <div class="field">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email"
            name="email" 
            [(ngModel)]="user.email" 
            #emailRef="ngModel" 
            required 
            email />
          
          <div *ngIf="emailRef.invalid && (emailRef.dirty || emailRef.touched)" class="error-msg">
            <span *ngIf="emailRef.errors?.['required']">Email is required.</span>
            <span *ngIf="emailRef.errors?.['email']">Please enter a valid email address.</span>
          </div>
        </div>

        <button type="submit" [disabled]="regForm.invalid">Submit</button>
      </form>
    </div>
  `,
  styles: [`
    .form-container { 
      border: 1px solid #10b981; 
      padding: 20px; 
      border-radius: 8px; 
      max-width: 320px; 
      font-family: sans-serif;
    }
    .field { margin-bottom: 14px; }
    label { display: block; margin-bottom: 4px; font-weight: bold; }
    input { width: 100%; padding: 6px 8px; border: 1px solid #d1d5db; border-radius: 4px; box-sizing: border-box; }
    input.ng-invalid.ng-touched { border-color: #dc2626; }
    .error-msg { color: #dc2626; font-size: 12px; margin-top: 4px; }
    button { background: #10b981; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
    button:disabled { background: #9ca3af; cursor: not-allowed; }
  `]
})
export class SignupFormComponent {
  user = {
    username: '',
    email: ''
  };

  handleSubmit(form: NgForm): void {
    if (form.valid) {
      console.log('Form Submitted successfully:', this.user);
      form.resetForm();
    }
  }
}
```

## Best Practices
1. **Always Specify the `name` Attribute**: When using `[(ngModel)]` inside a `<form>`, the `name` attribute is mandatory. Angular uses the `name` attribute to register the control with the parent `NgForm` group.
2. **Add `novalidate` to `<form>`**: Add the `novalidate` attribute to the `<form>` element to prevent the browser's default HTML5 validation tooltips from clashing with Angular's custom validation messages.
3. **Leverage Angular CSS Status Classes**: Style valid/invalid states using Angular's automatic CSS classes (`.ng-touched`, `.ng-dirty`, `.ng-invalid`, `.ng-valid`).

## Common Mistakes
* **Missing the `name` Attribute**: Omitting the `name` attribute on an input using `ngModel` inside a form causes a runtime error because Angular cannot register the control.
* **Overcomplicating with Template-Driven Forms**: Attempting to implement complex dynamic form arrays, multi-step wizards, or cross-field validation with template-driven forms. Use **Reactive Forms** for complex scenarios instead.

## Interview Questions & Answers
### Q: What is the role of `ngModel` in Template-Driven Forms?
**A**: `ngModel` creates an implicit `FormControl` instance, binds the form input value to a component property via two-way data binding, registers the input with the parent `NgForm` directive, and tracks validation status (`touched`, `dirty`, `valid`, `invalid`).

### Q: How do you reset a Template-Driven Form in Angular?
**A**: Capture a template reference variable to `ngForm` (e.g., `#regForm="ngForm"`), pass it to the submission method, and invoke `form.resetForm()`. This clears both the underlying model values and resets state flags (`pristine`, `untouched`).

## Summary
Template-Driven Forms provide a fast, declarative approach to managing simple forms in Angular. By applying `ngModel` and standard validation attributes directly within the template, you can handle input binding and validation with minimal TypeScript configuration.

---

Previous : [Routing and Navigation](./13_Routing_and_Navigation.md) | Index : [Home](./00_index.md) | Next : [Reactive Forms](./15_Reactive_Forms.md)
