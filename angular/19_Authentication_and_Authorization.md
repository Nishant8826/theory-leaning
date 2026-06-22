# Authentication and Authorization

## What is it?
Authentication is the process of verifying a user's identity (who they are). Authorization is the process of verifying their access permissions (what they are allowed to do). In Angular, this is managed using JSON Web Tokens (JWT), HTTP Interceptors, Route Guards, and role-based checks.

## Why do we need it?
Without authentication and authorization, users could access restricted parts of an application (like administrative settings or billing dashboards) by entering the URL path directly. Angular applications need to restrict access to routes, add security tokens to API requests, and handle token expiration securely.

```
Access Request Flow:
User navigates to /admin ──> CanMatch/CanActivate Guard checks JWT 
                          ──> Valid JWT? ──> Check user role (Admin?) ──> Render Admin View
                          ──> Expired JWT? ──> Interceptor requests Refresh Token ──> Swap tokens ──> Load admin view
                          ──> No token? ──> Redirect to /login
```

## How does it work?
1. **JWT (JSON Web Tokens)**: The server issues an Access Token (short-lived) to authenticate API requests, and a Refresh Token (long-lived) to request new access tokens when they expire.
2. **Secure Client Storage**: Access tokens are stored in memory or SessionStorage, while refresh tokens can be stored in HTTP-only cookies to prevent cross-site scripting (XSS) attacks.
3. **Route Guards**: Functional gatekeepers (like `CanActivate` and `CanMatch`) that check if a user is logged in and authorized before loading components.
4. **HTTP Interceptors**: Automatically append the `Authorization: Bearer <token>` header to outgoing API requests.

## Impact
* **Application Architecture**: Directs routing layouts, separating public routes from private authenticated sub-sections.
* **Performance**: `CanMatch` prevents unauthorized bundles from being lazy-loaded, saving bandwidth.
* **Security**: Centralizes authentication headers and token refreshes, protecting sensitive API endpoints.

## Real World Example
In a healthcare management portal, doctors can view and edit patient records. If a billing clerk attempts to access the record editing route, the `CanMatch` route guard checks their role permissions, blocks the route, and redirects them to the billing page.

## Syntax
* **Role Guard checking JWT claim**:
```typescript
export const roleGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const requiredRole = route.data['role'];
  return auth.hasRole(requiredRole) ? true : router.createUrlTree(['/unauthorized']);
};
```

## Hinglish Explanation

Authentication aur Authorization ka matlab hai **"Pehchan verify karna aur Permissions check karna"**.
* **Authentication (Pehchan):** User check karna (jaise login screen validation).
* **Authorization (Adhikar):** logged-in user ko kin modules ko access karne ki permission hai (e.g. Admin view dashboard vs basic user list).

### 1. Functional Route Guards (Suraksha Guard)
* Angular routes ko secure karne ke liye guards use hote hain:
* `canActivate`: Target component open hone dena hai ya login page par redirect karna hai.
* `canMatch`: User permissions check karke lazy load route assets load hone dena hai ya nahi.

### 2. JWT Interceptor (Pass Card Attacher)
* Token validation standard follow karne ke liye hum HTTP interceptor use karte hain jo automatic outgoing HTTP API calls ke request parameters clone karke usme `Authorization: Bearer <token>` token attach kar deta hai.

### 3. Silent Refresh Flow (Background Token Update)
* Access token expire hone par server 401 error return karega, toh interceptor background me dynamic token renew (refresh token API use karke) request bhejta hai aur current requests refresh response validation ke baad new token ke sath automatically send kar deta hai.

## Code Examples
Below is a complete implementation demonstrating token refresh handling inside an HTTP Interceptor, along with functional route guards.

