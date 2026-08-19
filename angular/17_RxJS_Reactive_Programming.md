# RxJS Reactive Programming

## What is it?
RxJS (Reactive Extensions for JavaScript) is a library for composing asynchronous and event-based programs using observable sequences. It serves as the backbone for reactive programming in Angular, enabling developers to treat user inputs, HTTP requests, timers, and application state transitions as continuous, transformable streams of data.

## Why do we need it?
Modern web applications must coordinate complex asynchronous operations—such as debouncing user input in search bars, coordinating parallel or sequential API requests, parsing real-time WebSocket feeds, and managing memory teardown cleanly. 

Using plain JavaScript callbacks or standard Promises quickly leads to "callback hell", race conditions, and unmanaged memory leaks. RxJS provides a declarative, functional approach to transform, combine, filter, and cancel asynchronous events with precision.

```
Observable Stream (Typeahead Live Search):
User Types ──> [ 'a' ... 'ab' ... 'abc' ]
           ──> debounceTime(300ms) ──> distinctUntilChanged()
           ──> switchMap(query => fetchResults(query)) ──> Renders Search Results
```

## How does it work?
1. **Observable**: A data stream that can push multiple values (events, data items, or errors) to subscribers over time.
2. **Observer**: A consumer object with `next()`, `error()`, and `complete()` handler callbacks that listens to an Observable.
3. **Subscription**: Represents the active execution of an Observable stream. Unsubscribing cancels ongoing work and frees browser memory.
4. **Subjects (Multicasting)**:
   - **`Subject`**: A multicast Observable that emits new values only to currently active subscribers.
   - **`BehaviorSubject`**: Holds an initial/current value and immediately emits the latest state to any new subscriber upon connection.
   - **`ReplaySubject`**: Buffers a specified number of past emissions and replays them to new subscribers.
5. **Higher-Order Flattening Operators**:
   - **`switchMap`**: Cancels any previous in-flight inner Observable as soon as a new emission arrives (ideal for autocomplete searches).
   - **`mergeMap`**: Handles multiple inner Observables concurrently in parallel without cancelling previous requests.
   - **`concatMap`**: Queues inner Observables sequentially, executing each one only after the previous one completes.
   - **`exhaustMap`**: Ignores incoming emissions while an existing inner Observable is currently executing (ideal for preventing duplicate form submissions on button double-clicks).

## Impact
* **Application Architecture**: Converts fragmented async logic into clean, declarative data transformation pipelines.
* **Performance**: Operators like `debounceTime`, `distinctUntilChanged`, and `throttleTime` drastically reduce redundant network requests and DOM updates.
* **Maintainability**: Replaces nested callback pyramids with clean, pipeable operators.

## Real World Example
In a real-time live search typeahead:
1. The user types characters into an input field.
2. `debounceTime(300)` waits until the user pauses typing for 300ms.
3. `distinctUntilChanged()` discards repeated identical queries.
4. `switchMap()` cancels previous in-flight HTTP search requests, preventing stale responses from overwriting the latest search results.

## Syntax
* **Creating an Observable**:
```typescript
const stream$ = new Observable<string>(subscriber => {
  subscriber.next('Event 1');
  subscriber.next('Event 2');
  subscriber.complete();
});
```
* **Piping Operators**:
```typescript
stream$.pipe(
  map(text => text.toUpperCase()),
  takeUntilDestroyed()
).subscribe(result => console.log(result));
```

