# HttpClient and API Integration

## What is it?
`HttpClient` is a built-in Angular service that enables applications to communicate with remote servers over HTTP. It is built on top of the browser's XMLHttpRequest API, returns RxJS Observables, handles request/response interception, and supports type-safe requests.

## Why do we need it?
Modern frontend applications need to interact with backend services to fetch and store data. While the browser's native `fetch` API is available, it lacks advanced features like automatic JSON parsing, request/response interceptors (essential for adding auth tokens), request progress tracking, and integration with RxJS streams. `HttpClient` simplifies API communication by packaging these features into an injectable utility.

```
API Request Flow:
Component triggers fetch ──> Service makes request ──> Auth Interceptor appends JWT token 
                         ──> Remote REST API Server ──> Error Interceptor parses codes (401/500) 
                         ──> Component receives data stream (RxJS Observable)
```

## How does it work?
1. **`provideHttpClient()`**: Registers the HTTP client provider during bootstrapping.
2. **Type Safety**: Methods like `http.get<Product[]>(url)` automatically cast JSON responses to the specified TypeScript types.
3. **Interceptors**: Functions that intercept outgoing requests or incoming responses to modify headers, append authentication tokens, or handle errors globally.
4. **RxJS Streams**: All request methods return cold observables that only execute when subscribed to.

## Impact
* **Application Architecture**: Centralizes HTTP requests in services, separating data loading from presentation components.
* **Performance**: Interceptors can implement client-side caching to reduce redundant network requests.
* **Security**: Centralized headers ensure security tokens (JWT) are appended consistently to all outbound requests.

## Real World Example
In a secure enterprise dashboard, a functional interceptor automatically intercepts every outbound HTTP request, reads the user's JWT from storage, and appends it to the `Authorization` header. If a response returns a `401 Unauthorized` status, the interceptor redirects the user to the login page.

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
Below is a complete implementation of an API service with functional interceptors, error handling, retry strategies, and CRUD operations.

### `app.config.ts` (Interceptor registration)
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
  
  // Clone the request and append the authorization header if token exists
  const modifiedReq = token ? req.clone({
    setHeaders: { Authorization: `Bearer ${token}` }
  }) : req;
  
  return next(modifiedReq);
};
```

### `error.interceptor.ts`
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error) => {
      if (error.status === 401) {
        console.warn('Unauthorized request - redirecting to login');
        localStorage.removeItem('access_token');
        // Redirect user or trigger logout flow
      }
      return throwError(() => new Error(error.message || 'Server Error'));
    })
  );
};
```

### `product.service.ts` (CRUD Operations)
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry, delay } from 'rxjs/operators';

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

  // 1. GET ALL
  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl).pipe(
      retry({ count: 2, delay: 1000 }), // Retry twice with 1 second delay
      catchError(this.handleError)
    );
  }

  // 2. CREATE
  addProduct(product: Partial<Product>): Observable<Product> {
    return this.http.post<Product>(this.apiUrl, product).pipe(
      catchError(this.handleError)
    );
  }

  // 3. DELETE
  deleteProduct(id: number): Observable<boolean> {
    return this.http.delete<boolean>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An unknown error occurred!';
    if (error.error instanceof ErrorEvent) {
      // Client-side or network error
      errorMessage = `Client Error: ${error.error.message}`;
    } else {
      // Backend returned an unsuccessful response code
      errorMessage = `Server Error Code: ${error.status}\\nMessage: ${error.message}`;
    }
    return throwError(() => new Error(errorMessage));
  }
}
```

## Best Practices
1. **Always Type Responses**: Do not make requests using `this.http.get('/api')` without specifying a type. Always use types: `this.http.get<MyType>('/api')`.
2. **Separate HTTP logic from UI**: Keep `HttpClient` dependencies inside services. Components should consume services, keeping component classes clean.
3. **Use catchError Globally and Locally**: Handle common server errors (like 401s and 500s) globally in an interceptor, and handle component-specific validation or fallback logic in the component.

## Common Mistakes
* **Forgetting to Subscribe**: Making HTTP calls like `this.http.post(url, body)` without calling `.subscribe()`. Angular HTTP observables are cold, meaning the network request will not be sent unless subscribed to.
* **Creating Interceptor Loops**: Writing an authentication interceptor that refreshes expired tokens by making another HTTP request that triggers the same interceptor, causing an infinite loop.

## Interview Questions & Answers
### Q: Why do `HttpClient` methods return cold RxJS Observables?
**A**: They return cold observables because HTTP requests are transactional. The request is not sent until a subscriber calls `.subscribe()`. This allows you to chain operators (like `retry`, `catchError`, or `map`) to the request before it executes.

### Q: What is the difference between functional interceptors and class-based interceptors?
**A**: Functional interceptors (introduced in modern Angular) are lightweight functions registered directly in `provideHttpClient(withInterceptors([...]))`. Class-based interceptors require creating a service that implements the `HttpInterceptor` interface and registering it as a multi-provider in the legacy DI system.

## Summary
`HttpClient` manages REST API requests in Angular. Using functional interceptors, retry policies, and type-safe interfaces simplifies network requests, global error handling, and authorization flows.

---

Previous : [Reactive Forms](./15_Reactive_Forms.md) | Index : [Home](./00_index.md) | Next : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md)
