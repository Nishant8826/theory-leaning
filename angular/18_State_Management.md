# State Management

## What is it?
State Management is the architectural design pattern used to manage and synchronize user data, configuration flags, and API responses across different parts of an application. It provides a single source of truth for the application's state.

## Why do we need it?
As applications grow, sharing data between unrelated components can become difficult. Without a state management strategy, developers end up passing properties through multiple levels of nested components (prop drilling) or writing buggy event handlers. State management solutions decouple state from components, placing it in a central store that any component can read from or write to.

```
Without Centralized State (Spaghetti Bindings):
Component A <──> Component B <──> Component C <──> Component D (Data changes get lost or de-synchronized)

With Centralized State (Single Source of Truth):
          ┌──────────────────────────────────┐
          │         Central Store            │
          │  (State, Reducers/Signal Store)  │
          └───────┬──────────────────▲───────┘
                  │                  │
    Reads state   │                  │ Dispatches Action
    (Selectors)   │                  │ (State Mutation)
                  ▼                  │
          ┌──────────────────────────┴───────┐
          │        Any Component UI          │
          └──────────────────────────────────┘
```

## How does it work?
1. **Local State**: State managed within a single component using Writable Signals or simple variables.
2. **Service State**: State managed within an injectable service using RxJS BehaviorSubjects or Signals.
3. **NgRx Store (Redux)**: A state management solution based on the Redux pattern:
   - **Actions**: Describe events that occur in the application.
   - **Reducers**: Functions that handle state changes. They accept the current state and an action, and return a new state object.
   - **Selectors**: Functions used to query specific slices of state from the store.
   - **Effects**: Handle side effects (like API requests) asynchronously outside components.
4. **NgRx Signal Store**: A lightweight, functional state management solution built on Angular's Signals API.

## Impact
* **Application Architecture**: Decouples UI layout code from state logic.
* **Performance**: Selectors and computed signals cache state queries, reducing change detection sweeps.
* **Maintainability**: Makes state changes predictable and easy to trace during debugging.

## Real World Example
In a collaborative design tool, the central store tracks the active project, user permissions, and undo/redo histories. When a user drags a canvas shape, the action updates the store, and all other components (like layer panels and coordinate bars) update their views.

## Syntax
* **NgRx Action**: `export const loadItems = createAction('[Catalog] Load Items');`
* **NgRx Reducer**:
```typescript
const itemReducer = createReducer(initialState, on(loadItemsSuccess, (state, { items }) => ({ ...state, items })));
```
* **Signal Store Definition**:
```typescript
export const TodoStore = signalStore(
  withState({ todos: [], loading: false }),
  withMethods((store) => ({ ... }))
);
```

## Hinglish Explanation

State Management ka matlab hai **"App ke dynamic data (state) ko ek single organized tareeke se update karna"**. Jaise ek shopping cart items list, login status ya dark/light theme options. Agar data control me na ho, toh components aapas me synchronization loss kar dete hain.

### 1. State Management ke teen levels:
* **Local State:** Jab data sirf ek hi page/component ke andar use ho (jaise accordion ka open/close boolean value).
* **Service-based State:** Jab dynamic data kuch components me shared ho. Iske liye hum ek singleton service me active signal ya BehaviorSubject use karte hain.
* **Global State (NgRx):** Jab application bohot complex ho aur saara global state (cart items, payment configuration, user session) centralized manage karna ho.

### 2. Immutability ka Niyam (State ko directly edit na karein)
* State management me data directly modify nahi kiya jata.
* **Bad Practice:** `myState.items.push(newItem)`
* **Good Practice:** `myState.items = [...myState.items, newItem]` (Purane items ko copy karke new item attach karke naya array assign karna).

### 3. Classic NgRx vs Modern Signal Store
* **Classic NgRx:** RxJS streams par run hota hai. Isme Actions, Reducers, aur Selectors ka set banaya jata hai jo complex updates me useful hai par boilerplate code badha deta hai.
* **NgRx Signal Store:** Angular v16+ signals par base hai. Yeh functional syntax use karta hai jisse code bohot short, readable aur execute karne me dynamic lagta hai.

## Code Examples
Below is an implementation of a modern state manager using the **NgRx Signal Store** API.

