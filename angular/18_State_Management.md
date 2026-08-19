# State Management

## What is it?
State Management is an architectural pattern used to store, synchronize, and update application data, user sessions, preferences, and server responses across multiple components and routes. It provides a predictable **Single Source of Truth** for application state.

## Why do we need it?
As web applications scale in size and complexity, sharing and synchronizing state across deeply nested or unrelated components becomes error-prone. Without a structured state pattern, developers often resort to "prop drilling" (passing data through multiple component layers) or fragile event emitters, leading to race conditions and desynchronized UIs. 

State management isolates state from UI components into a centralized store, providing predictable, unidirectional data flow and effortless state inspection.

```
Without Centralized State (Spaghetti State):
Component A <──> Component B <──> Component C <──> Component D (State mutations become untraceable)

With Centralized State (Single Source of Truth):
          ┌──────────────────────────────────┐
          │         Central Store            │
          │  (State, Reducers/Signal Store)  │
          └───────┬──────────────────▲───────┘
                  │                  │
    Reads State   │                  │ Dispatches Action / Calls Method
    (Selectors)   │                  │ (Immutable State Mutation)
                  ▼                  │
          ┌──────────────────────────┴───────┐
          │        Any Component UI          │
          └──────────────────────────────────┘
```

## How does it work?
1. **Local State**: Component-specific UI state (e.g., dropdown open/closed status), managed via Writable Signals or component properties.
2. **Service-Based State**: Shared state managed inside an `@Injectable({ providedIn: 'root' })` singleton service using Signals or `BehaviorSubject` streams.
3. **NgRx Global Store (Redux Pattern)**: An enterprise-grade reactive store enforcing strict unidirectional flow:
   - **Actions**: Plain objects describing unique events dispatched by components (e.g., `[Cart] Add Item`).
   - **Reducers**: Pure functions that take the current state and an Action, returning a brand-new immutable state copy.
   - **Selectors**: Pure, memoized query functions that extract and compute specific slices of state.
   - **Effects**: Classes/functions that listen for specific actions, perform asynchronous side effects (such as HTTP calls), and dispatch new result actions.
4. **NgRx Signal Store**: A modern, lightweight, and modular state management library built on Angular Signals, offering reactive state with minimal boilerplate.

## Impact
* **Application Architecture**: Strictly separates business logic, caching, and state transitions from template rendering and user interactions.
* **Performance**: Memoized selectors and fine-grained Signal subscriptions update only the specific UI elements that depend on modified state slices.
* **Maintainability**: Makes state transitions deterministic, trackable with time-travel debugging tools (Redux DevTools), and easy to unit test.

## Real World Example
In a collaborative cloud document editor:
- The central store maintains the active document metadata, canvas elements, and undo/redo history stacks.
- When an engineer resizes an element on canvas, an action is dispatched to the store.
- The canvas, right-hand properties sidebar, and revision history panel all update instantaneously via selectors.

## Syntax
* **NgRx Action**: `export const loadItems = createAction('[Catalog] Load Items');`
* **NgRx Reducer**:
```typescript
const itemReducer = createReducer(
  initialState, 
  on(loadItemsSuccess, (state, { items }) => ({ ...state, items }))
);
```
* **NgRx Signal Store Definition**:
```typescript
export const TodoStore = signalStore(
  withState({ todos: [], loading: false }),
  withMethods((store) => ({ ... }))
);
```

## Code Examples
Below is a complete implementation of a modern state management solution using **NgRx Signal Store**:

### `todo.store.ts`
```typescript
import { signalStore, withState, withMethods, patchState, withComputed } from '@ngrx/signals';
import { computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { pipe, switchMap, tap, catchError, of } from 'rxjs';

export interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

export interface TodoState {
  todos: Todo[];
  loading: boolean;
  error: string | null;
}

const initialState: TodoState = {
  todos: [],
  loading: false,
  error: null
};

export const TodoStore = signalStore(
  { providedIn: 'root' },
  withState(initialState),
  
  // Computed Signals derived from store state
  withComputed(({ todos }) => ({
    completedCount: computed(() => todos().filter(t => t.completed).length),
    pendingCount: computed(() => todos().filter(t => !t.completed).length)
  })),

  // Methods and Async Effects
  withMethods((store, http = inject(HttpClient)) => ({
    addTodo(title: string): void {
      const newTodo: Todo = { id: Date.now(), title, completed: false };
      patchState(store, (state) => ({ todos: [...state.todos, newTodo] }));
    },

    toggleTodo(id: number): void {
      patchState(store, (state) => ({
        todos: state.todos.map(t => t.id === id ? { ...t, completed: !t.completed } : t)
      }));
    },

    // Reactive method for asynchronous API integration
    loadTodos: rxMethod<void>(
      pipe(
        tap(() => patchState(store, { loading: true })),
        switchMap(() => {
          return http.get<Todo[]>('https://jsonplaceholder.typicode.com/todos?_limit=5').pipe(
            tap((todos) => patchState(store, { todos, loading: false })),
            catchError((err) => {
              patchState(store, { error: err.message, loading: false });
              return of([]);
            })
          );
        })
      )
    )
  }))
);
```

