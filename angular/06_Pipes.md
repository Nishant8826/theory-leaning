# Pipes

## What is it?
Pipes Angular ke template utilities hain jinhe HTML templates ke andar data ko directly transform karne ke liye design kiya gaya hai. Yeh input data receive karte hain, guidelines ke mutabik use process karte hain, aur formatted result output karte hain bina component class ke actual/raw data ko modify kiye.

## Why do we need it?
Database values aksar raw aur unformatted format me store hoti hain (jaise lowercase strings, numeric timestamps, ya float numbers). Is raw data ko directly users ko dikhana sahi nahi lagta. Alag-alag components me formatting methods likhne ke bajaye, aap templates ke andar directly currencies, dates, percentages, aur cases ko format karne ke liye pipes use kar sakte hain.

```
Raw Data in Class: 
birthday = Date("1998-05-15")

Formatted Output via Pipe in Template:
{{ birthday | date:'longDate' }} ──> May 15, 1998
```

## How does it work?
1. **Built-in Pipes**: Angular me standard formats ke liye pehle se built-in pipes milte hain (jaise `DatePipe`, `UpperCasePipe`, `LowerCasePipe`, `CurrencyPipe`, `PercentPipe`, `DecimalPipe`, `JsonPipe`, aur `AsyncPipe`).
2. **Pure Pipes (Default)**: Angular pure pipe ko tabhi execute karta hai jab use input value reference (primitive values me changes ya object/array reference swap) me koi badlaav dikhta hai. Is wajah se pure pipes highly performant hote hain.
3. **Impure Pipes**: Angular impure pipes ko har change detection cycle ke dauran execute karta hai, chahe input change hua ho ya nahi. Yeh array ya object mutations ko track karne me kaam aata hai, lekin performance issues se bachne ke liye ise dhyan se use karna chahiye.

## Impact
* **Application Architecture**: Formatting logics ko components ke beech highly reusable banata hai.
* **Performance**: Pure pipes unnecessary calculations se bachate hain, lekin impure pipes change detection cycle me slow processing badha kar performance degrade kar sakte hain.
* **Maintainability**: Formatting logic ko ek central place par manage karta hai, jisse dynamic modifications pure application me instantly reflect ho jati hain.

## Real World Example
Ek international financial app me dynamic currency values floating-point format me store hoti hain. Hum client location ke coordinates ke mutabik numbers ko currency filter me `currency:'EUR'` pass karke display karte hain.

## Syntax
* **Applying a pipe**: `{{ value | pipeName }}`
* **Passing parameters**: `{{ value | pipeName:arg1:arg2 }}`
* **Chaining pipes**: `{{ value | pipe1 | pipe2 }}`

## Code Examples
Neeche text truncate karne wale **pure pipe** aur collection filter karne wale **impure pipe** ka custom implementation demo component ke sath diya gaya hai:

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
1. **Keep Pipes Pure**: Jab tak bohot zaroori na ho, pipes ko `pure: true` hi rakhein. Pure pipes results ko cache karte hain, jisse performance kaafi improve hoti hai.
2. **Never Put Expensive Logic in Impure Pipes**: Impure pipes me heavy calculations, network APIs calls, ya database handling logic kabhi na likhein.
3. **Prefer Pipes Over Component Methods**: Template bindings me code operations ke liye component methods (jaise `{{ formatName(user) }}`) calls avoid karne chahiye. Method calls change detection cycle par repeat call hote hain, jagki pipes references checks filter caching use karte hain.

## Common Mistakes
* **Mutating Arrays and Expecting Pure Pipes to Update**: Array me `.push()` se element insert karne par object index reference change nahi hota, isliye pure pipe updates show nahi karta. Array update ke liye hamesha reference change karein: `items = [...items, newItem]`.
* **Injecting HTTP Calls into Pipes**: Pipes ke andar directly network API requests trigger karna. Yeh layout rendering parameters ko slow aur infinite loop me fansa sakta hai. API calls ko services me handle karein.

## Interview Questions & Answers
### Q: What is the difference between a Pure and an Impure Pipe?
**A**: Pure pipe tabhi execute hota hai jab input reference badalta hai. Impure pipe har change detection cycle par chalta hai chahe input badla ho ya nahi. Pure pipes caching use karte hain isliye faster hote hain, jabki impure pipes arrays/objects mutations live track karne me use hote hain par slow hote hain.

### Q: Why is the `Async` pipe highly recommended?
**A**: `AsyncPipe` templates me directly Observable/Promise data stream handle karta hai. Yeh background me dynamically subscribe karta hai aur component destroy phase me auto-unsubscribe triggers handle karta hai, jisse memory leaks control hoti hain.

## Summary
Pipes templates me visual presentation ke liye data format change karte hain. Pure pipes inputs caching se rendering performance optimize rakhte hain aur async pipe subscriptions flow logic direct handle karta hai. Custom pipes hum `@Pipe` decorator se bana sakte hain.

---

Previous : [Components and Templates](./05_Components_and_Templates.md) | Index : [Home](./00_index.md) | Next : [Directives](./07_Directives.md)
