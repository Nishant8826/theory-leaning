# 13 – Server Actions in Next.js

---

## What are Server Actions?

Server Actions are **functions that run on the server** but can be called directly from your frontend components — without writing an API route. They're the simplest way to handle form submissions, data mutations, and server-side logic in Next.js.

```
Traditional Approach (3 steps):
  1. Create an API route (backend)
  2. Write a fetch() call (frontend)
  3. Handle request/response manually

Server Actions Approach (1 step):
  1. Write a function with "use server" → Call it from your form → Done!
```

---

## Why Use Server Actions?

| Without Server Actions | With Server Actions |
|-----------------------|---------------------|
| Create API route file | No API route needed |
| Write fetch logic in client | Direct function call |
| Handle serialization manually | Automatic serialization |
| Manage loading/error states yourself | Works with `useFormStatus` |
| CSRF protection = manual | Built-in CSRF protection |

**Real-world Example:**
A contact form on your website:
- **Old way:** Create `/api/contact`, write `fetch('/api/contact', { method: 'POST', ... })`, handle loading/error
- **Server Actions:** Write one function, bind it to `<form action={myFunction}>`, done

---

## How Server Actions Work

### Method 1: Inline Server Action (Inside a Server Component)

```jsx
// app/contact/page.js — Server Component
export default function ContactPage() {

  // This function runs on the SERVER
  async function submitForm(formData) {
    "use server";

    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');

    // Save to database
    await db.contact.create({
      data: { name, email, message }
    });

    // Send email
    await sendEmail({ to: 'admin@site.com', subject: `New message from ${name}` });
  }

  return (
    <form action={submitForm}>
      <input name="name" placeholder="Your name" required />
      <input name="email" type="email" placeholder="Email" required />
      <textarea name="message" placeholder="Your message" required />
      <button type="submit">Send Message</button>
    </form>
  );
}
```

**What happens when the user submits:**
1. Browser sends form data to the server
2. `submitForm` function runs on the server
3. Data is saved to DB, email is sent
4. Page automatically revalidates (shows fresh data)

### Method 2: Separate Action File (Recommended for Reuse)

```jsx
// app/actions/contact.js
"use server";

import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function submitContactForm(formData) {
  const name = formData.get('name');
  const email = formData.get('email');
  const message = formData.get('message');

  // Validate
  if (!name || !email || !message) {
    return { error: 'All fields are required' };
  }

  // Save to database
  await db.contact.create({
    data: { name, email, message },
  });

  // Revalidate the page to show updated data
  revalidatePath('/contact');

  return { success: true, message: 'Message sent successfully!' };
}
```

```jsx
// app/contact/page.js
import { submitContactForm } from '@/app/actions/contact';
import ContactForm from '@/components/ContactForm';

export default function ContactPage() {
  return (
    <div>
      <h1>Contact Us</h1>
      <ContactForm action={submitContactForm} />
    </div>
  );
}
```

```jsx
// components/ContactForm.js
"use client";

import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Sending...' : 'Send Message'}
    </button>
  );
}

export default function ContactForm({ action }) {
  const [state, formAction] = useActionState(action, null);

  return (
    <form action={formAction}>
      {state?.error && <p style={{ color: 'red' }}>{state.error}</p>}
      {state?.success && <p style={{ color: 'green' }}>{state.message}</p>}

      <input name="name" placeholder="Your name" required />
      <input name="email" type="email" placeholder="Email" required />
      <textarea name="message" placeholder="Your message" required />
      <SubmitButton />
    </form>
  );
}
```

---

## ⭐ Most Important Concepts

### 1. Server Actions vs API Routes

| Feature | Server Actions | API Routes |
|---------|---------------|------------|
| **File** | Any file with `"use server"` | `route.js` |
| **Returns** | Data (auto-serialized) | `NextResponse.json()` |
| **Calling** | `<form action={fn}>` or direct call | `fetch('/api/...')` |
| **CSRF Protection** | Built-in | Manual |
| **Best For** | Form submissions, data mutations | External consumers, webhooks, mobile apps |
| **Works With** | `useFormStatus`, `useActionState` | Manual loading/error states |

**Rule of Thumb:**
- **Server Actions** → For YOUR app's forms and mutations
- **API Routes** → For external consumers (mobile apps, third-party services)

### 2. Data Revalidation After Mutations

After changing data (create, update, delete), you need to tell Next.js to refresh the cached data:

```jsx
"use server";

import { revalidatePath } from 'next/cache';
import { revalidateTag } from 'next/cache';

export async function createPost(formData) {
  await db.post.create({ data: { title: formData.get('title') } });

  // Option 1: Revalidate a specific path
  revalidatePath('/blog');          // Refresh the blog listing page

  // Option 2: Revalidate by tag
  revalidateTag('posts');           // Refresh all fetches tagged 'posts'

  // Option 3: Revalidate a specific layout
  revalidatePath('/blog', 'layout');
}
```