### `todo-list.component.ts`
```typescript
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TodoStore } from './todo.store';

@Component({
  selector: 'app-todo-list',
  standalone: true,
  imports: [CommonModule],
  providers: [TodoStore],
  template: `
    <div class="todo-widget">
      <h3>Signal Store Todos</h3>
      <p>Tasks Completed: {{ store.completedCount() }} / {{ store.todos().length }}</p>

      <div *ngIf="store.loading()" class="loading">Loading tasks from API...</div>
      <div *ngIf="store.error()" class="error">Error: {{ store.error() }}</div>

      <ul>
        <li 
          *ngFor="let item of store.todos()" 
          (click)="store.toggleTodo(item.id)"
          [class.done]="item.completed">
          {{ item.title }}
        </li>
      </ul>

      <button (click)="addNew()">Add Custom Task</button>
    </div>
  `,
  styles: [`
    .todo-widget { border: 1px solid #7c3aed; padding: 20px; border-radius: 8px; max-width: 400px; font-family: sans-serif; }
    .done { text-decoration: line-through; color: #9ca3af; }
    li { cursor: pointer; padding: 6px 0; border-bottom: 1px solid #f3f4f6; }
    .loading { color: #6d28d9; font-style: italic; margin: 8px 0; }
    .error { color: #dc2626; font-size: 13px; }
    button { margin-top: 12px; padding: 8px 14px; background: #7c3aed; color: white; border: none; border-radius: 4px; cursor: pointer; }
  `]
})
export class TodoListComponent implements OnInit {
  readonly store = inject(TodoStore);

  ngOnInit(): void {
    this.store.loadTodos();
  }

  addNew(): void {
    this.store.addTodo('Master NgRx Signal Store Patterns');
  }
}
```

## Best Practices
1. **Choose the Right State Level**: Do not introduce a heavy global store for simple applications. For small-to-medium apps, an Injectable Singleton Service with Signals is often sufficient. Use NgRx Store or Signal Store for complex enterprise apps with extensive cross-feature state.
2. **Always Keep State Immutable**: Never mutate state objects directly (e.g., `state.todos.push(item)`). Always use `patchState` or the object spread operator (`...`) to create and emit new state references.
3. **Use Memoized Selectors / Computed Signals**: Perform data transformations, filtering, and sorting inside selectors or `withComputed` blocks rather than recalculating values inside component templates.

## Common Mistakes
* **Duplicate State**: Storing duplicate copies of the same data in both local component state and the global store, leading to state synchronization bugs.
* **Over-Storing Ephemeral UI State**: Storing transient UI state (such as modal visibility or button hover states) in the global store. Ephemeral UI state should always stay local to the component.

## Interview Questions & Answers
### Q: What is the Redux pattern and how does NgRx implement it?
**A**: The Redux pattern enforces a single global store, read-only state, and state changes via pure functions. NgRx implements this through **Actions** (describing what happened), **Reducers** (pure functions returning new state), **Selectors** (memoized queries to read slices of state), and **Effects** (handling asynchronous side effects like HTTP calls).

### Q: What is the difference between Classic NgRx Store and the NgRx Signal Store?
**A**: Classic NgRx Store relies heavily on RxJS Observables and requires substantial boilerplate code across separate files (actions, reducers, effects, selectors). The **NgRx Signal Store** is built natively on Angular Signals, offering a functional, highly modular API with seamless TypeScript type inference and significantly less boilerplate while remaining fully composable.

## Summary
State management establishes a predictable, single source of truth for application state. By leveraging modern approaches like the NgRx Signal Store or service-based Signals, developers can manage complex data flows, caching, and reactivity across large enterprise codebases cleanly and efficiently.

---

Previous : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md) | Index : [Home](./00_index.md) | Next : [Authentication and Authorization](./19_Authentication_and_Authorization.md)
