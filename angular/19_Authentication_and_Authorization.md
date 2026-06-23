# Authentication and Authorization

## What is it?
Authentication user identity verify karne ka process hai (ki user kaun hai). Authorization user access permissions check karne ka process hai (ki user ko kya-kya karne ki permission hai). Angular applications me ise JSON Web Tokens (JWT), HTTP Interceptors, functional Route Guards, aur role-based check logics ke zariye handle kiya jata hai.

## Why do we need it?
Authentication aur Authorization ke bina koi bhi user secure routes (jaise admin dashboard ya billing reports) ko browser URL bar me direct paste karke access kar sakta hai. Angular apps me routes access control restrict karne, client API requests me token headers attach karne, aur expired tokens ko coordinate/refresh karne ke liye in mechanisms ki zaroorat hoti hai.

```
Access Request Flow:
User navigates to /admin ──> CanMatch/CanActivate Guard checks JWT 
                          ──> Valid JWT? ──> Check user role (Admin?) ──> Render Admin View
                          ──> Expired JWT? ──> Interceptor requests Refresh Token ──> Swap tokens ──> Load admin view
                          ──> No token? ──> Redirect to /login
```

## How does it work?
1. **JWT (JSON Web Tokens)**: Authentication state maintain karne ke liye server login response me short-lived Access Token aur long-lived Refresh Token return karta hai.
2. **Secure Storage**: Access tokens ko in-memory storage ya SessionStorage me rakha jata hai, aur refresh tokens ko securely HTTP-only cookies me store kiya jata hai taaki script-based XSS attacks se bach sakein.
3. **Route Guards**: Functional gatekeepers (jaise `CanActivate` aur `CanMatch`) jo components rendering ya chunk loading se pehle authentication status check karte hain.
4. **HTTP Interceptors**: Outgoing API requests me automatic `Authorization: Bearer <token>` header inject karte hain.

### 🔑 Access Token vs. Refresh Token (In-Depth)

Dono tokens API safety aur user session boundaries manage karne ke liye mandatory hain, par inke functions aur storage policies different hote hain:

| Property | Access Token (Short-Lived) | Refresh Token (Long-Lived) |
| :--- | :--- | :--- |
| **Purpose** | Resource Server APIs ko verify aur authenticate karne ke liye. | Expire hone par naya Access Token generate karne ke liye. |
| **Life Span** | Behad short (e.g., 15 mins to 1 hour). | Long duration (e.g., 7 days to 30 days). |
| **Stored In** | Application memory (Signals/Service) ya SessionStorage. | Secure HTTP-only, Secure, SameSite Cookie (Server-side manage). |
| **Exposure Risks** | XSS (Cross-Site Scripting) attack se chori ho sakta hai agar localStorage me rakhein. | CSRF (Cross-Site Request Forgery) protect karna zaroori hai. |
| **Format** | Signed JWT string (UserId, Role, Expiration attributes carry karta hai). | Random string ya cryptographically signed string, server side validation base token. |

#### 🔄 Token Refresh Flow (The Silent Exchange)

1. **Client API Request**: Angular component page load par API data fetch request bhejta hai. HTTP Interceptor active Access Token ko `Authorization: Bearer <Access_Token>` header me append kar deta hai.
2. **401 Unauthorized Error**: Agar access token expire ho jata hai, toh backend server `401 Unauthorized` response code return karta hai.
3. **Catch & Intercept**: HTTP Interceptor handle checks me is error ko intercept karta hai aur ongoing requests queue ko pause (hold) par daal deta hai.
4. **Refresh Call**: Interceptor automatic background me `/api/refresh` endpoint par hit trigger karta hai (browser securely HTTP-only cookie me save Refresh Token auto-attach bhej deta hai).
5. **New Token Issuance**: Server refresh token check karke new dynamic Access Token emit karta hai.
6. **Retry Queue**: Angular interceptor new access token ko parameters me update karke paused requests ko modify (clone) kar retry karta hai, jisse user page load transition smooth complete ho jata hai.

