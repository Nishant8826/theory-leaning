# State Management

## What is it?
State Management ek software architectural pattern hai jiska use application ke users data, configurations flags, aur API response coordinates ko different routes/components me synchronized aur organize rakhne ke liye kiya jata hai. Yeh application ke state ke liye single source of truth (ek hi reliable repository) provide karta hai.

## Why do we need it?
Jaise-jaise web application ka size badhta hai, alag-alag components ke beech data sync coordinate karna mushkil ho jata hai. State management ke bina developers properties values levels bypass karke nested component chains (prop drilling) build karne lagte hain, jiski wajah se state synchronizations control se bahar ho jati hain. State management systems data ko UI layout code se alag (decouple) karke ek centralized store parameters storage me locate karte hain jahan koi bhi component data read/write commands execute kar sakta hai.

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
1. **Local State**: Single component boundary ke andar limit data, jo writable signals ya basic classes variables ke through manage kiya jata hai.
2. **Service State**: Singleton helper service parameters me store data, jo dynamic values BehaviorSubjects ya reactive signals se communicate hota hai.
3. **NgRx Store (Redux)**: Redux structural rules par based enterprise store system:
   - **Actions**: App events logs coordinate karte hain (jaise `[Cart] Add Item`).
   - **Reducers**: Pure functions jo action dynamic triggers analyze karke state variables ki absolute new copies returns karte hain.
   - **Selectors**: Central state parameters se custom filter data slice fetch karne wale functions.
   - **Effects**: Asynchronous background operations handles variables (jaise network API call actions dispatch).
4. **NgRx Signal Store**: Angular dynamic Signals framework variables par based dynamic, modular lightweight state system.

## Impact
* **Application Architecture**: Data state rules and actions logic codes ko visual HTML display codes se complete isolate rakhta hai.
* **Performance**: State cache calculations and filters mechanisms parameters unnecessary components checking loops optimize rakhte hain.
* **Maintainability**: Web updates values transitions predictable aur log check parameters me easily traceable ho jati hain.

## Real World Example
Dynamic document editor application portal me, store system project metadata, details list, undo history track parameters manage karta hai. Jab user shape element slide coordinates manipulate karta hai, updates action dispatch hokar store changes refresh karta hai aur sidebar metrics panels values instantly update ho jati hain.

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
1. **Choose the Right Tool**: Simple projects ke liye heavy state engines (NgRx) install na karein. Singleton services variables setup and signals direct use dynamic parameters scale solve kar dete hain.
2. **Keep State Immutable**: State values ko directly modify (`state.value = 5`) na karein. Humesha destructured array copy parameters tools spread operator (`[...items, newItem]`) use kar reference return update settings target karein.
3. **Use Selectors for Complex Queries**: Classic NgRx flow use case validations configurations details setups checks me hamesha filters selector functions design karein taaki views clean variables read karein.

## Common Mistakes
* **Duplicate State**: Same details profiles variables different files (jaise local components variables and global services cache variables) me separately store aur updates logic likhna, jo data maps desynchronization bug alerts create kar sakta hai.
* **Overusing global stores**: UI structural indicators (jaise modal visible status popup active settings flags) global centralized store data settings me push coordinate settings apply karna. In properties coordinates checks local views component scopes me hi handle rakhein.

## Interview Questions & Answers
### Q: What is the Redux pattern and how does NgRx implement it?
**A**: Redux data operations predictability maintain karne ke liye global store structures parameters use karta hai jahan actions reducers side-effects filters systems coordination details setups execute parameters enforce check rules run hote hain.

### Q: What is the difference between classic NgRx and the NgRx Signal Store?
**A**: Classic NgRx RxJS Observables par based hai jisme state read karne aur actions dispatch karne ke liye bohot saara boilerplate code (Actions, Reducers, Selectors, Effects) likhna padta hai.

## Summary
State management applications components logic aur shared data sets centralized predictability provide karta hai. Central structures coordinate stores dynamic actions controllers rules systems web application integrity safe rakhne me leverage karte hain.

---

Previous : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md) | Index : [Home](./00_index.md) | Next : [Authentication and Authorization](./19_Authentication_and_Authorization.md)
