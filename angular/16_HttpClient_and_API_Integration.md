# HttpClient and API Integration

## What is it?
`HttpClient` Angular ka ek built-in service utility module hai jo web applications ko remote servers ke sath HTTP protocol ke zariye communicate karne ki capability deta hai. Yeh browser ke native XMLHttpRequest API par based hai, response me RxJS Observables return karta hai, global request/response interception support karta hai, aur type-safe operations provide karta hai.

## Why do we need it?
Modern frontend applications ko data read aur write karne ke liye backend server APIs se connect hona padta. Browser ke standard `fetch` API ke comparison me, `HttpClient` me advanced configurations (jaise automatic JSON parsing, request/response interceptors jo header auth tokens append karne me use hote hain, dynamic progress tracking, aur RxJS streams integration) built-in milti hain, jisse API integration clear aur systematic ho jata hai.

```
API Request Flow:
Component triggers fetch ──> Service makes request ──> Auth Interceptor appends JWT token 
                          ──> Remote REST API Server ──> Error Interceptor parses codes (401/500) 
                          ──> Component receives data stream (RxJS Observable)
```

## How does it work?
1. **`provideHttpClient()`**: App configuration bootstrap options setups me HttpClient features initialize aur register karne ke liye use hota hai.
2. **Type Safety**: API calls requests (jaise `http.get<Product[]>(url)`) database parameters ko automatically mapping specifications ke target TypeScript models arrays/objects formats me convert kar deti hain.
3. **Interceptors**: Functions jo outgoing requests or incoming responses ko intercept karke request headers update, jwt auth token apply, ya error codes handling globally manage karte hain.
4. **RxJS Streams**: Saare network calls functions transactions base variables data return cold observables me deliver karte hain jo subscribe triggers apply hone par hi run parameters resolve karte hain.

## Impact
* **Application Architecture**: Data fetch operations backend APIs integrations components controls se move karke dynamic client services file me isolate rakhta hai.
* **Performance**: Interceptors me local caching logic build karke standard GET request server trips save kiye ja sakte hain.
* **Security**: Globally applied headers mechanism auth JWT settings standard maintain rakhta hai jisse automatic validations complete security checkpoints establish hote hain.

## Real World Example
Secure enterprise system dashboard me, functional interceptor automatic setup apply karta hai. Outgoing dynamic API request coordinate parameters me client authorization keys, JWT headers value index update settings background automatically write execute kar details forward parameters check trigger kar leta hai.

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
Neeche functional interceptors, custom error logic handle actions, automatic API retries aur complete backend CRUD actions handle karne wala services integration example configure kiya gaya hai:

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
      }
      return throwError(() => new Error(error.message || 'Server Error'));
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
      retry({ count: 2, delay: 1000 }),
      catchError(this.handleError)
    );
  }

  addProduct(product: Partial<Product>): Observable<Product> {
    return this.http.post<Product>(this.apiUrl, product).pipe(
      catchError(this.handleError)
    );
  }

  deleteProduct(id: number): Observable<boolean> {
    return this.http.delete<boolean>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An unknown error occurred!';
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client Error: ${error.error.message}`;
    } else {
      errorMessage = `Server Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(() => new Error(errorMessage));
  }
}
```

## Best Practices
1. **Always Type Responses**: Non-typed data load queries `this.http.get('/api')` avoid karein. Response models properties verification structures clean rakhne ke liye hamesha strict types use karein: `this.http.get<MyType>('/api')`.
2. **Separate HTTP logic from UI**: Components templates boundaries coordinate controllers clear rakhein. Components class API URLs variables direct access na karein, unhe services methods coordinate streams call targets par bind rakhein.
3. **Use catchError Globally and Locally**: Main application level exceptions checks error alerts logic globally interceptors context handlers check me write karein aur views specific exceptions configurations local catch parameters rules execute karein.

## Common Mistakes
* **Forgetting to Subscribe**: HttpClient methods use dynamic setup triggers, jaise `this.http.post(url, body)` call logic setup me `.subscribe()` block parameters skip rakhna. Observables system parameters values flow calls trigger nahi honge jab tak indicators variables subscribe actions handle na karein.
* **Creating Interceptor Loops**: Auth check validation token reload actions check flows me custom interceptors coordinates calls recursively loop limits evaluate validation criteria loop limits crash warnings throw kar deta hai.

## Interview Questions & Answers
### Q: Why do `HttpClient` methods return cold RxJS Observables?
**A**: HttpClient transactions based REST request systems return parameters elements me dynamic operations pipeline calculations checks flow rules apply settings trigger hone tak parameters execute blocks coordinate nahi karte jab tak client subscribe elements execution run functions trigger na kare.

### Q: What is the difference between functional interceptors and class-based interceptors?
**A**: Modern functional interceptors simple logic functions settings parameters patterns me direct registers optimize structures handle karte hain, jabki legacy class structures components updates details registers providers rules setups utilize karte hain jisme extra boilerplate setup configurations compile dependencies add ho jati hain.

## Summary
`HttpClient` Angular applications REST interface dynamic backend communications utilities options coordinate configure karta hai. Functional interceptors patterns, data filters retry methods validations pipelines layout setup optimize configurations manage karte hain.

---

Previous : [Reactive Forms](./15_Reactive_Forms.md) | Index : [Home](./00_index.md) | Next : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md)
