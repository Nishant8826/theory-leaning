# Performance Optimization

## What is it?
Performance Optimization in Angular involves techniques used to accelerate rendering times, minimize JavaScript bundle sizes, and optimize runtime change detection checks.

## Why do we need it?
By default, Angular applications check the entire component tree for changes whenever an asynchronous event (like a keystroke or timer) occurs. While this works well for small apps, it can cause lagging UIs in large enterprise applications with thousands of active DOM elements. Optimizing change detection and lazy-loading code chunks ensures fast rendering times and smooth user interactions.

```
Standard Change Detection (Full Scan):
Any event ──> Scans all components (Comp A ──> Comp B ──> Comp C ──> Comp D)

OnPush Change Detection (Optimized Scan):
Any event ──> Only scans branch if Input Reference changed, Event fired, or explicitly requested
```

## How does it work?
1. **`ChangeDetectionStrategy.OnPush`**: Instructs Angular to only run change detection on a component when:
   - One of its `@Input` references changes.
   - An event handler in the component triggers.
   - You request a check manually using `ChangeDetectorRef.markForCheck()`.
2. **Zoneless Angular**: Replaces Zone.js with Signals to update the DOM directly, reducing change detection overhead.
3. **Deferred Loading (`@defer` block)**: Lazily loads components and dependencies when specific conditions are met (e.g. when a component enters the viewport).
4. **List Tracking (`track` loop)**: Tracks list items using unique identifiers (like `id`) instead of array index references. This prevents Angular from recreating the entire list structure when array elements change.
5. **Virtual Scrolling**: Only renders elements that are currently visible within the browser's viewport.

## Impact
* **Application Architecture**: Directs component and module structure design to enable lazy-loading.
* **Performance**: Reduces change detection sweeps, resulting in faster rendering times and smaller bundle sizes.
* **Scalability**: Keeps user interfaces responsive even when rendering large lists or processing heavy datasets.

## Real World Example
An e-commerce catalog page renders hundreds of product cards. By using `ChangeDetectionStrategy.OnPush` and tracking items using `track product.id`, the catalog updates smoothly without page lag when users toggle filters.

