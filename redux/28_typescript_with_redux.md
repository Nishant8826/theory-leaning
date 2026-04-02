# TypeScript with Redux

---

## 1. What

Using TypeScript with Redux ensures that your state, actions, and API responses are strongly typed. It prevents runtime errors like undefined properties, incorrect action bodies, or trying to render data that doesn't exist on objects.

---

## 2. Why

Before Redux Toolkit and TypeScript, Redux was a notoriously buggy experience for large applications. You often misspelled an action type string, or dispatched an action with `{ pylaod: data }` instead of `{ payload: data }`.

TypeScript makes these mistakes impossible. 

RTK was designed specifically with TypeScript in mind, meaning type inference does 90% of the heavy lifting.

---

## 3. How

To effectively use TypeScript with Redux:
1. Define the interface for your State inside each Slice.
2. Infer `RootState` and `AppDispatch` directly from the `store` object.
3. Use the `PayloadAction<T>` generic provided by RTK to type your reducers.
4. Export pre-typed hooks (`useAppSelector`, `useAppDispatch`).

---

## 4. Implementation

### 1. Typing the State and Reducers

```ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// 1. Define the precise shape of the state
interface CounterState {
  count: number;
  lastUpdated: string | null;
}

const initialState: CounterState = {
  count: 0,
  lastUpdated: null,
};

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    // Basic reducer (no payload)
    increment(state) {
      state.count++;
    },
    // Reducer with payload. Notice PayloadAction<number>
    incrementByAmount(state, action: PayloadAction<number>) {
      state.count += action.payload;
    },
  },
});
```

### 2. Typing the Store

```ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: { counter: counterReducer },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// AppDispatch ensures any dispatched Thunks are properly typed!
export type AppDispatch = typeof store.dispatch;
```

### 3. Typing Async Thunks

```ts
import { createAsyncThunk } from '@reduxjs/toolkit';
import { RootState, AppDispatch } from './store';

// createAsyncThunk<Return Type, Argument Type, ThunkAPI Configuration>
export const fetchUser = createAsyncThunk<
  User, // Expected Return Type
  number, // Argument Type (userId)
  { state: RootState } // Optional thunkAPI config (for getState context)
>('users/fetch', async (userId, thunkAPI) => {
  const state = thunkAPI.getState(); // Now strongly typed!
  const response = await fetch(`/api/users/${userId}`);
  return (await response.json()) as User;
});
```

---

## 5. React Integration

By exporting typed hooks, your React components are fully aware of what lives inside your Redux Store.

```tsx
import { useAppSelector, useAppDispatch } from './hooks'; // from file 16

function Counter() {
  const count = useAppSelector((state) => state.counter.count); // VSCode autocompletes `.count`!
  const dispatch = useAppDispatch(); // VSCode prevents dispatching wrong action shapes!

  return <button onClick={() => dispatch(incrementByAmount(5))}> Add 5 </button>;
}
```

---

## 6. Next.js Integration

Behaves identically to generic React apps. The typing rules remain standard across platforms.

---

## 7. Impact

### Developer Experience (DX)
TypeScript makes Redux discoverable. Instead of checking a reducer file to see what data an object has, you type `state.` and let intellisense guide you.

### RTK Query Types
RTK Query handles types brilliantly:
`builder.query<ResponseDataType, ArgumentType>({...})`.
If an endpoint doesn't require an argument, use `void`. If it returns nothing, use `void`.

---

## 8. Summary

- `PayloadAction<T>` explicitly defines what data an action carries.
- Infer `RootState` from `ReturnType<typeof store.getState>`.
- Infer `AppDispatch` from `typeof store.dispatch`.
- Always generate and use typed custom hooks (`useAppSelector`, `useAppDispatch`).
- `createAsyncThunk` accepts three type arguments: `Return Type`, `Arg Type`, and optionally `Store Configuration`.

---

**Prev:** [27_architecture_and_best_practices.md](./27_architecture_and_best_practices.md) | **Next:** [29_nextjs_integration.md](./29_nextjs_integration.md)
