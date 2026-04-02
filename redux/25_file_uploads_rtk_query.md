# File Uploads with RTK Query

---

## 1. What

Uploading files (images, documents, PDFs) to an API requires handling binary data, specifically `FormData`. 
RTK Query can handle file uploads, but it requires a slightly different approach than typical JSON payloads.

---

## 2. Why

Standard requests stringify JavaScript objects into JSON format via `JSON.stringify()`.
If you pass a JavaScript `File` object to `JSON.stringify()`, it becomes an empty object `{}`.

To send a file to a server, we must send it as `multipart/form-data`, passing the native `FormData` object directly through the HTTP request.

---

## 3. How

To upload files via RTK Query:
1. Define your mutation payload to accept `FormData`.
2. Ensure you **do not manually set the `Content-Type` header**. The browser will automatically set `Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...` when it detects a `FormData` payload.
3. If necessary, you can set `formData: true` in newer versions of RTK Query depending on how the fetch base query is configured.

---

## 4. Implementation

### Creating the Endpoint:

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

interface UploadResponse {
  imageUrl: string;
}

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    
    // The argument is of type `FormData`
    uploadProfilePicture: builder.mutation<UploadResponse, FormData>({
      query: (formData) => ({
        url: '/users/upload-avatar',
        method: 'POST',
        body: formData,
        // Crucial: Do NOT set Content-Type header here. 
        // fetchBaseQuery handles FormData automatically.
      }),
    }),

  }),
});

export const { useUploadProfilePictureMutation } = apiSlice;
```

---

## 5. React Integration

### Handling the Input and Mutation:

```tsx
import { useState } from 'react';
import { useUploadProfilePictureMutation } from '../features/api/apiSlice';

function AvatarUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadProfilePicture, { isLoading, isSuccess, data }] = useUploadProfilePictureMutation();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    // 1. Create a FormData object
    const formData = new FormData();
    // 2. Append the file with the key expected by your backend
    formData.append('avatar', file);
    // You can also append other string fields if needed
    // formData.append('userId', '123');

    try {
      // 3. Trigger the mutation with the FormData payload
      await uploadProfilePicture(formData).unwrap();
    } catch (err) {
      console.error('File upload failed', err);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      <button onClick={handleUpload} disabled={!file || isLoading}>
        {isLoading ? 'Uploading...' : 'Upload'}
      </button>

      {isSuccess && (
        <div>
          <p>Upload successful!</p>
          <img src={data?.imageUrl} alt="Uploaded Avatar" width={100} />
        </div>
      )}
    </div>
  );
}
```

---

## 6. Next.js Integration

Works identically via Client Components. If you are uploading files via Next.js Server Actions, you would bypass RTK Query and use the native Next.js logic. However, if building a standard SPA client over Next.js, this exact RTK Query pattern is correct.

---

## 7. Impact

### Why use RTK Query for Uploads?
While you could just write a standard `fetch` call inside a component for file uploads, routing it through RTK Query lets you:
- Track `isLoading` automatically to show spinners.
- Track `isError` automatically.
- Easily invalidate tags! (e.g. `invalidatesTags: ['UserProfile']` to refresh the user profile query and show the newly uploaded avatar immediately).

---

## 8. Summary

- Files cannot be sent as JSON.
- Create a native `FormData` object in your component.
- Append the `File` object to the `FormData`.
- Pass the `FormData` object directly as the body to the RTK Query mutation.
- Do not manually set `Content-Type: multipart/form-data`, fetch handles boundary generation for you.

---

**Prev:** [24_optimistic_updates.md](./24_optimistic_updates.md) | **Next:** [26_rtk_query_vs_react_query.md](./26_rtk_query_vs_react_query.md)
