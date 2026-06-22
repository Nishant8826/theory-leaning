# Template-Driven Forms

## What is it?
Template-Driven Forms rely on directives inside the HTML template to build and manage form models. Instead of creating programmatic form groups, developers write HTML inputs and bind state using directives like `ngModel` and standard validation attributes (`required`, `email`, `minlength`).

## Why do we need it?
Every application requires forms (like logins, search filters, or feedback cards) to collect user inputs. For simple forms, writing programmatic configurations can feel repetitive. Template-driven forms provide a declarative way to manage values and validation directly within HTML markup, reducing setup overhead.

```
Template-Driven Form (HTML Centric):
Input Tag (with ngModel) ──> Angular automatically creates Form Control
                         ──> Validations evaluated in HTML (required, email)
                         ──> Exposes state variable to class via #myForm="ngForm"
```

## How does it work?
1. **`FormsModule`**: Enables template-driven form directives across standalone components.
2. **`ngModel`**: Automatically registers inputs with the parent form group and handles two-way data binding.
3. **`ngForm`**: Attached to `<form>` tags to track the overall validity, dirty/pristine states, and submit events.
4. **HTML validation attributes**: Attributes like `required`, `email`, and `minlength` are processed by Angular to update the form's validity state.

## Impact
* **Application Architecture**: Binds forms to template configurations, which is useful for simple inputs but can be harder to test.
* **Performance**: Lightweight and fast to load, with minimal logic overhead.
* **Maintainability**: Centralizes simple validations inside the template, keeping the component class clean.

## Real World Example
A newsletter signup box contains a single email input and a submit button. The email input must validate its format and require entry before enabling the submit button.

## Syntax
* **Binding input**: `<input name="username" [(ngModel)]="user.username" />`
* **Form reference**: `<form #signupForm="ngForm" (ngSubmit)="onSubmit(signupForm)">`
* **Validation reference**: `<input #emailRef="ngModel" name="email" required email />`

## Hinglish Explanation

Template-Driven Forms ka simple matlab hai **"Validation aur Form structure ka saara control HTML template me hi rakhna"**. Is approach me component class (TypeScript) me minimal code likhna padta hai, aur logic attributes HTML tags me hi set hote hain (jaise `required`, `email`, `minlength`).

### 1. ngModel (Do-tarfa Connection)
* Jab input tag me `[(ngModel)]="user.username"` lagate hain, toh input ki value aur component variable aapas me dynamically sync ho jate hain.
* **Maha-mantra (Rule):** `ngModel` use karne par input tag me `name="username"` attribute hona mandatory hai. Agar `name` miss kiya, toh compiler page ko crash kar dega.

### 2. ngForm (Form ka Remote Control)
* Pure form tag ko control karne ke liye hum ek template variable banate hain: `#regForm="ngForm"`.
* Is remote control se hum pure form ki validation status check kar sakte hain, jaise submit button tabhi active ho jab form valid ho: `[disabled]="regForm.invalid"`.

### 3. Validation States (CSS classes)
Angular automatically input element par CSS classes apply karta hai jo design styling me bohot kaam aate hain:
* `.ng-untouched` / `.ng-touched` (User ne field ko select kiya ya nahi)
* `.ng-pristine` / `.ng-dirty` (User ne type karna shuru kiya ya nahi)
* `.ng-valid` / `.ng-invalid` (Field rules correct hain ya galat)

## Code Examples
Below is a complete implementation of a template-driven signup form with validation.

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
      
      <!-- NgForm Reference -->
      <form #regForm="ngForm" (ngSubmit)="handleSubmit(regForm)" novalidate>
        
        <!-- Username input with validation -->
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

        <!-- Email input with validation -->
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
            <span *ngIf="emailRef.errors?.['email']">Enter a valid email format.</span>
          </div>
        </div>

        <button type="submit" [disabled]="regForm.invalid">Submit</button>
      </form>
    </div>
  `,
  styles: [`
    .form-container { border: 1px solid #10b981; padding: 20px; border-radius: 8px; max-width: 320px; }
    .field { margin-bottom: 12px; }
    label { display: block; margin-bottom: 4px; font-weight: bold; }
    input { width: 100%; padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; box-sizing: border-box; }
    .error-msg { color: #dc2626; font-size: 12px; margin-top: 4px; }
    button { background: #10b981; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; }
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
      console.log('Form Submitted successfully!', this.user);
      form.resetForm(); // Reset form and validation state
    }
  }
}
```

## Best Practices
1. **Always Set the Name Attribute**: Directives like `ngModel` require the `name` attribute on input tags to register them with the parent form group.
2. **Handle CSS states**: Use classes like `.ng-invalid` and `.ng-touched` to apply styles (like red borders) to invalid fields.
3. **Use novalidate**: Add the `novalidate` attribute to your `<form>` tag to disable browser validations and allow Angular to handle validation styling.

## Common Mistakes
* **Forgetting the Name Attribute**: Forgetting to add the `name` attribute on an input tag, which throws errors because `ngModel` cannot register the field without a name.
* **Testing Ambiguities**: Writing complex validation logic inside template markup. This makes it difficult to run unit tests without rendering the DOM.

## Interview Questions & Answers
### Q: What is the purpose of `ngModel` in template-driven forms?
**A**: `ngModel` is a directive that enables two-way data binding between input values and class properties. It also creates a `FormControl` instance behind the scenes to track the input's value, validity, and dirty/touched state.
* **Hinglish Explanation**: `ngModel` ek directive hai jo inputs aur component class variables ke beech double-way connection (two-way data binding) banata hai. Iske sath hi, yeh internal-level par ek `FormControl` instance bhi create karta hai jo field ki value, invalidity (sahi/galat status), aur touched/dirty state (user ne field me click kiya ya nahi) ko tracking ke liye manage karta hai.

### Q: How do you reset a template-driven form?
**A**: Query the template-driven form using a template reference variable (e.g. `#regForm="ngForm"`), pass it to your component class or submit method, and call `.resetForm()`. This resets the form value and clears dirty/touched styles.
* **Hinglish Explanation**: Form ko reset karne ke liye hum template me form ka handle le kar (jaise `#regForm="ngForm"`) submit method me use pass karte hain. Phir, component class ke submit function ke andar `.resetForm()` call karte hain. Yeh function form variables ki values ko reset toh karta hi hai, sath hi validation states (touched/dirty status aur unke red borders) ko bhi default par clear kar deta hai.

## Summary
Template-driven forms rely on HTML directive attributes (like `ngModel` and `required`) to handle simple input models. This approach reduces component class boilerplate, making it ideal for simple forms.

---

Previous : [Routing and Navigation](./13_Routing_and_Navigation.md) | Index : [Home](./00_index.md) | Next : [Reactive Forms](./15_Reactive_Forms.md)
