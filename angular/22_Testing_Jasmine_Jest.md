# Testing (Jasmine & Jest)

## What is it?
Testing in Angular is the automated verification process that confirms individual code units (Components, Services, Pipes, Directives) and end-to-end user workflows operate according to specifications. Angular provides first-class support for Unit & Integration Testing (via Jasmine, Karma, or Jest/Vitest) and End-to-End (E2E) UI Testing (via Playwright or Cypress).

## Why do we need it?
Deploying untested frontend code to production risks shipping regressions, broken UI bindings, and application crashes directly to end users. Automated testing catches bugs early during development or in CI/CD pipelines, giving engineering teams high confidence when refactoring or adding new features.

```
The Testing Pyramid:
     ▲
    / \     E2E Testing (Playwright / Cypress) - Test complete user journeys in real browsers
   /   \    Integration Testing (TestBed) - Test component DOM bindings & event interactions
  /     \   Unit Testing (Jasmine / Jest) - Test pure TypeScript logic, calculations, & services
 ─────────
```

## How does it work?
1. **`TestBed`**: The primary Angular testing utility that configures an isolated, simulated Angular module environment to instantiate and inject components and services under test.
2. **Assertions & Matchers**: Test structure blocks (`describe`, `it`, `beforeEach`) and assertion checks (`expect(actual).toBe(expected)`, `toEqual()`, `toBeTruthy()`).
3. **Component Fixture (`ComponentFixture<T>`)**: A testing wrapper around a component instance that provides access to the component class, the rendered DOM tree (`fixture.nativeElement`), and manual change detection triggering (`fixture.detectChanges()`).
4. **`HttpTestingController`**: Angular's testing backend for intercepting outgoing `HttpClient` calls, verifying request URLs/methods, and flushing mock JSON responses without making real network calls.
5. **Spies & Mocks**: Jasmine spies (`spyOn()`) or Jest mocks to spy on method invocations and replace external dependencies with mock implementations.

## Impact
* **Application Architecture**: Writing testable code naturally encourages loose coupling, small focused functions, and disciplined dependency injection.
* **Performance**: Catches infinite loops, unhandled change detection cycles, and memory leaks before code reaches production.
* **Maintainability**: Automated tests serve as living documentation, ensuring that refactoring legacy code does not break existing application behavior.

## Real World Example
In an e-commerce checkout flow, automated tests verify that:
- The "Pay Now" button remains disabled until credit card validation passes.
- Clicking "Pay Now" triggers the `PaymentService.processOrder()` method once with correct payload parameters.
- If the payment API returns an error, an accessible alert banner is rendered in the DOM.

## Syntax
* **Service Testing Configuration**:
```typescript
beforeEach(() => {
  TestBed.configureTestingModule({
    providers: [MyService]
  });
  service = TestBed.inject(MyService);
});
```
* **Jasmine / Jest Assertion**: `expect(component.title).toEqual('Angular Academy');`

## Code Examples
Below are complete implementations for testing an HTTP service with `HttpTestingController` and testing a standalone component's DOM interactions:

### `product.service.spec.ts`
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
        provideHttpClientTesting() // Configures mock HTTP backend
      ]
    });

    service = TestBed.inject(ProductService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Asserts that no unhandled HTTP requests are left open
  });

  it('should fetch and return product list from API', () => {
    const mockProducts: Product[] = [
      { id: 1, title: 'Mechanical Keyboard', price: 120 },
      { id: 2, title: 'Gaming Mouse', price: 60 }
    ];

    service.getProducts().subscribe((data) => {
      expect(data.length).toBe(2);
      expect(data).toEqual(mockProducts);
    });

    // Expect a single GET request to the designated endpoint
    const req = httpMock.expectOne('https://api.escuelajs.co/api/v1/products');
    expect(req.request.method).toBe('GET');
    
    // Respond with mock data
    req.flush(mockProducts);
  });
});
```

### `counter.component.spec.ts`
```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <div>
      <span class="count-display">Value: {{ count() }}</span>
      <button class="btn-inc" (click)="increment()">Increment</button>
    </div>
  `
})
export class CounterComponent {
  count = signal(0);
  
  increment(): void { 
    this.count.update(c => c + 1); 
  }
}

describe('CounterComponent DOM & Interaction Tests', () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent] // Standalone components are imported directly
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // Initial change detection to render template bindings
  });

  it('should render the default initial count value of 0', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const text = compiled.querySelector('.count-display')?.textContent;
    expect(text).toContain('Value: 0');
  });

  it('should increment count and update DOM on button click', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const button = compiled.querySelector<HTMLButtonElement>('.btn-inc');

    // Simulate user button click
    button?.click();
    fixture.detectChanges(); // Trigger change detection to re-render DOM

    const text = compiled.querySelector('.count-display')?.textContent;
    expect(text).toContain('Value: 1');
  });
});
```

## Best Practices
1. **Always Isolate Unit Tests**: Mock external HTTP requests, routing dependencies, and third-party services using `provideHttpClientTesting()` or custom mock providers to ensure tests execute quickly and reliably in CI environments.
2. **Call `fixture.detectChanges()` Explicitly**: In unit tests, Angular does not run automatic change detection. You must explicitly invoke `fixture.detectChanges()` after modifying component properties or triggering DOM events.
3. **Always Call `httpMock.verify()` in `afterEach`**: Ensures that every expected HTTP call was made and that no unexpected requests were left pending.
4. **Use E2E Testing for Critical User Journeys**: Use Playwright or Cypress for full user flows (such as authentication, multi-step checkout, and file uploads).

## Common Mistakes
* **Omitting `httpMock.verify()`**: Missing verification calls can hide accidental duplicate HTTP requests or unhandled request timeouts.
* **Accessing DOM Elements Before Change Detection**: Querying native DOM elements immediately after component creation without calling `fixture.detectChanges()`, which results in empty or un-rendered template nodes.

## Interview Questions & Answers
### Q: What is the purpose of `TestBed` in Angular?
**A**: `TestBed` is Angular's core testing API that creates an isolated testing module environment. It allows developers to configure providers, import standalone components or modules, resolve mock dependencies, and instantiate components wrapped in a `ComponentFixture` for unit and integration testing.

### Q: Why do we use `HttpTestingController` instead of making real HTTP calls in unit tests?
**A**: Real network requests introduce flakiness, latency, and backend dependency into test suites. `HttpTestingController` intercepts Angular's `HttpClient` requests, allowing tests to verify request URLs, HTTP methods, and headers, and synchronously simulate server responses (`req.flush()`) or error scenarios (`req.error()`) without hitting a real server.

## Summary
Automated testing guarantees software stability, reliability, and maintainability. Using `TestBed`, `ComponentFixture`, and `HttpTestingController`, developers can thoroughly test TypeScript logic, template DOM bindings, and asynchronous API interactions with confidence.

---

Previous : [Performance Optimization](./21_Performance_Optimization.md) | Index : [Home](./00_index.md) | Next : [Security Best Practices](./23_Security_Best_Practices.md)
