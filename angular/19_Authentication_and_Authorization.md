# Authentication and Authorization

## What is it?
- **Authentication** is the process of verifying a user's identity (answering: *"Who are you?"*).
- **Authorization** is the process of verifying a user's access permissions (answering: *"What resources are you allowed to access or modify?"*).

In Angular applications, authentication and authorization are implemented using JSON Web Tokens (JWT), HTTP Interceptors, functional Route Guards (`CanActivateFn`, `CanMatchFn`), and role-based access control (RBAC) patterns.

## Why do we need it?
Without proper authentication and authorization controls, any user could navigate directly to restricted application routes (such as `/admin/finance` or `/user/billing`) by pasting the URL into the browser. 

In addition, protected backend REST APIs require a valid credential header on every request. Angular coordinates client-side route access control, attaches credentials to outgoing API requests, and seamlessly refreshes expired tokens in the background.

```
Access Request Flow:
User navigates to /admin ──> CanMatch / CanActivate Guard checks JWT 
                          ──> Valid JWT? ──> Check user role (e.g., 'admin') ──> Render Admin View
                          ──> Expired JWT? ──> Interceptor requests Refresh Token ──> Swap tokens ──> Load admin view
                          ──> No Token / Invalid? ──> Redirect to /login
```

## How does it work?
1. **JWT (JSON Web Tokens)**: Upon successful login, the authentication server returns a short-lived **Access Token** and a long-lived **Refresh Token**.
2. **Secure Token Storage**:
   - Access tokens are stored in-memory (inside an Angular service or Signal) or in `sessionStorage`.
   - Refresh tokens are stored in secure, `HttpOnly`, `SameSite` cookies managed by the backend, protecting them from JavaScript-based Cross-Site Scripting (XSS) extraction.
3. **Route Guards**: Functional gatekeepers (`CanMatchFn`, `CanActivateFn`) that intercept route transitions, verifying authentication and role permissions before lazy chunks are downloaded or components are rendered.
4. **HTTP Interceptors**: Automatically clone and attach `Authorization: Bearer <token>` headers to outgoing backend requests and catch `401 Unauthorized` responses to initiate silent token refresh flows.

---

### 🔑 Access Token vs. Refresh Token (In-Depth)

Both tokens are essential for balancing API security with a smooth, continuous user experience:

| Property | Access Token (Short-Lived) | Refresh Token (Long-Lived) |
| :--- | :--- | :--- |
| **Primary Purpose** | Authorize requests against backend resource APIs. | Obtain a new Access Token once the current one expires. |
| **Lifespan** | Very short (e.g., 10–15 minutes). | Long duration (e.g., 7–30 days). |
| **Storage Location** | Application memory (Angular Service/Signal) or `sessionStorage`. | Secure `HttpOnly`, `Secure`, `SameSite` Cookie (managed by server). |
| **Security Risk** | Vulnerable to XSS if placed in `localStorage`. | Vulnerable to CSRF if not protected with `SameSite` and anti-CSRF headers. |
| **Format** | Cryptographically signed JWT containing claims (`sub`, `role`, `exp`). | Opaque random string or encrypted token tracked in a backend database. |

#### 🔄 The Silent Token Refresh Flow

1. **Client API Request**: An Angular component triggers an API call. The HTTP Interceptor appends the active Access Token in the `Authorization: Bearer <Access_Token>` header.
2. **401 Unauthorized Response**: If the access token has expired, the resource server rejects the request with a `401 Unauthorized` status code.
3. **Catch & Intercept**: The Angular HTTP Interceptor intercepts the 401 error and temporarily pauses pending API calls in an internal queue.
4. **Silent Refresh Request**: The interceptor dispatches a POST request to `/api/auth/refresh`. The browser automatically includes the secure `HttpOnly` refresh token cookie.
5. **New Token Issuance**: The backend verifies the refresh token against its database/cache and issues a brand-new short-lived Access Token.
6. **Replay Pending Requests**: The interceptor clones the original failed request with the new Access Token, replays it to the server, and returns the successful response to the waiting component seamlessly.

---

