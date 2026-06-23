# Directives

## What is it?

### Simplified Core Definition:
* **Component** ek **custom HTML tag** hota hai (jaise `<app-profile-card>`) jo aapke UI ke ek poore section ko define karta hai (iska apna HTML template, CSS styles, aur TS logic hota hai).
* **Directive** ek **custom HTML attribute** hota hai (jaise `<p appZoom>` me `appZoom`) jise aap **pehle se maujood HTML tags** (jaise `<button>`, `<p>`, ya `<div>`) par lagate hain taaki unhe naya behavior ya style diya ja sake bina original tags me badlaav kiye.

## Why do we need it?
Jab components pure visual view blocks ko represent karte hain, toh kai baar aapko existing HTML elements par aam aur reusable behaviors attach karne ki zaroorat hoti hai (jaise hover karne par tooltip dikhana, character inputs restrict karna, ya lazy rendering apply karna). Aise behaviors ko har component ke andar manually likhna duplicate code create karta hai. Directives is problem ko solve karti hain behavior ko ek single, standalone class me wrap karke jise kisi bhi HTML tag par apply kiya ja sakta hai.

```
Element:
<button appRipple>Save</button>

Under the hood:
Directive intercepts element ──> Attaches HostListeners (click/hover) ──> Updates HostBindings (style.background)
```

## How does it work?
1. **Component Directives**: Ek component structure ke level par directive hi hota hai jiske sath ek HTML template attached hoti hai.
2. **Attribute Directives**: Yeh element ke look-and-feel ya behavior ko badalte hain (jaise dynamic classes lagane ke liye `NgClass`, custom style badalne ke liye `NgStyle`, ya custom hover behaviors).
3. **Structural Directives**: Yeh DOM ke layout structure ko manipulate karte hain elements ko add, remove, ya swap karke. Inki pehchan asterisk `*` prefix se hoti hai (jaise legacy syntax me `*ngIf`, `*ngFor` jo background compilation me `@if` aur `@for` control flow blocks me map ho jate hain).
4. **Host Decoration**:
   - `@HostBinding`: Directive ki property ko host element (jis tag par directive lagaya hai) ki style/class properties ke sath direct bind karta hai.
   - `@HostListener`: Host element ke native events (jaise click, hover, scroll) ko capture karta hai aur directive method call karta hai.

## Impact
* **Application Architecture**: DOM utility behaviors ko component files se alag karke clean aur modular architecture banata hai.
* **Performance**: Lightweight aur compiler-optimized. Yeh compiler time par direct browser DOM modifications code me transpile ho jate hain.
* **Scalability**: Custom dynamic form validations, event listeners, aur tracking triggers ko ek baar likhkar poori application me use kiya ja sakta hai.

## Real World Example
Ek Custom directive `appClickOutside` ko drop-down menu par lagaya ja sakta hai taaki jab user drop-down area ke bahar kahin click kare, toh menu auto-close ho jaye.

## Syntax
* **Applying an attribute directive**: `<p appHighlight>Content</p>`
* **Host Binding**: `@HostBinding('style.color') textColor = 'blue';`
* **Host Listener**: `@HostListener('click', ['$event']) onClick(event: Event) { ... }`

## Code Examples
Neeche teen tarah ke directives ka custom integration example diya gaya hai:

### 1. Component Directive
```typescript
// alert-box.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-alert-box',
  standalone: true,
  template: `
    <div class="alert">
      <strong>Alert:</strong> <ng-content></ng-content>
    </div>
  `,
  styles: [`
    .alert { padding: 12px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 4px; }
  `]
})
export class AlertBoxComponent {}
```

### 2. Attribute Directive
```typescript
// hover-scale.directive.ts
import { Directive, HostListener, HostBinding, Input } from '@angular/core';

@Directive({
  selector: '[appHoverScale]',
  standalone: true
})
export class HoverScaleDirective {
  @Input() scaleFactor: number = 1.1;
  @Input() defaultColor: string = 'transparent';
  @Input() hoverColor: string = '#e0f2fe';

  // HostBinding connects class fields directly to HTML style properties
  @HostBinding('style.backgroundColor') backgroundColor: string = this.defaultColor;
  @HostBinding('style.transition') transition: string = 'transform 0.2s ease, background-color 0.2s';
  @HostBinding('style.transform') transform: string = 'scale(1)';

  // HostListener intercepts native browser events on the host element
  @HostListener('mouseenter') onMouseEnter() {
    this.backgroundColor = this.hoverColor;
    this.transform = `scale(${this.scaleFactor})`;
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.backgroundColor = this.defaultColor;
    this.transform = 'scale(1)';
  }
}
```

