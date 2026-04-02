# Async State Handling — Loading, Error, Success

---

## 1. What

Every async operation (API call) in your app goes through three stages:

| State | Meaning | UI Shows |
|-------|---------|----------|
| **Loading / Pending** | Request is in progress | Spinner, skeleton, "Loading..." |
| **Success / Fulfilled** | Request completed successfully | Data, success message |
| **Error / Rejected** | Request failed | Error message, retry button |

Managing these three states properly is **critical** for a good user experience.

---

## 2. Why

### Bad User Experience Without Proper State Handling:
```
❌ No loading state → User clicks button, nothing happens... are they confused? Yes.
❌ No error state → API fails silently, user sees blank screen forever.
❌ No success state → Data loads but no feedback to the user.
```

### Good User Experience With Proper State Handling:
```
✅ Loading → User sees a spinner → Knows something is happening
✅ Error → User sees error message + retry button → Knows what went wrong
✅ Success → Data appears smoothly → User is happy
```

---

## 3. How

### The Pattern:

Every async operation in Redux follows this pattern:

```ts
interface AsyncState<T> {
  data: T | null;       // The actual data
  loading: boolean;     // Is the request in progress?
  error: string | null; // Error message (if any)
}

// Transitions:
// IDLE:    { data: null,  loading: false, error: null  }
// LOADING: { data: null,  loading: true,  error: null  }
// SUCCESS: { data: [...], loading: false, error: null  }
// ERROR:   { data: null,  loading: false, error: "..." }
```

### State Machine Visualization:

```
            dispatch(fetchData())
  ┌─IDLE──────────────────────────▶ LOADING ─┐
  │                                    │      │
  │                    ┌───────────────┤      │
  │                    ▼               ▼      │
  │              FULFILLED         REJECTED   │
  │              (success)          (error)   │
  │                    │               │      │
  │                    └───────┬───────┘      │
  │                            │              │
  │                   dispatch(fetchData())   │
  │                            │              │
  └────────────────────────────┴──────────────┘
```

---

## 4. Implementation

### Approach 1: Simple Loading/Error/Success:

```ts
// features/products/productSlice.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

interface Product {
  id: number;
  title: string;
  price: number;
  description: string;
  image: string;
}

interface ProductState {
  products: Product[];
  loading: boolean;
  error: string | null;
}

const initialState: ProductState = {
  products: [],
  loading: false,
  error: null,
};

export const fetchProducts = createAsyncThunk(
  "products/fetchAll",
  async () => {
    const res = await fetch("https://fakestoreapi.com/products");
    if (!res.ok) throw new Error("Failed to fetch products");
    return (await res.json()) as Product[];
  }
);

const productSlice = createSlice({
  name: "products",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Something went wrong";
      });
  },
});

export default productSlice.reducer;
```

### Approach 2: Status Enum (More Explicit):

```ts
// Using an enum instead of separate boolean + string
type RequestStatus = "idle" | "loading" | "succeeded" | "failed";

interface ProductState {
  products: Product[];
  status: RequestStatus;
  error: string | null;
}

const initialState: ProductState = {
  products: [],
  status: "idle",
  error: null,
};

const productSlice = createSlice({
  name: "products",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message ?? "Failed";
      });
  },
});
```

### Approach 3: Multiple Async Operations in One Slice:

```ts
interface ProductState {
  // List of products
  products: Product[];
  productsLoading: boolean;
  productsError: string | null;

  // Single product detail
  selectedProduct: Product | null;
  selectedLoading: boolean;
  selectedError: string | null;

  // Create product status
  createLoading: boolean;
  createError: string | null;

  // Delete product status
  deleteLoading: boolean;
  deleteError: string | null;
}

export const fetchProducts = createAsyncThunk(
  "products/fetchAll",
  async () => {
    const res = await fetch("https://fakestoreapi.com/products");
    return res.json() as Promise<Product[]>;
  }
);

export const fetchProductById = createAsyncThunk(
  "products/fetchById",
  async (id: number) => {
    const res = await fetch(`https://fakestoreapi.com/products/${id}`);
    return res.json() as Promise<Product>;
  }
);

