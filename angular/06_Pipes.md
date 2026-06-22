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

## Hinglish Explanation

Pipes ka simple kaam hai **"Data ko display ke liye format karna"**. Yeh background data ko actual me change kiye bina, user ko screen par sahi tarike se show karne ke liye use hote hain (jaise lower case ko upper case banana ya raw number ko currency format me convert karna).

### 1. Built-in Pipes (Pehle se bane pipes)
* **Uppercase/Lowercase:** Text ko caps/small karne ke liye: `{{ 'hello' | uppercase }}` -> HELLO.
* **Currency:** Numbers ko currency format me transform karne ke liye: `{{ 100 | currency }}` -> $100.00.
* **Date:** Raw timestamp ko standard date format me show karne ke liye.

### 2. Pure Pipes (Smart & Performance Friendly)
* By default, Angular ke saare pipes **Pure** hote hain.
* Yeh tabhi chalte hain jab inki input value (ya object/array reference) change hoti hai. Agar input badla nahi hai, toh yeh cached value return kar dete hain, jisse computation power bachti hai.
* **Example/Gotcha:** Agar aap kisi array me `.push()` se element insert karte hain, toh pure pipe run nahi hoga kyunki array ka references (address) change nahi hua. Isko fix karne ke liye hume de-structuring use karke array reference change karna padta hai: `items = [...items, newItem]`.

### 3. Impure Pipes (Har cycle par chalne wale)
* Inhe `@Pipe({ name: 'myPipe', pure: false })` se define kiya jata hai.
* Yeh component ke har ek action (change detection cycle) par execute hote hain. Yeh memory leaks ya performance issue kar sakte hain, isliye inka use avoid karna chahiye jab tak array/object elements ke andar deep mutation track na karni ho.

### 4. Async Pipe (`async`)
* Yeh Angular ka sabse popular pipe hai. Jab dynamic data (Observables/Promises) direct template me render karna ho, tab iska use hota hai.
* Yeh component lifecycle ke sath synchronous subscribe aur unsubscribe handle kar leta hai, jisse memory leaks ka khatra bilkul zero ho jata hai.

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
* **Hinglish Explanation**: Pure Pipe tabhi execute hota hai jab uski input value/reference badalta hai (primitive type badle ya array/object ka reference badle). Impure Pipe har change detection cycle par chalta hai, chahe input change hua ho ya nahi. Pure pipe caching ki wajah se bohot fast aur performant hota hai, jabki impure pipe performance slow kar sakta hai par array modifications ko update karne me useful hota hai.

### Q: Why is the `Async` pipe highly recommended?
**A**: The `AsyncPipe` automatically subscribes to an Observable or Promise, returns the emitted values to the template, and handles unsubscription when the component is destroyed. This prevents memory leaks without requiring manual subscription cleanup in your TypeScript code.
* **Hinglish Explanation**: `AsyncPipe` bohot useful hai kyunki yeh component template me directly Observable ya Promise ko handle karta hai. Yeh background me auto-subscribe karta hai aur component destroy hone par auto-unsubscribe bhi kar deta hai. Isse memory leak hone ka khatra bilkul khatam ho jata hai aur aapko TS file me manual subscription aur unsubscription ka boilerplate code nahi likhna padta.

## Summary
Pipes format data for display in HTML templates. Pure pipes optimize performance by caching results, while the async pipe automatically manages subscriptions. Custom pipes are easily declared using the `@Pipe` decorator.

---

Previous : [Components and Templates](./05_Components_and_Templates.md) | Index : [Home](./00_index.md) | Next : [Directives](./07_Directives.md)
