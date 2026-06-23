# Testing (Jasmine & Jest)

## What is it?
Angular me Testing ka matlab hai yeh verify karna ki individual code units (jaise components aur services) aur complete user pathways behaviors specs ke mutabik perform kar rahe hain. Angular unit tests (using Jasmine, Karma, ya Jest) aur End-to-End (E2E) UI scripts tests (using Playwright ya Cypress) dono mechanisms supports provide karta hai.

## Why do we need it?
Bina test kiye code changes ko production par deploy karne se bugs create ho sakte hain jo UI elements ko break kar deta hai ya data corrupt kar sakta hai. Automated testing se development phase me ya CI/CD pipeline runs me hi bugs early trace ho jate hain, jisse yeh safety confirmation milti hai ki naye changes se existing features parameters break nahi huye hain.

```
Testing Pyramid:
     ▲
    / \     E2E Testing (Playwright / Cypress) - Test full user journeys
   /   \    Integration Testing (TestBed) - Test component DOM interactions
  /     \   Unit Testing (Jasmine / Jest) - Test pure logic & service APIs
 ─────────
```

## How does it work?
1. **`TestBed`**: Component parameters testing environments configurations, compile, aur dependency injection setups create karne ke liye primary Angular utility class framework.
2. **Jasmine/Jest Assertions**: Test files structure (`describe`, `it`) maintain karne aur dynamic expectations parameters outputs verify checks (jaise `expect(val).toBe(true)`) execute karne wale tools.
3. **Component Fixture (`ComponentFixture`)**: Test component logic control panel wrapper. Change detection triggers manually execute karne ka feature deta hai.
4. **Mocking HTTP (`HttpTestingController`)**: Fakes network routes setups parameters manage check, jo services backend data API responses status handle scenarios test setups coordinate karta hai.

## Impact
* **Application Architecture**: Solid code design decouple pattern (lightweight views interfaces, robust business logic services) follow rules enforce karta hai.
* **Performance**: UI infinite loop bugs, event leaks variables, aur memory crash points testing me pehle hi pakad me aa jate hain.
* **Maintainability**: Clear testing cases configurations documentation components behaviour specs represent karte hain jisse refactoring execution easy ho jati hai.

## Real World Example
Payment billing checkout component testing flow me, unit test check execute karta hai ki credit card details number logic correct patterns checks verify settings trigger status validation complete hone tak submit operations button locked position target state default ensure kare.

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
Neeche dynamic HTTP Mock service testing aur DOM visual elements check unit test script design coordinate components check options configurations models compile examples diye gaye hain:

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
1. **Always Isolate Unit Tests**: External dependencies coordinate API classes parameters coordinates spy functions triggers mock settings check verify isolated test pipelines configure karein.
2. **Call `fixture.detectChanges()`**: Component parameters values mock UI templates updates verify checks limits updates render coordinates apply setups me hamesha manually change detector check update method `detectChanges()` trigger call use karein.
3. **Write E2E Tests for Critical Paths**: Application core logic paths (jaise login options checkout flow transactions) automation verify test checks ke liye standard Playwright E2E files define karein.

## Common Mistakes
* **Forgetting `httpMock.verify()`**: Mock requests check verify assertions parameters calls block coordinates end me `verify()` tag call clean features miss karna, jo unexpected network pending queries ignore updates warnings throw kar leta hai.
* **Testing DOM elements before compile**: Compile components structures actions trigger declarations sets parameters initialization calculations run `compileComponents()` coordinates call setup se pehle elements select access karna (null target values warnings check).

## Interview Questions & Answers
### Q: What is the purpose of `TestBed` in Angular testing?
**A**: `TestBed` Angular applications components services unit testing config environment settings initialize aur mock inputs components compile setups manage coordinate classes setup target handle karta hai.

### Q: Why do we use `HttpTestingController` in unit tests?
**A**: Unit tests parameters setup limits me backend connection block options coordinates mock checks compile setups use handles controllers verify parameters, `flush()` dynamic payloads logic test coordinate paths utilize setups configure checks implement karke.

## Summary
Testing applications scripts codes dynamic behaviors control checks coordinate verify karta hai. Unit test codes validation `TestBed` checks and assertions configurations coordinates maintain check run, play scripts browsers E2E testing systems safe systems setups manage rules ensure karte hain.

---

Previous : [Performance Optimization](./21_Performance_Optimization.md) | Index : [Home](./00_index.md) | Next : [Security Best Practices](./23_Security_Best_Practices.md)
