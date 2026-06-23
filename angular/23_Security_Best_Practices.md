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
1. **Sanitization**: Angular by default saari dynamic user values ko untrusted (unsafe) treatment deta hai. Templates HTML elements variable inputs bindings compilation runtime par scripts tags filter mechanisms clean features run kar dynamic links save karta hai.
2. **`DomSanitizer`**: Angular default sanitization filters bypass engine coordinate interface. Agar hume target external assets source links (jaise dynamic external iframe URLs ya dynamic SVG markup) securely load settings override parameters trigger karne hon.
3. **Context-Specific Security**: Angular elements attributes dynamic environments safety checks context levels classify (HTML, Style, URL, Resource URL) categories me monitor karta hai aur validation rules check run karta hai.
4. **CSRF (Cross-Site Request Forgery) Prevention**: Angular `HttpClient` cookies validation coordinate logic support target (jaise `XSRF-TOKEN` values check) out of the box automate configure kar headers sets verify coordinate requests origins validation secure banata hai.

## Impact
* **Application Architecture**: Data properties injection secure template parameters setup enforce karta hai.
* **Performance**: Auto-sanitization procedures checks millisecond calculations limits execute dynamic check loops optimize rakhte hain.
* **Security**: Out of the box sanitizations standard client checks vulnerabilities mitigates dynamic logic check.

## Real World Example
Social chat application me user input field box me `<script>hack()</script>` malicious alert command code type karke parameters send karta hai. Angular validation check runtime script filter tags clean kar textual format me message screen standard rendering display settings apply kar safe rakhta hai.

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
Neeche CSRF token headers apply, dynamic HTML rendering safety checks aur `DomSanitizer` use logic integration model code sample configure kiya gaya hai:

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
1. **Avoid `ElementRef.nativeElement` for DOM Mutations**: Direct DOM changes native elements indicators coordinates scripts `innerHTML` bypass updates patterns apply checks avoid karein. Humesha `Renderer2` features standard template bindings structures utilize karein.
2. **Limit Bypassing Sanitization**: DomSanitizer methods properties bypass inputs logic updates systems (jaise `bypassSecurityTrustHtml`) use case values target control boundaries limits verify checks ke baad hi configure parameters set verify.
3. **Configure Content Security Policy (CSP) Headers**: Servers boundaries deployment coordinate setup me strict CSP HTTP headers define check apply, jo inline script executions variables settings block.

## Common Mistakes
* **Using DomSanitizer on raw user input**: User parameters values direct inputs options bypass sanitize wrappers me pass dynamic checks override code lines verify configurations set logic variables inject.
* **Binding to Dynamic Resource URLs**: Dynamic urls controls coordinate iframe targets sets parameters bypass checks filter dynamic logic controls execute check criteria ignore.

## Interview Questions & Answers
### Q: How does Angular protect applications from Cross-Site Scripting (XSS) attacks?
**A**: Angular dynamic bindings contexts input updates parameters sanitization rules systems automatically apply karke elements codes layout setup safety checks compile standard configure karta hai.

### Q: When and why should you use `DomSanitizer`?
**A**: DomSanitizer resources bypass systems templates check settings override structures maps coordinates check options limits use case values dynamic coordinate logic variables safe properties definitions target sets checks me select kiya jata hai.

## Summary
Angular web templates data values injection security controls systems manage karta hai. DomSanitizer interfaces overrides exceptions features inputs parameters checks setups safety boundaries details secure system setups handle rules execute karte hain.

---

Previous : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md) | Index : [Home](./00_index.md) | Next : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md)
