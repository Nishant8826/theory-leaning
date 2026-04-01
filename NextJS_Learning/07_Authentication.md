# 07 – Authentication in Next.js

---

## What is Authentication?

Authentication is the process of **verifying who a user is** — confirming their identity before granting access to protected resources.

```
User enters email + password
        ↓
Server checks if credentials are correct
        ↓
If YES → Create a session/token → User is "logged in"
If NO  → Show error message
```

**Related Concept — Authorization:**
- **Authentication** = "Who are you?" (login/signup)
- **Authorization** = "What are you allowed to do?" (admin vs regular user)

---

## Why Does Authentication Matter?

| Without Auth | With Auth |
|-------------|-----------|
| Anyone can see everything | Only logged-in users see protected data |
| No user-specific experience | Personalized dashboards, profiles |
| No data protection | Sensitive data stays safe |
| No role-based access | Admin, editor, viewer roles enforced |

**Real-world Examples:**
- **Amazon:** You must log in to see your orders, manage your cart, and make purchases
- **Instagram:** You must be logged in to post, like, and comment
- **Admin Dashboard:** Only admins can access user management section

---

## How Authentication Works in Next.js

### The Most Popular Solution: NextAuth.js (Auth.js)

NextAuth.js (now called **Auth.js**) is the standard authentication library for Next.js. It supports:
- Email/Password login
- OAuth providers (Google, GitHub, Facebook, etc.)
- Magic links (passwordless)
- JWT and database sessions

### Setup Flow:

```
1. Install NextAuth.js
        ↓
2. Configure providers (Google, GitHub, Credentials)
        ↓
3. Create API route for auth handlers
        ↓
4. Wrap app with SessionProvider
        ↓
5. Protect pages/routes using session checks
```

### Step 1: Install

```bash
npm install next-auth
```

### Step 2: Configure Auth

```jsx
// app/api/auth/[...nextauth]/route.js
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';

const handler = NextAuth({
  providers: [
    // Google OAuth Login
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),

    // Email/Password Login
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        // Check credentials against your database
        const user = await db.user.findUnique({
          where: { email: credentials.email },
        });

        if (user && await bcrypt.compare(credentials.password, user.password)) {
          return user;   // Login success
        }
        return null;     // Login failed
      },
    }),
  ],

  session: {
    strategy: 'jwt',   // Use JWT tokens (stateless)
  },

  pages: {
    signIn: '/login',   // Custom login page
  },
});

export { handler as GET, handler as POST };
```

### Step 3: Create Login Page

```jsx
// app/login/page.js
"use client";

import { signIn } from 'next-auth/react';
import { useState } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await signIn('credentials', {
      email,
      password,
      redirect: false,
    });

    if (result.error) {
      setError('Invalid email or password');
    } else {
      window.location.href = '/dashboard';
    }
  };

  return (
    <div>
      <h1>Login</h1>

      {/* Google Login */}
      <button onClick={() => signIn('google')}>
        Sign in with Google
      </button>

      <hr />

      {/* Email/Password Login */}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
```

### Step 4: SessionProvider Wrapper

```jsx
// app/providers.js
"use client";

import { SessionProvider } from 'next-auth/react';

export default function Providers({ children }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

```jsx
// app/layout.js
import Providers from './providers';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Step 5: Protect Pages

#### Client-Side Protection:

```jsx
// app/dashboard/page.js
"use client";

import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';

export default function DashboardPage() {
  const { data: session, status } = useSession();

  if (status === 'loading') return <p>Loading...</p>;
  if (!session) redirect('/login');

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

#### Server-Side Protection (Recommended):

```jsx
// app/dashboard/page.js — Server Component
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session) {
    redirect('/login');  // Redirect before any content loads
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
    </div>
  );
}
```

---

## ⭐ Most Important Concepts

### 1. JWT vs Database Sessions

| Feature | JWT (JSON Web Token) | Database Sessions |
|---------|---------------------|-------------------|
| **Storage** | Token stored in cookie | Session ID in cookie, data in DB |
| **Speed** | Faster (no DB lookup) | Slower (DB query per request) |
| **Scalability** | Better (stateless) | Needs shared DB for multiple servers |
| **Revocation** | Hard to invalidate | Easy to destroy session |
| **Size** | Cookie grows with data | Constant small cookie |
| **Best for** | Most apps, APIs | Apps needing instant session revocation |

**Most common choice:** JWT — it's simpler, faster, and works well for most applications.

### 2. OAuth Flow (Google/GitHub Login)

```
User clicks "Sign in with Google"
        ↓
Browser redirects to Google's login page
        ↓
User enters Google credentials
        ↓
Google verifies and redirects back to YOUR app
with an authorization code
        ↓
