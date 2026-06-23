# Component Communication

## What is it?
Component Communication un techniques aur patterns ko represent karta hai jiske zariye components aapas me data, commands, aur events share karte hain. Yeh techniques components ke isolated instances ke tree structures ko aapas me interact karke ek unified web application ki tarah chalne me help karti hain.

## Why do we need it?
Components ko reusable aur isolated rakhne ke liye unhe separate folders me design kiya jata hai. Lekin, wo fully azaad/isolated hokar app nahi chala sakte. Jaise ki, ek product-list component ko shopping-cart component ko notify karna padta hai jab user "Add to Cart" par click kare. Component communication patterns define karte hain ki kaise data (inputs/outputs) aur services safely coordinate honge.

```
          ┌──────────────────────────────────┐
          │         Parent Component         │
          │     [data]           (onEvent)   │
          └───────┬──────────────────▲───────┘
                  │                  │
  1. Input Binding│                  │ 2. Output Event
  (Data Down)     │                  │ (Events Up)
                  ▼                  │
          ┌──────────────────────────┴───────┐
          │         Child Component          │
          └──────────────────────────────────┘
```

## How does it work?
1. **Parent-to-Child (`@Input` / modern `input()` Signal)**: Data top directions me parent component se child inputs variables me flow hota hai.
2. **Child-to-Parent (`@Output` & `EventEmitter` / modern `output()` API)**: Child components actions complete hone par event signals/payloads parent events handlers me emit karte hain.
3. **Template Queries (`@ViewChild`, `@ViewChildren`, `@ContentChild`)**: Components class ko programmatic access deta hai child components views, template refs ya projected structures par.
4. **Content Projection (`<ng-content>`)**: Parent component ko child template layout coordinates ke andar custom HTML segments inject karne ki facility deta hai.
5. **Dynamic Components**: Container directives (`ViewContainerRef`) aur helpers classes ke zariye runtime code configurations par dynamically load hone wale components.

## Impact
* **Application Architecture**: Solid component state separation logic (Smart components manage state; Dumb components manage presentation).
* **Performance**: Direct variables transmission se global stores parameters updates bypass hote hain, jisse changes immediate local limits me apply ho jate hain.
* **Maintainability**: Clear and defined inputs/outputs boundaries code testing aur debugging ko easy banate hain.

## Real World Example
Video streaming app dashboard page me, parent component select ki gayi video URL child player component me pass karta hai (using `@Input`), aur jab play complete ho jata hai, tab child event emit karta hai (using `@Output`) taaki dashboard script next episode trigger kar sake.

## Syntax
* **Inputs & Outputs**:
  - Input: `@Input() item: string = '';`
  - Output: `@Output() itemSelected = new EventEmitter<string>();`
* **ViewChild Query**: `@ViewChild('childRef') childElement!: ElementRef;`
* **Content Projection**: `<ng-content select=".card-header"></ng-content>`

## Code Examples
Neeche Parent-Child communication, content projection, view queries, aur shared services ka full implementation diya gaya hai:

