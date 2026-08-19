# Reactive Forms

## What is it?
Reactive Forms is a model-driven, programmatic approach to handling form inputs and validations in Angular. Built on top of reactive programming principles and immutable data structures, Reactive Forms manage form controls, validation rules, and state transitions explicitly in TypeScript, exposing values and validation statuses as RxJS Observables.

## Why do we need it?
In complex enterprise applications, forms often require dynamic field additions (e.g., repeating line items), conditional validation rules, cross-field dependencies, and asynchronous backend validation checks. 

Template-Driven Forms struggle to handle these advanced requirements cleanly. Reactive Forms solve this by decoupling the entire form model, validation logic, and state management from the HTML template and placing it directly into the TypeScript component class, making complex forms robust, predictable, and easy to unit test.

```
Reactive Form Flow (Model-Centric):
TypeScript Class defines FormControl structure ──> Binds to HTML via [formGroup] & formControlName
                                                ──> Values and status emit as RxJS streams
                                                ──> Validation logic unit-tested synchronously in isolation
```

## How does it work?
1. **`ReactiveFormsModule`**: Must be imported into the component's `imports: [...]` array to enable reactive form directives.
2. **`FormControl`**: Tracks the value, validation status, and user interaction flags (`dirty`, `touched`) of an individual input field.
3. **`FormGroup`**: Groups a collection of `FormControl`, `FormGroup`, or `FormArray` instances into a single object schema.
4. **`FormArray`**: Manages an ordered, index-based array of form controls, allowing fields to be dynamically inserted, reordered, or removed at runtime.
5. **`FormBuilder` / `NonNullableFormBuilder`**: A syntactic helper service that reduces boilerplate when instantiating complex nested form groups and controls.
6. **Validators**: Pure functions that accept an `AbstractControl` and return either `ValidationErrors` or `null` (for synchronous validation) or an `Observable<ValidationErrors | null>` (for asynchronous validation).

## Impact
* **Application Architecture**: Centralizes all form schemas and validation rules inside TypeScript classes, keeping HTML templates clean and purely presentational.
* **Performance**: Direct programmatic access and predictable immutable updates eliminate continuous template parsing overhead.
* **Maintainability**: Pure TypeScript validation functions can be thoroughly unit-tested in isolation without rendering any HTML DOM elements.

## Real World Example
In a financial loan application wizard:
- Applicants dynamically add or remove co-signers and employment history entries via `FormArray`.
- The form validates unique ID numbers against a backend database via asynchronous validators.
- Total household income and loan eligibility are recalculated reactively by subscribing to `form.valueChanges`.

## Syntax
* **Instantiating a FormGroup**:
```typescript
profileForm = new FormGroup({
  name: new FormControl('', Validators.required),
  email: new FormControl('', [Validators.required, Validators.email])
});
```
* **Binding to the Template**:
```html
<form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
  <input formControlName="name" />
  <input formControlName="email" />
</form>
```

## Code Examples
Below is a complete implementation demonstrating typed reactive forms, dynamic `FormArray` management, custom synchronous validators, and async username availability checking:

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

// 1. Custom Synchronous Validator (Disallow "admin")
export function forbiddenNameValidator(control: AbstractControl): ValidationErrors | null {
  const forbidden = /admin/i.test(control.value);
  return forbidden ? { forbiddenName: { value: control.value } } : null;
}

