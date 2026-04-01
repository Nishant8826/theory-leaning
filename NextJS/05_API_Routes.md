# 05 – API Routes in Next.js

---

## What are API Routes?

API Routes let you build **backend API endpoints** directly inside your Next.js project. You don't need a separate Express.js or Node.js server.

Think of it this way:
- **Without Next.js:** You need a React frontend + a separate Node/Express backend
- **With Next.js:** Frontend + Backend live in the **same project**

```
Traditional Setup:
  [React App] ──HTTP──► [Express Server] ──► [Database]
     (Port 3000)            (Port 5000)

Next.js Setup:
  [Next.js App (Frontend + API Routes)] ──► [Database]
     (Port 3000 — everything in one place)
```

---

## Why Use API Routes?

| Benefit | Explanation |
|---------|------------|
| **No separate backend** | Build full-stack apps in one project |
| **Same deployment** | API and frontend deploy together |
| **Easy to build** | No extra setup, just create a file |
| **Serverless by default** | Each route runs as an independent function |
| **Environment variables** | Securely access secrets server-side |

**Real-world Example:**
Building a contact form:
- Without Next.js API Routes: You need an Express server to handle form submissions
- With Next.js API Routes: Create one file → it handles the form → sends email → done

---

## How API Routes Work

### App Router: Route Handlers (`route.js`)

In the App Router, you create a `route.js` file (not `page.js`) to define an API endpoint.

#### Basic GET Endpoint

```jsx
// app/api/products/route.js
import { NextResponse } from 'next/server';

export async function GET() {
  const products = [
    { id: 1, name: 'Laptop', price: 999 },
    { id: 2, name: 'Phone', price: 699 },
    { id: 3, name: 'Headphones', price: 199 },
  ];

  return NextResponse.json(products);
}

// URL: GET /api/products
// Response: [{ id: 1, name: "Laptop", price: 999 }, ...]
```

#### POST Endpoint (Receive Data)

```jsx
// app/api/contact/route.js
import { NextResponse } from 'next/server';

export async function POST(request) {
  const body = await request.json();

  // body = { name: "John", email: "john@email.com", message: "Hello" }
  console.log('New contact form:', body);

  // In real app: save to database, send email, etc.

  return NextResponse.json(
    { success: true, message: 'Message received!' },
    { status: 201 }
  );
}

// Usage from frontend:
// fetch('/api/contact', {
//   method: 'POST',
//   headers: { 'Content-Type': 'application/json' },
//   body: JSON.stringify({ name: 'John', email: 'john@email.com', message: 'Hello' })
// })
```

#### Dynamic API Routes

```jsx
// app/api/products/[id]/route.js
import { NextResponse } from 'next/server';

export async function GET(request, { params }) {
  const { id } = params;

  // In real app: fetch from database
  const product = { id: parseInt(id), name: 'Laptop', price: 999 };

  if (!product) {
    return NextResponse.json(
      { error: 'Product not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(product);
}

// GET /api/products/1 → { id: 1, name: "Laptop", price: 999 }
// GET /api/products/42 → { id: 42, name: "Laptop", price: 999 }
```

#### All HTTP Methods in One File

```jsx
// app/api/posts/route.js
import { NextResponse } from 'next/server';

// GET — Fetch all posts
export async function GET() {
  const posts = await db.post.findMany();
  return NextResponse.json(posts);
}

// POST — Create a new post
export async function POST(request) {
  const body = await request.json();
  const newPost = await db.post.create({ data: body });
  return NextResponse.json(newPost, { status: 201 });
}

// PUT — Update a post
export async function PUT(request) {
  const body = await request.json();
  const updated = await db.post.update({
    where: { id: body.id },
    data: body,
  });
  return NextResponse.json(updated);
}

// DELETE — Delete a post
export async function DELETE(request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  await db.post.delete({ where: { id: parseInt(id) } });
  return NextResponse.json({ message: 'Post deleted' });
}
```

---

## ⭐ Most Important Concepts

### 1. Reading Request Data

```jsx
export async function POST(request) {
  // Read JSON body
  const body = await request.json();

  // Read URL search params: /api/search?q=laptop&page=1
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('q');      // "laptop"
  const page = searchParams.get('page');    // "1"

  // Read headers
  const authToken = request.headers.get('Authorization');

  // Read cookies
  const token = request.cookies.get('session-token');

  return NextResponse.json({ query, page });
}
```

### 2. Setting Response Headers & Cookies

```jsx
export async function POST(request) {
  const response = NextResponse.json({ success: true });

  // Set custom headers
  response.headers.set('X-Custom-Header', 'hello');

  // Set cookies
  response.cookies.set('session-token', 'abc123', {
    httpOnly: true,       // Can't be accessed by JavaScript
    secure: true,         // Only sent over HTTPS
    sameSite: 'strict',   // Protection against CSRF
    maxAge: 60 * 60 * 24, // 1 day in seconds
  });

  return response;
}
```

### 3. API Route vs Server Component — When to Use Which?

