# Pipes

## What is it?
Pipes in Angular are template transformation functions designed to format raw data directly within HTML templates. A pipe takes an input value, processes it according to specified parameters, and outputs the formatted result for display without altering the underlying data in the TypeScript component class.

## Why do we need it?
Databases and API endpoints typically return data in raw, unformatted structures (e.g., ISO timestamp strings, lowercase status codes, unrounded floating-point numbers). Presenting raw values directly to end users creates a poor user experience. 

Instead of writing repetitive transformation functions across multiple component classes, Angular pipes allow you to declaratively format currencies, dates, percentages, strings, and JSON directly in the template.

```
Raw Data in TypeScript: 
birthday = new Date("1998-05-15")

Formatted Output via Pipe in Template:
{{ birthday | date:'longDate' }} ──> May 15, 1998
```

## How does it work?
1. **Built-in Pipes**: Angular ships with a rich set of built-in pipes, including `DatePipe`, `UpperCasePipe`, `LowerCasePipe`, `CurrencyPipe`, `PercentPipe`, `DecimalPipe`, `JsonPipe`, and `AsyncPipe`.
2. **Pure Pipes (Default)**: Angular executes a pure pipe **only** when it detects a change to the input value (a change to a primitive value or a new object/array reference). Pure pipes memoize (cache) results for optimal performance.
3. **Impure Pipes (`pure: false`)**: Angular executes an impure pipe on **every single change detection cycle**, regardless of whether the input reference has changed. This is useful for tracking mutations within arrays or objects, but must be used with caution to avoid performance degradation.

## Impact
* **Application Architecture**: Encapsulates data formatting into reusable, testable utilities across the entire project.
* **Performance**: Pure pipes prevent redundant computations through input memoization.
* **Maintainability**: Keeps formatting logic centralized, so updating a date or currency format across an application requires changing only the pipe or its format configuration.

## Real World Example
In a multi-currency international e-commerce platform, raw product prices stored as numeric floats (e.g., `1299.99`) are formatted according to the user's localized currency (`{{ price | currency:'EUR':'symbol':'1.2-2' }}`).

## Syntax
* **Applying a pipe**: `{{ value | pipeName }}`
* **Passing parameters**: `{{ value | pipeName:arg1:arg2 }}`
* **Chaining multiple pipes**: `{{ value | pipe1 | pipe2 }}`

## Code Examples
Below is a complete implementation demonstrating a custom **pure pipe** (for text truncation), a custom **impure pipe** (for collection filtering), and built-in pipes including `AsyncPipe`:

```typescript
import { Pipe, PipeTransform, Component } from '@angular/core';
import { CommonModule } from '@angular/common';

// 1. Custom Pure Pipe
@Pipe({
  name: 'truncate',
  standalone: true,
  pure: true // Default: executes only when reference/primitive changes
})
export class TruncatePipe implements PipeTransform {
  transform(value: string, limit: number = 20, suffix: string = '...'): string {
    if (!value) return '';
    return value.length > limit ? value.substring(0, limit) + suffix : value;
  }
}

// 2. Custom Impure Pipe
@Pipe({
  name: 'filterList',
  standalone: true,
  pure: false // Executes on every change detection cycle to detect array mutations
})
export class FilterListPipe implements PipeTransform {
  transform(items: string[], filterText: string): string[] {
    if (!items || !filterText) return items;
    return items.filter(item => item.toLowerCase().includes(filterText.toLowerCase()));
  }
}

// 3. Demo Component
@Component({
  selector: 'app-pipes-demo',
  standalone: true,
  imports: [CommonModule, TruncatePipe, FilterListPipe],
  template: `
    <div class="demo-box">
      <h3>Custom Pure Truncate Pipe:</h3>
      <p>{{ longArticleText | truncate:35 }}</p>

      <h3>Built-in Currency Pipe:</h3>
      <p>{{ price | currency:'USD':'symbol':'1.2-2' }}</p>

      <h3>Async Pipe with Promise:</h3>
      <p>Loaded Data: {{ asyncMessage$ | async }}</p>
    </div>
  `,
  styles: [`
    .demo-box { 
      font-family: Arial, sans-serif; 
      padding: 20px; 
      border: 1px dashed #3b82f6; 
      max-width: 520px; 
    }
    h3 { 
      margin-top: 15px; 
      color: #1e3a8a; 
    }
  `]
})
export class PipesDemoComponent {
  longArticleText = 'Angular standalone pipelines make processing data on screen cleaner and more modular than ever before.';
  price = 1299.99;

  asyncMessage$: Promise<string> = new Promise((resolve) => {
    setTimeout(() => resolve('Data loaded asynchronously via Promise!'), 1200);
  });
}
```

## Best Practices
1. **Keep Pipes Pure**: Unless strictly necessary, always keep pipes pure (`pure: true`). Pure pipes cache results and avoid running on every tick.
2. **Never Place Heavy Logic in Impure Pipes**: Avoid heavy computations, deep array loops, or network calls inside impure pipes.
3. **Prefer Pure Pipes Over Component Methods in Templates**: Avoid writing `{{ formatUser(user) }}` in templates. Component methods execute on every single change detection cycle, whereas pure pipes cache the output until the input reference changes.

## Common Mistakes
* **Mutating Arrays and Expecting Pure Pipes to Update**: Using `array.push(newItem)` modifies the internal array but does not change the array reference. Because the reference stays the same, pure pipes will not re-run. Always create a new reference using the spread operator (`items = [...items, newItem]`).
* **Triggering HTTP Calls Inside Pipes**: Triggering HTTP requests inside pipe `transform()` methods can cause infinite request loops and sever performance issues. Keep HTTP communication strictly inside injectable services.

## Interview Questions & Answers
### Q: What is the key difference between a Pure Pipe and an Impure Pipe?
**A**: A pure pipe runs only when Angular detects a change to the primitive value or object reference passed as an input. It leverages caching/memoization for high performance. An impure pipe runs on every change detection cycle, regardless of whether inputs have changed. Impure pipes can detect internal object or array mutations, but introduce significant performance overhead if misused.

### Q: Why is `AsyncPipe` considered a best practice when working with Observables?
**A**: `AsyncPipe` automatically subscribes to an `Observable` or `Promise`, delivers the latest emitted value to the template, and marks the component for change detection. Most importantly, it **automatically unsubscribes** when the component is destroyed, preventing memory leaks without manual lifecycle management.

## Summary
Pipes provide clean, declarative data formatting directly in Angular templates. Pure pipes optimize rendering performance through memoization, while specialized pipes like `AsyncPipe` streamline asynchronous data streams and prevent memory leaks.

---

Previous : [Components and Templates](./05_Components_and_Templates.md) | Index : [Home](./00_index.md) | Next : [Directives](./07_Directives.md)