## Code Examples
Below is a complete typeahead search component demonstrating `debounceTime`, `distinctUntilChanged`, `switchMap`, error resilience, and proper unsubscription:

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
      <h3>Product Live Search</h3>
      <input [formControl]="searchControl" placeholder="Type product name to search..." />
      
      <div *ngIf="loading" class="spinner">Searching live catalog...</div>

      <ul class="results">
        <li *ngFor="let item of results">{{ item.title }}</li>
        <li *ngIf="results.length === 0 && !loading && searchControl.value">
          No matching products found.
        </li>
      </ul>
    </div>
  `,
  styles: [`
    .search-box { border: 1px solid #7c3aed; padding: 20px; border-radius: 8px; max-width: 380px; font-family: sans-serif; }
    input { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    .results { list-style: none; padding: 0; margin-top: 12px; }
    .results li { padding: 8px; border-bottom: 1px solid #f3f4f6; font-size: 14px; }
    .spinner { color: #6d28d9; font-size: 13px; margin: 8px 0; font-style: italic; }
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
      debounceTime(300),              // Wait for 300ms pause in typing
      distinctUntilChanged(),         // Only search if the query text actually changed
      tap(() => {
        this.loading = true;
        this.results = [];
      }),
      switchMap(query => {
        if (!query || query.trim() === '') {
          return of([]);
        }
        // Cancel any pending HTTP search if the user types a new character
        return this.fetchSearchResults(query).pipe(
          catchError((err) => {
            console.error('Search API error:', err);
            return of([]); // Graceful fallback to empty results
          })
        );
      }),
      takeUntil(this.destroy$)        // Automatically unsubscribe on component teardown
    ).subscribe(data => {
      this.results = data;
      this.loading = false;
    });
  }

  fetchSearchResults(query: string): Observable<SearchResult[]> {
    const url = `https://api.escuelajs.co/api/v1/products/?title=${encodeURIComponent(query)}`;
    return this.http.get<SearchResult[]>(url);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Best Practices
1. **Always Manage Subscriptions**: Never leave subscriptions open indefinitely. Use `takeUntilDestroyed()` (Angular 16+) or the `takeUntil(destroy$)` pattern in `ngOnDestroy` to prevent browser memory leaks.
2. **Prefer the `AsyncPipe`**: Whenever possible, bind Observables directly in templates using `| async`. The `AsyncPipe` handles subscription management and automatic unsubscription upon component destruction.
3. **Choose the Correct Flattening Operator**:
   - Use `switchMap` when earlier requests should be abandoned in favor of newer ones (e.g., search queries, route changes).
   - Use `concatMap` when execution order must be preserved sequentially.
   - Use `mergeMap` when all requests must complete concurrently in parallel.
   - Use `exhaustMap` to ignore subsequent actions until the active operation finishes (e.g., login or save buttons).

## Common Mistakes
* **Nested Subscriptions**: Calling `.subscribe()` inside another `.subscribe()` callback. This creates callback hell and makes error propagation difficult. Always use flattening operators (`switchMap`, `mergeMap`, `concatMap`).
* **Uncaught Stream Errors**: If an Observable pipeline encounters an error without `catchError()`, the stream terminates permanently and stops responding to future events.

## Interview Questions & Answers
### Q: What is the difference between `switchMap`, `mergeMap`, and `concatMap`?
**A**:
- **`switchMap`**: Cancels the current in-flight inner Observable whenever a new outer emission arrives.
- **`mergeMap`**: Runs multiple inner Observables concurrently without cancelling or waiting.
- **`concatMap`**: Runs inner Observables sequentially in order, waiting for each to complete before starting the next.

### Q: What is the difference between a `Subject` and a `BehaviorSubject`?
**A**: A `Subject` does not store an initial or current value; new subscribers only receive values emitted after the moment of subscription. A `BehaviorSubject` requires an initial value, always holds a current state value (retrievable via `.getValue()`), and immediately emits that current value to any new subscriber.

## Summary
RxJS provides a powerful toolkit for managing complex asynchronous events and data flows in Angular. By utilizing pipeable operators, flattening strategies, and automated subscription management, developers can build robust, reactive web applications.

---

Previous : [HttpClient and API Integration](./16_HttpClient_and_API_Integration.md) | Index : [Home](./00_index.md) | Next : [State Management](./18_State_Management.md)
