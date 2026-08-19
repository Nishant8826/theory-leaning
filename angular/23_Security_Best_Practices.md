# Security Best Practices

## What is it?
Security in Angular refers to the built-in defenses, framework sanitization protocols, and architectural best practices designed to protect web applications against common web vulnerabilities—such as Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF/XSRF), and unauthorized data tampering.

## Why do we need it?
Modern web applications handle sensitive user information, session tokens, and financial records. If an application contains an XSS vulnerability, attackers can inject malicious JavaScript into the browser to steal active authentication tokens, hijack user sessions, or execute unauthorized transactions. 

Angular treats all untrusted values as dangerous by default, automatically sanitizing values before rendering them in the DOM to neutralize injection attacks.

```
Untrusted Input (Standard Angular Handling):
Attacker injects <script> ──> Angular sanitizes string (strips executable <script>) ──> Safe UI Rendering

Bypassing Security Unsafely:
Attacker injects <script> ──> Developer calls bypassSecurityTrustHtml(untrustedInput) 
                          ──> Malicious script executes ──> Session token compromised (XSS Exploit)
```

## How does it work?
1. **Automatic Contextual Sanitization**: Angular recognizes different security contexts:
   - **HTML**: Rendered inside `[innerHTML]`. Strips executable tags like `<script>`, `onload`, `onerror`.
   - **Style**: Rendered inside `[style]`. Validates safe CSS properties and URL functions.
   - **URL / ResourceURL**: Rendered inside `<a [href]>` or `<iframe [src]>`. Blocks dangerous URI schemes like `javascript:`.
2. **`DomSanitizer`**: An injectable service used to explicitly mark trusted strings (e.g., trusted SVG markup or external partner iframe URLs) when developers intentionally need to bypass Angular's built-in sanitization.
3. **Built-in CSRF / XSRF Defense**: `HttpClient` automatically reads the `XSRF-TOKEN` cookie (if present) and appends it as an `X-XSRF-TOKEN` header on mutating HTTP requests (POST, PUT, DELETE).
4. **Content Security Policy (CSP)**: Angular is designed to be fully compatible with strict CSP HTTP headers, eliminating the need for `unsafe-inline` or `unsafe-eval` scripts.

## Impact
* **Application Architecture**: Integrates automatic sanitization directly into the template compiler, enforcing security by default without developer overhead.
* **Performance**: Lightweight native sanitization adds virtually zero overhead during template evaluation.
* **Security**: Eliminates the vast majority of client-side XSS injection vectors out of the box.

## Real World Example
In a real-time messaging application, if a malicious user sends a chat message containing `<img src="x" onerror="stealSessionCookie()">`, Angular automatically strips the dangerous `onerror` event handler before inserting the HTML, rendering the broken image harmlessly without executing the attack script.

## Syntax
* **Injecting DomSanitizer**:
```typescript
private sanitizer = inject(DomSanitizer);
```
* **Explicitly Bypassing Sanitization for Trusted Content**:
```typescript
this.trustedUrl = this.sanitizer.bypassSecurityTrustResourceUrl('https://maps.google.com/embed?...');
```

## Code Examples
Below is a complete implementation demonstrating Angular's built-in sanitization, explicit `DomSanitizer` usage, and global XSRF cookie configuration:

### `app.config.ts` (XSRF Protection)
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withXsrfConfiguration } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withXsrfConfiguration({
        cookieName: 'XSRF-TOKEN',      // Name of the cookie issued by backend
        headerName: 'X-XSRF-TOKEN'     // Name of the HTTP header Angular attaches
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
      <h3>Angular Security Sandbox</h3>
      
      <!-- 1. Automatic Framework Sanitization -->
      <h4>Default Sanitization (Strips dangerous script tags):</h4>
      <div [innerHTML]="rawUntrustedContent" class="preview-box"></div>

      <hr />

      <!-- 2. Explicitly Trusted Content via DomSanitizer -->
      <h4>Explicitly Trusted Content (DomSanitizer):</h4>
      <div [innerHTML]="trustedContent()" class="preview-box"></div>
    </div>
  `,
  styles: [`
    .security-box { border: 2px solid #dc2626; padding: 24px; border-radius: 8px; max-width: 480px; font-family: sans-serif; }
    h4 { margin-top: 14px; color: #991b1b; }
    .preview-box { padding: 12px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 4px; }
  `]
})
export class SecurityDemoComponent {
  private sanitizer = inject(DomSanitizer);

  // Untrusted input containing a malicious script tag
  rawUntrustedContent = `
    <p>Standard paragraph text.</p>
    <script>console.error("XSS Script Execution Attempted!");</script>
    <span style="color: red; font-weight: bold;">Safe styled text.</span>
  `;

  trustedContent = signal<SafeHtml>('');

  constructor() {
    // Trusted HTML from an internal verified source
    const verifiedMarkup = '<strong style="color: green;">Verified & Trusted Server HTML.</strong>';
    
    // Explicitly bypass sanitization only when source is 100% verified
    this.trustedContent.set(
      this.sanitizer.bypassSecurityTrustHtml(verifiedMarkup)
    );
  }
}
```

## Best Practices
1. **Never Mutate DOM Directly with `ElementRef`**: Avoid writing `this.elementRef.nativeElement.innerHTML = userInput`. Direct DOM property assignments bypass Angular's security compiler completely. Use template bindings or `Renderer2`.
2. **Never Pass Untrusted User Input to `DomSanitizer`**: Never call `bypassSecurityTrustHtml(userInput)` on raw data from forum posts, URL query parameters, or form fields. Only sanitize hardcoded or cryptographically signed strings.
3. **Configure Strict Content Security Policy (CSP)**: Enforce strong CSP response headers on your web server (e.g., `default-src 'self'; script-src 'self'`).

## Common Mistakes
* **Using `DomSanitizer` as a General HTML Formatter**: Passing unvalidated user input into `bypassSecurityTrustHtml()` just to render rich text, which completely opens the door to XSS exploits.
* **Binding Unvalidated URLs to `src` Attributes**: Dynamically binding `<iframe [src]="userSuppliedUrl">` without URL validation, which could allow attackers to execute clickjacking or phishing payloads.

## Interview Questions & Answers
### Q: How does Angular protect against Cross-Site Scripting (XSS) attacks?
**A**: Angular treats all untrusted values as potentially malicious. When dynamic values are bound via `[innerHTML]`, `[href]`, or `[style]`, the Angular compiler passes the value through a contextual sanitizer that cleans dangerous tags (`<script>`, `onload`, `onerror`) and unsafe URI schemes (`javascript:`) before inserting them into the DOM.

### Q: When is it appropriate to use `DomSanitizer` in Angular?
**A**: `DomSanitizer` should be used only when you have trusted, verified HTML, CSS, or URLs (such as trusted embedded video players, internal sanitized SVG icons, or safe partner iframes) that Angular's default sanitizer would otherwise block. It should never be invoked on raw user inputs.

## Summary
Angular incorporates multi-layered security defenses by default. Automatic contextual sanitization prevents XSS attacks, built-in XSRF configuration protects against cross-site request forgery, and `DomSanitizer` provides secure, explicit control when handling verified external markup.

---

Previous : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md) | Index : [Home](./00_index.md) | Next : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md)