### 🔌 Full-Stack Architecture (Angular + Node.js/Express + Database)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                    FRONTEND LAYER                                      │
│                                   (Angular 17/18+)                                     │
│   • Access Token: In-memory (Signals / AuthService)                                    │
│   • Refresh Token: Secure HTTP-Only Cookie (automatically attached by browser)         │
│   • HTTP Client: Configured with withCredentials: true                                 │
└───────────┬────────────────────────────────────────────────────────────────▲───────────┘
            │                                                                │
     Sends API Request                                                Emits New Token
   (Bearer AccessToken)                                             (and updates Cookie)
            │                                                                │
┌───────────▼────────────────────────────────────────────────────────────────┴───────────┐
│                                    BACKEND SERVER                                      │
│                                  (Node.js / Express)                                   │
│   • jwt.sign(payload, ACCESS_SECRET, { expiresIn: '15m' }) ──> JSON Body               │
│   • jwt.sign(payload, REFRESH_SECRET, { expiresIn: '7d' }) ──> HttpOnly Cookie Header │
│   • Validates Refresh Token against Database on /api/auth/refresh                      │
└───────────┬────────────────────────────────────────────────────────────────▲───────────┘
            │                                                                │
       Saves / Checks                                                   Query Result
       Refresh Token                                                  (Token is Valid)
            │                                                                │
┌───────────▼────────────────────────────────────────────────────────────────┴───────────┐
│                                    DATABASE LAYER                                      │
│                                  (MongoDB / MySQL)                                     │
│   • MongoDB Schema: { userId: ObjectId, token: String, expiresAt: Date }               │
│   • MySQL Table: RefreshTokens (id, userId, token, expiresAt, isRevoked)               │
│   • Purpose: Centralized session revocation (Logout, Password Reset, Device Purge)    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Frontend Configuration
Because the Refresh Token resides inside an `HttpOnly` cookie, cross-origin requests must include credentials:
* In Angular: Use `withInterceptors()` in `provideHttpClient()` and ensure request clones include `withCredentials: true`.

#### 2. Backend Server Setup (Node.js + Express)
```javascript
// Sign Access Token (Short-Lived)
const accessToken = jwt.sign(
  { id: user._id, role: user.role }, 
  process.env.ACCESS_TOKEN_SECRET, 
  { expiresIn: '15m' }
);

// Sign Refresh Token (Long-Lived)
const refreshToken = jwt.sign(
  { id: user._id }, 
  process.env.REFRESH_TOKEN_SECRET, 
  { expiresIn: '7d' }
);

// Persist Refresh Token to Database for revocation support
await tokenService.saveRefreshToken(user._id, refreshToken);

// Set secure HttpOnly Cookie
res.cookie('refreshToken', refreshToken, {
  httpOnly: true, // Prevents JavaScript access (Immune to XSS)
  secure: true,   // Transmitted only over HTTPS
  sameSite: 'Strict',
  maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
});

// Return Access Token in JSON response body
res.json({ accessToken, user: { name: user.name, role: user.role } });
```

#### 3. Database Layer (Session Revocation)
Tracking refresh tokens in the database allows the server to invalidate user sessions immediately upon **Logout** or **Password Reset**:
* **MongoDB**: Use a TTL (Time-To-Live) index on `expiresAt` to automatically clean up expired tokens from the collection.
* **MySQL**: Store token records with an `isRevoked` boolean flag. If `isRevoked === true` during `/api/auth/refresh`, the server rejects the request immediately.

---

## Impact
* **Application Architecture**: Clear boundary between unauthenticated public views, protected user sections, and administrative portals.
* **Performance**: `CanMatch` prevents unauthorized users from downloading lazy-loaded feature JavaScript bundles, preserving bandwidth and security.
* **Security**: Multi-layered defense combining short-lived in-memory tokens, `HttpOnly` cookies, and server-side session revocation.

## Real World Example
In a healthcare hospital management system:
- Standard staff members can access patient records in read-only mode.
- If a nurse attempts to navigate to `/admin/billing`, the `roleGuard` checks the JWT role claim, detects the lack of the `admin` role, and redirects to an `/unauthorized` view without downloading administrative bundle code.

## Syntax
* **Functional Role Guard**:
```typescript
export const roleGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const requiredRole = route.data['role'];

  return auth.hasRole(requiredRole) ? true : router.createUrlTree(['/unauthorized']);
};
```

## Code Examples
Below is a complete Angular authentication architecture with an `AuthService`, a silent refresh `jwtInterceptor`, and a role guard:

