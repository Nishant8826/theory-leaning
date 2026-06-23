# RxJS Reactive Programming

## What is it?
RxJS (Reactive Extensions for JavaScript) asynchronous aur event-based programs likhne ke liye observable sequences compose karne ki ek helper library hai. Yeh Angular me reactive programming ke liye foundation provide karti hai, jisse aap network requests, user inputs, aur state updates ko data ke continuous streams ke roop me manage kar sakte hain.

## Why do we need it?
Modern application components ko complex asynchronous tasks handle karne padte hain (jaise parallel API calls coordinate karna, search fields me character typing debounce karna, real-time WebSocket messages parse karna, aur memory leak control cleanup manage karna). Standard promises ya event listeners un actions me limits force karte hain. RxJS asynchronous data flows ko transform, combine aur clean karne ke liye simple declarative operators aur streams provide karta hai.

```
Observable Stream (Search Input):
User Types ──> [ 'a' ... 'ab' ... 'abc' ]
           ──> debounceTime(300ms) ──> distinctUntilChanged()
           ──> switchMap(query => fetchResults(query)) ──> Renders search results
```

## How does it work?
1. **Observable**: Ek aisa variable ya stream collection jo continuous values ya dynamic events updates time to time deliver karta hai.
2. **Observer**: Callback collection blocks jo Observables flows me values (`next`), exceptions (`error`), ya completed indicators (`complete`) ko listen karte hain.
3. **Subscription**: Observable stream execution setup link. Subscriptions objects check control se memory leaks save karne ke liye paths unsubscribe triggers trigger kiye jate hain.
4. **Subjects**: Multicast systems jo multiple observers ko values share karte hain:
   - **Subject**: Active subscribers ko runtime events deliver karta hai.
   - **BehaviorSubject**: Ek initial data store rakhta hai aur new subscriptions ko immediately state current status return karta hai.
   - **ReplaySubject**: New subscribers connect hone par historical index collections values return triggers execute karta hai.
5. **Flattening Operators**: Nested inputs parameters observables handles logic:
   - **`switchMap`**: Chal rahe execution context ko abort kar immediately next input value check select stream par switch kar leta hai. Search auto-complete structures me best hai.
   - **`mergeMap`**: Background parallel operations trigger coordinates parameters run karta hai.
   - **`concatMap`**: Sequentially serial order flow inputs tasks checks execute karta hai.
   - **`exhaustMap`**: Current background API processing time ke doran incoming requests skip filters parameters check active rakhta hai. Submit double clicks prevention checks me useful hai.

## Impact
* **Application Architecture**: Data fetch pipelines API to template integration layers me declarative rules define karta hai.
* **Performance**: Stream control filters (`debounceTime`, `distinctUntilChanged`) server trips request traffic limit down rakhte hain.
* **Maintainability**: Nested callback lines "callback hell" code traps bypass kar clean codes patterns establish karta hai.

## Real World Example
Real-time chat platform portal application interface me, online users list variable `BehaviorSubject` me save hoti hai. User select profile details switch logic checks trigger karne par dynamic requests checks `switchMap` process handle karta hai aur `shareReplay(1)` cache filters values data return handles check active rakhta hai redundant network network loading bypass setups ke liye.

## Syntax
* **Creating an Observable**:
```typescript
const stream$ = new Observable(subscriber => {
  subscriber.next('Hello');
  subscriber.complete();
});
```
* **Piping Operators**:
```typescript
stream$.pipe(
  map(val => val.toUpperCase()),
  takeUntilDestroyed()
).subscribe(val => console.log(val));
```

## Code Examples
Neeche auto-completion search box ka custom input reactive pipeline integration sample coordinate code structure diya gaya hai:

