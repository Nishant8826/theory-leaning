# Testing (Jasmine & Jest)

## What is it?
Angular me Testing ka matlab hai yeh verify karna ki individual code units (jaise components aur services) aur complete user flows specs ke mutabik perform kar rahe hain. Angular unit tests (using Jasmine, Karma, ya Jest) aur End-to-End (E2E) UI testing (using Playwright ya Cypress) dono ko support karta hai.

## Why do we need it?
Bina test kiye code production par deploy karne se bugs create ho sakte hain jo user experience ko break kar sakte hain. Automated testing se development time ya CI/CD run me hi bugs trace ho jate hain, jisse safety confirmation milti hai ki naye changes se purana code break nahi hua hai.

```
Testing Pyramid:
     ▲
    / \     E2E Testing (Playwright / Cypress) - Test full user journeys
   /   \    Integration Testing (TestBed) - Test component DOM interactions
  /     \   Unit Testing (Jasmine / Jest) - Test pure logic & service APIs
 ─────────
```

## How does it work?
1. **`TestBed`**: Testing context me components aur services ko configure aur compile karne ke liye primary Angular utility class hai.
2. **Assertions**: Test files structure (`describe`, `it`) aur expectations verify checks (jaise `expect(val).toBe(true)`) execute karne wale functions.
3. **Component Fixture (`ComponentFixture`)**: Test component ka handler wrapper jo DOM interaction testing aur manual change detection trigger (`fixture.detectChanges()`) verify karne ka access deta hai.
4. **Mocking HTTP (`HttpTestingController`)**: Fake API responses return karke HTTP request flow aur response handling behaviors ko test karne ka tool.

## Impact
* **Application Architecture**: Code testable hone se modular architecture aur solid design pattern self-enforce ho jata hai.
* **Performance**: Infinite rendering loops aur event subscription memory leaks logic tests me hi pakad me aa jate hain.
* **Maintainability**: Unit tests documentation specs ki tarah behave karte hain jisse component refactoring safe aur easy ho jati hai.

## Real World Example
Jaise payment checkout component me testing yeh verify karti hai ki card details validate hone se pehle submit button locked rahey, aur invalid input par validator error display kare.

## Syntax
* **Service Testing Structure**:
```typescript
beforeEach(() => {
  TestBed.configureTestingModule({ providers: [MyService] });
  service = TestBed.inject(MyService);
});
```
* **Jasmine Assertion**: `expect(component.title).toEqual('New App');`

## Code Examples
Neeche dynamic HTTP service mocking aur DOM component interaction testing ke complete code examples diye gaye hain:

### `api-test.service.spec.ts`
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
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(ProductService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
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

    const req = httpMock.expectOne('https://api.escuelajs.co/api/v1/products');
    expect(req.request.method).toBe('GET');
    
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
    fixture.detectChanges();
  });

  it('should render default value', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.count-display')?.textContent).toContain('Value: 0');
  });

  it('should increment value on button click', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const button = compiled.querySelector('button');

    button?.click();
    fixture.detectChanges();

    expect(compiled.querySelector('.count-display')?.textContent).toContain('Value: 1');
  });
});
```

## Best Practices
1. **Always Isolate Unit Tests**: External services aur HTTP requests ko mock karne ke liye spies/mocks ya mock classes injection configure karein taaki test cases isolated pipeline me run ho saken.
2. **Call `fixture.detectChanges()`**: Component state change hone par UI template re-rendering updates check karne ke liye hamesha manually `fixture.detectChanges()` trigger karein.
3. **Write E2E Tests for Critical Paths**: Application ke main features (jaise authentication ya checkout dynamic paths) ko end-to-end testing systems (jaise Playwright) se verify karein.

## Common Mistakes
* **Forgetting `httpMock.verify()`**: Test case completion par `httpMock.verify()` call na karna, jisse unexpected pending network requests detect nahi ho pati hain.
* **Testing DOM elements before compile**: `compileComponents()` execute hone se pehle templates select/access karne ki koshish karna, jisse components instantiation compile errors throw kar dete hain.

## Interview Questions & Answers
### Q: What is the purpose of `TestBed` in Angular testing?
**A**: `TestBed` Angular applications ke components aur services unit testing ke liye testing sandbox environment create karta hai. Yeh standard dependencies aur mock inputs providers register karne aur components compile karne me help karta hai.

### Q: Why do we use `HttpTestingController` in unit tests?
**A**: `HttpTestingController` real HTTP backend calls ko block karke dynamic assertions verify karta hai. Yeh faked responses return karne (`flush()`) aur pending HTTP connections check settings verify karne ke options compile karta hai.

## Summary
Testing code behaviors aur system flows validation ensure karta hai. Unit testing (`TestBed` and assertions) controllers and templates rules check manage karte hain, jabki E2E tests complete browser features simulate karte hain.

---

Previous : [Performance Optimization](./21_Performance_Optimization.md) | Index : [Home](./00_index.md) | Next : [Security Best Practices](./23_Security_Best_Practices.md)
