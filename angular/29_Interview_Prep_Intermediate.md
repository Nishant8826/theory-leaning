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

### Q2: What is the purpose of `@ViewChild` and when are its queried elements available?
**A**: `@ViewChild` queries child component instances, directives, or DOM element references declared within a component's own template. These elements are not available in `ngOnInit` and can only be accessed after the view has finished rendering in `ngAfterViewInit`.

### Q3: Explain the difference between pure and impure pipes.
**A**: A pure pipe (default) is only executed when its input reference changes, caching values for better performance. An impure pipe is executed on every change detection cycle, regardless of input changes, making it useful for tracking mutations within arrays but less performant.

### Q4: Why is it important to unsubscribe from observables and how can you do it?
**A**: Active subscriptions that are not cleaned up when components are destroyed can create memory leaks and run unwanted network calls. They can be cleaned up using the `async` pipe in templates (which unsubscribes automatically), or by using the `takeUntil` operator with a destroy notifier Subject in the class.

### Q5: What is the difference between constructor injection and the modern `inject()` function?
**A**: Constructor injection declares dependencies in the class constructor: `constructor(private api: ApiService)`. The modern `inject()` function resolves dependencies as property initializers: `api = inject(ApiService)`. This writes cleaner classes and makes property inheritance straightforward.

### Q6: What does the `@HostListener` decorator do?
**A**: The `@HostListener` decorator binds an event handler method in a directive or component to a DOM event of its host element (such as clicks, mouse entries, or scrolls), allowing the class to respond to interactions.

## Summary
Intermediate interviews focus on component interaction, form logic, pipes/directives, and basic RxJS stream cleanups. Mastering these concepts shows that developers can write clean, performance-oriented code.

---

Previous : [Beginner Interview Prep](./28_Interview_Prep_Beginner.md) | Index : [Home](./00_index.md) | Next : [Advanced Interview Prep](./30_Interview_Prep_Advanced.md)
