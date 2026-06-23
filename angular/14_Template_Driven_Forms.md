# Template-Driven Forms

## What is it?
Template-Driven Forms HTML templates ke andar direct directives and attributes ka use karke form models aur validation structure setup karte hain. Isme programmatic configurations class files me likhne ke bajaye, HTML inputs elements par directives (jaise `ngModel`) aur standard validations attributes (jaise `required`, `email`, `minlength`) apply kiye jate hain.

## Why do we need it?
Har web application me forms (jaise login, signups, search bars, ya feedback panels) user data collect karne ke liye use hote hain. Simple forms setup ke liye TS class me programmatic configurations configure karna repetitive aur verbose lagta hai. Template-driven forms template parameters directives ke zariye declarative way me validation aur state setup direct HTML code me handle kar dete hain.

```
Template-Driven Form (HTML Centric):
Input Tag (with ngModel) ──> Angular automatically creates Form Control
                         ──> Validations evaluated in HTML (required, email)
                         ──> Exposes state variable to class via #myForm="ngForm"
```

## How does it work?
1. **`FormsModule`**: Standalone component declarations me template-driven features active karne ke liye standard module register check apply karta hai.
2. **`ngModel`**: Dynamic value flow aur event tracking input element ko parent form controller me auto-register kar data sync (two-way) handle karta hai.
3. **`ngForm`**: Form elements wrapper `<form>` tags par attach hokar values coordinate karta hai, forms fields dirty/pristine states trace karta hai aur form submission events coordinate karta hai.
4. **HTML validation attributes**: Standard attributes (jaise `required`, `email`, `minlength`) browser engine validations check Angular inputs system ke dynamic validation algorithms par redirect mapping check logic run karte hain.

## Impact
* **Application Architecture**: Form attributes aur validations direct templates structure coordinate settings me run karte hain, jo simple inputs settings ke liye neat hai par heavy complex layouts custom tests me limits badha sakta hai.
* **Performance**: Lightweight rendering flow, minimally logic memory processing resources utilize karta hai.
* **Maintainability**: Custom parameters validation templates ke limits me encapsulate hone ke karan component logic TS code files tidy rehti hain.

## Real World Example
Newsletter subscription popup form me simple email input field aur button setup required hota hai. Hamen HTML validations controls input tag me specify karne hote hain taaki email pattern values check correctly complete hone par submit actions automatically enable parameters coordinates update kar de.

## Syntax
* **Binding input**: `<input name="username" [(ngModel)]="user.username" />`
* **Form reference**: `<form #signupForm="ngForm" (ngSubmit)="onSubmit(signupForm)">`
* **Validation reference**: `<input #emailRef="ngModel" name="email" required email />`

## Code Examples
Signup form validation aur submission operations ka custom template-driven implementation model:

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
      form.resetForm();
    }
  }
}
```

## Best Practices
1. **Always Set the Name Attribute**: Directives jaise `ngModel` use karte waqt input elements me standard `name` attribute declare karna mandatory hai taaki compiler data tracking maps correctly bind kar sake.
2. **Handle CSS states**: Input fields validation visual alerts setup karne ke liye Angular status dynamic CSS classes (jaise `.ng-invalid`, `.ng-touched`) class styles apply karein.
3. **Use novalidate**: Form tag configurations parameters me standard `novalidate` declare karein taaki default browser validation engines bypass hokar component logic checks customize trigger hon.

## Common Mistakes
* **Forgetting the Name Attribute**: Input elements options declare karte waqt `name` parameter miss karna, jiske chalte page render failures aur compilation errors check loops return ho jate hain.
* **Testing Ambiguities**: Validations formulas layout checks expressions parameters directly template HTML markers me include karna, jise programmatic unit testing algorithms coordinate tests bypass systems mock structures access setups tough ho jate hain.

## Interview Questions & Answers
### Q: What is the purpose of `ngModel` in template-driven forms?
**A**: `ngModel` input tag value aur component class properties me two-way data sync set karta hai aur internally default dynamic `FormControl` values tracking handle karta hai.

### Q: How do you reset a template-driven form?
**A**: Template variable link (jaise `#regForm="ngForm"`) reference select karke class component logic method ke coordinates parameters target me `.resetForm()` parameter execute command apply karein.

## Summary
Template-driven forms HTML element level parameters attributes direct declarations rules (ngModel, required) check simple structure forms design optimization manage karte hain. Isse extra class files logics boilerplate code minimize ho jata hai.

---

Previous : [Routing and Navigation](./13_Routing_and_Navigation.md) | Index : [Home](./00_index.md) | Next : [Reactive Forms](./15_Reactive_Forms.md)
