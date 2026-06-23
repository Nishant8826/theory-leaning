# Authentication and Authorization

## What is it?
Authentication user identity verify karne ka process hai (ki user kaun hai). Authorization user access permissions check karne ka process hai (ki user ko kya-kya karne ki permission hai). Angular applications me ise JSON Web Tokens (JWT), HTTP Interceptors, functional Route Guards, aur role-based check logics ke zariye handle kiya jata hai.

## Why do we need it?
Authentication aur Authorization ke bina koi bhi user secure paths (jaise administrative dashboards ya billing reports pages) ko browser URL address bar me direct link write karke access kar sakega. Angular apps me routes access restricts set karne, client network requests me token headers attach karne, aur token expiration parameters coordinate check handle karne ke liye in frameworks ki zaroorat hoti hai.

```
Access Request Flow:
User navigates to /admin ──> CanMatch/CanActivate Guard checks JWT 
                          ──> Valid JWT? ──> Check user role (Admin?) ──> Render Admin View
                          ──> Expired JWT? ──> Interceptor requests Refresh Token ──> Swap tokens ──> Load admin view
                          ──> No token? ──> Redirect to /login
```

## How does it work?
1. **JWT (JSON Web Tokens)**: Authentication verify rakhne ke liye server user validation par Access Token (short-lived) return karta hai, aur session check maintenance ke liye Refresh Token (long-lived) assign karta hai jo access token expire hone par use renew karne me use hota hai.
2. **Secure Client Storage**: Access tokens elements dynamic memory contexts/SessionStorage options me place kiye jate hain, jabki Refresh tokens cookies security parameters (HTTP-only) options utilize kar store kiye jate hain taaki XSS injections vulnerabilities control rahein.
3. **Route Guards**: Functional gatekeepers (jaise `CanActivate` aur `CanMatch`) jo component render cycles active hone se pehle check run karte hain ki user logged in hai ya authorized hai.
4. **HTTP Interceptors**: Outgoing backend API requests me `Authorization: Bearer <token>` authorization headers dynamically auto-append aur inject karte hain.

## Impact
* **Application Architecture**: Routes levels check boundary layout setup separation parameters maintain karta hai.
* **Performance**: `CanMatch` authorization status check failure par lazy load route code bundles dynamic download stop karta hai, jisse client bandwidth aur data usage control hote hain.
* **Security**: Client authorization token headers inject and refresh operations parameters centrally automate aur verify rakhta hai.

## Real World Example
Medical management dashboard portal me, medical staff entries view aur write actions perform kar sakte hain. Jab security desk checker staff coordinates verify kiye bina editing options settings access karke actions trigger karna chahega, toh `CanMatch` guard status check abort kar use billing index login options block page par redirect kar dega.

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
Neeche HTTP Interceptor ke andar token refresh operations, authentication states check aur functional route guards use karne ka full implementation class parameters configure kiya gaya hai:

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
1. **Store Tokens Securely**: User session tokens parameters local storage checks variables me write na karein. Refresh token handling parameters systems secure HTTP-only cookies boundaries settings implement check apply karein.
2. **Use `CanMatch` over `CanActivate`**: Route level bundles logic blocks downloading secure coordinate rules apply settings parameters setup me `CanMatch` route filters use karein.
3. **Parse JWT claims on the Server**: Client side checks routes guards parameters user experiences transitions dynamic layouts settings ke liye hote hain. Core validation checks checks and locks checks hamesha server side interfaces controls targets levels par enforce karein.

## Common Mistakes
* **Leaking Tokens**: Access tokens JWT header values parameters coordinates external dynamic addresses API calls requests me automatically leak parameters update block check indicators missing rakhna.
* **Storing Tokens in localStorage Permanently**: Token values ko permanent limits me local parameters browser variables memory me place rakhna, jo client script injections vulnerabilities data leak traps increase kar sakta hai.

## Interview Questions & Answers
### Q: What is the difference between `CanActivate` and `CanMatch` route guards?
**A**: `CanActivate` code compile files dynamic download check templates updates evaluate actions run check setup follow karta hai. `CanMatch` layout coordinates selection flow run parameters download checks settings run optimize block implement karta hai.

### Q: How does a silent JWT refresh flow work in an HTTP interceptor?
**A**: Server validation response codes checks me interceptor `401 Unauthorized` checks coordinate updates triggers detect karta hai. Yeh background me tokens refresh network checks calls execute parameters complete kar new dynamic token parameters original request me clone kar dynamic updates redirect run kar leta hai.

## Summary
Authentication aur Authorization Angular applications safety check boundaries manage karte hain. Functional route guards (`CanMatch`) layouts protect coordinate setups, HTTP interceptors automatics bearer token setups updates execute secure client servers validations structures manage karte hain.

---

Previous : [State Management](./18_State_Management.md) | Index : [Home](./00_index.md) | Next : [Angular Material](./20_Angular_Material.md)