```typescript
import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Subject, Observable, of } from 'rxjs';
import { 
  debounceTime, 
  distinctUntilChanged, 
  switchMap, 
  catchError, 
  takeUntil, 
  tap 
} from 'rxjs/operators';

interface SearchResult {
  id: number;
  title: string;
}

@Component({
  selector: 'app-search-autocomplete',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="search-box">
      <h3>Live Search Box</h3>
      <input [formControl]="searchControl" placeholder="Type here to search..." />
      
      <div *ngIf="loading" class="spinner">Searching products...</div>

      <ul class="results">
        <li *ngFor="let item of results">{{ item.title }}</li>
        <li *ngIf="results.length === 0 && !loading">No results found</li>
      </ul>
    </div>
  `,
  styles: [`
    .search-box { border: 1px solid #7c3aed; padding: 20px; border-radius: 8px; max-width: 350px; }
    input { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    .results { list-style: none; padding: 0; margin-top: 10px; }
    .results li { padding: 6px; border-bottom: 1px solid #f3f4f6; }
    .spinner { color: #6d28d9; font-size: 13px; margin: 8px 0; }
  `]
})
export class SearchAutocompleteComponent implements OnInit, OnDestroy {
  private http = inject(HttpClient);
  private destroy$ = new Subject<void>();

  searchControl = new FormControl('');
  results: SearchResult[] = [];
  loading = false;

  ngOnInit(): void {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      tap(() => {
        this.loading = true;
        this.results = [];
      }),
      switchMap(query => {
        if (!query || query.trim() === '') {
          return of([]);
        }
        return this.fetchSearchResults(query).pipe(
          catchError(() => {
            console.error('Search failed - returning empty results');
            return of([]);
          })
        );
      }),
      takeUntil(this.destroy$)
    ).subscribe(data => {
      this.results = data;
      this.loading = false;
    });
  }

  fetchSearchResults(query: string): Observable<SearchResult[]> {
    const url = `https://api.escuelajs.co/api/v1/products/?title=${query}`;
    return this.http.get<SearchResult[]>(url);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Best Practices
1. **Always Clean Up Subscriptions**: Memory leaks block updates handle checks settings coordinate me `takeUntil` operators direct custom Subject alert config rules compile ya modern `takeUntilDestroyed()` apply checks rules setup ensure karein.
2. **Prefer the `Async` Pipe**: HTML view templates variables bindings me observable outputs maps coordinate `async` pipe target verify check apply karein. Isse auto-unsubscribe mechanisms self-manage compile logic run coordinate parameters complete options configure hote hain.
3. **Choose the Right Flattening Operator**:
   - Outgoing processes requests cancel checks rules setup parameters me `switchMap` execute trigger set karein.
   - Double click checks triggers protection constraints rules setup properties checks me `exhaustMap` target set karein.

## Common Mistakes
* **Manual subscriptions without cleanup**: Components TS lifecycle logic codes me streams subscribe lines create parameters, reset hooks options parameters clear actions target ignore karna.
* **Nested subscriptions (Callback Hell)**: Nesting subscribe commands parameters like `service.getData().subscribe(x => { service.getDataB(x).subscribe(y => ...) })`. Request chains flow logic coordinates linear configure variables setup flat targets (jaise `switchMap`) configure check implement karein.

## Interview Questions & Answers
### Q: What is the difference between `switchMap`, `mergeMap`, and `concatMap`?
**A**: `switchMap` new values arriving coordinate updates par existing inner operations abort settings parameters apply karta hai. `mergeMap` parallel coordinate processes dynamic flows handle karta hai. `concatMap` sequentially serial queue updates setups target use karta hai.

### Q: What is a BehaviorSubject and how does it differ from a standard Subject?
**A**: Standard `Subject` state indicators values memory storage maintain nahi karta. `BehaviorSubject` initialization parameters settings checks me default starting parameters accept target set karke hamesha dynamic variables status cache hold check update coordinate patterns rules maintain rakhta hai.

## Summary
RxJS dynamic web apps interfaces asynchronous events streams data components control settings configure karta hai. Functional filters pipeline operations (`switchMap`, `debounceTime`) data memory safe parameters integrations execute dynamic robust systems coordinate settings ensure karte hain.

---

Previous : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md) | Index : [Home](./00_index.md) | Next : [State Management](./18_State_Management.md)
