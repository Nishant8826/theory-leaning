# Immer & Immutability in Redux

---

## 1. What

**Immutability** means **never changing existing data directly**. Instead of modifying an object, you create a **new copy** with the changes applied.

**Immer** is a library that RTK uses internally to let you write code that **looks like mutation** but actually produces a **new immutable state**. It's the magic that makes `createSlice` reducers so clean.

### The Magic:
```ts
// This LOOKS like mutation...
state.user.name = "Nishant";

// But Immer converts it to THIS under the hood:
return {
  ...state,
  user: {
    ...state.user,
    name: "Nishant",
  },
};
```

---

## 2. Why

### Why is Immutability Important in Redux?

**Reason 1: Change Detection**
React-Redux uses **reference equality** (`===`) to detect state changes:

```ts
// React-Redux internally does:
if (previousState === currentState) {
  // No re-render — same reference, nothing changed
} else {
  // Re-render! — new reference, something changed
}
```

If you mutate the existing state object directly, the reference stays the same, and **React won't know that something changed** — your UI won't update!

```ts
// ❌ BAD — Direct mutation (same reference)
state.count = 5;
// state === state → true → React thinks nothing changed → NO re-render! 😱

// ✅ GOOD — New object (new reference)
return { ...state, count: 5 };
// newState === state → false → React detects change → Re-renders! ✅
```

**Reason 2: Predictability**
Immutability ensures that functions don't have unexpected side effects:

```ts
// ❌ Mutating — Side effect! The original array is modified
function addItem(items: string[], newItem: string) {
  items.push(newItem); // Modifies the original array!
  return items;
}

// ✅ Immutable — Original array is untouched
function addItem(items: string[], newItem: string) {
  return [...items, newItem]; // New array, original intact
}
```

**Reason 3: Time-Travel Debugging**
Redux DevTools can show you every state snapshot because old states are never overwritten — they're preserved as immutable snapshots.

---

## 3. How

### How Immer Works Internally:

Immer uses a concept called **"structural sharing with proxies"**:

```
Step 1: Immer creates a PROXY (draft) of your state
Step 2: You modify the draft (which looks like mutation)
Step 3: Immer compares the draft to the original
Step 4: Immer creates a NEW object with ONLY the changed parts
Step 5: Unchanged parts are SHARED by reference (efficient!)
```

### Visual Example:

```
Original State:
{
  user: { name: "Nishant", age: 25 },  ← Object A
  settings: { theme: "dark" },          ← Object B
}

You modify: state.user.name = "John"

New State (produced by Immer):
{
  user: { name: "John", age: 25 },     ← New Object A' (changed)
  settings: { theme: "dark" },          ← SAME Object B (shared reference!)
}

// Only the changed path gets new objects
// Unchanged branches keep their references → efficient!
```

### Structural Sharing:
```
oldState.settings === newState.settings  // true! (shared reference)
oldState.user === newState.user          // false (new object because it changed)
oldState === newState                    // false (root changed)
```

This is why `useSelector` can efficiently detect changes — if a reference hasn't changed, that part of state hasn't changed.

---

## 4. Implementation

### Without Immer (Legacy Redux — The Painful Way):

```ts
interface AppState {
  users: {
    [id: string]: {
      name: string;
      profile: {
        bio: string;
        address: {
          city: string;
          country: string;
        };
        social: {
          twitter: string;
          github: string;
        };
      };
      posts: Array<{
        id: string;
        title: string;
        tags: string[];
      }>;
    };
  };
}

// ❌ Update a deeply nested field WITHOUT Immer
function updateCity(state: AppState, userId: string, newCity: string): AppState {
  return {
    ...state,
    users: {
      ...state.users,
      [userId]: {
        ...state.users[userId],
        profile: {
          ...state.users[userId].profile,
          address: {
            ...state.users[userId].profile.address,
            city: newCity, // 😩 Seven levels of spreading!
          },
        },
      },
    },
  };
}

// ❌ Add a tag to a specific post WITHOUT Immer
function addTag(
  state: AppState,
  userId: string,
  postId: string,
  tag: string
): AppState {
  return {
    ...state,
    users: {
      ...state.users,
      [userId]: {
        ...state.users[userId],
        posts: state.users[userId].posts.map((post) =>
          post.id === postId
            ? { ...post, tags: [...post.tags, tag] }
            : post
        ),
      },
    },
  };
}
```

### With Immer (RTK Way — The Clean Way):

```ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Same complex state, but updates are TRIVIAL:

const userSlice = createSlice({
  name: "users",
  initialState: {} as AppState,
  reducers: {
    // ✅ Update deeply nested field — ONE LINE!
    updateCity(
      state,
      action: PayloadAction<{ userId: string; city: string }>
    ) {
      state.users[action.payload.userId].profile.address.city =
        action.payload.city;
    },

    // ✅ Add tag to a post — SIMPLE!
    addTag(
      state,
      action: PayloadAction<{ userId: string; postId: string; tag: string }>
    ) {
      const { userId, postId, tag } = action.payload;
      const post = state.users[userId].posts.find((p) => p.id === postId);
      if (post) {
        post.tags.push(tag); // push is fine with Immer!
      }
    },

    // ✅ Remove a user — ONE LINE!
    removeUser(state, action: PayloadAction<string>) {
      delete state.users[action.payload];
    },

    // ✅ Sort posts — direct mutation!
    sortPosts(state, action: PayloadAction<string>) {
      state.users[action.payload].posts.sort((a, b) =>
        a.title.localeCompare(b.title)
      );
    },
  },
});
```

### Important Immer Rules:

```ts
const slice = createSlice({
  name: "example",
  initialState: { value: 0, items: [] as string[] },
  reducers: {
    // ✅ Rule 1: Either MUTATE the draft...
    mutate(state) {
      state.value = 42; // Mutate the draft, no return needed
    },

    // ✅ Rule 2: ...OR RETURN a new value (NOT both!)
    replace(state) {
      return { value: 42, items: [] }; // Return new state entirely
    },

    // ❌ WRONG: Don't do BOTH!
    wrong(state) {
      state.value = 42;
      return { value: 42, items: [] }; // ERROR! Can't mutate AND return!
    },

    // ✅ You CAN return undefined (Immer uses the mutated draft)
    mutateAndReturn(state) {
      state.value = 42;
      return undefined; // This is fine (Immer uses the draft)
    },

    // ✅ Array mutations work naturally
    pushItem(state, action: PayloadAction<string>) {
      state.items.push(action.payload);        // push
      state.items.splice(0, 1);                // splice
      state.items.unshift("first");            // unshift
      state.items.sort();                       // sort
      state.items.reverse();                   // reverse
      // All of these are safe with Immer!
    },
  },
});
```

### Using Immer Standalone (Outside Redux):

```ts
import { produce } from "immer";

interface State {
  user: { name: string; age: number };
  items: string[];
}

const originalState: State = {
  user: { name: "Nishant", age: 25 },
  items: ["apple", "banana"],
};

// produce(currentState, recipe) → newState
const newState = produce(originalState, (draft) => {
  draft.user.name = "John";
  draft.items.push("cherry");
});

console.log(originalState.user.name); // "Nishant" (unchanged!)
console.log(newState.user.name);      // "John" (new state)
console.log(originalState === newState); // false (different objects)
console.log(originalState.items === newState.items); // false (items changed)
```

---

## 5. React Integration

Immer works transparently inside Redux — you don't need to import it or configure anything. Just write reducers in `createSlice` and Immer handles immutability.

```tsx
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "./store";
import { updateCity } from "./userSlice";

function UserProfile() {
  const city = useSelector(
    (state: RootState) => state.users["1"]?.profile.address.city
  );
  const dispatch = useDispatch();

  return (
    <div>
      <p>City: {city}</p>
      <button
        onClick={() =>
          dispatch(updateCity({ userId: "1", city: "New Delhi" }))
        }
      >
        Move to Delhi
      </button>
    </div>
  );
}
```

---

## 6. Next.js Integration

No special configuration needed. Immer works the same in Next.js — it's a Redux internal detail.

---

## 7. Impact

### Performance Impact:
- **Structural sharing** means Immer is **memory efficient** — unchanged parts share references
- Immer has a small runtime overhead (~2-3x slower than manual spreading) but this is **negligible** for real apps
- The **developer productivity gains** far outweigh the tiny performance cost

### Common Gotchas:

```ts
// ❌ Gotcha 1: Don't reassign the entire state parameter
reducers: {
  reset(state) {
    state = initialState; // ❌ This reassigns the local variable, not the draft!
    return initialState;  // ✅ Return a new value instead
  }
}

// ❌ Gotcha 2: Don't use async in reducers
reducers: {
  async fetchData(state) { // ❌ Reducers MUST be synchronous
    const data = await fetch("/api/data"); // NEVER DO THIS
  }
}

// ❌ Gotcha 3: Immer only works with plain objects and arrays
// Maps, Sets, and class instances are NOT supported by default
```

---

## 8. Summary

- **Immutability** = never change existing data, always create new copies
- React-Redux uses **reference equality** (`===`) to detect changes — mutations break this
- **Immer** lets you write "mutating" code that produces immutable results
- Immer uses **JavaScript Proxies** to track changes and create new state
- **Structural sharing** = unchanged parts keep their references (efficient!)
- **Rule:** In RTK reducers, either MUTATE the draft OR RETURN a new value — never both
- Immer handles: objects, arrays, and all their methods (push, splice, sort, etc.)
- You don't need to install or configure Immer — RTK includes it automatically

---

**Prev:** [08_create_action_and_create_reducer.md](./08_create_action_and_create_reducer.md) | **Next:** [10_thunks.md](./10_thunks.md)
