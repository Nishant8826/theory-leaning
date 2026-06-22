# Reactive Forms

## What is it?
Reactive Forms provide a programmatic, model-driven approach to managing form state in Angular. They are built around immutable data structures and provide synchronous access to form controls, value streams, and validation state.

## Why do we need it?
Simple template-driven forms can become difficult to manage when building large, dynamic enterprise forms. For instance, if you need to add inputs dynamically, validate values against database APIs in real-time, or write unit tests for validation rules, reactive forms are a better choice. They move validation and control configuration out of the HTML and into the component's TypeScript class, offering better scalability and testability.

```
Reactive Form Flow (Model Centric):
TypeScript Class defines FormControl structure ──> Bind to HTML via formControlName
                                               ──> Values/status changes flow as RxJS streams
                                               ──> Unit test validation rules synchronously
```

## How does it work?
1. **`ReactiveFormsModule`**: Must be imported by standalone components to enable reactive directives.
2. **`FormControl`**: Tracks the value and validation status of an individual form input.
3. **`FormGroup`**: Groups multiple `FormControl` (or other `FormGroup`) instances together.
4. **`FormArray`**: Manages an ordered array of form controls, allowing you to add or remove inputs dynamically.
5. **Validators**: Functions that validate controls. Can be synchronous (`Validators.required`) or asynchronous (checking database values via API).

## Impact
* **Application Architecture**: Moves form configuration to the logic layer, improving separation of concerns.
* **Performance**: Synchronous state updates make change detection predictable.
* **Maintainability**: Makes form rules and validations easy to test.

## Real World Example
In a user registration form, the application dynamically adds "Phone Number" fields when the user clicks "Add Phone", and validates the username's availability against a database API in real-time using an asynchronous validator.

## Syntax
* **Instantiating a Group**:
```typescript
profileForm = new FormGroup({
  name: new FormControl('', Validators.required),
  email: new FormControl('')
});
```
* **Binding to template**:
```html
<form [formGroup]="profileForm">
  <input formControlName="name" />
</form>
```

## Hinglish Explanation

Reactive Forms ko **"TypeScript-Driven Forms"** kehte hain. Is approach me form ka saara structure, configuration aur validation logic component class (TypeScript) me programmatically define kiya jata hai. HTML template me hum bas use bind karte hain.

### 1. Reactive Forms ke 3 pillars:
* **`FormControl`:** Yeh kisi single, individual input element (jaise email field) ka state aur value track karta hai.
* **`FormGroup`:** Yeh dynamic ya static structure me controls ko ek object shape (key-value pair) me bind karta hai.
* **`FormArray`:** Yeh dynamic inputs ke liye use hota hai jahan hum dynamic index check ke through list of fields ko programmatically add, insert ya delete kar sakte hain.

### 2. FormBuilder (Code helper)
Manual validation array aur FormControl syntax ko clean aur short likhne ke liye hum constructor me `FormBuilder` inject karte hain:
* `this.fb.group({ email: ['', Validators.required] })`

### 3. Reactive Forms ke Fayde:
* **Testing:** Validation logic TS me hota hai, isliye direct test cases likhna easy hota hai.
* **Dynamic validators:** Kisi field ki value ke status ke basis par hum programmatically validators change ya remove kar sakte hain (e.g. conditional fields).

## Code Examples
Below is an implementation of a dynamic reactive form containing custom synchronous and asynchronous validators, and a `FormArray`.

