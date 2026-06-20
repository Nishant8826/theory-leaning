# Component Communication

## What is it?
Component Communication represents the techniques components use to share data, commands, and events. These techniques enable a composite tree of isolated component instances to function as an integrated application.

## Why do we need it?
To maintain modularity and reusability, components must remain isolated. However, they cannot work in complete isolation. For instance, a product list component needs to tell a shopping cart component that a user clicked "Add to Cart". Component communication patterns define how components share data (inputs/outputs) and request services safely.

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
1. **Parent-to-Child (`@Input` / modern `input()` Signal)**: Data flows from parent components down to child inputs.
2. **Child-to-Parent (`@Output` & `EventEmitter` / modern `output()` API)**: Child components emit event payloads up to parent listener handlers.
3. **Template Queries (`@ViewChild`, `@ViewChildren`, `@ContentChild`)**: Grants components programmatic access to children, nested template wrappers, or projected content.
4. **Content Projection (`<ng-content>`)**: Allows a parent component to inject custom HTML layouts into specific parts of a child's template.
5. **Dynamic Components**: Instantiated programmatically at runtime using container directives (`ViewContainerRef`) and helper classes.

## Impact
* **Application Architecture**: Directs component hierarchy design (Smart components manage state; Dumb components manage presentation).
* **Performance**: Direct data passing avoids global state managers, keeping DOM updates isolated and fast.
* **Maintainability**: Clear communication interfaces (inputs/outputs) make child components highly testable.

## Real World Example
In a video streaming interface, a parent dashboard component passes the active video url down to the player component (via `@Input`), and listens for the child player to emit an event (via `@Output`) when the video finishes, allowing the dashboard to load the next episode.

## Syntax
* **Inputs & Outputs**:
  - Input: `@Input() item: string = '';`
  - Output: `@Output() itemSelected = new EventEmitter<string>();`
* **ViewChild Query**: `@ViewChild('childRef') childElement!: ElementRef;`
* **Content Projection**: `<ng-content select=".card-header"></ng-content>`

## Code Examples
Below is a complete implementation demonstrating Parent-Child communication, content projection, and view queries.

### `child-card.component.ts`
```typescript
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child-card',
  standalone: true,
  template: `
    <div class="card">
      <!-- Content Projection Container -->
      <div class="header">
        <ng-content select="[card-title]"></ng-content>
      </div>

      <!-- Input Data Display -->
      <div class="body">
        <p>Item: {{ itemName }}</p>
        <p>Quantity Available: {{ stock }}</p>
      </div>

      <!-- Output Event Trigger -->
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
      
      <!-- 1. Parent to Child communication via [itemName] & [stock] -->
      <!-- 2. Content Projection via card-title -->
      <!-- 3. Child to Parent communication via (purchase) -->
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

  // Query child component instance directly
  @ViewChild('productCard') childInstance!: ChildCardComponent;

  ngAfterViewInit() {
    // childInstance is now available
    console.log('Queried Child Stock:', this.childInstance.stock);
  }

  handlePurchase(product: string) {
    this.message = `Purchase requested for: ${product}`;
  }
}
```

### Unrelated Components Communication (Using Shared Services)
When components do not share a parent-child relationship (e.g., sibling components, or components in different routes), they communicate by injecting a shared singleton service. This service exposes either a reactive Angular Signal or an RxJS `BehaviorSubject` stream that components can subscribe/bind to.

#### `theme.service.ts` (Shared Service)
```typescript
import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  // Option A: Signals (Modern)
  themeSignal = signal<'light' | 'dark'>('light');

  // Option B: RxJS BehaviorSubject (Classic)
  private themeSubject = new BehaviorSubject<'light' | 'dark'>('light');
  theme$ = this.themeSubject.asObservable();

  toggleTheme() {
    const nextTheme = this.themeSignal() === 'light' ? 'dark' : 'light';
    this.themeSignal.set(nextTheme);
    this.themeSubject.next(nextTheme);
  }
}
```

#### `component-a.component.ts` (Updates State)
```typescript
import { Component } from '@angular/core';
import { ThemeService } from './theme.service';

@Component({
  selector: 'app-comp-a',
  standalone: true,
  template: `<button (click)="themeService.toggleTheme()">Toggle System Theme</button>`
})
export class ComponentA {
  // Inject service via constructor
  constructor(public themeService: ThemeService) {}
}
```

#### `component-b.component.ts` (Reads State)
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

  // Inject service via constructor and map the signal
  constructor(public themeService: ThemeService) {
    this.currentThemeSignal = this.themeService.themeSignal;
  }
}
```

## Best Practices
1. **Unidirectional Data Flow**: Data should always flow down (Inputs) and events should always flow up (Outputs). Avoid mutating input properties inside child components.
2. **Use Content Projection for Wrapper UI**: Utilize `<ng-content>` for generic wrapper cards, dialog popups, or grid cells to keep layout code clean.
3. **Explicit Output Typing**: Always specify the type of value emitted by `EventEmitter` (e.g. `new EventEmitter<string>()` instead of raw `new EventEmitter()`).

## Common Mistakes
* **Mutating Parent State Directly**: Mutating objects passed down in inputs directly inside child components. This bypasses change detection, making debugging difficult.
* **Accessing `@ViewChild` properties inside `ngOnInit`**: Querying views before the template is rendered. Always query child elements inside `ngAfterViewInit`.

## Interview Questions & Answers
### Q: What is the difference between `@ViewChild` and `@ContentChild`?
**A**: `@ViewChild` queries elements that are declared directly inside the component's *own* HTML template. `@ContentChild` queries elements that are projected into the component via content projection (`<ng-content>`) from a parent template.

### Q: What is content projection and how do you achieve multi-slot projection?
**A**: Content projection allows you to inject custom HTML content from a parent component into a child component's template. Multi-slot projection is achieved by using the `select` attribute on the `<ng-content>` tag (e.g., `<ng-content select="[card-header]">`), which targets elements matching specific selectors.

## Summary
Component communication links isolated components together. Inputs send data down, outputs emit events up, and template queries allow components to interact programmatically. Content projection allows parents to inject custom layouts directly into child components.

---

Previous : [Component Lifecycle](./08_Component_Lifecycle.md) | Index : [Home](./00_index.md) | Next : [Signals](./10_Signals.md)
