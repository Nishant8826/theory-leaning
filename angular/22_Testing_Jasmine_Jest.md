# Testing (Jasmine & Jest)

## What is it?
Testing in Angular involves verifying that individual units of code (like components and services) and full user scenarios behave as expected. Angular supports unit testing (using Jasmine, Karma, or Jest) and End-to-End (E2E) testing (using Playwright or Cypress).

## Why do we need it?
Deploying untested code changes to production can introduce bugs that break user interfaces or corrupt data. Automated testing helps catch bugs early during development or in CI/CD pipelines, ensuring that additions do not break existing functionality.

```
Testing Pyramid:
     ▲
    / \     E2E Testing (Playwright / Cypress) - Test full user journeys
   /   \    Integration Testing (TestBed) - Test component DOM interactions
  /     \   Unit Testing (Jasmine / Jest) - Test pure logic & service APIs
 ─────────
```

## How does it work?
1. **`TestBed`**: The primary Angular utility used to configure and initialize environments for testing components, services, and directives.
2. **Jasmine/Jest Assertions**: Frameworks that structure tests (`describe`, `it`) and check behavior using assertions (e.g. `expect(value).toBe(true)`).
3. **Component Fixture (`ComponentFixture`)**: A wrapper around a tested component that allows you to query the DOM, update inputs, and trigger change detection manually during testing.
4. **Mocking HTTP (`HttpTestingController`)**: Mocks network requests to verify how services handle successful API calls and server errors.

## Impact
* **Application Architecture**: Directs how decoupled and testable components are designed (thin views, thick services).
* **Performance**: Automated testing catches infinite change detection loops and memory leaks early.
* **Maintainability**: Clear test assertions document application behavior, making it easier to refactor code.

## Real World Example
In a checkout module, a unit test checks that the "Pay" button remains disabled until the user enters a valid credit card number. An integration test verifies that clicking the button sends the payment data to a gateway API.

## Syntax
* **Service Testing Structure**:
```typescript
beforeEach(() => {
  TestBed.configureTestingModule({ providers: [MyService] });
  service = TestBed.inject(MyService);
});
```
* **Jasmine Assertion**: `expect(component.title).toEqual('New App');`

## Hinglish Explanation

Testing ka simple matlab hai **"Code deploy hone se pehle check karna ki saare features sahi se kaam kar rahe hain"**. Angular me two types of testing key roles play karti hain:

### 1. Unit Testing (Individual files check)
* Ek akele component class, service ya pipe ke function ko isolated check karna.
* **`TestBed`:** Yeh ek temporary, virtual testing framework module setup karta hai jisme hum dynamic dependencies aur mock inject kar sakte hain.
* **`detectChanges()`:** JUnit test run hone par browser dynamic compile process control me nahi rehta, isliye test case variables change hone par component view compile check run karne ke liye hum manually `fixture.detectChanges()` execute karte hain.

### 2. HTTP Request Mocking (Fake network request)
* Unit tests me real server API requests block ki jati hain. Uske badle `HttpTestingController` use karke hum dynamic network response `.flush(mockData)` return karte hain taaki API validation flows local verification pipeline me check ho sakein.

## Code Examples
Below are implementation examples for a **Service Unit Test** (using `HttpTestingController`) and a **Component Test**.

### `api-test.service.spec.ts` (Service Unit Test)
```typescript
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ProductService, Product } from './product.service';

describe('ProductService Unit Tests', () => {
  let service: ProductService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ProductService,
        provideHttpClient(),
        provideHttpClientTesting() // Mock HttpClient
      ]
    });

    service = TestBed.inject(ProductService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Verify no open requests remain
  });

  it('should fetch products list successfully', () => {
    const mockProducts: Product[] = [
      { id: 1, title: 'Laptop', price: 999 },
      { id: 2, title: 'Phone', price: 499 }
    ];

    service.getProducts().subscribe((data) => {
      expect(data.length).toBe(2);
      expect(data).toEqual(mockProducts);
    });

    // Expect a single GET request to the API URL
    const req = httpMock.expectOne('https://api.escuelajs.co/api/v1/products');
    expect(req.request.method).toBe('GET');
    
    req.flush(mockProducts); // Flush mock data
  });
});
```

### `counter.component.spec.ts` (Component DOM Test)
```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <div>
      <span class="count-display">Value: {{ count() }}</span>
      <button (click)="increment()">Add</button>
    </div>
  `
})
export class CounterComponent {
  count = signal(0);
  increment() { this.count.update(c => c + 1); }
}

describe('CounterComponent DOM tests', () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // Trigger initial change detection
  });

  it('should render default value', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.count-display')?.textContent).toContain('Value: 0');
  });

  it('should increment value on button click', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const button = compiled.querySelector('button');

    button?.click(); // Simulate user click
    fixture.detectChanges(); // Render updated state

    expect(compiled.querySelector('.count-display')?.textContent).toContain('Value: 1');
  });
});
```
## Best Practices
1. **Always Isolate Unit Tests**: Mock external dependencies (like HTTP services) using spy utilities to verify class logic in isolation.
2. **Call `fixture.detectChanges()`**: Always call `detectChanges()` after modifying properties or triggering events in component tests to render updates in the DOM.
3. **Write E2E Tests for Critical Paths**: Use Playwright or Cypress to write tests for critical user journeys (like login, checkout, or billing) to ensure they work in real browser environments.

## Common Mistakes
* **Forgetting `httpMock.verify()`**: Forgetting to call `verify()` in HTTP tests, which can allow unexpected network requests to pass silently and cause tests to behave unpredictably.
* **Testing DOM elements before compile**: Querying component template elements before calling `compileComponents()` or `fixture.detectChanges()`, which returns null because the template hasn't compiled yet.

## Interview Questions & Answers
### Q: What is the purpose of `TestBed` in Angular testing?
**A**: `TestBed` is an API provided by the Angular testing utility. It configures and initializes environments for testing components, services, and directives, creating dynamic test modules that let you inject mocks and compile templates.
* **Hinglish Explanation**: `TestBed` Angular ka primary testing tool hai jo test hone wale components/services ke liye ek "Fake Angular Module" (virtual environment) configure aur initialize karta hai. Iski madad se hum dependency injection set kar sakte hain, components/templates ko compile kar sakte hain, aur unke instances create karke testing kar sakte hain.

### Q: Why do we use `HttpTestingController` in unit tests?
**A**: We use `HttpTestingController` to mock backend network requests. It intercepts HTTP calls made by services, checks request details (like URLs and HTTP methods), and returns mock data using `.flush()` to test success and error flows without making real network requests.
* **Hinglish Explanation**: Unit testing me actual network request nahi chalani chahiye. `HttpTestingController` ka use API calls ko mock (fake) karne ke liye kiya jata hai. Yeh component ya service dwara hone wali HTTP calls ko intercept (rok) leta hai, aur hum `.flush(mockData)` function ka use karke custom data supply karte hain taaki different scenarios (success ya errors) ko local network ke bina test kiya ja sake.

## Summary
Testing validates the behavior of components and services. Unit tests use `TestBed` and Jasmine/Jest to check logic, while E2E tools like Playwright and Cypress verify user flows in real browser environments.

---

Previous : [Performance Optimization](./21_Performance_Optimization.md) | Index : [Home](./00_index.md) | Next : [Security Best Practices](./23_Security_Best_Practices.md)
