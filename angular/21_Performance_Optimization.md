# Performance Optimization

## What is it?
Angular me Performance Optimization un techniques aur methods ka collection hai jiske zariye page rendering speed ko fast kiya jata hai, JavaScript bundle size minimize kiya jata hai, aur runtime change detection cycle ko optimize kiya jata hai.

## Why do we need it?
Default settings me, Angular state updates check karne ke liye pure application component tree ko traverse (scan) karta hai jab bhi koi event ya click trigger ho. Chote apps me isse issue nahi hota, par bade projects me yeh screen lag create kar sakta hai. Change detection logic ko optimize karne aur bundles lazy load karne se application performance super-smooth ho jati hai.

```
Standard Change Detection (Full Scan):
Any event ──> Scans all components (Comp A ──> Comp B ──> Comp C ──> Comp D)

OnPush Change Detection (Optimized Scan):
Any event ──> Only scans branch if Input Reference changed, Event fired, or explicitly requested
```

## How does it work?
1. **OnPush Strategy**: Angular change detector ko instruct karta hai ki component tree tabhi scan ho jab:
   - One of its `@Input` references changes.
   - An event handler in the component triggers.
   - You request a check manually using `ChangeDetectorRef.markForCheck()`.
2. **Zoneless Angular**: Zone.js bypass karke change detection logic ko custom signals se connect karna, jisse useless global loops avoid ho saken.
3. **Deferred Loading (`@defer` block)**: Heavy elements ya components ki loading tab tak delay karna jab tak specific triggers meet na ho (jaise user viewport scroll).
4. **List Tracking (`track` loop)**: Loop arrays render karte waqt unique track keys specify karna, taaki updates par poori list refresh hone ke bajaye sirf changed items hi re-render hon.
5. **Virtual Scrolling**: Heavy tables ya lists ke liye sirf viewport me visible records hi render karna aur memory leakage avoid karna.

## Impact
* **Application Architecture**: Decoupled modules split hone se chunks size optimized rehta hai.
* **Performance**: Browser scanning time drop hone se UI responsiveness milliseconds me execute hoti hai.
* **Scalability**: Heavy datasets render hone par bhi interface smooth aur responsive behave karta hai.

## Real World Example
Jaise e-commerce website list page me cards render karte waqt `@for` loop me `track product.id` custom configuration use karte hain, taaki user scroll karte waqt components dynamically re-render na hon.

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

## Code Examples
Neeche dynamic list updates optimizations, `@defer` trigger methods aur `OnPush` components setups configuration details program build integration model diya gaya hai:

```typescript
import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  selector: 'app-perf-demo',
  standalone: true,
  imports: [CommonModule, ScrollingModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="perf-container">
      <h3>Performance Optimization Sandbox</h3>

      <div class="list-section">
        <h4>User Accounts (track optimization)</h4>
        <ul>
          <li *ngFor="let user of users; track: user.id">
            {{ user.name }} (ID: {{ user.id }})
          </li>
        </ul>
      </div>

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
    .deferred-section { margin-top: 400px; }
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
1. **Default to OnPush**: Naye components create karte waqt by default `ChangeDetectionStrategy.OnPush` change detection strategy use karein.
2. **Always Use Unique Track Identifiers**: Looping arrays me track functions me index ke bajaye humesha unique ID (jaise `track user.id`) use karein.
3. **Lazy Load Heavy Components**: Heavy UI elements (jaise charts, graphs, dynamic modals) ko render karne ke liye `@defer` blocks ka use karein.

## Common Mistakes
* **Mutating Objects in OnPush Components**: OnPush components me state objects ko directly mutate karna. Reference change na hone par Angular detection updates skip kar deta hai. Isliye hamesha spread operator se new reference overwrite use karein.
* **Underestimating `@defer` triggers**: `@defer` block par specific conditions (viewport, interaction, prefetch) na lagana, jisse dynamic code splitted bundles sahi time par load nahi ho paate.

## Interview Questions & Answers
### Q: How does `ChangeDetectionStrategy.OnPush` improve application performance?
**A**: `OnPush` strategy component scans aur change detection checks ko restricted/limited kar deti hai. Isse irrelevant events par components branches re-evaluation bypass skip ho jati hai.

### Q: What is the purpose of the `@defer` block in modern Angular?
**A**: `@defer` block codes split chunks loading ko optimized delay apply setup configure karta hai, jo conditions met hone par template chunks ko on-demand lazy load karke execute aur update karta hai.

## Summary
Angular me performance optimization bundles minimize karne aur unnecessary rendering loops ko restrict karne par depend karta hai. `OnPush` change detection aur `@defer` control patterns ke dynamic use se application loading speeds smooth behave karti hai.

---

Previous : [Angular Material](./20_Angular_Material.md) | Index : [Home](./00_index.md) | Next : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md)
