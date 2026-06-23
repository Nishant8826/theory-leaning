# State Management

## What is it?
State Management ek software architectural pattern hai jiska use application data, user preferences, aur API responses ko pure app ke components aur routes me synchronized aur organize rakhne ke liye kiya jata hai. Yeh state ke liye a single source of truth provide karta hai.

## Why do we need it?
Jaise-jaise web application ka size badhta hai, alag-alag components ke beech data sync karna complex ho jata hai. Iske bina developers nested component chains (prop drilling) build karne lagte hain, jisse state flow track karna mushkil ho jata hai. State management systems data ko UI code se alag karke ek centralized store me rakhti hain jahan se koi bhi component directly data read ya update kar sakta hai.

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
1. **Local State**: Kisi single component tak limited data status (jaise dynamic visibility flags), jo writable signals ya variables ke through manage hota hai.
2. **Service State**: Singleton service me stored state data, jo dynamic values ko BehaviorSubjects ya signals ke through share karta hai.
3. **NgRx Store (Redux)**: Redux structural rules par based enterprise store system:
   - **Actions**: Application events jo state modification trigger karte hain (jaise `[Cart] Add Item`).
   - **Reducers**: Pure functions jo actions ko evaluate karke state ki new immutable copy return karte hain.
   - **Selectors**: Central store state se specific slices (filter data) read karne ke functions.
   - **Effects**: Background async operations (jaise network API requests triggers aur actions dispatch) handle karne wale classes/functions.
4. **NgRx Signal Store**: Angular dynamic Signals framework variables par based dynamic, modular lightweight state system.

## Impact
* **Application Architecture**: State logic aur business transitions ko templates aur visual markup code se fully decouple karta hai.
* **Performance**: Memoized selectors aur state caching ke through component check loop optimize rehta hai.
* **Maintainability**: Application state updates transition flow history predictable aur debugging me trace karna aasan ho jata hai.

## Real World Example
Jaise dynamic document editor application me application store metadata, details list, aur undo history ko manage karta hai. Jab user kisi object shape ke slide coordinates badalta hai, tab state update action dispatch hota hai aur sidebar metrics panels instantly update ho jate hain.

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

## Code Examples
Neeche **NgRx Signal Store** API use karne wale modern store model aur component implementation example coordinate setup diya gaya hai:

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
  
  withComputed(({ todos }) => ({
    completedCount: computed(() => todos().filter(t => t.completed).length),
    pendingCount: computed(() => todos().filter(t => !t.completed).length)
  })),

  withMethods((store, http = inject(HttpClient)) => ({
    addTodo(title: string) {
      const newTodo: Todo = { id: Date.now(), title, completed: false };
      patchState(store, (state) => ({ todos: [...state.todos, newTodo] }));
    },

    toggleTodo(id: number) {
      patchState(store, (state) => ({
        todos: state.todos.map(t => t.id === id ? { ...t, completed: !t.completed } : t)
      }));
    },

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
  readonly store = inject(TodoStore);

  ngOnInit() {
    this.store.loadTodos();
  }

  addNew() {
    this.store.addTodo('Learn NgRx Signal Store APIs');
  }
}
```

## Best Practices
1. **Choose the Right Tool**: Chote aur simple projects ke liye heavy state library (jaise classic NgRx) ka use na karein. Singleton services aur signals se state clean format me manage ho jati hai.
2. **Keep State Immutable**: State objects ko directly mutate na karein. Humesha state updates ke liye spread operator (`...`) ka use karke new references return karein.
3. **Use Selectors for Complex Queries**: Complex data processing aur calculation steps ke liye store me selectors write karein taaki UI layers clean and formatted data read kar saken.

## Common Mistakes
* **Duplicate State**: Same state ko local component aur global store dono me update aur synchronize karna, jisse desynchronization errors ho sakte hain.
* **Overusing global stores**: Local UI elements states (jaise toggles ya modal visibility) ko global store me push karna. Aisi values ko components ke local scopes me hi handle karein.

## Interview Questions & Answers
### Q: What is the Redux pattern and how does NgRx implement it?
**A**: Redux global single store aur unidirectional data flow par work karta hai. NgRx ise standard components me actions (events), reducers (state update logic), aur selectors (queries) ke zariye integrate karta hai.

### Q: What is the difference between classic NgRx and the NgRx Signal Store?
**A**: Classic NgRx RxJS Observables par based hai jisme state read karne aur actions dispatch karne ke liye bohot saara boilerplate code (Actions, Reducers, Selectors, Effects) likhna padta hai.

## Summary
State management system application ke complex data flows ko unidirectional, single source of truth ke zariye handle karta hai. Yeh state changes ko easily testable aur transparent banata hai.

---

Previous : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md) | Index : [Home](./00_index.md) | Next : [Authentication and Authorization](./19_Authentication_and_Authorization.md)