export const createProduct = createAsyncThunk(
  "products/create",
  async (product: Omit<Product, "id">, thunkAPI) => {
    const res = await fetch("https://fakestoreapi.com/products", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(product),
    });
    if (!res.ok) return thunkAPI.rejectWithValue("Failed to create product");
    return res.json() as Promise<Product>;
  }
);

export const deleteProduct = createAsyncThunk(
  "products/delete",
  async (id: number) => {
    await fetch(`https://fakestoreapi.com/products/${id}`, {
      method: "DELETE",
    });
    return id;
  }
);

const productSlice = createSlice({
  name: "products",
  initialState: {
    products: [],
    productsLoading: false,
    productsError: null,
    selectedProduct: null,
    selectedLoading: false,
    selectedError: null,
    createLoading: false,
    createError: null,
    deleteLoading: false,
    deleteError: null,
  } as ProductState,
  reducers: {
    clearErrors(state) {
      state.productsError = null;
      state.selectedError = null;
      state.createError = null;
      state.deleteError = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch all
      .addCase(fetchProducts.pending, (state) => {
        state.productsLoading = true;
        state.productsError = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.productsLoading = false;
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.productsLoading = false;
        state.productsError = action.error.message ?? "Failed";
      })

      // Fetch by ID
      .addCase(fetchProductById.pending, (state) => {
        state.selectedLoading = true;
        state.selectedError = null;
      })
      .addCase(fetchProductById.fulfilled, (state, action) => {
        state.selectedLoading = false;
        state.selectedProduct = action.payload;
      })
      .addCase(fetchProductById.rejected, (state, action) => {
        state.selectedLoading = false;
        state.selectedError = action.error.message ?? "Not found";
      })

      // Create
      .addCase(createProduct.pending, (state) => {
        state.createLoading = true;
        state.createError = null;
      })
      .addCase(createProduct.fulfilled, (state, action) => {
        state.createLoading = false;
        state.products.unshift(action.payload);
      })
      .addCase(createProduct.rejected, (state, action) => {
        state.createLoading = false;
        state.createError = action.error.message ?? "Create failed";
      })

      // Delete
      .addCase(deleteProduct.pending, (state) => {
        state.deleteLoading = true;
      })
      .addCase(deleteProduct.fulfilled, (state, action) => {
        state.deleteLoading = false;
        state.products = state.products.filter((p) => p.id !== action.payload);
      })
      .addCase(deleteProduct.rejected, (state, action) => {
        state.deleteLoading = false;
        state.deleteError = action.error.message ?? "Delete failed";
      });
  },
});

export const { clearErrors } = productSlice.actions;
export default productSlice.reducer;
```

### Approach 4: Generic Async State Helper:

```ts
// utils/asyncState.ts
// Reusable helper for consistent async state handling

interface AsyncState<T> {
  data: T;
  loading: boolean;
  error: string | null;
}

function createInitialAsyncState<T>(defaultData: T): AsyncState<T> {
  return {
    data: defaultData,
    loading: false,
    error: null,
  };
}

// Usage in a slice:
interface ProductState {
  list: AsyncState<Product[]>;
  detail: AsyncState<Product | null>;
}

const initialState: ProductState = {
  list: createInitialAsyncState<Product[]>([]),
  detail: createInitialAsyncState<Product | null>(null),
};
```

---

## 5. React Integration

### Complete UI with Loading/Error/Success:

```tsx
// components/ProductList.tsx
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "../store";
import {
  fetchProducts,
  deleteProduct,
  clearErrors,
} from "../features/products/productSlice";

function ProductList() {
  const {
    products,
    productsLoading,
    productsError,
    deleteLoading,
  } = useSelector((state: RootState) => state.products);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);

  // ─── LOADING STATE ───
  if (productsLoading) {
    return (
      <div className="loading-container">
        <div className="spinner" />
        <p>Loading products...</p>
      </div>
    );
  }

  // ─── ERROR STATE ───
  if (productsError) {
    return (
      <div className="error-container">
        <h2>⚠️ Something went wrong</h2>
        <p>{productsError}</p>
        <button onClick={() => dispatch(fetchProducts())}>🔄 Retry</button>
        <button onClick={() => dispatch(clearErrors())}>✖ Dismiss</button>
      </div>
    );
  }

  // ─── EMPTY STATE ───
  if (products.length === 0) {
    return (
      <div className="empty-container">
        <p>No products found.</p>
      </div>
    );
  }

  // ─── SUCCESS STATE ───
  return (
    <div>
      <h1>Products ({products.length})</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <img src={product.image} alt={product.title} width={50} />
            <h3>{product.title}</h3>
            <p>${product.price}</p>
            <button
              onClick={async () => {
                try {
                  await dispatch(deleteProduct(product.id)).unwrap();
                  alert("Deleted!");
                } catch {
                  alert("Failed to delete");
                }
              }}
              disabled={deleteLoading}
            >
              {deleteLoading ? "Deleting..." : "Delete"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductList;
```

### Reusable Async Wrapper Component:

```tsx
// components/AsyncWrapper.tsx
interface AsyncWrapperProps<T> {
  loading: boolean;
  error: string | null;
  data: T | null;
  onRetry?: () => void;
  children: (data: T) => React.ReactNode;
  loadingComponent?: React.ReactNode;
}

function AsyncWrapper<T>({
  loading,
  error,
  data,
  onRetry,
  children,
  loadingComponent,
}: AsyncWrapperProps<T>) {
  if (loading) {
    return loadingComponent ? <>{loadingComponent}</> : <p>Loading...</p>;
  }

  if (error) {
    return (
      <div>
        <p>Error: {error}</p>
        {onRetry && <button onClick={onRetry}>Retry</button>}
      </div>
    );
  }

  if (!data) return <p>No data available</p>;

  return <>{children(data)}</>;
}

// Usage:
function App() {
  const { products, productsLoading, productsError } = useSelector(
    (state: RootState) => state.products
  );
  const dispatch = useDispatch<AppDispatch>();

  return (
    <AsyncWrapper
      loading={productsLoading}
      error={productsError}
      data={products.length > 0 ? products : null}
      onRetry={() => dispatch(fetchProducts())}
    >
      {(products) => (
        <ul>
          {products.map((p) => (
            <li key={p.id}>{p.title}</li>
          ))}
        </ul>
      )}
    </AsyncWrapper>
  );
}
```

---

## 6. Next.js Integration

### App Router:
Same as React — use `"use client"` components with `useEffect` for data fetching.

### Pages Router with SSR:
Fetch data server-side to avoid showing loading states on initial render:

```tsx
// pages/products.tsx
import { GetServerSideProps } from "next";

export const getServerSideProps: GetServerSideProps = async () => {
  const res = await fetch("https://fakestoreapi.com/products");
  const products = await res.json();

  return {
    props: { products }, // Pre-rendered with data — no loading state needed!
  };
};
```

---

## 7. RTK Query Alternative

RTK Query handles ALL of this automatically:

```ts
const { data, isLoading, isError, error, refetch } = useGetProductsQuery();

// No manual loading/error/success states needed!
// No useEffect!
// No dispatch!
```

More details in the RTK Query chapters.

---

## 8. Impact

### Good Async State Handling = Professional Apps
- Users always know what's happening
- Errors are recoverable (retry buttons)
- Loading states prevent confusion
- Empty states guide users to take action

### Common Patterns:
- **Skeleton loaders** for initial loads
- **Inline spinners** for mutations (delete, update)
- **Toast notifications** for success/error feedback
- **Optimistic updates** for instant-feeling UIs

---

## 9. Summary

- Every async operation has three states: **loading**, **success**, **error**
- Handle all three in `extraReducers` with **pending/fulfilled/rejected**
- Use `.unwrap()` for component-level error handling
- Consider a **status enum** (`"idle" | "loading" | "succeeded" | "failed"`) for clarity
- Create **reusable patterns** (helper functions, wrapper components)
- Always provide **retry buttons** for error states
- RTK Query automates all of this — prefer it for data fetching
- For multiple operations in one slice, use separate loading/error fields

---

**Prev:** [11_create_async_thunk.md](./11_create_async_thunk.md) | **Next:** [13_provider.md](./13_provider.md)
