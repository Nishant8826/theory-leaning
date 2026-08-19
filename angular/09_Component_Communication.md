# Component Communication

## What is it?
Component Communication refers to the patterns and mechanisms used by Angular components to exchange data, dispatch events, and invoke behaviors across component hierarchies. These communication techniques enable isolated, decoupled component trees to interact seamlessly as a unified web application.

## Why do we need it?
To maintain modularity and reusability, components are designed in isolation. However, real-world applications require components to share data and coordinate actions. For example, a `ProductListComponent` needs to notify a `ShoppingCartComponent` when a user clicks "Add to Cart". 

Standard communication patterns establish clear data boundaries, ensuring data flows predictably and changes remain easy to trace and debug.

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
1. **Parent-to-Child (`@Input()` / modern `input()` Signal)**: Data flows downward from parent to child via property binding.
2. **Child-to-Parent (`@Output()` with `EventEmitter` / modern `output()` API)**: Child components emit event payloads upward to parent event listeners.
3. **Template Queries (`@ViewChild`, `@ViewChildren`, `@ContentChild`)**: Grants the parent component programmatic access to child component instances, native DOM elements, or template references.
4. **Content Projection (`<ng-content>`)**: Allows a parent component to project custom HTML blocks into designated slots within a child component's template.
5. **Shared Services**: Unrelated or deeply nested sibling components communicate reactively via a shared singleton service powered by Signals or RxJS Subjects.

## Impact
* **Application Architecture**: Promotes the "Smart (Container) vs. Dumb (Presentational)" component pattern. Smart components manage data and state, while dumb components focus solely on presentation and inputs/outputs.
* **Performance**: Direct input/output bindings avoid global state overhead, confining change detection updates to the relevant local component branch.
* **Maintainability**: Clear, explicit component contracts make testing, mocking, and refactoring straightforward.

## Real World Example
In a video streaming platform:
- The parent dashboard passes the active video URL down to the child video player component using `@Input()`.
- When the video finishes playing, the child player emits a `videoEnded` event using `@Output()`, prompting the parent to trigger the next playlist episode.

## Syntax
* **Input & Output Decorators**:
  - Input: `@Input() itemName: string = '';`
  - Output: `@Output() itemSelected = new EventEmitter<string>();`
* **ViewChild Query**: `@ViewChild('childRef') childElement!: ElementRef;`
* **Content Projection**: `<ng-content select="[card-title]"></ng-content>`

## Code Examples
Below is a complete implementation covering parent-child communication, content projection, `@ViewChild` queries, and cross-component service communication:

### `child-card.component.ts`
```typescript
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child-card',
  standalone: true,
  template: `
    <div class="card">
      <div class="header">
        <!-- Content Projection Slot -->
        <ng-content select="[card-title]"></ng-content>
      </div>

      <div class="body">
        <p>Item: {{ itemName }}</p>
        <p>Quantity Available: {{ stock }}</p>
      </div>

      <button (click)="buyItem()" [disabled]="stock <= 0">
        {{ stock > 0 ? 'Buy Now' : 'Out of Stock' }}
      </button>
    </div>
  `,
  styles: [`
    .card { 
      border: 1px solid #10b981; 
      padding: 16px; 
      border-radius: 8px; 
      margin: 10px 0; 
    }
    .header { 
      font-weight: bold; 
      font-size: 18px; 
      margin-bottom: 8px; 
    }
    button {
      padding: 8px 16px;
      background-color: #10b981;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    button:disabled {
      background-color: #9ca3af;
      cursor: not-allowed;
    }
  `]
})
export class ChildCardComponent {
  @Input() itemName: string = '';
  @Input() stock: number = 0;
  @Output() purchase = new EventEmitter<string>();

  buyItem(): void {
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
      
      <!-- Parent to Child via [itemName] and [stock], Child to Parent via (purchase) -->
      <app-child-card 
        #productCard
        [itemName]="'Mechanical Keyboard'" 
        [stock]="5" 
        (purchase)="handlePurchase($event)">
        <span card-title>Premium Gaming Hardware</span>
      </app-child-card>
 
      <p class="notification" *ngIf="message">{{ message }}</p>
    </div>
  `,
  styles: [`
    .dashboard { padding: 20px; font-family: sans-serif; }
    .notification { color: #2563eb; font-weight: bold; margin-top: 15px; }
  `]
})
export class ParentDashboardComponent implements AfterViewInit {
  message = '';

  @ViewChild('productCard') childInstance!: ChildCardComponent;

  ngAfterViewInit(): void {
    console.log('Direct Child Query - Initial Stock:', this.childInstance.stock);
  }

  handlePurchase(product: string): void {
    this.message = `Purchase order created for: ${product}`;
  }
}
```

### Cross-Component Communication (Unrelated Components via Shared Service)

#### `theme.service.ts`
```typescript
import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  // Modern Signals approach
  themeSignal = signal<'light' | 'dark'>('light');

  // Traditional RxJS approach
  private themeSubject = new BehaviorSubject<'light' | 'dark'>('light');
  theme$ = this.themeSubject.asObservable();

  toggleTheme(): void {
    const nextTheme = this.themeSignal() === 'light' ? 'dark' : 'light';
    this.themeSignal.set(nextTheme);
    this.themeSubject.next(nextTheme);
  }
}
```

#### `component-a.component.ts` (Sender)
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

#### `component-b.component.ts` (Receiver)
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemeService } from './theme.service';

@Component({
  selector: 'app-comp-b',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div [class]="themeService.themeSignal()">
      <p>Active Theme (Signal): {{ themeService.themeSignal() }}</p>
      <p>Active Theme (RxJS): {{ themeService.theme$ | async }}</p>
    </div>
  `
})
export class ComponentB {
  constructor(public themeService: ThemeService) {}
}
```

## Best Practices
1. **Enforce Unidirectional Data Flow**: Always pass data down via inputs and emit events up via outputs. Never mutate parent objects directly inside child components.
2. **Use Content Projection for Reusable Containers**: For generic UI wrappers (dialogs, cards, accordions), leverage `<ng-content>` instead of complex nested inputs.
3. **Always Type EventEmitters**: Explicitly specify the generic payload type for `EventEmitter` (e.g., `new EventEmitter<string>()` instead of `new EventEmitter()`) to catch payload type mismatches at compile time.

## Common Mistakes
* **Direct State Mutation in Children**: Modifying parent arrays or objects inside a child component breaks change detection assumptions and makes debugging state changes extremely difficult.
* **Accessing `@ViewChild` in `ngOnInit`**: Attempting to read `@ViewChild` references before `ngAfterViewInit` results in `undefined` because child templates have not yet been rendered in the DOM.

## Interview Questions & Answers
### Q: What is the difference between `@ViewChild` and `@ContentChild`?
**A**: `@ViewChild` queries for an element, component, or directive located directly inside the component's own HTML template. `@ContentChild` queries for projected content passed into the component via `<ng-content>` from an external parent template.

### Q: What is content projection and how do you achieve multi-slot projection?
**A**: Content projection is a pattern where a parent passes HTML content into a child component placeholder (`<ng-content>`). Multi-slot projection uses the `select` attribute (e.g., `<ng-content select="[card-header]">` and `<ng-content select="[card-body]">`) to route specific content blocks to their designated layout slots.

## Summary
Component communication connects isolated components into a unified architecture. Inputs pass data down, outputs emit event notifications up, template queries provide programmatic access to child instances, and shared services enable reactive communication between unrelated components.

---

Previous : [Component Lifecycle](./08_Component_Lifecycle.md) | Index : [Home](./00_index.md) | Next : [Signals](./10_Signals.md)
