# Performance Optimization

## What is it?
Performance Optimization in Angular is a suite of techniques, compiler capabilities, and architectural practices aimed at maximizing rendering speed, minimizing JavaScript bundle size, reducing memory consumption, and streamlining the runtime change detection cycle.

## Why do we need it?
By default, Angular's change detection engine checks the entire component tree from top to bottom whenever an asynchronous browser event (such as a click, timer, or HTTP response) occurs. 

While this default behavior is fast enough for small applications, large enterprise applications with thousands of bindings can suffer from UI lag, frame drops, and slower response times. Optimizing change detection, deferring heavy dependencies, and tracking list items ensures 60 FPS user interfaces even under heavy workloads.

```
Default Change Detection (Full Tree Scan):
Any Event ──> Traverses and checks every single component (Root ──> Child A ──> Child B ──> Child C)

OnPush Change Detection (Optimized Branch Scan):
Any Event ──> Scans component ONLY if:
             1. An @Input() object reference changes
             2. An internal event handler fires
             3. A bound Signal emits a new value
             4. Manually triggered via ChangeDetectorRef.markForCheck()
```

## How does it work?
1. **`ChangeDetectionStrategy.OnPush`**: Instructs Angular to skip checking a component branch unless its input references change, an event originates from within the component, or a bound Signal updates.
2. **Fine-Grained Signals & Zoneless Mode**: Replaces Zone.js dirty-checking with direct signal-to-DOM updates, eliminating global top-down change detection passes entirely.
3. **Deferrable Views (`@defer` block)**: Lazily loads and renders heavy components only when specific trigger conditions are met (e.g., when scrolled into `viewport`, on user `interaction`, on `idle`, or on `timer`).
4. **List Tracking (`@for (...; track item.id)`)**: Ensures Angular identifies which specific list items are added, moved, or deleted by their unique IDs, updating only modified DOM nodes rather than destroying and recreating the entire list.
5. **Image Optimization (`NgOptimizedImage`)**: Automatically enforces responsive image sizing (`srcset`), prevents Cumulative Layout Shift (CLS), and enables lazy loading.
6. **CDK Virtual Scrolling (`ScrollingModule`)**: Renders only the small subset of items currently visible in the user's viewport, preventing DOM bloat when displaying lists with thousands of records.

## Impact
* **Application Architecture**: Encourages clean, immutable data practices and isolated feature chunking.
* **Performance**: Drastically reduces initial bundle size, improves Core Web Vitals (LCP, FID, CLS), and cuts CPU rendering time.
* **Scalability**: Enables applications to render massive data grids and complex visualization dashboards without sluggishness.

## Real World Example
In a high-frequency trading dashboard or social media feed:
- Items in the feed are rendered using `@for (post of posts; track post.id)`.
- Heavy analytical charts below the fold are wrapped inside `@defer (on viewport)`.
- Component change detection is set to `OnPush`, ensuring new market ticker events re-render only the affected balance widget rather than the entire dashboard.

## Syntax
* **Configuring OnPush**:
```typescript
@Component({
  selector: 'app-user-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush
})
```
* **Deferrable View Syntax**:
```html
@defer (on viewport) {
  <app-heavy-chart />
} @placeholder {
  <div class="skeleton-chart">Loading preview...</div>
} @loading (minimum 500ms) {
  <div class="spinner">Fetching chart assets...</div>
}
```

## Code Examples
Below is a complete implementation demonstrating `OnPush` change detection, `@defer` viewport triggers, and list tracking optimization:

```typescript
import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';

export interface UserAccount {
  id: number;
  name: string;
  role: string;
}

@Component({
  selector: 'app-perf-demo',
  standalone: true,
  imports: [CommonModule, ScrollingModule],
  changeDetection: ChangeDetectionStrategy.OnPush, // Skips unnecessary checks
  template: `
    <div class="perf-container">
      <h3>Performance Optimization Showcase</h3>

      <!-- 1. Tracked List Rendering -->
      <div class="list-section">
        <h4>User Directory (Optimized List Tracking)</h4>
        <ul>
          @for (user of users; track user.id) {
            <li>{{ user.name }} - <span class="role">{{ user.role }}</span></li>
          } @empty {
            <li>No user records available.</li>
          }
        </ul>
      </div>

      <!-- 2. Deferrable View Loader -->
      <div class="deferred-section">
        <h4>Lazy Heavy Chart</h4>
        
        @defer (on viewport) {
          <div class="heavy-mock-chart">
            <p>📈 Heavy Analytics Chart Component loaded on-demand as it entered the viewport!</p>
          </div>
        } @placeholder {
          <div class="placeholder-box">
            <p>Scroll down to load the heavy chart assets...</p>
          </div>
        } @loading (minimum 800ms) {
          <div class="loading-box">
            <p>Downloading chart JavaScript bundles...</p>
          </div>
        }
      </div>
    </div>
  `,
  styles: [`
    .perf-container { padding: 24px; font-family: sans-serif; }
    .list-section ul { list-style: none; padding: 0; }
    .list-section li { padding: 8px; border-bottom: 1px solid #e5e7eb; }
    .role { color: #6b7280; font-size: 13px; }
    .deferred-section { margin-top: 350px; }
    .heavy-mock-chart { height: 160px; background: #e0f2fe; border: 2px solid #0284c7; padding: 20px; border-radius: 6px; }
    .placeholder-box { height: 160px; background: #f9fafb; border: 2px dashed #9ca3af; padding: 20px; border-radius: 6px; display: flex; align-items: center; justify-content: center; }
    .loading-box { height: 160px; background: #fef3c7; border: 1px solid #f59e0b; padding: 20px; border-radius: 6px; }
  `]
})
export class PerfDemoComponent {
  @Input() users: UserAccount[] = [
    { id: 101, name: 'Alex Developer', role: 'Staff Architect' },
    { id: 102, name: 'Sarah Connor', role: 'Frontend Lead' },
    { id: 103, name: 'John Doe', role: 'Systems Engineer' }
  ];
}
```

## Best Practices
1. **Default All Components to `OnPush`**: Set `changeDetection: ChangeDetectionStrategy.OnPush` on all newly created components. This ensures optimal rendering performance from day one.
2. **Always Track Loops by Unique IDs**: In `@for` loops, always use unique entity identifiers (e.g., `track item.id`) instead of array indexes (`track $index`). Tracking by ID prevents Angular from destroying and recreating unmodified DOM nodes when array order changes.
3. **Defer Non-Critical Views with `@defer`**: Wrap heavy third-party widgets, charts, modals, and below-the-fold content in `@defer (on viewport)` or `@defer (on interaction)`.
4. **Use Immutability**: Always produce new object/array references using spread operators (`[...items, newItem]`) when updating state in `OnPush` components.

## Common Mistakes
* **Mutating Objects In-Place in `OnPush` Components**: Directly mutating an array with `.push()` or modifying an object property without creating a new reference. Because the object reference does not change, `OnPush` components will not detect the change or update the view.
* **Missing Trigger Conditions on `@defer`**: Using `@defer` without configuring appropriate `@placeholder` or `@loading` blocks, leading to layout shifts (CLS) when the deferred component renders.

## Interview Questions & Answers
### Q: How does `ChangeDetectionStrategy.OnPush` improve Angular performance?
**A**: `OnPush` eliminates unnecessary change detection passes. Instead of checking every component on every browser event, Angular skips `OnPush` components unless an `@Input()` reference changes, an event originated inside the component, a bound Signal updates, or `markForCheck()` is explicitly called.

### Q: What is the purpose of the `@defer` block in modern Angular?
**A**: The `@defer` block enables template-level declarative lazy loading. It automatically extracts the enclosed components into separate JavaScript chunks and downloads/renders them only when specified trigger conditions are met (e.g., `on viewport`, `on interaction`, `on idle`, `on hover`, `when condition`), improving initial page load times.

## Summary
Performance optimization in Angular centers on minimizing bundle sizes and reducing unnecessary change detection cycles. By adopting `OnPush`, leveraging modern `@for` tracking, utilizing `@defer` for below-the-fold views, and embracing Signals, developers can build ultra-responsive web applications.

---

Previous : [Angular Material](./20_Angular_Material.md) | Index : [Home](./00_index.md) | Next : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md)
