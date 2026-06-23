# Components and Templates

## What is it?
Component Angular application ka sabse basic aur important building block hai. Yeh teen parts ko encapsulate karta hai: UI (HTML template), layout styling (CSS), aur logical behavior (TypeScript class). Templates HTML layout hote hain jo view ko represent karte hain, aur inme data show/bind karne ke liye special Angular template syntax use hota hai.

## Why do we need it?
Vanilla web development me, JS variables ko DOM ke sath sync rakhne ke liye baar-baar `document.getElementById().innerText = value` jaise element queries likhne padte hain. Angular components aur templates ise declarative aur automated data binding ke zariye solve karte hain. Isse jab bhi runtime logic variables change hote hain, UI instantly aur automatically update ho jati hai.

```
┌─────────────────────────────────────────────────────────┐
│                    Component Class                      │
│                  username: 'Nishant'                    │
│└──────────────────────────┬──────────────────────────────┘
│                            │ (Data Binding)
│                            ▼
│┌─────────────────────────────────────────────────────────┐
││                    HTML Template                        │
││             <p>Welcome, {{ username }}</p>              │
│└─────────────────────────────────────────────────────────┘
```

## How does it work?
1. **Property Binding & Interpolation**: Values component class se generate hokar bottom direction me HTML DOM template me display hoti hain (One-Way).
2. **Event Binding**: Interactive actions (clicks, keypresses) view layer se trigger hokar up direction me component class ke methods ko trigger karte hain (One-Way).
3. **Two-Way Binding**: Input elements aur TypeScript variables ko double-way sync structure me bind kar deta hai (Two-Way).
4. **Change Detection**: Jab bhi koi browser event trigger hota hai, Angular check karta hai ki kya koi data variables change huye hain, aur update hone par template ko refresh karta hai.

## Impact
* **Application Architecture**: Fully component-oriented architecture. Reusable, isolated, aur independent UI widgets banane ko promote karta hai.
* **Performance**: Ivy compiler templates ko high-performance, compact JavaScript functions me compile karta hai, jisse virtual DOM diff calculations bypass ho jate hain.
* **Maintainability**: Web page styling (HTML/CSS) aur dynamic code presentation behavior (TS) me saaf separation of concerns rehta hai.

## Real World Example
User settings page par, jaise hi user text box me apna naya username type karta hai, header text real-time me updates dikhane lagta hai aur data binding ki wajah se 'Save' button dynamically active ho jata hai.

## Syntax
* **Interpolation**: `{{ expression }}`
* **Property Binding**: `[target]="expression"`
* **Event Binding**: `(target)="statement()"`
* **Two-Way Binding**: `[(ngModel)]="property"`
* **Template Reference Variable**: `#varName`

## Code Examples
Neeche dynamic data bindings support karne wale standalone component ka full example diya gaya hai:

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
1. **No Side Effects in Interpolation**: Templates me `{{ }}` brackets ke andar kabhi bhi complex computations ya expensive loops execute na karein, kyunki yeh change detection cycle par baar-baar run hote hain.
2. **Use Two-Way Binding Exclusively for Form Elements**: Input elements ko chhodkar, other logic flows ke liye normal unidirectional bindings target karein.
3. **Prefer Component Styles**: Global CSS codebases ko pollute karne ke bajaye, component level `styles` ya style encapsulation settings utilize karein.

## Common Mistakes
* **Syntax Confusions**: Property binding ke liye square brackets na lagana, jaise `<img src="imageUrl">` likhne par src variable string `"imageUrl"` set ho jayega na ki variable value.
* **Binding directly to expensive methods**: Elements dynamic behaviors me expensive logic lagana, jaise `[disabled]="calculateTax()"`, jo pure page updates ko slow aur unresponsive bana deta hai.

## Interview Questions & Answers
### Q: What is the difference between Property Binding and Interpolation?
**A**: Interpolation ek direct shortcut syntax hai jo values ko string me badal kar templates me insert karta hai. Property binding generic hai; yeh variable data ko directly DOM properties ke sath connect karta hai, jiske through object, array ya boolean dynamic types elements me pass kiye ja sakte hain.

### Q: What is a Template Reference Variable and how do you use it?
**A**: Template reference variable (jo `#varName` se declare hota hai) template inside HTML elements, directives ya child components ka ek reference identifier hota hai. Yeh direct values ya inputs ko template me access karne me help karta hai bina TS file handlers setup kiye.

## Summary
Components TypeScript code, HTML template, aur design styles ka ek package hote hain. Template bindings (interpolation, property, event, two-way, aur template variables) state variables aur visual page markup ke beech dynamic link activate karte hain.

---

Previous : [Angular Architecture](./04_Angular_Architecture.md) | Index : [Home](./00_index.md) | Next : [Pipes](./06_Pipes.md)
