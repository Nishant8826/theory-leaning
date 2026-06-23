# Security Best Practices

## What is it?
Angular me Security un strategies, built-in features aur server configurations ka collection hai jo web application ko vulnerabilities (jaise Cross-Site Scripting - XSS, Cross-Site Request Forgery - CSRF, aur unauthorized data access) se protect karne me use hota hai.

## Why do we need it?
Modern web applications sensitive user data (jaise passwords, session auth tokens, aur billing logs) browser variables me store karte hain. XSS vulnerability attackers ko client browser page par malicious scripts execute karne ki permission deti hai, jisse session tokens steal ho sakte hain. Client code bases ko secure design karna aur templates constraints properly apply karna XSS risks ko resolve karta hai.

```
Attacker injects script tag ──> Angular sanitizes string by default (strips <script>) ──> Safe UI rendering

Attacker injects script tag ──> Developer bypasses security with bypassSecurityTrustHtml 
                            ──> Malicious script executes ──> Session token compromised (XSS exploit)
```

## How does it work?
1. **Sanitization**: Angular default behavior me dynamic value inputs ko raw text ki tarah handle karta hai aur dynamic HTML elements/script tags ko render hone se pehle sanitizes/clean kar deta hai.
2. **`DomSanitizer`**: Ek framework utility jiske zariye explicit trust relationships configure kar dynamic resources (jaise trusted SVG markup ya custom iframe URLs) ko bypass kar load kiya ja sake.
3. **Context-Specific Security**: Angular HTML context (HTML templates), Style context (styles), aur URL context ke distinct values aur security rules check automatically execute karta hai.
4. **CSRF (Cross-Site Request Forgery) Prevention**: Angular `HttpClient` server verification token check (`XSRF-TOKEN` check) out-of-the-box support automate karta hai, jisse dynamic network operations coordinate and secure hote hain.

## Impact
* **Application Architecture**: Built-in template protection patterns secure coding standard set karte hain.
* **Performance**: Lightweight sanitization mechanism bina compile checks speed ko drop kiye secure rendering perform karta hai.
* **Security**: Client applications standard web security benchmarks automatically fulfill ho jate hain.

## Real World Example
Jaise chat application me agar koi user input box me `<script>maliciousCode()</script>` enter karke submit kare, toh Angular automatically script tags ko filter/strip kar deta hai taaki screen par normal string display ho aur dynamic exploit run na ho sake.

## Syntax
* **Inject DomSanitizer**:
```typescript
private sanitizer = inject(DomSanitizer);
```
* **Bypass Sanitization**:
```typescript
this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl('https://trusted-site.com');
```

## Code Examples
Neeche CSRF token configure karne aur `DomSanitizer` utilize karne ka complete implementation setup design diya gaya hai:

### `app.config.ts`
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withXsrfConfiguration } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withXsrfConfiguration({
        cookieName: 'MY-XSRF-COOKIE',
        headerName: 'X-XSRF-TOKEN'
      })
    )
  ]
};
```

### `safe-render.component.ts`
```typescript
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-security-demo',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="security-box">
      <h3>Security Sandbox</h3>
      
      <h4>Default Sanitization (Strips script tags):</h4>
      <div [innerHTML]="rawUserContent"></div>

      <hr />

      <h4>Explicitly Trusted Content (Bypassed):</h4>
      <div [innerHTML]="safeUserContent()"></div>
    </div>
  `,
  styles: [`
    .security-box { border: 2px solid #dc2626; padding: 20px; border-radius: 8px; max-width: 450px; }
    h4 { margin-top: 10px; color: #991b1b; }
  `]
})
export class SecurityDemoComponent {
  private sanitizer = inject(DomSanitizer);

  rawUserContent = `
    <p>This is standard text.</p>
    <script>alert("XSS Vulnerability Executed!")</script>
    <div style="color: red;">Red styling applied.</div>
  `;

  safeUserContent = signal<SafeHtml>('');

  constructor() {
    const trustedHtml = '<strong style="color: green;">Explicitly trusted green text.</strong>';
    this.safeUserContent.set(
      this.sanitizer.bypassSecurityTrustHtml(trustedHtml)
    );
  }
}
```

## Best Practices
1. **Avoid `ElementRef.nativeElement` for DOM Mutations**: Direct DOM mutations (jaise `nativeElement.innerHTML = ...`) avoid karein. Humesha standard template data bindings ya `Renderer2` service ka use karein.
2. **Limit Bypassing Sanitization**: `DomSanitizer` bypass methods (jaise `bypassSecurityTrustHtml`) ka use restrict karein aur clean check ke baad hi manually trusted declare karein.
3. **Configure Content Security Policy (CSP) Headers**: Server side settings deployment configuration me strict CSP headers implement karein, jo unauthorized dynamic script loading ko block karein.

## Common Mistakes
* **Using DomSanitizer on raw user input**: Direct user inputs ko check kiye bina `DomSanitizer` ke bypass methods me pass karna, jisse XSS security checks bypass ho sakti hain.
* **Binding to Dynamic Resource URLs**: Dynamic URLs ko proper sanitization ya context constraints lagaye bina script variables or dynamic components parameters me access karna.

## Interview Questions & Answers
### Q: How does Angular protect applications from Cross-Site Scripting (XSS) attacks?
**A**: Angular dynamic values ko templates me render karne se pehle automatically sanitize karta hai. Agar value me unsafe HTML ya scripts tags aate hain, toh yeh unhe parse kar strip kar deta hai.

### Q: When and why should you use `DomSanitizer`?
**A**: Jab hume security constraints bypass karke intentionally external resources or unsafe elements load karne hon (jaise raw HTML ya safe iframe URLs), tab specific trust APIs (jaise `bypassSecurityTrustHtml`) use karne ke liye `DomSanitizer` use kiya jata hai.

## Summary
Angular applications standard features dynamic sanitization aur XSS protection implement karte hain. `DomSanitizer` explicit exceptions rules configure karne ke paths manage karta hai jo application layers and resources ko safe banate hain.

---

Previous : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md) | Index : [Home](./00_index.md) | Next : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md)