### 🔌 Full-Stack Integration (Node.js + JWT + Angular/React + MongoDB/MySQL)

Dono tokens flow frontend clients (Angular/React), backend server (Node.js), aur database storage (MongoDB/MySQL) ke beech coordination se set hote hain:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                    FRONTEND LAYER                                      │
│                                   (Angular / React)                                    │
│   • Access Token: In-memory (Signals / state)                                          │
│   • Refresh Token: Secure HTTP-Only Cookie (Set by Backend)                            │
│   • Request Setup: Hamesha 'withCredentials: true' trigger karein                      │
└───────────┬────────────────────────────────────────────────────────────────▲───────────┘
            │                                                                │
     Sends API Call                                                   Emits new Token
 (Bearer AccessToken)                                               (and updates Cookie)
            │                                                                │
┌───────────▼────────────────────────────────────────────────────────────────┴───────────┐
│                                    BACKEND SERVER                                      │
│                                  (Node.js / Express)                                   │
│   • sign(payload, ACCESS_SECRET, { expiresIn: '15m' }) ──> JSON Response               │
│   • sign(payload, REFRESH_SECRET, { expiresIn: '7d' }) ──> Cookie Header               │
│   • Verify Refresh Token against Database (on refresh requests)                        │
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
│   • Purpose: Central tracking for session revocation (password reset, logout)          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Frontend Configuration (Angular vs. React Axios)
Chunki Refresh Token browser ke securely managed cookies (HTTP-Only) me hota hai, isliye har request me cookies send karne ke liye settings enable karni padti hain:
* **Angular**: `provideHttpClient()` configuration me `withInterceptors()` use karein. Interceptor me request clone karte waqt request options me `withCredentials: true` set karein.
* **React (Axios)**: Axios custom instance create karte waqt options config me defaults property set karein: `axios.defaults.withCredentials = true;`.

#### 2. Backend Server Setup (Node.js + Express)
Server side par login endpoint dynamic access aur refresh verify parameters signs karta hai:
```javascript
// Sign Access Token (Short-lived)
const accessToken = jwt.sign({ id: user.id, role: user.role }, process.env.ACCESS_SECRET, { expiresIn: '15m' });

// Sign Refresh Token (Long-lived)
const refreshToken = jwt.sign({ id: user.id }, process.env.REFRESH_SECRET, { expiresIn: '7d' });

// Save Refresh Token in Database (MongoDB/MySQL)
await tokenService.saveRefreshToken(user.id, refreshToken);

// Send Refresh Token as secure Cookie
res.cookie('refreshToken', refreshToken, {
  httpOnly: true, // Secure logic: JavaScript cannot access it
  secure: true,   // Serves only over HTTPS
  sameSite: 'Strict',
  maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days in ms
});

// Return Access Token in Response JSON
res.json({ accessToken, user: { name: user.name, role: user.role } });
```

#### 3. Database Layer (MongoDB vs. MySQL)
Stateless JWT flows me single session logout ya password resets handle check logic verify karne ke liye Refresh Tokens ko DB me track karna mandatory hai:
* **MongoDB (Mongoose Schema)**:
  ```javascript
  const RefreshTokenSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    token: { type: String, required: true, unique: true },
    expiresAt: { type: Date, required: true }
  });
  // Auto-delete expired documents using TTL index
  RefreshTokenSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });
  ```
* **MySQL (Sequelize Schema)**:
  ```javascript
  // Table: RefreshTokens
  const RefreshToken = sequelize.define('RefreshToken', {
    userId: { type: DataTypes.INTEGER, allowNull: false },
    token: { type: DataTypes.STRING, allowNull: false, unique: true },
    expiresAt: { type: DataTypes.DATE, allowNull: false },
    isRevoked: { type: DataTypes.BOOLEAN, defaultValue: false }
  });
  ```
  Jab user **Logout** karta hai ya **Password Reset** karta hai, toh server database se is record ko delete ya `isRevoked = true` kar deta hai. Jab `/api/refresh` request chalegi, backend validation check DB search queries me failure payega aur access block kar dega.

