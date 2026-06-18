# RxJS Reactive Programming

## What is it?
RxJS (Reactive Extensions for JavaScript) is a library for composing asynchronous and event-based programs using observable sequences. It provides the foundation for reactive programming in Angular, enabling you to manage network requests, user inputs, and state updates as continuous streams of data.

## Why do we need it?
Modern applications must handle complex asynchronous operations: coordinating multiple concurrent API calls, debouncing keystrokes on search fields, managing real-time WebSocket notifications, and cleaning up subscriptions to prevent memory leaks. Standard JavaScript APIs (like Promises and event listeners) can be difficult to coordinate under these conditions. RxJS solves this by providing a unified model to transform, combine, and clean up asynchronous events using declarative operators.

```
Observable Stream (Search Input):
User Types ──> [ 'a' ... 'ab' ... 'abc' ]
           ──> debounceTime(300ms) ──> distinctUntilChanged()
           ──> switchMap(query => fetchResults(query)) ──> Renders search results
```

## How does it work?
1. **Observable**: A collection that emits values asynchronously over time.
2. **Observer**: A set of callbacks that listens for values (`next`), errors (`error`), or completion signals (`complete`) emitted by an Observable.
3. **Subscription**: Represents the execution of an Observable. Used to cancel stream execution and prevent memory leaks.
4. **Subjects**: Multicast observables that allow values to be sent to multiple observers:
   - **Subject**: Emits values to active subscribers.
   - **BehaviorSubject**: Stores the latest value and emits it to new subscribers immediately.
   - **ReplaySubject**: Replays a specified number of past emissions to new subscribers.
5. **Flattening Operators**: Manage nested observables (like making an API call based on a search input change):
   - **`switchMap`**: Cancels the active inner observable and switches to the new one. Useful for search boxes.
   - **`mergeMap`**: Runs multiple inner observables concurrently. Useful for batch requests.
   - **`concatMap`**: Runs inner observables sequentially in order. Useful for queued updates.
   - **`exhaustMap`**: Ignores new emissions while the current inner observable is running. Useful for double-click prevention on submit buttons.

## Impact
* **Application Architecture**: Enables declarative, reactive data flows from APIs to views.
* **Performance**: Stream throttling (`debounceTime`, `distinctUntilChanged`) prevents redundant network requests.
* **Maintainability**: Keeps async operations clean, avoiding "callback hell".

## Real World Example
In a real-time chat application, a `BehaviorSubject` stores the active list of online users. A `switchMap` fetches user profiles dynamically when a user is selected, and `shareReplay(1)` caches the profile data so other parts of the UI can read it without triggering duplicate network requests.

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
Below is a complete implementation demonstrating search auto-completion with request debouncing, request flattening (`switchMap`), and subscription management.

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
  private destroy$ = new Subject<void>(); // Unsubscription notifier

  searchControl = new FormControl('');
  results: SearchResult[] = [];
  loading = false;

  ngOnInit(): void {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),          // Wait for 300ms of silence
      distinctUntilChanged(),     // Ignore if value matches the previous one
      tap(() => {
        this.loading = true;
        this.results = [];
      }),
      switchMap(query => {
        if (!query || query.trim() === '') {
          return of([]); // Return empty array if input is cleared
        }
        return this.fetchSearchResults(query).pipe(
          catchError(() => {
            console.error('Search failed - returning empty results');
            return of([]); // Fallback to empty array on error
          })
        );
      }),
      takeUntil(this.destroy$) // Automatically unsubscribe when component is destroyed
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
    this.destroy$.next(); // Trigger unsubscription
    this.destroy$.complete();
  }
}
```

## Best Practices
1. **Always Clean Up Subscriptions**: Prevent memory leaks by using `takeUntil` with a destroy notifier Subject, or the modern `takeUntilDestroyed()` operator.
2. **Prefer the `Async` Pipe**: Bind observable streams directly in templates using the `async` pipe. It handles subscriptions and cleanups automatically, avoiding manual component subscriptions.
3. **Choose the Right Flattening Operator**:
   - Use `switchMap` to cancel ongoing requests when a new event fires (e.g. search boxes).
   - Use `exhaustMap` to ignore new events while a request is in progress (e.g. submit buttons).

## Common Mistakes
* **Manual subscriptions without cleanup**: Subscribing directly to streams in component classes and forgetting to unsubscribe, which leaves active subscription timers running when the component is destroyed.
* **Nested subscriptions (Callback Hell)**: Writing code like `service.getData().subscribe(id => { service.getDetails(id).subscribe(details => { ... }) })`. Use flattening operators (like `switchMap`) to chain requests instead.

## Interview Questions & Answers
### Q: What is the difference between `switchMap`, `mergeMap`, and `concatMap`?
**A**: `switchMap` cancels the active inner observable when a new value arrives (useful for search boxes). `mergeMap` processes all inner observables concurrently (useful for parallel requests). `concatMap` queues inner observables to run sequentially in order (useful for transactional operations).

### Q: What is a BehaviorSubject and how does it differ from a standard Subject?
**A**: A standard `Subject` does not store values and only emits values to active subscribers. A `BehaviorSubject` requires an initial value, stores its latest emitted value, and emits it to new subscribers immediately upon subscription.

## Summary
RxJS manages asynchronous events and streams in Angular. Using operators (like `switchMap` and `debounceTime`) and subjects (like `BehaviorSubject`) helps build reactive, memory-safe, and performant web applications.

---

Previous : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md) | Index : [Home](./00_index.md) | Next : [State Management](./18_State_Management.md)
