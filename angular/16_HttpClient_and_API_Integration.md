# HttpClient and API Integration

## What is it?
`HttpClient` is Angular's built-in HTTP client service module that enables frontend applications to communicate with remote backend servers over the HTTP/HTTPS protocol. Built on top of the browser's `XMLHttpRequest` API, `HttpClient` delivers typed response contracts, automatic JSON parsing, request/response interceptors, progress events, and native RxJS Observable integration.

## Why do we need it?
Modern frontend web applications must reliably exchange data with backend REST APIs and microservices. Compared to the browser's native `fetch` API, Angular's `HttpClient` provides enterprise-ready features out of the box:
- Automatic JSON transformation for requests and responses.
- Functional interceptors for global authentication token injection, logging, and unified error handling.
- Automatic retry pipelines and timeout handling via RxJS operators.
- High testability with dedicated mock backend utilities (`HttpTestingController`).

```
API Request Flow:
Component triggers fetch ──> Service initiates request 
                         ──> Auth Interceptor attaches JWT Bearer Token 
                         ──> Remote REST API Server 
                         ──> Error Interceptor catches status codes (401/500) 
                         ──> Service processes stream (RxJS Observable) 
                         ──> Component renders data in UI
```

## How does it work?
1. **`provideHttpClient()`**: In modern standalone Angular, HTTP communication is enabled globally in `app.config.ts` using `provideHttpClient(withInterceptors([...]))`.
2. **Type Safety**: API calls accept a TypeScript generic to strongly type the response payload (e.g., `this.http.get<Product[]>('/api/products')`).
3. **HTTP Interceptors**: Middleware functions that intercept and transform outgoing requests or incoming responses before they reach the component.
4. **Cold Observables**: All `HttpClient` methods return cold RxJS Observables. The actual network request is **not** dispatched until a subscriber connects (via `.subscribe()` or the `AsyncPipe`).

## Impact
* **Application Architecture**: Decouples API endpoints and networking protocols from UI components into centralized, reusable services.
* **Performance**: Enables request deduplication, response caching, and automated retry logic for transient network failures.
* **Security**: Enforces centralized credential injection and token refresh routines, preventing sensitive authentication tokens from being hardcoded or mishandled.

## Real World Example
In a secure banking or dashboard application, an HTTP Interceptor inspects every outgoing network call, adds the active `Authorization: Bearer <token>` header, and if an API returns `401 Unauthorized`, automatically attempts a silent token refresh or redirects the user to the login screen.

## Syntax
* **GET Request**: `this.http.get<User[]>('/api/users')`
* **POST Request**: `this.http.post<User>('/api/users', payload)`
* **Functional Interceptor**:
```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const cloned = req.clone({ headers: req.headers.set('Authorization', 'Bearer token') });
  return next(cloned);
};
```

## Code Examples
Below is a complete enterprise implementation featuring standalone HTTP configuration, functional authentication & error interceptors, and a full CRUD service with automated retries and error handling:

### `app.config.ts`
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './auth.interceptor';
import { errorInterceptor } from './error.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor, errorInterceptor])
    )
  ]
};
```

### `auth.interceptor.ts`
```typescript
import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access_token');
  
  // Clone the request because HttpRequest objects are immutable
  const modifiedReq = token ? req.clone({
    setHeaders: { Authorization: `Bearer ${token}` }
  }) : req;
  
  return next(modifiedReq);
};
```

### `error.interceptor.ts`
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);

  return next(req).pipe(
    catchError((error) => {
      if (error.status === 401) {
        console.warn('Unauthorized request - redirecting to login page');
        localStorage.removeItem('access_token');
        router.navigate(['/login']);
      }
      return throwError(() => new Error(error.message || 'Remote Server Error'));
    })
  );
};
```

### `product.service.ts`
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

export interface Product {
  id: number;
  title: string;
  price: number;
}

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private http = inject(HttpClient);
  private apiUrl = 'https://api.escuelajs.co/api/v1/products';

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl).pipe(
      retry({ count: 2, delay: 1000 }), // Automatically retry up to 2 times on network failure
      catchError(this.handleError)
    );
  }

  addProduct(product: Partial<Product>): Observable<Product> {
    return this.http.post<Product>(this.apiUrl, product).pipe(
      catchError(this.handleError)
    );
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown network error occurred!';
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client-side error: ${error.error.message}`;
    } else {
      errorMessage = `Server Error [${error.status}]: ${error.message}`;
    }
    return throwError(() => new Error(errorMessage));
  }
}
```

## Best Practices
1. **Always Type HTTP Calls**: Never make untyped requests like `this.http.get('/api')`. Always pass a generic model interface (`this.http.get<Product[]>('/api')`) to guarantee compile-time type safety.
2. **Encapsulate HTTP Logic in Services**: Never inject `HttpClient` directly into components. Always route network calls through dedicated service classes.
3. **Handle Errors at Both Levels**: Use interceptors for global errors (e.g., 401 Unauthorized or 500 Internal Server Error) and handle specific business errors (e.g., duplicate email during registration) inside local component subscriptions.

## Common Mistakes
* **Forgetting to Subscribe**: Calling an `HttpClient` method (e.g., `this.http.post(...)`) without calling `.subscribe()` or using the `AsyncPipe`. Because Observables are cold, no HTTP request will be sent to the network.
* **Mutating Requests Directly in Interceptors**: Attempting to modify `req.headers` directly. `HttpRequest` objects are strictly immutable; you must use `req.clone()` to attach new headers or parameters.

## Interview Questions & Answers
### Q: Why do `HttpClient` methods return cold Observables?
**A**: `HttpClient` returns cold Observables to ensure network requests execute only when there is an active subscriber (`.subscribe()` or `| async`). This allows developers to chain operators (e.g., `retry`, `timeout`, `catchError`, `map`) before the request is dispatched.

### Q: What is the advantage of modern Functional Interceptors over legacy Class-Based Interceptors?
**A**: Functional interceptors (`HttpInterceptorFn`) are lightweight standalone functions configured via `withInterceptors([fn])`. They eliminate the class boilerplate and `HTTP_INTERCEPTORS` multi-provider syntax, and they can use Angular's `inject()` function directly to resolve services.

## Summary
`HttpClient` is Angular's robust solution for connecting to backend APIs. Functional interceptors handle global security headers, logging, and error parsing, while RxJS Observables provide powerful streaming, retries, and data transformations.

---

Previous : [Reactive Forms](./15_Reactive_Forms.md) | Index : [Home](./00_index.md) | Next : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md)
