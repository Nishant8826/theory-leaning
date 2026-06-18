# Security Best Practices

## What is it?
Security in Angular involves the strategies, features, and configurations used to protect applications from vulnerabilities like Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), and unauthorized data access.

## Why do we need it?
Modern web applications handle sensitive user data (like passwords, session tokens, and personal details) and run scripts in browser environments. Vulnerabilities like XSS allow attackers to inject malicious scripts into pages, potentially stealing user sessions or credentials. Securing client-side code and configuring the browser properly helps prevent unauthorized script execution.

```
Attacker injects script tag ──> Angular sanitizes string by default (strips <script>) ──> Safe UI rendering

Attacker injects script tag ──> Developer bypasses security with bypassSecurityTrustHtml 
                            ──> Malicious script executes ──> Session token compromised (XSS exploit)
```

## How does it work?
1. **Sanitization**: Angular treats all user values as untrusted by default. When inserting values into templates via interpolation or bindings, it automatically sanitizes them, stripping out unsafe scripts or styling configurations.
2. **`DomSanitizer`**: A service used to bypass Angular's default sanitization when you explicitly trust a resource (e.g. embedding safe external IFrames or raw HTML).
3. **Context-Specific Security**: Angular classifies values into security contexts (HTML, Style, URL, Resource URL) and sanitizes them according to their context rules.
4. **CSRF (Cross-Site Request Forgery) Prevention**: Angular's `HttpClient` can read security tokens from cookies (such as `XSRF-TOKEN`) and append them to outgoing headers, ensuring requests originate from authenticated user sessions.

## Impact
* **Application Architecture**: Enforces secure data binding and input validation across components.
* **Performance**: Sanitization processes run quickly with minimal change detection overhead.
* **Security**: Automatic sanitization mitigates common client-side vulnerabilities out of the box.

## Real World Example
In a chat application, a user types `<script>maliciousCode()</script>` into a message field. Angular sanitizes this input, displaying it as plain text instead of executing it in other users' browsers.

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
Below is an implementation demonstrating how to render dynamic HTML safely, bypass sanitization for trusted resources, and configure CSRF cookie tracking.

### `app.config.ts` (CSRF Cookie Tracking Configuration)
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withXsrfConfiguration } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      // Configure client to read cookie and append token to headers
      withXsrfConfiguration({
        cookieName: 'MY-XSRF-COOKIE',
        headerName: 'X-XSRF-TOKEN'
      })
    )
  ]
};
```

### `safe-render.component.ts` (Sanitization Demonstration)
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
      
      <!-- 1. Default Sanitization (Safe) -->
      <h4>Default Sanitization (Strips script tags):</h4>
      <div [innerHTML]="rawUserContent"></div>

      <hr />

      <!-- 2. Bypassed Sanitization (Danger) -->
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

  // Untrusted input from user
  rawUserContent = `
    <p>This is standard text.</p>
    <script>alert("XSS Vulnerability Executed!")</script>
    <div style="color: red;">Red styling applied.</div>
  `;

  // Trusted content (using DomSanitizer to bypass checks)
  safeUserContent = signal<SafeHtml>('');

  constructor() {
    const trustedHtml = '<strong style="color: green;">Explicitly trusted green text.</strong>';
    
    // Explicitly bypass sanitization for trusted HTML
    this.safeUserContent.set(
      this.sanitizer.bypassSecurityTrustHtml(trustedHtml)
    );
  }
}
```

## Best Practices
1. **Avoid `ElementRef.nativeElement` for DOM Mutations**: Direct DOM mutations bypass Angular's sanitization checks, which can introduce XSS vulnerabilities. Use `Renderer2` or standard template bindings instead.
2. **Limit Bypassing Sanitization**: Use `DomSanitizer` methods (such as `bypassSecurityTrustHtml`) sparingly. Always sanitize inputs on the server before treating them as trusted in the client.
3. **Configure Content Security Policy (CSP) Headers**: Set up strict CSP HTTP headers on your server to restrict where scripts can be loaded from and block inline script executions.

## Common Mistakes
* **Using DomSanitizer on raw user input**: Passing raw user inputs directly into `bypassSecurityTrustHtml`. This allows users to execute malicious scripts in other users' browsers.
* **Binding to Dynamic Resource URLs**: Binding dynamic URLs to `iframe` sources without validating them, allowing attackers to load malicious external web resources.

## Interview Questions & Answers
### Q: How does Angular protect applications from Cross-Site Scripting (XSS) attacks?
**A**: Angular protects applications by treating all user values as untrusted by default. When values are inserted into templates, it automatically sanitizes them, stripping out unsafe tags (like `<script>` or `<iframe>`) and styling attributes.

### Q: When and why should you use `DomSanitizer`?
**A**: Use `DomSanitizer` when you need to bypass Angular's default sanitization to render trusted content (like safe external IFrames or pre-sanitized HTML). You should only use it on trusted values, as it disables security checks for that content.

## Summary
Angular sanitizes user inputs by default to protect applications from vulnerabilities like XSS. While services like `DomSanitizer` can bypass these security checks for trusted content, they should be used with caution.

---

Previous : [Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md) | Index : [Home](./00_index.md) | Next : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md)