| Feature | API Route (`route.js`) | Server Component (`page.js`) |
|---------|----------------------|------------------------------|
| **Purpose** | Backend API endpoints | Rendering UI pages |
| **Returns** | JSON data | JSX / HTML |
| **Used by** | Frontend fetch, mobile apps, third parties | Internal rendering only |
| **HTTP Methods** | GET, POST, PUT, DELETE | N/A (just page rendering) |
| **When to use** | External consumers, form handling, webhooks | Internal data display |

**Rule of thumb:**
- Need to **show data on a page**? → Use Server Component (fetch directly)
- Need an **endpoint** that external things call? → Use API Route

### 4. Handling Errors Properly

```jsx
// app/api/users/[id]/route.js
import { NextResponse } from 'next/server';

export async function GET(request, { params }) {
  try {
    const user = await db.user.findUnique({
      where: { id: parseInt(params.id) }
    });

    if (!user) {
      return NextResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(user);
  } catch (error) {
    console.error('Database error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### 5. Protecting API Routes

```jsx
// app/api/admin/route.js
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

export async function GET(request) {
  // Check if user is authenticated
  const session = await getServerSession();

  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // Check if user is admin
  if (session.user.role !== 'admin') {
    return NextResponse.json(
      { error: 'Forbidden — Admin only' },
      { status: 403 }
    );
  }

  // Return admin data
  const adminData = await getAdminStats();
  return NextResponse.json(adminData);
}
```

---

## Impact – Real-World Use Cases

| Use Case | API Route Example |
|----------|------------------|
| **Contact Form** | `POST /api/contact` — Receive form data, send email |
| **Authentication** | `POST /api/auth/login` — Verify credentials, set cookie |
| **Payment Webhook** | `POST /api/webhooks/stripe` — Receive payment confirmation |
| **File Upload** | `POST /api/upload` — Handle file uploads |
| **Search** | `GET /api/search?q=shoes` — Return search results |
| **Third-Party Integration** | `POST /api/webhooks/github` — Receive GitHub events |

---

## Pages Router (Legacy) — For Reference

```jsx
// pages/api/products.js
export default function handler(req, res) {
  if (req.method === 'GET') {
    res.status(200).json([{ id: 1, name: 'Laptop' }]);
  } else if (req.method === 'POST') {
    const body = req.body;
    res.status(201).json({ success: true });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
```

**Key Difference:** Pages Router uses a single `handler` function with `req.method` checks. App Router exports separate named functions (`GET`, `POST`, `PUT`, `DELETE`). The App Router approach is cleaner.

---

## Interview Questions & Answers

### Q1: What are API routes in Next.js?
**Answer:** API routes are serverless backend endpoints built inside a Next.js project. In the App Router, you create a `route.js` file inside the `app/api/` directory and export named functions for HTTP methods (GET, POST, PUT, DELETE). They let you build full-stack applications without a separate backend server.

### Q2: What is the difference between `route.js` and `page.js`?
**Answer:** `page.js` defines a UI page (returns JSX/HTML for the browser). `route.js` defines an API endpoint (returns JSON/data). They serve different purposes and **cannot coexist in the same folder** — a folder is either a page route or an API route.

### Q3: How do you read the request body in an API route?
**Answer:** In the App Router, use `const body = await request.json()` to parse JSON body data. For URL search parameters, use `new URL(request.url).searchParams`. For headers, use `request.headers.get('key')`. For cookies, use `request.cookies.get('name')`.

### Q4: Are Next.js API routes serverless?
**Answer:** Yes, when deployed on Vercel or similar platforms, each API route runs as an independent serverless function. It only runs when called and shuts down after execution, which is cost-efficient. However, when self-hosting with `next start`, they run as part of a Node.js server.

### Q5: When should you use API routes vs Server Components for data fetching?
**Answer:** Use Server Components when you just need to fetch and **display** data on a page (simpler, less overhead). Use API routes when you need an **endpoint** that can be called by external consumers (mobile apps, third-party services, webhooks), or when handling form submissions, authentication, and file uploads.

### Q6 (Scenario): You need to build a contact form that sends an email. How?
**Answer:** Create `app/api/contact/route.js` with a POST handler that receives form data via `request.json()`, validates it, then uses a service like Nodemailer or Resend to send the email. The frontend form submits to `/api/contact` via fetch. The API route keeps the email service credentials safe on the server.

### Q7 (Scenario): A third-party payment provider needs a webhook URL. How do you handle it in Next.js?
**Answer:** Create `app/api/webhooks/payment/route.js` with a POST handler. Verify the webhook signature to ensure it's genuinely from the provider, then process the payload (update order status, send confirmation email). Return a 200 status to acknowledge receipt. The endpoint URL would be `https://yoursite.com/api/webhooks/payment`.

---

### 🔗 Navigation
- ⬅️ Previous: [04_Data_Fetching.md](./04_Data_Fetching.md)
- ➡️ Next: [06_Components_Layouts.md](./06_Components_Layouts.md)