### 3. Calling Server Actions from Client Components

```jsx
// app/actions/cart.js
"use server";

export async function addToCart(productId) {
  const session = await getSession();
  if (!session) throw new Error('Must be logged in');

  await db.cart.create({
    data: {
      userId: session.user.id,
      productId: productId,
    },
  });

  revalidatePath('/cart');
  return { success: true };
}
```

```jsx
// components/AddToCartButton.js
"use client";

import { addToCart } from '@/app/actions/cart';
import { useState } from 'react';

export default function AddToCartButton({ productId }) {
  const [loading, setLoading] = useState(false);
  const [added, setAdded] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      await addToCart(productId);
      setAdded(true);
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? 'Adding...' : added ? '✅ Added' : '🛒 Add to Cart'}
    </button>
  );
}
```

### 4. Optimistic Updates

Show the expected result immediately, before the server confirms:

```jsx
"use client";

import { useOptimistic } from 'react';
import { likePost } from '@/app/actions/posts';

export default function LikeButton({ postId, initialLikes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (currentLikes) => currentLikes + 1
  );

  const handleLike = async () => {
    addOptimisticLike(); // Show +1 immediately (optimistic)
    await likePost(postId); // Then confirm with server
  };

  return (
    <button onClick={handleLike}>
      ❤️ {optimisticLikes}
    </button>
  );
}
```

**Real-world Example:** Instagram's like button — the heart turns red instantly despite the server call taking 200ms. If the server call fails, it reverts.

### 5. Validation with Zod

Always validate input on the server — never trust the client:

```jsx
// app/actions/register.js
"use server";

import { z } from 'zod';

const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export async function registerUser(formData) {
  const rawData = {
    name: formData.get('name'),
    email: formData.get('email'),
    password: formData.get('password'),
  };

  // Validate
  const result = registerSchema.safeParse(rawData);
  if (!result.success) {
    return {
      error: result.error.flatten().fieldErrors,
    };
  }

  // Safe to use — data is validated
  const { name, email, password } = result.data;

  await db.user.create({
    data: { name, email, password: await hashPassword(password) },
  });

  return { success: true };
}
```

---

## Impact — Real-World CRUD with Server Actions

| Operation | Server Action |
|-----------|--------------|
| **Create** | `<form action={createPost}>` |
| **Read** | Server Component with `async/await` (not a Server Action) |
| **Update** | `<form action={updatePost}>` with hidden `id` field |
| **Delete** | `<form action={deletePost}>` with hidden `id` field |

```jsx
// Delete example
"use server";
export async function deletePost(formData) {
  const id = formData.get('id');
  await db.post.delete({ where: { id } });
  revalidatePath('/blog');
}

// In the component:
<form action={deletePost}>
  <input type="hidden" name="id" value={post.id} />
  <button type="submit">🗑️ Delete</button>
</form>
```

---

## Interview Questions & Answers

### Q1: What are Server Actions in Next.js?
**Answer:** Server Actions are asynchronous functions that run on the server and can be called directly from components. They're marked with `"use server"` and eliminate the need for API routes for form handling and data mutations. They provide built-in CSRF protection and integrate with React's form handling hooks.

### Q2: How are Server Actions different from API Routes?
**Answer:** Server Actions are called directly from components (via `<form action={fn}>` or function calls) and handle serialization automatically. API Routes are HTTP endpoints (`route.js`) that return JSON via `NextResponse`. Use Server Actions for internal app mutations, API Routes for external consumers.

### Q3: What is `revalidatePath` and when do you use it?
**Answer:** `revalidatePath('/path')` tells Next.js to refresh the cached data for a specific page. You call it inside a Server Action after mutating data (create, update, delete) so the UI shows the latest information. Without it, the page might show stale cached data.

### Q4: How do you show loading state during a Server Action?
**Answer:** Use the `useFormStatus` hook from `react-dom`. It provides a `pending` boolean that's `true` while the action is executing. Create a submit button component that uses this hook and disable the button or show "Submitting..." text.

### Q5: What is an optimistic update?
**Answer:** An optimistic update shows the expected result immediately in the UI before the server confirms. For example, showing a like count increment instantly. If the server call fails, the UI reverts. Use `useOptimistic` from React for this pattern.

### Q6 (Scenario): Your form saves data but the page still shows old data afterwards. What's wrong?
**Answer:** The Server Action is missing `revalidatePath()` or `revalidateTag()`. After the data mutation, Next.js is still serving the cached version of the page. Adding `revalidatePath('/your-page')` at the end of the action forces a refresh of the cached data.

### Q7 (Scenario): A user submits a form on a slow connection. The form submits twice because they clicked the button again. How do you prevent this?
**Answer:** Use `useFormStatus` to get the `pending` state and disable the submit button while the action is in progress. This prevents double submissions.

---

### 🔗 Navigation

---

← Previous: [12_Middleware.md](12_Middleware.md) | Next: [14_Caching.md](14_Caching.md) →
