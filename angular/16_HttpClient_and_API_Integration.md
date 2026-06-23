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
1. **`provideHttpClient()`**: Application bootstrap ke waqt `app.config.ts` me HTTP services ko globally register karne ke liye `provideHttpClient()` ka use kiya jata hai.
2. **Type Safety**: API requests ko response type dynamically override karne ke liye strong models/interfaces support milta hai, jaise `http.get<Product[]>(url)`.
3. **Interceptors**: Yeh global handlers hote hain jo outgoing HTTP requests ya incoming responses ko process karte hain (jaise automatic headers set karna ya request intercept karna).
4. **RxJS Streams**: HTTP operations cold observables return karte hain, yaani jab tak hum unhe subscribe nahi karte, tab tak actual network call trigger nahi hota.

## Impact
* **Application Architecture**: API communications UI component class se completely decoupled hokar dedicated services me handle hoti hai.
* **Performance**: API caching configure karke network round trips ko optimize kiya ja sakta hai.
* **Security**: HTTP Interceptors request headers me secure credentials attach karte hain taaki access endpoints valid rahen.

## Real World Example
Jaise secure dashboard page me JWT Token add karne ke liye, hum ek auth interceptor likhte hain. Yeh interceptor har ek outgoing request ke header me token inject karta hai, jisse dynamic backend endpoints authenticate ho sakein.

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
1. **Always Type Responses**: Bina type ke HTTP requests (jaise `this.http.get('/api')`) call na karein. Hamesha response data models ke liye strict type parameters define karein, jaise `this.http.get<MyType>('/api')`.
2. **Separate HTTP logic from UI**: HTTP operations ko component templates ya components se seedhe call na karein. Humesha HTTP logic ko services me delegate karein aur component me sirf un methods ko call karein.
3. **Use catchError Globally and Locally**: Application level errors ko globally handle karne ke liye interceptor me `catchError` lagayein, aur components ke specific error responses ko handle karne ke liye local level par check karein.

## Common Mistakes
* **Forgetting to Subscribe**: HttpClient methods (jaise `this.http.post(...)`) call karte waqt `.subscribe()` call karna bhool jana. Jab tak hum observable stream ko subscribe nahi karte, tab tak request dispatch nahi hoti.
* **Creating Interceptor Loops**: Interceptor ke andar token refresh ya error fallback call karte waqt circular loop create kar dena, jisse request flow crash ho jaye.

## Interview Questions & Answers
### Q: Why do `HttpClient` methods return cold RxJS Observables?
**A**: `HttpClient` ke methods "cold" streams return karte hain. Iska matlab hai ki request tab tak fire nahi hoti jab tak client explicitly `.subscribe()` call na kare. Isse hum request pipeline ko subscribe karne se pehle modify ya abort kar sakte hain.

### Q: What is the difference between functional interceptors and class-based interceptors?
**A**: Functional interceptors simple JS functions hote hain jo dependency injection `inject()` use karte hain aur lightweight hote hain. Legacy class-based interceptors class structures hote hain jinki configuration aur registering dependency injection providers setup me extra boilerplate aur compile code lagta hai.

## Summary
`HttpClient` Angular applications me REST APIs ke sath communication set karne ke liye primary tool hai. Interceptors ke zariye headers, logging, token attach, aur security mechanisms ko globally manage kiya jata hai.

---

Previous : [Reactive Forms](./15_Reactive_Forms.md) | Index : [Home](./00_index.md) | Next : [RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md)
