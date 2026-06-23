# Reactive Forms

## What is it?
Reactive Forms Angular applications me form status manage karne ka model-driven programmatic approach hain. Yeh immutable data patterns aur coordinates ke structures par work karte hain aur form controls values, dynamic value streams aur validation status ka synchronous verification support provide karte hain.

## Why do we need it?
Complex enterprise applications me jab large aur heavy inputs features design karne hote hain, tab simple template-driven models limits tough ho jati hain. Jaise dynamic form inputs modify karna, database APIs values sync checks execute karna, ya validations rules ke test cases verify karna. Reactive forms validations control coordinates setup HTML markers se coordinate paths bypass karke class component TS file me transfer karte hain, jo structural testing aur scaling options easy banate hain.

```
Reactive Form Flow (Model Centric):
TypeScript Class defines FormControl structure ──> Bind to HTML via formControlName
                                               ──> Values/status changes flow as RxJS streams
                                               ──> Unit test validation rules synchronously
```

## How does it work?
1. **`ReactiveFormsModule`**: Component code metadata array imports directives me reactive options support enable karne ke liye declare hona chahiye.
2. **`FormControl`**: Dynamic variables state inputs indicators level par single fields data status aur values check values maintain karta hai.
3. **`FormGroup`**: Multiple controls objects schemas (key-value pair details) bundle coordination handle karta hai.
4. **`FormArray`**: Ordered inputs fields checks arrays details maintain karta hai jisse dynamically list elements add aur delete methods coordinates settings process kiye ja sakein.
5. **Validators**: Form variables fields filters parameters jo check validations logic run karte hain. Yeh synchronous (`Validators.required`) ya asynchronous (caching data fetch checks database queries validation options) use cases target kar sakte hain.

## Impact
* **Application Architecture**: Form controls details aur configuration setup TS class levels logic parameters me encapsulate karta hai.
* **Performance**: Synchronous data state operations update behaviors change verification predictions dynamic optimize rakhte hain.
* **Maintainability**: Complete forms status validations methods code testing unit flows execute checks smooth ho jate hain.

## Real World Example
Dynamic user registration form me, checkout options select settings coordinates par dynamic fields append logic inject karna (jaise parameters "Add Phone" inputs click events handle checks) aur data check validator validation checks active trigger coordinate features reactive structure configurations me simple implement ho jate hain.

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
**A**: `FormGroup` fixed schema ke key-value variables objects controls handle karta hai. `FormArray` index-based list controls maintain karta hai jo elements coordinates dynamically dynamic add/delete options interfaces support karta hai.

### Q: How do you configure a validator to only run on blur?
**A**: `FormControl` inputs configuration attributes array parameter initialization coordinates block target me `updateOn: 'blur'` configuration property assign karke.

## Summary
Reactive forms components level dynamic definitions controls (`FormGroup`, `FormControl`, `FormArray`) code architectures manage karte hain. Programmatic validators validations coordinate flows, secure configurations setups scaling robust systems ensure karte hain.

---

Previous : [Template-Driven Forms](./14_Template_Driven_Forms.md) | Index : [Home](./00_index.md) | Next : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md)