## Syntax
* **Configuring OnPush**:
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
```
* **Deferred Block**:
```html
@defer (on viewport) {
  <app-heavy-chart />
} @placeholder {
  <p>Loading chart preview...</p>
}
```

## Hinglish Explanation

Performance optimization ke teen core techniques hain:

### 1. OnPush Change Detection (Smart checking)
* **Default:** Angular me jab bhi koi mouse click ya event hota hai, toh wo pure components tree me check karta hai ki data badla ya nahi (Dirty Checking).
* **OnPush:** `@Component` me `changeDetection: ChangeDetectionStrategy.OnPush` lagane se Angular faaltu checking rok deta hai. Yeh component ko sirf tabhi scan karega jab input parameters ka reference badlega ya component me koi click event hoga.

### 2. track check validation (Lists updating)
* `@for (user of users; track user.id)` me `track` specify karna mandatory hai. Isse list me naya item add hone par Angular poori HTML list re-render nahi karta, balki sirf badle hue element ko hi target karke modify karta hai.

### 3. `@defer` blocks (Lazy Loading for elements)
* `@defer` modern Angular (v17+) ka automatic lazy loading block hai.
* Hum heavy charts, feedback dialogs ya map widgets ko `@defer (on viewport)` block me wrap kar dete hain. Isse page ke initial loading bundles lightweight rehte hain aur jab widget screen par scroll hone par scroll-range me aata hai, tabhi browser bundle load aur compile karta hai.

## Code Examples
Below is an implementation demonstrating the modern `@defer` control block, list tracking, and the `OnPush` change detection strategy.

```typescript
import { Component, ChangeDetectionStrategy, Input, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  selector: 'app-perf-demo',
  standalone: true,
  imports: [CommonModule, ScrollingModule],
  // 1. Configure OnPush Change Detection
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="perf-container">
      <h3>Performance Optimization Sandbox</h3>

      <!-- 2. Track By List Optimization -->
      <div class="list-section">
        <h4>User Accounts (track optimization)</h4>
        <ul>
          <!-- Using Angular 17+ new control flow track syntax -->
          <li *ngFor="let user of users; track: user.id">
            {{ user.name }} (ID: {{ user.id }})
          </li>
        </ul>
      </div>

      <!-- 3. Deferred Block: Loads only when it enters the viewport -->
      <div class="deferred-section">
        <h4>Lazy Chart Loader</h4>
        @defer (on viewport) {
          <div class="heavy-mock-chart">
            <p>📈 Interactive Chart component loaded on-demand!</p>
          </div>
        } @placeholder {
          <div class="placeholder-box">
            <p>Scroll down to load the chart...</p>
          </div>
        } @loading (minimum 1s) {
          <p>Compiling chart bundles...</p>
        }
      </div>
    </div>
  `,
  styles: [`
    .perf-container { padding: 20px; font-family: sans-serif; }
    .heavy-mock-chart { height: 150px; background: #e0f2fe; border: 2px solid #0284c7; padding: 20px; }
    .placeholder-box { height: 150px; background: #f3f4f6; border: 2px dashed #9ca3af; padding: 20px; }
    .deferred-section { margin-top: 400px; } /* Force scroll space */
  `]
})
export class PerfDemoComponent {
  @Input() users: { id: number; name: string }[] = [
    { id: 101, name: 'Nishant' },
    { id: 102, name: 'Alice' },
    { id: 103, name: 'Bob' }
  ];
}
```

## Best Practices
1. **Default to OnPush**: Configure `ChangeDetectionStrategy.OnPush` as the default change detection strategy for new components.
2. **Always Use Unique Track Identifiers**: Track list elements using unique identifiers (like `id`) instead of array indexes when rendering lists using loops.
3. **Lazy Load Heavy Components**: Wrap heavy charts, complex markdown parsers, or modal windows in `@defer` blocks to prevent them from increasing the initial bundle size.

## Common Mistakes
* **Mutating Objects in OnPush Components**: Mutating object properties directly (e.g. `user.name = 'new name'`) in components that use the `OnPush` strategy. Angular checks object references rather than property values, so it will not detect the change.
* **Underestimating `@defer` triggers**: Using `@defer` without specifying triggers (such as `on viewport` or `on interaction`), which can cause components to load immediately and increase initial bundle sizes.

## Interview Questions & Answers
### Q: How does `ChangeDetectionStrategy.OnPush` improve application performance?
**A**: By default, Angular checks the entire component tree for changes whenever an asynchronous event occurs. Setting `changeDetection` to `OnPush` instructs Angular to skip checking the component and its children unless it receives updated input references, event handlers trigger within the component, or you request a check manually using `ChangeDetectorRef`.
* **Hinglish Explanation**: Default change detection me Angular har asynchronous event (jaise mouse click ya timer) par pure component tree ko upar se niche tak scan karta hai. Jabki `OnPush` strategy use karne par Angular us component aur uske child elements ko change detection scan se skip kar deta hai. Yeh sirf tabhi check karta hai jab: (1) Component ko parent se bilkul naya `@Input()` reference mile, (2) Component ke template ke andar se koi event trigger ho, ya (3) Hum manually `ChangeDetectorRef` ke zariye check request karne ke liye command chalayein.

### Q: What is the purpose of the `@defer` block in modern Angular?
**A**: The `@defer` block enables deferred loading for components, directives, and pipes. It compiles these dependencies into separate JavaScript chunks, loading them only when specific conditions are met (such as entering the viewport or on user interaction), which helps keep the initial page load fast.
* **Hinglish Explanation**: `@defer` block (v17+) components, directives, aur pipes ki lazy loading ko control karne ka ek modern declarative feature hai. Yeh block un parts ko automatically alag JavaScript bundles me compile kar deta hai aur tabhi load karta hai jab unki actual requirements puri hon (jaise jab element scroll hokar viewport me aaye, ya user kisi element par click ya hover kare). Isse page ka initial bundle size bohot control me rehta hai.

## Summary
Optimizing Angular performance involves managing change detection and code bundles. Using `OnPush` strategies, tracking list items, and deferred loading (`@defer`) helps keep application interfaces responsive and load times fast.

---

Previous : [Angular Material](./20_Angular_Material.md) | Index : [Home](./00_index.md) | Next : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md)
