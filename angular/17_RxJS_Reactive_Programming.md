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
1. **Observable**: Ek data stream jo future me clean sequence of events ya values emit karti hai.
2. **Observer**: Callbacks ka collection jo observable stream ke standard emissions (`next`, `error`, `complete`) ko listen karta hai.
3. **Subscription**: Yeh execution link hai jo observable stream ko run karta hai. Memory leaks se bachne ke liye subscriptions ko unsubscribe karna zaroori hai.
4. **Subjects**: Ek special type ka Observable jo values ko multiple observers me multicast kar sakta hai:
   - **Subject**: Naye events ko real-time me active subscribers ko emit karta hai.
   - **BehaviorSubject**: Ek default ya current state value hold karke rakhta hai, aur naye subscribers ko join karte hi wahi value immediately mil jati hai.
   - **ReplaySubject**: Naye subscribers ko subscription ke waqt past/historical emitted values ka buffer replay karta hai.
5. **Flattening Operators**: Yeh nested observables ko flatten karke single stream me convert karte hain:
   - **`switchMap`**: Naya response/request aate hi pichli active request ko cancel karke new stream par switch kar jata hai (jaise auto-complete searches).
   - **`mergeMap`**: Har event ke liye parallel streams run karta hai bina kisi query ko cancel kiye.
   - **`concatMap`**: Streams ko serial queue order me sequentially run karta hai.
   - **`exhaustMap`**: Jab tak active stream execute ho rahi hai, tab tak aane wali duplicate/extra events ko ignore karta hai (jaise double-click form submits prevent karna).

## Impact
* **Application Architecture**: Data flows aur event transitions declarative pipelines ke roop me define hote hain.
* **Performance**: Operators jaise `debounceTime` network traffic aur duplicate API requests ko filter karte hain.
* **Maintainability**: JavaScript ke callback hell/spaghetti patterns ko pure, pipeline design options se bypass karta hai.

## Real World Example
Jaise real-time chat application me users list `BehaviorSubject` me store hoti hai. Jab user kisi alag profile card par click karta hai, toh dynamic details load karne ke liye `switchMap` pichli HTTP requests ko abort kar deta hai, aur `shareReplay(1)` cache ke zariye duplicate network loading bypass karta hai.

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
1. **Always Clean Up Subscriptions**: Memory leaks se bachne ke liye `takeUntil` ya naye `takeUntilDestroyed()` operator ka use karke subscriptions ko automatically destroy phase me unsubscribe karein.
2. **Prefer the `Async` Pipe**: Templates me data render karne ke liye `async` pipe prefer karein. Yeh auto-subscribe aur component destroy hone par auto-unsubscribe handle kar leta hai.
3. **Choose the Right Flattening Operator**:
   - Outgoing processes requests ko cancel karne ke liye `switchMap` use karein.
   - Form submissions ko double click clicks se protect karne ke liye `exhaustMap` use karein.

## Common Mistakes
* **Manual subscriptions without cleanup**: Component lifecycle me manually subscribe karna aur `ngOnDestroy` me unsubscribe clear actions perform na karna.
* **Nested subscriptions (Callback Hell)**: Ek subscription ke andar dusri subscribe logic nested tarike se run karna. Linear streams ke liye hamesha flattening operators (jaise `switchMap`, `mergeMap`) ka use karein.

## Interview Questions & Answers
### Q: What is the difference between `switchMap`, `mergeMap`, and `concatMap`?
**A**: `switchMap` naya incoming event/request aate hi purani active request abort kar deta hai. `mergeMap` parallel tasks request execute karta hai. `concatMap` serial queue design structures me request sequentially run karta hai.

### Q: What is a BehaviorSubject and how does it differ from a standard Subject?
**A**: Standard `Subject` state store nahi karta. `BehaviorSubject` ek default value accept karta hai aur subscription par immediate current state return kar caching patterns support karta hai.

## Summary
RxJS asynchronous event streams aur data pipelines ko manage karne ka standard framework hai. Declarative filters aur operations (`switchMap`, `debounceTime`) memory leaks prevent karte hain aur complex async flows ko predictable banate hain.

---

Previous : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md) | Index : [Home](./00_index.md) | Next : [State Management](./18_State_Management.md)