```typescript
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  ReactiveFormsModule, 
  FormGroup, 
  FormControl, 
  FormArray, 
  Validators, 
  AbstractControl, 
  ValidationErrors 
} from '@angular/forms';
import { Observable, of } from 'rxjs';
import { delay, map } from 'rxjs/operators';

// 1. Custom Synchronous Validator (Forbidden Words)
export function forbiddenNameValidator(control: AbstractControl): ValidationErrors | null {
  const forbidden = /admin/i.test(control.value);
  return forbidden ? { forbiddenName: { value: control.value } } : null;
}

// 2. Custom Asynchronous Validator (Username Availability Check)
export class UniqueUsernameValidator {
  static createValidator(): (control: AbstractControl) => Observable<ValidationErrors | null> {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      if (!control.value) return of(null);
      // Simulate API call check
      return of(control.value === 'nishant123' ? { usernameTaken: true } : null).pipe(
        delay(1000) // Simulate network delay
      );
    };
  }
}

@Component({
  selector: 'app-reactive-registration',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="form-box">
      <h3>User Registration</h3>
      <form [formGroup]="regForm" (ngSubmit)="onSubmit()">
        
        <!-- Name Field -->
        <div class="field">
          <label>Username</label>
          <input formControlName="username" />
          <div *ngIf="regForm.get('username')?.pending" class="pending">Checking availability...</div>
          <div *ngIf="regForm.get('username')?.invalid && regForm.get('username')?.touched" class="error">
            <span *ngIf="regForm.get('username')?.errors?.['required']">Username required.</span>
            <span *ngIf="regForm.get('username')?.errors?.['forbiddenName']">"admin" is forbidden.</span>
            <span *ngIf="regForm.get('username')?.errors?.['usernameTaken']">Username is already taken.</span>
          </div>
        </div>

        <!-- Dynamic FormArray Fields -->
        <div class="field" formArrayName="hobbies">
          <label>Hobbies</label>
          <div *ngFor="let hobby of hobbies.controls; let i = index">
            <input [formControlName Vice]="i" [formControl]="getHobbyControl(i)" />
            <button type="button" (click)="removeHobby(i)">Remove</button>
          </div>
          <button type="button" (click)="addHobby()">Add Hobby</button>
        </div>

        <button type="submit" [disabled]="regForm.invalid">Register</button>
      </form>
    </div>
  `,
  styles: [`
    .form-box { border: 1px solid #3b82f6; padding: 20px; border-radius: 8px; max-width: 400px; }
    .field { margin-bottom: 15px; }
    label { display: block; font-weight: bold; margin-bottom: 4px; }
    input { width: 70%; padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
    .error { color: #dc2626; font-size: 12px; margin-top: 4px; }
    .pending { color: #d97706; font-size: 12px; }
    button { padding: 6px 12px; margin: 4px; cursor: pointer; }
  `]
})
export class ReactiveRegistrationComponent implements OnInit {
  regForm!: FormGroup;

  ngOnInit() {
    this.regForm = new FormGroup({
      username: new FormControl('', {
        validators: [Validators.required, forbiddenNameValidator],
        asyncValidators: [UniqueUsernameValidator.createValidator()],
        updateOn: 'blur' // Run validation only on blur
      }),
      hobbies: new FormArray([])
    });
  }

  get hobbies(): FormArray {
    return this.regForm.get('hobbies') as FormArray;
  }

  getHobbyControl(index: number): FormControl {
    return this.hobbies.at(index) as FormControl;
  }

  addHobby() {
    this.hobbies.push(new FormControl('', Validators.required));
  }

  removeHobby(index: number) {
    this.hobbies.removeAt(index);
  }

  onSubmit() {
    if (this.regForm.valid) {
      console.log('Registration Data:', this.regForm.value);
    }
  }
}
```

## Best Practices
1. **Use Typed Forms**: Since Angular 14, default form controls are strongly typed. Avoid using untyped variants unless migrating legacy modules.
2. **Optimize Async Validation**: Use `updateOn: 'blur'` for fields with asynchronous validation to prevent API requests from running on every keystroke.
3. **Use `FormBuilder`**: Utilize the `FormBuilder` utility service to clean up form instantiation boilerplate.

## Common Mistakes
* **Type Casting Arrays**: Not casting `FormArray` controls correctly in templates, which can throw compilation errors when using strict TypeScript configurations.
* **Creating Memory Leaks with valueChanges**: Subscribing to `valueChanges` or `statusChanges` observables without cleaning them up in `ngOnDestroy`.

## Interview Questions & Answers
### Q: What is the difference between a FormArray and a FormGroup?
**A**: A `FormGroup` manages form controls as named key-value pairs (an object), which is ideal for fixed schemas. A `FormArray` manages form controls as an ordered list (an array), which is ideal for dynamic forms where inputs can be added or removed programmatically.
* **Hinglish Explanation**: `FormGroup` key-value pairs ke roop me form controls ko group (manage) karta hai (jaise ek JavaScript object jiska fixed schema ho, e.g. `{ name, email }`). `FormArray` form controls ko ek ordered list (index-based array) me manage karta hai. Yeh tab use hota hai jab dynamic forms banane hon jisme user buttons click karke fields add ya remove kar sake (jaise dynamic address fields ya dynamic list of hobbies).

### Q: How do you configure a validator to only run on blur?
**A**: Pass an options object as the second argument when instantiating a `FormControl`, and set `updateOn: 'blur'`. For example: `new FormControl('', { validators: [...], updateOn: 'blur' })`.
* **Hinglish Explanation**: Validator ko sirf focus change hone par (`blur` event) chalane ke liye hum `FormControl` create karte waqt config object me `updateOn: 'blur'` set karte hain. Jaise: `new FormControl('', { validators: [Validators.required], updateOn: 'blur' })`. Isse validation har keypress (keystroke) par chalne ke bajaye tabhi chalti hai jab user us field se cursor bahar le jata hai.

## Summary
Reactive forms use programmatic validation and configuration models to manage form state. They utilize groups (`FormGroup`), controls (`FormControl`), and arrays (`FormArray`) to build dynamic, scalable, and testable form architectures.

---

Previous : [Template-Driven Forms](./14_Template_Driven_Forms.md) | Index : [Home](./00_index.md) | Next : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md)
