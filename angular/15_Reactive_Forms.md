# Reactive Forms

### What is it?
Reactive Forms Angular applications me form state manage karne ka model-driven programmatic approach hai. Yeh immutable data patterns par work karte hain, aur form controls values aur validation status ko streams ke roop me provide karte hain.

## Why do we need it?
Complex enterprise applications me jab dynamic form fields, conditional validation rules, aur APIs sync ki zaroorat hoti hai, tab template-driven forms restrict ho jate hain. Reactive forms complete form state aur validations ko template (HTML) se alag karke component class (TypeScript) me transfer karte hain, jisse complex logic handle karna aur unit testing karna behad aasan ho jata hai.

```
Reactive Form Flow (Model Centric):
TypeScript Class defines FormControl structure ──> Bind to HTML via formControlName
                                               ──> Values/status changes flow as RxJS streams
                                               ──> Unit test validation rules synchronously
```

## How does it work?
1. **`ReactiveFormsModule`**: Reactive forms features ko components me use karne ke liye standalone components ke `imports` block me use kiya jata hai.
2. **`FormControl`**: Yeh single input field ke value, status, aur validation rules ko track karta hai.
3. **`FormGroup`**: Yeh multiple FormControls ko group karta hai (jaise ek complete form shape).
4. **`FormArray`**: Yeh ordered list of controls maintain karta hai jisse dynamically new fields add ya remove kiye ja sakein.
5. **Validators**: Form fields validation apply karne ke functions hain (jaise synchronous `Validators.required` ya asynchronous username check validator).

## Impact
* **Application Architecture**: Form structure aur logic template se alag rehkar TypeScript file me centralized rehta hai.
* **Performance**: Direct programmatic validations updates change detection logic ke through fast rendering ensure karte hain.
* **Maintainability**: Pure class component ko bin rendering ke isolate testing context me test kiya ja sakta hai.

## Real World Example
Jaise dynamic user registration form me user event ke basis par naye input fields (phone numbers) dynamically append karna, custom validators add karna, aur instant validation status verify karna reactive forms me easy hai.

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

## Code Examples
Neeche dynamic FormArray, synchronous aur asynchronous custom validators use karne wala signup component implementation model diya gaya hai:

```typescript
import { Component, OnInit } from '@angular/core';
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
import { delay } from 'rxjs/operators';

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

        <div class="field" formArrayName="hobbies">
          <label>Hobbies</label>
          <div *ngFor="let hobby of hobbies.controls; let i = index">
            <input [formControlName]="i" />
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
        updateOn: 'blur'
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
**A**: `FormGroup` ek predefined key-value object schema ke controls ko handle karta hai. `FormArray` index-based dynamic list of controls ko hold karta hai jisme dynamically input fields ko add/remove kiya ja sakta hai.

### Q: How do you configure a validator to only run on blur?
**A**: `FormControl` create karte waqt option parameters block me `updateOn: 'blur'` set karke dynamic check apply kar sakte hain.

## Summary
Reactive forms component class me dynamically forms instantiate karne ke kaam aate hain. Inke programmatic validators aur values changes observables systems code scaling aur unit testing ko aasan banate hain.

---

Previous : [Template-Driven Forms](./14_Template_Driven_Forms.md) | Index : [Home](./00_index.md) | Next : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md)
