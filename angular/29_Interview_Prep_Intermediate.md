# Intermediate Interview Prep

## What is it?
Intermediate Interview Preparation un core concepts, architectural rules, aur API usages ka compilation hai jo developers ko mid-level Angular roles ke liye interview dete waqt pata hone chahiye.

## Why do we need it?
Mid-level roles ke liye basic templates se aage badhkar framework ki deeper understanding hona zaroori hai. Forms (reactive vs template-driven), lifecycle hooks, custom directives, service lifecycles, aur RxJS integration jaise topics ko review karne se developers practical problem-solving skills demonstrate kar sakte hain.

```
Preparation Flow:
Review Component Communication ──> Study Directives/Pipes ──> Practice Forms ──> Learn RxJS Operators ──> Master Intermediate Concepts
```

## How does it work?
1. **Component Communication**: Inputs, outputs, view queries, aur content projection ki understanding ko validate karta hai.
2. **Forms & Services**: Programmatic validation, singleton services, aur custom directives ki knowledge ko test karta hai.
3. **RxJS Streams**: Observables, subscriptions, aur operators ke basic familiarity ko verify karta hai.

## Impact
* **Application Architecture**: Decoupled components aur reusable services likhne ko promote karta hai.
* **Performance**: Memory leaks ko rokne ke liye resources ke proper cleanup ko encourage karta hai.
* **Scalability**: Developers ko flexible features design karne me help karta hai jinhe modules ke beech share kiya ja sake.

## Real World Example
Ek dynamic candidate se pucha jata hai ki component me RxJS streams ko subscribe karte waqt memory leaks se kaise bacha jaye. Candidate explain karta hai ki dynamic subscriptions ko unsubscribe karne ke liye `takeUntil` aur ek destroy notifier Subject ka use kaise kiya jata hai, jo resource management ke intermediate knowledge ko demonstrate karta hai.

## Syntax
Ek custom pure pipe declaration:
```typescript
@Pipe({
  name: 'myPipe',
  standalone: true
})
export class MyPipe implements PipeTransform {
  transform(value: any) { return value; }
}
```

## Code Examples
Neeche ek custom attribute directive ka implementation diya gaya hai jo hover durations ko log karta hai, aur event listeners aur host bindings ko demonstrate karta hai.

```typescript
import { Directive, HostListener, HostBinding, signal } from '@angular/core';

@Directive({
  selector: '[appHoverTracker]',
  standalone: true
})
export class HoverTrackerDirective {
  private enterTime: number = 0;

  @HostBinding('style.cursor') cursor = 'pointer';
  @HostBinding('class.hovered') isHovered = false;

  @HostListener('mouseenter') onEnter() {
    this.enterTime = Date.now();
    this.isHovered = true;
  }

  @HostListener('mouseleave') onLeave() {
    this.isHovered = false;
    const duration = (Date.now() - this.enterTime) / 1000;
    console.log(`Hover completed. Duration: ${duration} seconds.`);
  }
}
```

## Best Practices
1. **Clean Up Subscriptions**: `ngOnDestroy` me hamesha `takeUntil` ya template me `async` pipe ka use karke subscriptions ko clean up (unsubscribe) karein.
2. **Use Reactive Forms for Complex Logic**: Complex validation rules ya dynamic fields likhte waqt template-driven forms ke mukable reactive forms ko prefer karein.
3. **Keep Directives camelCase**: Custom directives ko camelCase format me rakhein (jaise `appTracker`) taaki standard HTML attributes ke sath naming collision na ho.

## Common Mistakes
* **Mutating Input Bindings**: Parent inputs se milne wali values ko child components me directly mutate karna, jo unidirectional data flow rules ko bypass karta hai.
* **Running heavy loops in templates**: String interpolations ke andar heavy calculations ya methods call karna, jisse wo har change detection cycle par run hone lagte hain aur performace low ho jati hai.

## Interview Questions & Answers

### Q1: What is the difference between Reactive Forms and Template-Driven Forms?
**A**: Reactive Forms model-driven hote hain, inka saara structure class (TypeScript) me likha jata hai, jisse dynamic validations aur testing synchronous aur safe ho jati hain. Template-Driven Forms HTML markup par depend karte hain aur `ngModel` use karte hain, jo ki chote forms ke liye simple hai par complex validations me testing limits cross ho jati hain.

### Q2: What is the purpose of `@ViewChild` and when are its queried elements available?
**A**: `@ViewChild` ka use template ke kisi element, child component, ya directive ka query handle pane ke liye kiya jata hai. Yeh elements component initiation `ngOnInit` ke time unavailable hote hain; unhe template rendering complete hone ke baad `ngAfterViewInit` hook me hi access kiya ja sakta hai.

### Q3: Explain the difference between pure and impure pipes.
**A**: Pure pipe tabhi execute hota hai jab uski input parameters ka reference value badal jaye (caching support). Impure pipe har change detection cycle par chalta hai, jisse dynamic deep array changes catch toh ho jate hain par application slow/unperformant ho sakti hai.

### Q4: Why is it important to unsubscribe from observables and how can you do it?
**A**: Unsubscribe na karne par active subscriptions background memory me run hoti rehti hain, jisse leaks aur garbage collection blockage (memory leaks) hote hain. Ise resolve karne ke liye template me `async` pipe (auto cleanup) use karein ya component class me `takeUntil` operator ke sath custom destroy notification stream pass karein.

### Q5: What is the difference between constructor injection and the modern `inject()` function?
**A**: Constructor injection traditional style hai jahan inputs constructor me pass hote hain: `constructor(private api: ApiService) {}`. Modern `inject()` approach direct class property initialization support karti hai: `api = inject(ApiService)`. Isse inheritance and configuration cleaner ho jate hain.

### Q6: What does the `@HostListener` decorator do?
**A**: `@HostListener` component ya custom directive ke Host element par hone wale user actions (jaise mouse click, keypress, hover) ko listen karta hai aur immediate uske associated class helper method ko execute kar deta hai.

## Summary
Intermediate level interviews component interaction, form logic, pipes/directives, aur basic RxJS stream cleanups par focus karte hain. In concepts ko master karne se candidate demonstrate kar sakte hain ki wo clean, performance-oriented code likh sakte hain.

---

Previous : [Beginner Interview Prep](./28_Interview_Prep_Beginner.md) | Index : [Home](./00_index.md) | Next : [Advanced Interview Prep](./30_Interview_Prep_Advanced.md)