### `todo.store.ts` (Functional Signal Store)
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
  // 1. Initialize State
  withState(initialState),
  
  // 2. Define Computed Properties
  withComputed(({ todos }) => ({
    completedCount: computed(() => todos().filter(t => t.completed).length),
    pendingCount: computed(() => todos().filter(t => !t.completed).length)
  })),

  // 3. Define Methods to Update State and Run Side Effects
  withMethods((store, http = inject(HttpClient)) => ({
    // Update local state directly
    addTodo(title: string) {
      const newTodo: Todo = { id: Date.now(), title, completed: false };
      patchState(store, (state) => ({ todos: [...state.todos, newTodo] }));
    },

    toggleTodo(id: number) {
      patchState(store, (state) => ({
        todos: state.todos.map(t => t.id === id ? { ...t, completed: !t.completed } : t)
      }));
    },

    // Side Effect: Fetch data using RxJS switchMap
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

### `todo-list.component.ts` (Component consuming Signal Store)
```typescript
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TodoStore } from './todo.store';

@Component({
  selector: 'app-todo-list',
  standalone: true,
  imports: [CommonModule],
  // Inject the Store directly as a provider
  providers: [TodoStore],
  template: `
    <div class="todo-widget">
      <h3>Signal Store Todos</h3>
      <p>Completed Tasks: {{ store.completedCount() }} / {{ store.todos().length }}</p>

      <div *ngIf="store.loading()">Loading items...</div>

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
    .todo-widget { border: 1px solid #7c3aed; padding: 20px; border-radius: 8px; max-width: 400px; }
    .done { text-decoration: line-through; color: #9ca3af; }
    li { cursor: pointer; padding: 4px 0; }
  `]
})
export class TodoListComponent implements OnInit {
  // Inject the functional Signal Store
  readonly store = inject(TodoStore);

  ngOnInit() {
    this.store.loadTodos(); // Load initial data
  }

  addNew() {
    this.store.addTodo('Learn NgRx Signal Store APIs');
  }
}
```
## Best Practices
1. **Choose the Right Tool**: Do not use full NgRx setups for simple applications. Use a shared service with signals for light state, and reserves NgRx for large enterprise apps.
2. **Keep State Immutable**: Never mutate state values directly (e.g. `state.todos.push(item)`). Always return updated copies of state objects using the spread operator (`[...todos, item]`).
3. **Use Selectors for Complex Queries**: When using classic NgRx, use selectors to filter, combine, or format slices of state before displaying them in components.

## Common Mistakes
* **Duplicate State**: Storing the same data in multiple places (like caching an API response in both a service and a component), which can cause synchronization bugs.
* **Overusing global stores**: Storing local UI state (like dropdown open states or modal visibility flags) in the global store. Keep local UI state in the component itself.

## Interview Questions & Answers
### Q: What is the Redux pattern and how does NgRx implement it?
**A**: The Redux pattern uses a single, centralized store to manage application state. State mutations are described by dispatching immutable Actions, which are handled by Reducers to return a new state. Asynchronous side effects are managed outside components by Effects. NgRx implements this pattern using RxJS streams and Angular services.
* **Hinglish Explanation**: Redux pattern poore app ke data ko ek single, centralized storage (Store) me rakhne ka rule hai. Isme state ko directly change nahi kiya ja sakta. State me changes karne ke liye ek description object (Action) bheja (dispatch kiya) jata hai. Phir Reducers (pure functions) us action aur old state ko lekar ek brand-new state design karte hain. Aur async operations (jaise API call) ko components se dur rakhne ke liye Effects use kiye jate hain. NgRx isi rule ko RxJS streams ke sath Angular me use karta hai.

### Q: What is the difference between classic NgRx and the NgRx Signal Store?
**A**: Classic NgRx uses RxJS Observables, Actions, Reducers, and Selectors, which can require a lot of boilerplate. The NgRx Signal Store is functional and relies on Angular's Signals API, providing a lightweight, reactive way to manage state with less boilerplate.
* **Hinglish Explanation**: Classic NgRx RxJS Observables par based hai jisme state read karne aur actions dispatch karne ke liye bohot saara boilerplate code (Actions, Reducers, Selectors, Effects) likhna padta hai. Jabki NgRx Signal Store modern, functional aur lightweight hai jo Angular Signals API ka use karta hai. Isme Observables ko subscribe karne ki zaroorat nahi padti aur simple functions ke zariye bina kisi extra boilerplate ke state handle ho jati hai.

## Summary
State management provides a single source of truth for your application. Using local state, service state, or global libraries like NgRx Store and Signal Store decouples UI components from data logic, keeping state changes predictable.

---

Previous : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md) | Index : [Home](./00_index.md) | Next : [Authentication and Authorization](./19_Authentication_and_Authorization.md)
