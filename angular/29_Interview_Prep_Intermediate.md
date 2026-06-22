# Intermediate Interview Prep

## What is it?
Intermediate Interview Preparation compiles core concepts, architectural rules, and API usages that developers should know when interviewing for mid-level Angular roles.

## Why do we need it?
Mid-level roles require a deeper understanding of the framework beyond basic templates. Reviewing topics like forms (reactive vs template-driven), lifecycle hooks, custom directives, service lifecycles, and RxJS integration ensures developers can demonstrate practical problem-solving skills.

```
Preparation Flow:
Review Component Communication ──> Study Directives/Pipes ──> Practice Forms ──> Learn RxJS Operators ──> Master Intermediate Concepts
```

## How does it work?
1. **Component Communication**: Validates understanding of inputs, outputs, view queries, and content projection.
2. **Forms & Services**: Tests knowledge of programmatic validation, singleton services, and custom directives.
3. **RxJS Streams**: Verifies basic familiarity with observables, subscriptions, and operators.

## Impact
* **Application Architecture**: Promotes writing decoupled components and reusable services.
* **Performance**: Encourages proper cleanup of resources to prevent memory leaks.
* **Scalability**: Helps developers design flexible features that can be shared across modules.

## Real World Example
A candidate is asked how to prevent memory leaks when subscribing to RxJS streams in a component. The candidate explains how to clean up subscriptions using `takeUntil` and a destroy notifier Subject, demonstrating intermediate knowledge of resource management.

## Syntax
A custom pure pipe declaration:
```typescript
@Pipe({
  name: 'myPipe',
  standalone: true
})
export class MyPipe implements PipeTransform {
  transform(value: any) { return value; }
}
```

## Hinglish Explanation

Intermediate level interview questions me components integration, form differences, custom directives, aur dynamic RxJS state handle karne ke logic check hote hain:

### 1. Component templates connection
* `@ViewChild` component ke host HTML template elements ko select karta hai. Yeh elements class logic ke `ngOnInit` step par create nahi hote, unhe dynamic checks ke liye `ngAfterViewInit` lifecycle hook me use kiya jata hai.

### 2. Custom Directive behaviors
* `@HostListener` ka use host tags (HTML elements jis par directive focused hai) par mouse hover, scroll, clicks check karne ke liye events bind karta hai.
* `@HostBinding` usi host element par CSS variables, color coding parameters ya transform scale updates direct apply (bind) karne me help karta hai.

### 3. Custom Pipes transformations
* Pure pipe data formatting updates cache memory me save rakhte hain aur tabhi chalte hain jab input inputs reference variables update hon. Agar dynamic array mutation check karni ho toh impure pipes compile rules override karke use hote hain par inka extra overhead performance impact dalta hai.

## Code Examples
Below is an implementation of a custom attribute directive that logs hover durations, demonstrating event listeners and host bindings.

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
1. **Clean Up Subscriptions**: Always clean up subscriptions in `ngOnDestroy` using `takeUntil` or the `async` pipe.
2. **Use Reactive Forms for Complex Logic**: Prefer reactive forms over template-driven forms when writing complex validation rules or dynamic fields.
3. **Keep Directives camelCase**: Prefix custom directives (e.g. `appTracker`) to avoid collisions with standard HTML attributes.

## Common Mistakes
* **Mutating Input Bindings**: Mutating values received from parent inputs inside child components, which bypasses unidirectional data flow rules.
* **Running heavy loops in templates**: Calling complex functions inside string interpolations, which forces them to run on every change detection cycle.

## Interview Questions & Answers

### Q1: What is the difference between Reactive Forms and Template-Driven Forms?
**A**: Reactive forms are model-driven and defined programmatically in the component class, offering synchronous testing, predictable state, and type safety. Template-driven forms are template-driven and defined declaratively in the HTML using directives like `ngModel`, which is simpler but less testable.
* **Hinglish Explanation**: Reactive Forms model-driven hote hain, inka saara structure class (TypeScript) me likha jata hai, jisse dynamic validations aur testing synchronous aur safe ho jati hain. Template-Driven Forms HTML markup par depend karte hain aur `ngModel` use karte hain, jo ki chote forms ke liye simple hai par complex validations me testing limits cross ho jati hain.

### Q2: What is the purpose of `@ViewChild` and when are its queried elements available?
**A**: `@ViewChild` queries child component instances, directives, or DOM element references declared within a component's own template. These elements are not available in `ngOnInit` and can only be accessed after the view has finished rendering in `ngAfterViewInit`.
* **Hinglish Explanation**: `@ViewChild` ka use template ke kisi element, child component, ya directive ka query handle pane ke liye kiya jata hai. Yeh elements component initiation `ngOnInit` ke time unavailable hote hain; unhe template rendering complete hone ke baad `ngAfterViewInit` hook me hi access kiya ja sakta hai.

### Q3: Explain the difference between pure and impure pipes.
**A**: A pure pipe (default) is only executed when its input reference changes, caching values for better performance. An impure pipe is executed on every change detection cycle, regardless of input changes, making it useful for tracking mutations within arrays but less performant.
* **Hinglish Explanation**: Pure pipe tabhi execute hota hai jab uski input parameters ka reference value badal jaye (caching support). Impure pipe har change detection cycle par chalta hai, jisse dynamic deep array changes catch toh ho jate hain par application slow/unperformant ho sakti hai.

### Q4: Why is it important to unsubscribe from observables and how can you do it?
**A**: Active subscriptions that are not cleaned up when components are destroyed can create memory leaks and run unwanted network calls. They can be cleaned up using the `async` pipe in templates (which unsubscribes automatically), or by using the `takeUntil` operator with a destroy notifier Subject in the class.
* **Hinglish Explanation**: Unsubscribe na karne par active subscriptions background memory me run hoti rehti hain, jisse leaks aur garbage collection blockage (memory leaks) hote hain. Ise resolve karne ke liye template me `async` pipe (auto cleanup) use karein ya component class me `takeUntil` operator ke sath custom destroy notification stream pass karein.

### Q5: What is the difference between constructor injection and the modern `inject()` function?
**A**: Constructor injection declares dependencies in the class constructor: `constructor(private api: ApiService)`. The modern `inject()` function resolves dependencies as property initializers: `api = inject(ApiService)`. This writes cleaner classes and makes property inheritance straightforward.
* **Hinglish Explanation**: Constructor injection traditional style hai jahan inputs constructor me pass hote hain: `constructor(private api: ApiService) {}`. Modern `inject()` approach direct class property initialization support karti hai: `api = inject(ApiService)`. Isse inheritance and configuration cleaner ho jate hain.

### Q6: What does the `@HostListener` decorator do?
**A**: The `@HostListener` decorator binds an event handler method in a directive or component to a DOM event of its host element (such as clicks, mouse entries, or scrolls), allowing the class to respond to interactions.
* **Hinglish Explanation**: `@HostListener` component ya custom directive ke Host element par hone wale user actions (jaise mouse click, keypress, hover) ko listen karta hai aur immediate uske associated class helper method ko execute kar deta hai.

## Summary
Intermediate interviews focus on component interaction, form logic, pipes/directives, and basic RxJS stream cleanups. Mastering these concepts shows that developers can write clean, performance-oriented code.

---

Previous : [Beginner Interview Prep](./28_Interview_Prep_Beginner.md) | Index : [Home](./00_index.md) | Next : [Advanced Interview Prep](./30_Interview_Prep_Advanced.md)
