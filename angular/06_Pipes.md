# Pipes

## What is it?
Pipes are template utilities in Angular designed to transform data directly within your HTML templates. They accept input data, process it according to instructions, and output the formatted result without altering the underlying raw data in the component class.

## Why do we need it?
Often, database values are stored in generic, unformatted structures (such as lowercase strings, numeric timestamps, or large float amounts). Displaying this raw data to users is unprofessional. Instead of writing duplicate formatting methods in multiple component files, you can use pipes to format currencies, dates, percentages, and case text directly inside templates.

```
Raw Data in Class: 
birthday = Date("1998-05-15")

Formatted Output via Pipe in Template:
{{ birthday | date:'longDate' }} ──> May 15, 1998
```

## How does it work?
1. **Built-in Pipes**: Angular includes standard formats (`DatePipe`, `UpperCasePipe`, `LowerCasePipe`, `CurrencyPipe`, `PercentPipe`, `DecimalPipe`, `JsonPipe`, and `AsyncPipe`).
2. **Pure Pipes (Default)**: Angular only executes a pure pipe when it detects a change in the input value reference (primitive change or object reference swap). This makes pure pipes highly performant.
3. **Impure Pipes**: Angular executes an impure pipe during every change detection cycle, regardless of whether the input has changed. This is useful for tracking mutations within arrays or objects, but must be used with caution to avoid performance issues.

## Impact
* **Application Architecture**: Keeps formatting utilities highly reusable across components.
* **Performance**: Pure pipes prevent unnecessary recalculations, but impure pipes can severely degrade performance if they run expensive logic during change detection.
* **Maintainability**: Centralizes formatting logic, allowing you to change display formats application-wide in one place.

## Real World Example
In an international financial portal, currency figures are stored as floating-point numbers. We use `currency:'EUR'` to display values formatted correctly for European users automatically.

## Syntax
* **Applying a pipe**: `{{ value | pipeName }}`
* **Passing parameters**: `{{ value | pipeName:arg1:arg2 }}`
* **Chaining pipes**: `{{ value | pipe1 | pipe2 }}`

## Code Examples
Below is an implementation of a custom **pure pipe** to truncate text and add an ellipsis, and an **impure pipe** to filter collections.

```typescript
import { Pipe, PipeTransform, Component } from '@angular/core';
import { CommonModule } from '@angular/common';

// 1. Custom Pure Pipe
@Pipe({
  name: 'truncate',
  standalone: true
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
  pure: false, // Setting pure to false makes it run on mutations
  standalone: true
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
      <h3>Truncate Pipe (Pure):</h3>
      <p>{{ longArticleText | truncate:30 }}</p>

      <h3>Built-in Currency Pipe:</h3>
      <p>{{ price | currency:'USD':'symbol':'1.2-2' }}</p>

      <h3>Async Pipe with Promise:</h3>
      <p>Loaded Data: {{ asyncMessage$ | async }}</p>
    </div>
  `,
  styles: [`
    .demo-box { font-family: Arial, sans-serif; padding: 20px; border: 1px dashed #3b82f6; max-width: 500px; }
    h3 { margin-top: 15px; color: #1e3a8a; }
  `]
})
export class PipesDemoComponent {
  longArticleText = 'Angular standalone pipelines make processing data on screen cleaner and more modular than ever before.';
  price = 1299.99;

  asyncMessage$: Promise<string> = new Promise((resolve) => {
    setTimeout(() => resolve('API Data loaded via Promise!'), 1500);
  });
}
```

## Best Practices
1. **Keep Pipes Pure**: Unless absolutely necessary, keep `pure: true`. Pure pipes cache values, providing a significant performance boost.
2. **Never Put Expensive Logic in Impure Pipes**: Avoid heavy array operations, network fetches, or database calls in impure pipes.
3. **Prefer Pipes Over Component Methods**: Using a method inside a template, like `{{ formatName(user) }}`, forces Angular to invoke it on every change detection sweep. Pipes avoid this by caching results based on input identity.

## Common Mistakes
* **Mutating Arrays and Expecting Pure Pipes to Update**: Mutating an array with `.push()` does not change its reference, so a pure pipe won't re-run. To trigger a pure pipe, replace the array reference: `items = [...items, newItem]`.
* **Injecting HTTP Calls into Pipes**: Using a pipe to fetch API details directly inside a template. This can create infinite network loops. Delegate API calls to services.

## Interview Questions & Answers
### Q: What is the difference between a Pure and an Impure Pipe?
**A**: A pure pipe is only executed when Angular detects a change in its input reference (primitive changes or reference updates for objects/arrays). An impure pipe is invoked during every change detection cycle, regardless of input changes, making it less performant but useful for tracking mutations within arrays or objects.

### Q: Why is the `Async` pipe highly recommended?
**A**: The `AsyncPipe` automatically subscribes to an Observable or Promise, returns the emitted values to the template, and handles unsubscription when the component is destroyed. This prevents memory leaks without requiring manual subscription cleanup in your TypeScript code.

## Summary
Pipes format data for display in HTML templates. Pure pipes optimize performance by caching results, while the async pipe automatically manages subscriptions. Custom pipes are easily declared using the `@Pipe` decorator.

---

Previous : [Components and Templates](./05_Components_and_Templates.md) | Index : [Home](./00_index.md) | Next : [Directives](./07_Directives.md)
