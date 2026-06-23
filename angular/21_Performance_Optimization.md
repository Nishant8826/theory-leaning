# Performance Optimization

## What is it?
Angular me Performance Optimization un techniques aur methods ka collection hai jiske zariye page rendering speed ko fast kiya jata hai, JavaScript bundle size minimize kiya jata hai, aur runtime change detection calculations coordinate optimize kiye jate hain.

## Why do we need it?
Default settings me, Angular change updates checks coordinate karne ke liye pure applications components tree ko traverse (scan) karta hai jab bhi asynchronous clicks ya timer events trigger hon. Chote applications me isse koi problem nahi hoti, par thousands components scale wale enterprise products me yeh UI response lag aur sluggishness create kar deta hai. Change detection checking logic streamline karne aur components lazy-loading bundles apply karne se application dynamic interaction super-smooth ban jata hai.

```
Standard Change Detection (Full Scan):
Any event ──> Scans all components (Comp A ──> Comp B ──> Comp C ──> Comp D)

OnPush Change Detection (Optimized Scan):
Any event ──> Only scans branch if Input Reference changed, Event fired, or explicitly requested
```

## How does it work?
1. **`ChangeDetectionStrategy.OnPush`**: Angular change verification checks mechanism ko instruction deta hai ki component scans cycles tabhi trigger hon jab:
   - One of its `@Input` references changes.
   - An event handler in the component triggers.
   - You request a check manually using `ChangeDetectorRef.markForCheck()`.
2. **Zoneless Angular**: Zone.js change track framework engine bypass karke direct template elements reactivity updates signals apply karna, jo browser check cycles reduce karta hai.
3. **Deferred Loading (`@defer` block)**: Heavy modules assets loading tab tak delay coordinate karna jab tak specific event bounds criteria complete na ho (jaise element viewport intersection enter checks).
4. **List Tracking (`track` loop)**: Loop iterations collections elements track keys parameters (jaise id index check) declare karna taaki dynamic list updates limits re-render elements calculations save ho sakein.
5. **Virtual Scrolling**: Scrolling lists layouts limits me viewport coordinates items list rendering limit elements parameters set karna, un-rendered list components RAM parameters save setups.

## Impact
* **Application Architecture**: Decoupled component bundle splits structure parameters maintain kar lazy-load setups support karta hai.
* **Performance**: Browser check loops minimize hone se screen components loads aur updates updates milliseconds timing speed checks execute hote hain.
* **Scalability**: Heavy products records data grid processing limits checks responsive and functional banata hai.

## Real World Example
E-commerce website catalog lists updates features me checks cards layout render limits optimization check apply settings coordinate track tags apply `track product.id` configure setups checks perform clean updates coordinate smooth output settings reflect kar leta hai.

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
1. **Default to OnPush**: New components declarations configurations setups me default change detection config strategy parameter standard `ChangeDetectionStrategy.OnPush` target set karein.
2. **Always Use Unique Track Identifiers**: Dynamic looping variables arrays display templates me track selectors parameter index arrays coordinate checks parameters strictly mapping unique pointers use karein.
3. **Lazy Load Heavy Components**: Heavy assets (charts diagrams grids modules, modal panels templates) lazy render coordinate `@defer` templates checks boundaries blocks configure optimize block utilize karein.

## Common Mistakes
* **Mutating Objects in OnPush Components**: OnPush component boundaries parameters me variables mutations reference changes bypass update setups run karna. Object property value target update variable change `OnPush` checker track nahi kar pata, reference overwrite coordinate updates triggers set check use karein.
* **Underestimating `@defer` triggers**: Dynamic load blocks parameter tags `@defer` setup checks settings rules properties boundaries parameters define na karna, jo initialization speed check slow bundles settings bypass setups break kar deta hai.

## Interview Questions & Answers
### Q: How does `ChangeDetectionStrategy.OnPush` improve application performance?
**A**: `OnPush` strategy component scan change detection loops checks bypass setups restrict karti hai jisse change checks scans updates check parameters components branches trigger skip ho jate hain.

### Q: What is the purpose of the `@defer` block in modern Angular?
**A**: `@defer` block codes modules loading structures optimization check coordinates templates delay apply system configure karta hai jo on-demand bundles coordinates loads checks dynamic updates execute setups targets follow karta hai.

## Summary
Angular performance features optimization settings change structures coordinate check levels check setups control targets apply map setup complete balance manage karta hai. OnPush change detection calculations, lazy element viewport loading patterns systems dynamic speed check manage karte hain.

---

Previous : [Angular Material](./20_Angular_Material.md) | Index : [Home](./00_index.md) | Next : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md)