Your server exchanges the code for user data
(name, email, profile picture)
        ↓
User is logged in — session created
```

**Why OAuth?**
- You don't store passwords (less security risk)
- Users don't create yet another account
- Trusted providers handle security (Google, GitHub)

### 3. Protecting API Routes

```jsx
// app/api/protected/route.js
import { getServerSession } from 'next-auth';
import { NextResponse } from 'next/server';

export async function GET() {
  const session = await getServerSession();

  if (!session) {
    return NextResponse.json(
      { error: 'You must be logged in' },
      { status: 401 }
    );
  }

  return NextResponse.json({
    message: `Hello ${session.user.name}!`,
    data: { secretInfo: 'This is protected' },
  });
}
```

### 4. Role-Based Authorization

```jsx
// app/admin/page.js
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';

export default async function AdminPage() {
  const session = await getServerSession();

  if (!session) redirect('/login');
  if (session.user.role !== 'admin') redirect('/unauthorized');

  return <h1>Admin Dashboard</h1>;
}
```

### 5. Middleware-Based Protection (Entire Routes)

```jsx
// middleware.js (root of project)
import { withAuth } from 'next-auth/middleware';

export default withAuth({
  pages: {
    signIn: '/login',
  },
});

// Protect all routes matching these patterns
export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*', '/profile/:path*'],
};
```

**Impact:** Instead of adding auth checks on every page, one middleware file protects entire route groups automatically.

---

## Impact – Real-World Architecture

| Feature | Implementation |
|---------|---------------|
| **Login page** | `app/login/page.js` — Client Component with form |
| **Google/GitHub login** | OAuth providers in NextAuth config |
| **Protected dashboard** | Server-side session check + redirect |
| **Admin panel** | Role-based check (`session.user.role`) |
| **API protection** | `getServerSession()` in API routes |
| **Route-level protection** | Middleware with path matchers |
| **Logout** | `signOut()` from `next-auth/react` |

---

## Interview Questions & Answers

### Q1: What is the difference between authentication and authorization?
**Answer:** Authentication verifies WHO the user is (login process). Authorization determines WHAT the user can access (permissions/roles). Authentication comes first — you must know who someone is before deciding what they're allowed to do.

### Q2: What is NextAuth.js and why use it?
**Answer:** NextAuth.js (Auth.js) is the standard authentication library for Next.js. It provides built-in support for OAuth providers (Google, GitHub), credential-based login, JWT/database sessions, and security features (CSRF protection, secure cookies). It eliminates the need to build auth from scratch.

### Q3: What is the difference between JWT and database sessions?
**Answer:** JWT stores session data in an encrypted token in the cookie (stateless, fast, no DB lookup needed). Database sessions store only a session ID in the cookie and keep the actual data in the database (easier to revoke, but requires DB query per request). JWT is the more common choice for most apps.

### Q4: How do you protect a page in Next.js?
**Answer:** Three approaches:
1. **Server-side:** Use `getServerSession()` in a Server Component and `redirect('/login')` if no session
2. **Client-side:** Use `useSession()` hook and redirect if unauthenticated
3. **Middleware:** Use NextAuth middleware to protect entire route groups automatically
Server-side protection is recommended because it prevents any UI flash.

### Q5: What is OAuth?
**Answer:** OAuth is a protocol that lets users log in to your app using their existing accounts (Google, GitHub, etc.) without sharing their passwords with you. Your app redirects users to the provider's login page, and the provider sends back verified user information.

### Q6: How do you implement role-based access in Next.js?
**Answer:** Store the user's role in the session/token (during the JWT callback in NextAuth). Then check `session.user.role` in pages, API routes, or middleware. Redirect unauthorized users to a "/forbidden" page or return a 403 response.

### Q7 (Scenario): Users report they can briefly see the dashboard before being redirected to login. How do you fix this?
**Answer:** This happens with client-side protection where `useSession()` has a loading state. Fix by switching to **server-side protection** using `getServerSession()` in a Server Component. The redirect happens before any HTML is sent, so users never see the dashboard content. Alternatively, show a loading spinner during the `status === 'loading'` phase.

### Q8 (Scenario): You need to log the user out from all devices. Which session strategy should you use?
**Answer:** Use **database sessions** instead of JWT. With database sessions, you can delete all session records for a user from the database, instantly logging them out everywhere. JWT tokens are stateless and can't be individually revoked without additional infrastructure (like a token blacklist).

---

### 🔗 Navigation
- ⬅️ Previous: [06_Components_Layouts.md](./06_Components_Layouts.md)
- ➡️ Next: [08_Performance_Optimization.md](./08_Performance_Optimization.md)
