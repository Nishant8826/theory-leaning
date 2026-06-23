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
1. **`FormsModule`**: Standalone component me template-driven features ko use karne ke liye ise imports array me register kiya jata hai.
2. **`ngModel`**: Yeh component class aur input elements ke beech data flow (two-way data binding) aur value tracking ko handle karta hai.
3. **`ngForm`**: Yeh dynamic form controls ko auto-detect karta hai, form ke state (dirty, pristine, valid, invalid) ko track karta hai, aur submit events handle karta hai.
4. **`HTML validation attributes`**: Standard HTML validation rules (required, minlength, email) ko direct templates me attach kiya jata hai jinhe Angular parse kar validations verify karta hai.

## Impact
* **Application Architecture**: Validation aur data binding HTML templates me hi manage hoti hai. Yeh simple forms ke liye toh sahi hai par complex forms ke testing aur scaling me dikkat karta hai.
* **Performance**: Light framework footprint ke chalte local inputs change fast render hote hain.
* **Maintainability**: Chote validation rules HTML code me hi rehne se TS file compact rehti hai.

## Real World Example
Jaise newsletter subscription popup me sirf ek email input aur submit button hota hai. Yahan HTML input validation rules direct define karke complete form configuration check ki ja sakti hai.

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
1. **Always Set the Name Attribute**: `ngModel` use karte waqt inputs me `name` attribute lagana zaroori hai, warna form control correctly register nahi ho payega.
2. **Handle CSS states**: Validation UI styling ke liye Angular dwara automatic apply hone wali CSS classes (jaise `.ng-invalid`, `.ng-touched`) ka use karein.
3. **Use novalidate**: Form tag par `novalidate` lagayein taaki browser ka default validation disabled ho jaye aur Angular ka custom validation logic chale.

## Common Mistakes
* **Forgetting the Name Attribute**: `ngModel` ke sath `name` attribute design na karna, jiske chalte run-time par data synchronization error ho sakta hai.
* **Testing Complexity**: Validation logic HTML templates me likha hone ke karan components ko programmatically unit test karna mushkil ho jata hai.

## Interview Questions & Answers
### Q: What is the purpose of `ngModel` in template-driven forms?
**A**: `ngModel` input control ko bind karta hai component properties se, aur template validation/state tracking ko maintain karta hai.

### Q: How do you reset a template-driven form?
**A**: Template side variable reference (jaise `#regForm="ngForm"`) ke through reference lekar TS component code me `regForm.resetForm()` method call karein.

## Summary
Template-driven forms simple forms ke liye design kiye gaye hain. HTML attributes ke zariye bindings aur validations declare kiye jate hain jisse template aur logic code separated rehkar dynamic forms create ho jate hain.

---

Previous : [Routing and Navigation](./13_Routing_and_Navigation.md) | Index : [Home](./00_index.md) | Next : [Reactive Forms](./15_Reactive_Forms.md)
