# Component Lifecycle

## What is it?
Component Lifecycle un phases ki series ko represent karta hai jisse ek component apni instantiation (banne) se lekar final destruction (khatam hone) tak guzarta hai. Angular "lifecycle hooks" (kuch interfaces) provide karta, jisse hum in phases ko intercept kar sakte hain aur un transitions ke dauran custom logic run kar sakte hain.

## Why do we need it?
Ek component ko setup tasks (jaise API data fetch karna) aur cleanup tasks (jaise active timers stop karna ya event streams unsubscribe karna) karne ki zaroorat hoti hai. Lifecycle hooks ke bina, developers ko pata nahi chalega ki component ke inputs kab ready hain, uske child elements kab render ho chuke hain, ya kab component ko DOM se remove kiya ja raha hai, jiski wajah se rendering errors aur memory leaks ho sakte hain.

```
Lifecycle Hook Execution Order:
Constructor ──> ngOnChanges ──> ngOnInit ──> ngDoCheck
                 ──> ngAfterContentInit ──> ngAfterContentChecked
                 ──> ngAfterViewInit ──> ngAfterViewChecked ──> ngOnDestroy
```

## How does it work?
Angular lifecycle ko internally manage karta hai. Jab yeh component tree ko traverse karta hai, toh serial wise in hook methods ko execute karta hai agar wo component class par implemented hain:

1. **`constructor()`**: Native ES6 class initialization phase. Dependency Injection resolution yahan hoti hai. Is waqt tak DOM elements ya `@Input` properties setup nahi hue hote.
2. **`ngOnChanges()`**: Jab bhi parent component se aane wali input bindings (`@Input` ya signal inputs) ke values change hote hain, tab yeh trigger hota hai.
3. **`ngOnInit()`**: Inputs bind hone ke baad ek hi baar run hota hai. API calls ya initialization tasks ke liye yeh sabse sahi jagah hai.
4. **`ngDoCheck()`**: Har change detection cycle me `ngOnChanges` aur `ngOnInit` ke thik baad chalta hai. Aise changes detect karne ke liye use hota hai jo default Change Detection mechanism se miss ho jate hain.
5. **`ngAfterContentInit()`**: Component ke template me external content (`<ng-content>`) load hone ke baad ek baar chalta hai.
6. **`ngAfterContentChecked()`**: Projected content ko check karne ke baad har cycle me execute hota hai.
7. **`ngAfterViewInit()`**: Component ka template layout aur saare child component structures browser me fully render hone ke baad ek baar run hota hai.
8. **`ngAfterViewChecked()`**: View check hone ke baad har cycle par execute hota hai.
9. **`ngOnDestroy()`**: Component destroy hone se thik pehle run hota hai. Resources free karne, active subscriptions close karne, aur memory leaks block karne ke liye yeh critical hai.

## Impact
* **Application Architecture**: Data loading, DOM logic, aur resource cleanup actions ko unki correct stages par align karta hai.
* **Performance**: Proper hooks use karne se client memory leaks aur extra layout rendering shifts se bacha ja sakta hai.
* **Maintainability**: Component setup code aur teardown actions ko clean segments me structure karta hai.

## Real World Example
Ek stock trading application me, `ngOnInit` WebSocket connection set up karke prices stream karna shuru karta hai, `ngOnChanges` chart design update karta hai jab stock code badalta hai, aur `ngOnDestroy` network connections close kar deta hai jab user page navigate kar jata hai.

## Syntax
Lifecycle hook use karne ke liye, interfaces import karein aur method declare karein:
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-demo',
  standalone: true,
  template: `<p>Lifecycle Demo</p>`
})
export class MyComponent implements OnInit, OnDestroy {
  ngOnInit(): void {
    // Component initialization logic
  }

  ngOnDestroy(): void {
    // Clean up logic
  }
}
```

## Code Examples
Neeche saare lifecycle hooks ke execution execution flow dikhane wala dynamic logger component implement kiya gaya hai:

```typescript
import { 
  Component, 
  Input, 
  OnInit, 
  OnChanges, 
  DoCheck, 
  AfterContentInit,
  AfterContentChecked,
  AfterViewInit, 
  AfterViewChecked,
  OnDestroy, 
  SimpleChanges 
} from '@angular/core';