### 3. Structural Directive
```typescript
// delay-render.directive.ts
import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appDelayRender]',
  standalone: true
})
export class DelayRenderDirective {
  constructor(
    private templateRef: TemplateRef<any>,       // Represents the HTML template block
    private viewContainer: ViewContainerRef      // Represents the DOM anchor to render inside
  ) {}

  @Input() set appDelayRender(timeMs: number) {
    // Clear container first
    this.viewContainer.clear();

    // Delay dynamic insertion into DOM
    setTimeout(() => {
      this.viewContainer.createEmbeddedView(this.templateRef);
    }, timeMs);
  }
}
```

### 4. Demo Component
```typescript
// directive-demo.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlertBoxComponent } from './alert-box.component';
import { HoverScaleDirective } from './hover-scale.directive';
import { DelayRenderDirective } from './delay-render.directive';

@Component({
  selector: 'app-directive-demo',
  standalone: true,
  imports: [CommonModule, AlertBoxComponent, HoverScaleDirective, DelayRenderDirective],
  template: `
    <div class="container">
      <h3>1. Component Directive Example</h3>
      <app-alert-box>Your subscription is expiring soon!</app-alert-box>

      <hr>

      <h3>2. Attribute Directive Example</h3>
      <div class="card" appHoverScale [scaleFactor]="1.05" [hoverColor]="'#f0fdf4'">
        <h4>Hover over this card</h4>
        <p>This box will expand slightly and turn green.</p>
      </div>

      <hr>

      <h3>3. Structural Directive Example</h3>
      <div *appDelayRender="3000" class="delayed-content">
        <p>🎉 This content was delayed by 3 seconds before rendering in the DOM!</p>
      </div>
    </div>
  `,
  styles: [`
    .container { padding: 20px; font-family: sans-serif; }
    .card { border: 1px solid #10b981; padding: 16px; border-radius: 8px; max-width: 300px; cursor: pointer; }
    .delayed-content { padding: 12px; background: #e0e7ff; border-radius: 4px; color: #4338ca; font-weight: bold; }
  `]
})
export class DirectiveDemoComponent {}
```

## Best Practices
1. **Always Use `Renderer2` or Host Decorators**: Native browser elements ko direct change karna (`nativeElement.style.color = ...`) avoid karein, kyunki yeh Server-Side Rendering (SSR) environments me crash kar sakta hai. `@HostBinding` ya `Renderer2` ka use karein.
2. **Prefix Selectors**: Selector names ke sath hamesha custom app prefix (jaise `appHighlight`) use karein taaki future HTML standard elements ke sath naming collision na ho.
3. **Clean Up Listeners**: `@HostListener` internally events self-cleanup kar deta hai, par agar aapne manually custom event listeners lagaye hain toh memory leaks se bachne ke liye unhe destroy phase me remove karein.

## Common Mistakes
* **Using structural syntax on custom attributes**: Standard attribute directive ko structural format `*appHighlight` me call karna. Agar directive me `TemplateRef` aur `ViewContainerRef` defined nahi hain, toh yeh compiler build error throw karega.
* **Adding Directives with the Same Name as Native Attributes**: Element native attribute names (jaise `[class]`) se directive selector design karna, jo standard class settings ko break kar sakta hai.

## Interview Questions & Answers
### Q: What is the difference between a Component and a Directive?
**A**: Component ek specialized directive hai jiske paas template visual design hota hai. Directive ke paas apna template nahi hota; yeh existing tags behavior properties change karne ke liye attributes ke roop me apply hota hai.

### Q: What are `@HostBinding` and `@HostListener` used for?
**A**: `@HostBinding` host element properties (jaise classes ya styles) ko directive property values se sync rakhta hai. `@HostListener` host element events listener events capture karke logic code execute karta hai.

## Summary
Directives elements behavior, styling, aur layout modify karte hain. Attribute directives visual appearance dynamically change karte hain, jabki structural directives DOM configuration modify karte hain. Host decorators logic ko seedhe host element properties aur actions se connect rakhte hain.

---

Previous : [Pipes](./06_Pipes.md) | Index : [Home](./00_index.md) | Next : [Component Lifecycle](./08_Component_Lifecycle.md)