### `child-card.component.ts`
```typescript
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child-card',
  standalone: true,
  template: `
    <div class="card">
      <div class="header">
        <ng-content select="[card-title]"></ng-content>
      </div>

      <div class="body">
        <p>Item: {{ itemName }}</p>
        <p>Quantity Available: {{ stock }}</p>
      </div>

      <button (click)="buyItem()" [disabled]="stock <= 0">Buy Now</button>
    </div>
  `,
  styles: [`
    .card { border: 1px solid #10b981; padding: 16px; border-radius: 8px; margin: 10px 0; }
    .header { font-weight: bold; font-size: 18px; margin-bottom: 8px; }
  `]
})
export class ChildCardComponent {
  @Input() itemName: string = '';
  @Input() stock: number = 0;
  @Output() purchase = new EventEmitter<string>();

  buyItem() {
    this.purchase.emit(this.itemName);
  }
}
```

### `parent-dashboard.component.ts`
```typescript
import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { ChildCardComponent } from './child-card.component';

@Component({
  selector: 'app-parent-dashboard',
  standalone: true,
  imports: [ChildCardComponent],
  template: `
    <div class="dashboard">
      <h2>E-Commerce Dashboard</h2>
      
      <app-child-card 
        #productCard
        [itemName]="'Mechanical Keyboard'" 
        [stock]="5" 
        (purchase)="handlePurchase($event)">
        <span card-title>Premium Hardware</span>
      </app-child-card>
 
      <p class="notification">{{ message }}</p>
    </div>
  `,
  styles: [`
    .dashboard { padding: 20px; font-family: sans-serif; }
    .notification { color: #2563eb; font-weight: bold; }
  `]
})
export class ParentDashboardComponent implements AfterViewInit {
  message = '';

  @ViewChild('productCard') childInstance!: ChildCardComponent;

  ngAfterViewInit() {
    console.log('Queried Child Stock:', this.childInstance.stock);
  }

  handlePurchase(product: string) {
    this.message = `Purchase requested for: ${product}`;
  }
}
```

### Unrelated Components Communication (Using Shared Services)

#### `theme.service.ts`
```typescript
import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  themeSignal = signal<'light' | 'dark'>('light');

  private themeSubject = new BehaviorSubject<'light' | 'dark'>('light');
  theme$ = this.themeSubject.asObservable();

  toggleTheme() {
    const nextTheme = this.themeSignal() === 'light' ? 'dark' : 'light';
    this.themeSignal.set(nextTheme);
    this.themeSubject.next(nextTheme);
  }
}
```

#### `component-a.component.ts`
```typescript
import { Component } from '@angular/core';
import { ThemeService } from './theme.service';

@Component({
  selector: 'app-comp-a',
  standalone: true,
  template: `<button (click)="themeService.toggleTheme()">Toggle System Theme</button>`
})
export class ComponentA {
  constructor(public themeService: ThemeService) {}
}
```

#### `component-b.component.ts`
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemeService } from './theme.service';

@Component({
  selector: 'app-comp-b',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div [class]="currentThemeSignal()">
      <p>Active Theme (Signal): {{ currentThemeSignal() }}</p>
      <p>Active Theme (RxJS): {{ themeService.theme$ | async }}</p>
    </div>
  `
})
export class ComponentB {
  currentThemeSignal;

  constructor(public themeService: ThemeService) {
    this.currentThemeSignal = this.themeService.themeSignal;
  }
}
```

## Best Practices
1. **Unidirectional Data Flow**: Data humesha downward (Inputs) flow hona chahiye aur events upward (Outputs). Child components ke andar direct input variables modify (mutate) na karein.
2. **Use Content Projection for Wrapper UI**: Custom dialog popups, cards, list grids layouts templates reuse ke liye `<ng-content>` use karein.
3. **Explicit Output Typing**: EventEmitter variables setup karte waqt emitted type hamesha specify karein (jaise `new EventEmitter<string>()` na ki standard type-less structure).

## Common Mistakes
* **Mutating Parent State Directly**: Child component ke andar direct parent arrays/objects modifications trigger karna. Isse Angular check updates systems rules break ho sakte hain aur dynamic values debug mushkil ho jata hai.
* **Accessing `@ViewChild` properties inside `ngOnInit`**: Template elements render hone se pehle hi view reference access karne ki koshish karna. Humesha `@ViewChild` attributes `ngAfterViewInit` method cycle ke baad use karein.

## Interview Questions & Answers
### Q: What is the difference between `@ViewChild` and `@ContentChild`?
**A**: `@ViewChild` component ke apne template elements select karne me use hota hai. `@ContentChild` external markup content elements select karta hai jo `<ng-content>` container template ke zariye project (inject) huye hon.

### Q: What is content projection and how do you achieve multi-slot projection?
**A**: Content projection parent elements HTML structures child components spaces me insert karne ka method hai. Multi-slot projection ke liye selectors custom names select attributes compile tags me configure karte hain.

## Summary
Component communication isolated elements ko connect karta hai. Inputs data bottom flow map banate hain, outputs alerts return events forward karte hain, aur view queries dynamic variables classes methods control karne me help karte hain. Content projection parent layout parameters directly insert karne ki flexibility deta hai.

---

Previous : [Component Lifecycle](./08_Component_Lifecycle.md) | Index : [Home](./00_index.md) | Next : [Signals](./10_Signals.md)
