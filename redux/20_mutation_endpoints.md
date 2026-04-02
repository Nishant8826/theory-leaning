# Mutation Endpoints — Writing Data

---

## 1. What

A **mutation endpoint** in RTK Query handles **data modification** operations — creating, updating, and deleting data (POST, PUT, PATCH, DELETE requests).

```ts
// Define a mutation
createUser: builder.mutation<User, NewUser>({
  query: (newUser) => ({
    url: "/users",
    method: "POST",
    body: newUser,
  }),
})

// Use the auto-generated hook
const [createUser, { isLoading, isSuccess, isError }] = useCreateUserMutation();
```

### Key Difference from Queries:
- **Queries** → auto-execute when the component mounts
- **Mutations** → only execute when you **explicitly call** the trigger function

---

## 2. Why

Mutations handle every "write" operation to your API:
- **Create** a new resource (POST)
- **Update** an existing resource (PUT/PATCH)
- **Delete** a resource (DELETE)
- **Any** non-idempotent operation

They also **integrate with cache invalidation** — after a mutation, related queries can automatically refetch.

---

## 3. How

### Mutation Hook Structure:

```ts
const [triggerFunction, result] = useSomeMutation();

// triggerFunction: Call this to execute the mutation
// result: Contains the state of the mutation

// result contains:
result.isLoading      // Is the mutation in progress?
result.isSuccess      // Did it succeed?
result.isError        // Did it fail?
result.error          // Error details
result.data           // Response data
result.reset          // Function to reset the mutation state
result.isUninitialized // Before first trigger
```

---

## 4. Implementation

### Defining Mutations:

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
}

interface CreateUserRequest {
  name: string;
  email: string;
  role: "admin" | "user";
}

interface UpdateUserRequest {
  id: number;
  name?: string;
  email?: string;
  role?: "admin" | "user";
}

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "https://api.example.com" }),
  tagTypes: ["User"],
  endpoints: (builder) => ({
    // GET users
    getUsers: builder.query<User[], void>({
      query: () => "/users",
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "User" as const, id })),
              { type: "User", id: "LIST" },
            ]
          : [{ type: "User", id: "LIST" }],
    }),

    // ── POST — Create user ──
    createUser: builder.mutation<User, CreateUserRequest>({
      query: (newUser) => ({
        url: "/users",
        method: "POST",
        body: newUser, // Automatically serialized to JSON
      }),
      // After creating a user, refetch the user list
      invalidatesTags: [{ type: "User", id: "LIST" }],
    }),

    // ── PUT — Full update ──
    replaceUser: builder.mutation<User, User>({
      query: (user) => ({
        url: `/users/${user.id}`,
        method: "PUT",
        body: user,
      }),
      invalidatesTags: (result, error, user) => [
        { type: "User", id: user.id },
        { type: "User", id: "LIST" },
      ],
    }),

    // ── PATCH — Partial update ──
    updateUser: builder.mutation<User, UpdateUserRequest>({
      query: ({ id, ...patch }) => ({
        url: `/users/${id}`,
        method: "PATCH",
        body: patch,
      }),
      invalidatesTags: (result, error, { id }) => [
        { type: "User", id },
        { type: "User", id: "LIST" },
      ],
    }),

    // ── DELETE — Remove user ──
    deleteUser: builder.mutation<{ success: boolean }, number>({
      query: (userId) => ({
        url: `/users/${userId}`,
        method: "DELETE",
      }),
      invalidatesTags: (result, error, userId) => [
        { type: "User", id: userId },
        { type: "User", id: "LIST" },
      ],
    }),

    // ── Custom mutation with headers ──
    uploadAvatar: builder.mutation<{ url: string }, { userId: number; file: FormData }>({
      query: ({ userId, file }) => ({
        url: `/users/${userId}/avatar`,
        method: "POST",
        body: file,
        // Don't set Content-Type — browser sets it with boundary for FormData
        formData: true,
      }),
      invalidatesTags: (result, error, { userId }) => [
        { type: "User", id: userId },
      ],
    }),
  }),
});

export const {
  useGetUsersQuery,
  useCreateUserMutation,
  useReplaceUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
  useUploadAvatarMutation,
} = apiSlice;
```

---

## 5. React Integration

### Using Mutations in Components:

```tsx
// components/CreateUserForm.tsx
import { useState, FormEvent } from "react";
import { useCreateUserMutation } from "../features/api/apiSlice";

function CreateUserForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  // Destructure the mutation hook
  const [createUser, { isLoading, isSuccess, isError, error, reset }] =
    useCreateUserMutation();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    try {
      // Call the trigger function with .unwrap()
      const newUser = await createUser({
        name,
        email,
        role: "user",
      }).unwrap();

      console.log("Created user:", newUser);
      setName("");
      setEmail("");
    } catch (err) {
      console.error("Failed to create user:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
        required
      />
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        type="email"
        required
      />

      <button type="submit" disabled={isLoading}>
        {isLoading ? "Creating..." : "Create User"}
      </button>

      {isSuccess && <p style={{ color: "green" }}>✅ User created!</p>}
      {isError && (
        <div>
          <p style={{ color: "red" }}>❌ Failed to create user</p>
          <button type="button" onClick={reset}>
            Dismiss
          </button>
        </div>
      )}
    </form>
  );
}
```

### Delete with Confirmation:

```tsx
function UserRow({ user }: { user: User }) {
  const [deleteUser, { isLoading: isDeleting }] = useDeleteUserMutation();

  const handleDelete = async () => {
    if (!confirm(`Delete ${user.name}?`)) return;

    try {
      await deleteUser(user.id).unwrap();
      // No need to manually update the list —
      // invalidatesTags triggers automatic refetch!
    } catch (err) {
      alert("Failed to delete user");
    }
  };

  return (
    <tr>
      <td>{user.name}</td>
      <td>{user.email}</td>
      <td>
        <button onClick={handleDelete} disabled={isDeleting}>
          {isDeleting ? "Deleting..." : "Delete"}
        </button>
      </td>
    </tr>
  );
}
```

### Inline Edit with Update:

```tsx
function EditableUser({ user }: { user: User }) {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(user.name);
  const [updateUser, { isLoading }] = useUpdateUserMutation();

  const handleSave = async () => {
    try {
      await updateUser({ id: user.id, name }).unwrap();
      setIsEditing(false);
    } catch {
      alert("Update failed");
    }
  };

  if (isEditing) {
    return (
      <div>
        <input value={name} onChange={(e) => setName(e.target.value)} />
        <button onClick={handleSave} disabled={isLoading}>
          {isLoading ? "Saving..." : "Save"}
        </button>
        <button onClick={() => setIsEditing(false)}>Cancel</button>
      </div>
    );
  }

  return (
    <div>
      <span>{user.name}</span>
      <button onClick={() => setIsEditing(true)}>Edit</button>
    </div>
  );
}
```

### File Upload:

```tsx
function AvatarUpload({ userId }: { userId: number }) {
  const [uploadAvatar, { isLoading, isSuccess }] = useUploadAvatarMutation();

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("avatar", file);

    try {
      const result = await uploadAvatar({ userId, file: formData }).unwrap();
      console.log("Uploaded:", result.url);
    } catch {
      alert("Upload failed");
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {isLoading && <p>Uploading...</p>}
      {isSuccess && <p>✅ Uploaded!</p>}
    </div>
  );
}
```

---

## 6. Next.js Integration

Works identically to React — mutations are client-side operations:

```tsx
// app/users/new/page.tsx
"use client";

import { useCreateUserMutation } from "@/lib/features/api/apiSlice";
import { useRouter } from "next/navigation";

export default function NewUserPage() {
  const [createUser, { isLoading }] = useCreateUserMutation();
  const router = useRouter();

  const handleSubmit = async (formData: FormData) => {
    try {
      await createUser({
        name: formData.get("name") as string,
        email: formData.get("email") as string,
        role: "user",
      }).unwrap();
      router.push("/users");
    } catch {
      alert("Failed");
    }
  };

  return (
    <form action={handleSubmit}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit" disabled={isLoading}>
        {isLoading ? "Creating..." : "Create"}
      </button>
    </form>
  );
}
```

---

## 7. Impact

### Mutations + Cache Invalidation = Magic:
1. User creates a new user → `createUser` mutation fires
2. Mutation succeeds → `invalidatesTags: ["User"]` triggers
3. All queries that `providesTags: ["User"]` → **automatically refetch**
4. User list updates without any manual work!

### Best Practices:
- Always use `.unwrap()` for error handling in components
- Use `reset()` to clear mutation state after handling
- Use `invalidatesTags` for automatic cache updates
- Use `formData: true` for file uploads

---

## 8. Summary

- **Mutations** handle write operations (POST, PUT, PATCH, DELETE)
- Hook returns `[triggerFunction, resultObject]`
- Trigger returns a Promise — use `.unwrap()` for error handling
- `invalidatesTags` automatically refetches related queries
- `result.reset()` clears the mutation state
- Mutations don't auto-execute — you must call the trigger function
- File uploads work with `FormData` and `formData: true`
- Cache invalidation connects mutations to queries seamlessly

---

**Prev:** [19_query_endpoints.md](./19_query_endpoints.md) | **Next:** [21_auto_generated_hooks.md](./21_auto_generated_hooks.md)