// 2. Custom Asynchronous Validator (Simulated Backend Username Check)
export class UniqueUsernameValidator {
  static createValidator(): (control: AbstractControl) => Observable<ValidationErrors | null> {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      if (!control.value) return of(null);
      // Simulate an asynchronous API verification call
      return of(control.value.toLowerCase() === 'developer123' ? { usernameTaken: true } : null).pipe(
        delay(800) // Simulate network latency
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
      <h3>User Registration (Reactive)</h3>
      <form [formGroup]="regForm" (ngSubmit)="onSubmit()">
        
        <!-- Username Field -->
        <div class="field">
          <label for="username">Username</label>
          <input id="username" formControlName="username" />
          
          <div *ngIf="regForm.get('username')?.pending" class="pending">
            Checking username availability...
          </div>
          
          <div *ngIf="regForm.get('username')?.invalid && regForm.get('username')?.touched" class="error">
            <span *ngIf="regForm.get('username')?.errors?.['required']">Username is required.</span>
            <span *ngIf="regForm.get('username')?.errors?.['forbiddenName']">"admin" is a reserved name.</span>
            <span *ngIf="regForm.get('username')?.errors?.['usernameTaken']">This username is already taken.</span>
          </div>
        </div>

        <!-- Dynamic FormArray for Hobbies -->
        <div class="field" formArrayName="hobbies">
          <label>Hobbies / Skills</label>
          <div *ngFor="let hobby of hobbies.controls; let i = index" class="array-row">
            <input [formControlName]="i" placeholder="Enter skill or hobby" />
            <button type="button" class="btn-remove" (click)="removeHobby(i)">Remove</button>
          </div>
          <button type="button" class="btn-add" (click)="addHobby()">+ Add Hobby</button>
        </div>

        <button type="submit" [disabled]="regForm.invalid || regForm.pending" class="btn-submit">
          Register User
        </button>
      </form>
    </div>
  `,
  styles: [`
    .form-box { border: 1px solid #3b82f6; padding: 24px; border-radius: 8px; max-width: 420px; font-family: sans-serif; }
    .field { margin-bottom: 16px; }
    label { display: block; font-weight: bold; margin-bottom: 6px; }
    input { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    .array-row { display: flex; gap: 8px; margin-bottom: 8px; }
    .error { color: #dc2626; font-size: 12px; margin-top: 4px; }
    .pending { color: #d97706; font-size: 12px; margin-top: 4px; }
    .btn-add { background: #e0f2fe; color: #0284c7; border: 1px dashed #0284c7; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
    .btn-remove { background: #fee2e2; color: #dc2626; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; }
    .btn-submit { background: #3b82f6; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 15px; }
    .btn-submit:disabled { background: #9ca3af; cursor: not-allowed; }
  `]
})
export class ReactiveRegistrationComponent implements OnInit {
  regForm!: FormGroup;

  ngOnInit(): void {
    this.regForm = new FormGroup({
      username: new FormControl('', {
        validators: [Validators.required, forbiddenNameValidator],
        asyncValidators: [UniqueUsernameValidator.createValidator()],
        updateOn: 'blur' // Run async validator only when user unfocuses the input
      }),
      hobbies: new FormArray<FormControl<string>>([])
    });
  }

  get hobbies(): FormArray {
    return this.regForm.get('hobbies') as FormArray;
  }

  addHobby(): void {
    this.hobbies.push(new FormControl('', { nonNullable: true, validators: Validators.required }));
  }

  removeHobby(index: number): void {
    this.hobbies.removeAt(index);
  }

  onSubmit(): void {
    if (this.regForm.valid) {
      console.log('Valid Registration Payload:', this.regForm.value);
    }
  }
}
```

## Best Practices
1. **Use Strictly Typed Forms**: Leverage strongly-typed `FormControl<T>` and `FormGroup<T>` (introduced in Angular 14+) to ensure type safety across all form values and mutations.
2. **Optimize Asynchronous Validators with `updateOn: 'blur'`**: Avoid running heavy async API validation on every keystroke. Set `updateOn: 'blur'` on the `FormControl` configuration to validate only when the user navigates away from the field.
3. **Use `FormBuilder` for Cleaner Syntax**: Inject `FormBuilder` (`fb = inject(FormBuilder)`) to instantiate nested groups, controls, and arrays with concise syntax.

## Common Mistakes
* **Type Casting `FormArray` Controls**: Forgetting to typecast `form.get('hobbies')` as a `FormArray` in component getters, which causes template compiler errors under strict TypeScript checks.
* **Unmanaged Subscriptions to `valueChanges`**: Subscribing directly to `control.valueChanges` inside `ngOnInit` without cleaning up via `takeUntilDestroyed()` or `ngOnDestroy`, causing memory leaks.

## Interview Questions & Answers
### Q: What is the difference between a `FormGroup` and a `FormArray`?
**A**: A `FormGroup` manages a fixed, key-value collection of named controls where each control is identified by a property key (e.g., `form.get('email')`). A `FormArray` manages an index-based, dynamically sizable collection of controls (e.g., `array.at(0)`), allowing controls to be pushed, inserted, or removed at runtime.

### Q: What is the difference between `setValue()` and `patchValue()` in Reactive Forms?
**A**: `setValue()` requires an exact structural match and will throw a runtime error if any control property in the group is omitted. `patchValue()` updates only the properties supplied in the object payload, safely ignoring missing keys.

## Summary
Reactive Forms offer a programmatic, model-driven architecture for complex form management in Angular. With strongly typed controls, dynamic FormArrays, and stream-based validation, they deliver unmatched flexibility, testability, and predictability for enterprise web applications.

---

Previous : [Template-Driven Forms](./14_Template_Driven_Forms.md) | Index : [Home](./00_index.md) | Next : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md)