@Component({
  selector: 'app-lifecycle-logger',
  standalone: true,
  template: `
    <div class="log-card">
      <h4>Lifecycle Monitor</h4>
      <p>Active User: {{ user }}</p>
      <ng-content></ng-content>
    </div>
  `,
  styles: [`
    .log-card { border: 1px solid #6366f1; padding: 12px; border-radius: 6px; }
  `]
})
export class LifecycleLoggerComponent implements 
  OnChanges, 
  OnInit, 
  DoCheck, 
  AfterContentInit, 
  AfterContentChecked, 
  AfterViewInit, 
  AfterViewChecked, 
  OnDestroy 
{
  @Input() user: string = '';

  constructor() {
    console.log('1. constructor - DI resolved, Inputs NOT ready yet');
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('2. ngOnChanges - Inputs bound or modified:', changes);
  }

  ngOnInit(): void {
    console.log('3. ngOnInit - Initialization complete, fetching data for:', this.user);
  }

  ngDoCheck(): void {
    console.log('4. ngDoCheck - Change detection cycle triggered for custom checks');
  }

  ngAfterContentInit(): void {
    console.log('5. ngAfterContentInit - External content (ng-content) projected into component');
  }

  ngAfterContentChecked(): void {
    console.log('6. ngAfterContentChecked - Projected content checked by Change Detector');
  }

  ngAfterViewInit(): void {
    console.log('7. ngAfterViewInit - DOM rendered, view templates and children accessible');
  }

  ngAfterViewChecked(): void {
    console.log('8. ngAfterViewChecked - Component template and child views checked');
  }

  ngOnDestroy(): void {
    console.log('9. ngOnDestroy - Cleaning up references, subscriptions, and timers');
  }
}
```

## Best Practices
1. **Never Make HTTP Requests in the Constructor**: Constructor ke andar kabhi API calls na lagayein, hamesha `ngOnInit` use karein taaki input properties fully ready rahein.
2. **Always Unsubscribe in `ngOnDestroy`**: Memory leaks se bachne ke liye `ngOnDestroy` me RxJS subscriptions (agar template me `Async` pipe nahi use kiya hai) aur background timers ko unsubscribe/clear karein.
3. **Keep `ngDoCheck` Thin**: `ngDoCheck` har change detection cycle par chalta hai, isliye isme heavy loops likhne se page slow ho jayega.

## Common Mistakes
* **Querying children before ViewInit**: `ngOnInit` stage par child references query (`@ViewChild`) karna. Is stage par child references `undefined` show honge, kyunki templates render phase `ngAfterViewInit` ke baad setup hota hai.
* **Modifying input data inside ngOnChanges**: `ngOnChanges` loop me direct input values mutate karna. Isse components variables values alter ho sakti hain aur `ExpressionChangedAfterItHasBeenCheckedError` aa sakta hai.

## Interview Questions & Answers
### Q: What is the purpose of `ngOnChanges` and when is it called?
**A**: `ngOnChanges` tab call hota hai jab variable inputs reference badalte hain. Yeh SimpleChanges object mapping accept karta hai jahan data variables ki dynamic `currentValue` aur `previousValue` verify ho jati hai.

### Q: Why shouldn't you write data fetching logic inside the component constructor?
**A**: Constructor native JS engine class execution structure hai. Is phase me variables values aur properties bindings binded status me ready nahi hote. Angular lifecycle hook `ngOnInit` exact location hai API call run karne ke liye.

## Summary
Lifecycle hooks component execution stages ko control karte hain. Input updates react ke liye `ngOnChanges`, variables fetch ke liye `ngOnInit`, template elements access ke liye `ngAfterViewInit`, aur cleanup actions ke liye `ngOnDestroy` use karein.

---

Previous : [Directives](./07_Directives.md) | Index : [Home](./00_index.md) | Next : [Component Communication](./09_Component_Communication.md)