## Impact
* **Application Architecture**: Routing barriers lagane se core views aur login workflow ka clear separation rehta hai.
* **Performance**: `CanMatch` guard fail hone par lazy-loaded route bundles download nahi hote, jisse bandwidth aur page load speed optimized rehte hain.
* **Security**: Interceptors centralizing security token attachment and refresh logic ko automate karte hain.

## Real World Example
Jaise medical dashboard portal me, doctor aur normal staff ke roles different hote hain. Agar user bina 'doctor' role ke edit section par navigate karne ki koshish karega, toh `CanMatch` routing block check karke use access denied page par redirect kar dega.

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

## Code Examples
Neeche HTTP Interceptor ke andar silent token refresh operations aur route guards use karne ka complete configuration design diya gaya hai:

### `auth.service.ts`
```typescript
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, throwError, Observable } from 'rxjs';

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
  currentUser = signal<{ name: string; role: string } | null>(null);

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  hasRole(role: string): boolean {
    const user = this.currentUser();
    return user ? user.role === role : false;
  }

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

### `jwt.interceptor.ts`
```typescript
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError, switchMap, throwError } from 'rxjs';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  let authReq = req;
  if (token) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(authReq).pipe(
    catchError((error) => {
      if (error instanceof HttpErrorResponse && error.status === 401) {
        return authService.refreshToken().pipe(
          switchMap((newTokens) => {
            const retriedReq = req.clone({
              setHeaders: { Authorization: `Bearer ${newTokens.accessToken}` }
            });
            return next(retriedReq);
          }),
          catchError((refreshErr) => {
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
1. **Store Tokens Securely**: Refresh token ko localStorage me store na karein. Uske liye secure HTTP-only cookies ka use karein.
2. **Use `CanMatch` over `CanActivate`**: Lazy-loaded module bundles download hone se pehle hi routes check secure karne ke liye `CanMatch` guard prefer karein.
3. **Parse JWT claims on the Server**: Client-side route guards sirf user experience (UI logic visibility) ke liye hote hain. Actual validation checks aur access controls hamesha backend server par hi verify and enforce karein.

## Common Mistakes
* **Leaking Tokens**: Access tokens ko third-party API calls me automatically headers me send kar dena, jisse dynamic token leakage ho sakti hai.
* **Storing Tokens in localStorage Permanently**: Tokens ko bina expiration check ke permanent store rakhna, jo script injection (XSS) ke chalte browser memory se extract kiya ja sake.

## Interview Questions & Answers
### Q: What is the difference between `CanActivate` and `CanMatch` route guards?
**A**: `CanActivate` check hone se pehle route bundle file load ho chuki hoti hai, bas dynamic navigation blocks check hote hain. `CanMatch` lazy bundle download hone se pehle hi dynamic routes filters verify karke, authorization fail hone par download chunk stop kar deta hai.

### Q: How does a silent JWT refresh flow work in an HTTP interceptor?
**A**: Jab API `401 Unauthorized` throw karti hai, interceptor pichli request pause karke background me token refresh request call karta hai. Agar refresh successful hota hai, toh new token ke sath original request clone karke retry ki jati hai, warna user session end redirect to login trigger ho jata hai.

## Summary
Authentication aur Authorization application safety boundaries ko secure karte hain. Functional guards (`CanMatch`) layouts aur code downloads protect karte hain, aur HTTP Interceptors transparently bearer tokens handle karke application data exchanges manage karte hain.

---

Previous : [State Management](./18_State_Management.md) | Index : [Home](./00_index.md) | Next : [Angular Material](./20_Angular_Material.md)