### `auth.service.ts`
```typescript
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, catchError, throwError, Observable, of } from 'rxjs';

export interface AuthResponse {
  accessToken: string;
  refreshToken: string;
  user: { name: string; role: string; };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private loginUrl = 'https://api.my-app.com/auth/login';

  // Signals to track authentication state
  currentUser = signal<{ name: string; role: string } | null>(null);

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  hasRole(role: string): boolean {
    const user = this.currentUser();
    return user ? user.role === role : false;
  }

  // Request new access token using refresh token
  refreshToken(): Observable<AuthResponse> {
    const rToken = localStorage.getItem('refresh_token');
    if (!rToken) return throwError(() => new Error('No refresh token available'));

    return this.http.post<AuthResponse>('https://api.my-app.com/auth/refresh', { refreshToken: rToken }).pipe(
      tap(res => {
        localStorage.setItem('access_token', res.accessToken);
        localStorage.setItem('refresh_token', res.refreshToken);
      })
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.currentUser.set(null);
  }
}
```

### `jwt.interceptor.ts` (Interceptor with silent refresh flow)
```typescript
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError, switchMap, throwError } from 'rxjs';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  // Clone request to add bearer token
  let authReq = req;
  if (token) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(authReq).pipe(
    catchError((error) => {
      // Catch token expiration errors (401 Unauthorized)
      if (error instanceof HttpErrorResponse && error.status === 401) {
        return authService.refreshToken().pipe(
          switchMap((newTokens) => {
            // Re-try the original request with the new access token
            const retriedReq = req.clone({
              setHeaders: { Authorization: `Bearer ${newTokens.accessToken}` }
            });
            return next(retriedReq);
          }),
          catchError((refreshErr) => {
            // Silent refresh failed - force log out the user
            authService.logout();
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
1. **Store Tokens Securely**: Avoid storing sensitive user information in access tokens. Use HTTP-only cookies for refresh tokens where possible to prevent XSS attacks.
2. **Use `CanMatch` over `CanActivate`**: Use `CanMatch` to prevent lazy-loaded modules from downloading if the user doesn't have permissions.
3. **Parse JWT claims on the Server**: Client-side routing checks are for user experience. Always enforce security checks on the server, as client-side code can be modified.

## Common Mistakes
* **Leaking Tokens**: Appending authorization headers to outgoing requests made to third-party domains (like external image hosts). Always check the request URL in your interceptors before adding tokens.
* **Storing Tokens in localStorage Permanently**: Leaving access tokens in `localStorage` indefinitely, making them vulnerable to cross-site scripting (XSS) attacks. Use short expiration times.

## Interview Questions & Answers
### Q: What is the difference between `CanActivate` and `CanMatch` route guards?
**A**: `CanActivate` runs after the code bundle for a route has been downloaded. It determines whether a component can be rendered, but still downloads the code. `CanMatch` runs before the route bundle is downloaded, preventing unauthorized users from downloading the code.
* **Hinglish Explanation**: `CanActivate` tab chalta hai jab routing path match hone ke baad us page ka code download ho chuka ho, aur yeh check karta hai ki user usey dekh sakta hai ya nahi. `CanMatch` routing selection se pehle hi chalta hai. Agar user authenticated nahi hai, toh yeh usey code bundle download karne hi nahi deta, jisse core enterprise code/secrets secure rehte hain.

### Q: How does a silent JWT refresh flow work in an HTTP interceptor?
**A**: When an API request fails with a `401 Unauthorized` status (indicating an expired token), the interceptor intercepts the error, calls a service to request a new access token using a refresh token, updates storage, and retries the original request with the new token.
* **Hinglish Explanation**: Silent JWT refresh flow me jab bhi koi API request server se `401 Unauthorized` error (token expire hone ki wajah se) ke sath return hoti hai, toh HTTP Interceptor us request ko catch (pause) kar leta hai. Phir background me ek `refreshToken()` call chalti hai naya token laane ke liye. Naya token milte hi, interceptor purani request ko clone karke usme naya token set karta hai aur use dobara trigger kar deta hai, jisse user ko page refresh nahi karna padta aur fluid user experience milta hai.

## Summary
Authentication and authorization manage user identity and access permissions in Angular. Functional route guards (`CanMatch`) secure routes, while HTTP interceptors append access tokens and manage silent token refreshes automatically.

---

Previous : [State Management](./18_State_Management.md) | Index : [Home](./00_index.md) | Next : [Angular Material](./20_Angular_Material.md)