### `auth.service.ts`
```typescript
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, throwError, Observable } from 'rxjs';

export interface AuthResponse {
  accessToken: string;
  user: { name: string; role: string; };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  
  // In-memory reactive user state
  currentUser = signal<{ name: string; role: string } | null>(null);
  private accessToken: string | null = null;

  getToken(): string | null {
    return this.accessToken;
  }

  setToken(token: string | null): void {
    this.accessToken = token;
  }

  hasRole(role: string): boolean {
    const user = this.currentUser();
    return user ? user.role === role : false;
  }

  refreshToken(): Observable<AuthResponse> {
    // Refresh token is automatically sent by the browser via HttpOnly cookie
    return this.http.post<AuthResponse>(
      'https://api.enterprise-app.com/api/auth/refresh', 
      {}, 
      { withCredentials: true }
    ).pipe(
      tap(res => {
        this.setToken(res.accessToken);
        this.currentUser.set(res.user);
      })
    );
  }

  logout(): void {
    this.http.post('https://api.enterprise-app.com/api/auth/logout', {}, { withCredentials: true }).subscribe();
    this.setToken(null);
    this.currentUser.set(null);
  }
}
```

### `jwt.interceptor.ts` (Silent Token Refresh)
```typescript
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError, switchMap, throwError } from 'rxjs';
import { Router } from '@angular/router';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();

  // Attach active bearer token if available
  let authReq = req;
  if (token) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(authReq).pipe(
    catchError((error) => {
      // Intercept 401 Unauthorized errors
      if (error instanceof HttpErrorResponse && error.status === 401) {
        return authService.refreshToken().pipe(
          switchMap((newTokens) => {
            // Replay original request with new access token
            const retriedReq = req.clone({
              setHeaders: { Authorization: `Bearer ${newTokens.accessToken}` }
            });
            return next(retriedReq);
          }),
          catchError((refreshErr) => {
            // If refresh fails, log out and redirect to login
            authService.logout();
            router.navigate(['/login']);
            return throwError(() => refreshErr);
          })
        );
      }
      return throwError(() => error);
    })
  );
};
```

## Best Practices
1. **Never Store Sensitive Refresh Tokens in LocalStorage**: `localStorage` is accessible to any JavaScript running on the page, making tokens vulnerable to Cross-Site Scripting (XSS). Always use backend-managed `HttpOnly`, `SameSite: Strict` cookies for refresh tokens.
2. **Prefer `CanMatch` Over `CanActivate`**: Use `CanMatchFn` on lazy routes so Angular stops unauthorized users from even downloading the lazy route's JavaScript bundle.
3. **Always Enforce Security on the Backend**: Client-side route guards and UI button states are purely for user experience. The backend server must independently validate JWT signatures and permissions on every incoming request.

## Common Mistakes
* **Sending Bearer Tokens to Third-Party Domains**: Configuring interceptors that attach authorization headers to external URLs (e.g., third-party CDNs or analytics endpoints), leaking private user tokens.
* **Infinite Refresh Loops**: If the `/api/auth/refresh` endpoint itself returns a `401 Unauthorized`, failing to exclude it from the interceptor retry logic will trigger an infinite request loop.

## Interview Questions & Answers
### Q: What is the difference between `CanActivate` and `CanMatch` route guards?
**A**: `CanActivate` runs *after* the lazy route chunk has already been downloaded to the browser, simply deciding whether to instantiate and render the component. `CanMatch` runs *before* the route chunk is fetched; if it returns `false`, Angular skips the route entirely and does not download the JavaScript bundle at all.

### Q: How does a silent JWT refresh flow work with an HTTP Interceptor?
**A**: When an API request fails with a `401 Unauthorized` status, the HTTP Interceptor catches the error, pauses outgoing requests, and calls `/api/auth/refresh` (sending the `HttpOnly` cookie). If the server returns a new access token, the interceptor clones the original failed request with the new header and replays it. If the refresh request also fails, it clears local session state and redirects the user to `/login`.

## Summary
Authentication verifies user identity, while Authorization regulates access to features and data. By combining functional route guards (`CanMatch`), secure `HttpOnly` cookies, in-memory access tokens, and silent refresh HTTP interceptors, Angular applications achieve enterprise-level security.

---

Previous : [State Management](./18_State_Management.md) | Index : [Home](./00_index.md) | Next : [Angular Material](./20_Angular_Material.md)
