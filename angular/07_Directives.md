# Directives

## What is it?
Directives are classes that add new behaviors, styles, or DOM modifications to elements in your Angular templates. They act as instruction sets for Angular's HTML parser, instructing it to attach event handlers, toggle classes, or manipulate layout structures.

### Simplified Core Definition:
* **A Component** is a **custom HTML tag** (like `<app-profile-card>`) that defines an entire section of your UI (it has its own HTML template, CSS styles, and TS logic).
* **A Directive** is a **custom HTML attribute** (like `appZoom` in `<p appZoom>`) that you attach to **already existing HTML tags** (like `<button>`, `<p>`, or `<div>`) to give them new behaviors or styles without modifying the original tags.


## Why do we need it?
While components represent whole visual view blocks, you often need to attach general, reusable behaviors to existing elements (such as showing a tooltip on hover, restricting character inputs, or lazily revealing an element). Writing these behaviors directly inside every component creates duplicate code. Directives solve this by encapsulating visual behavior in standalone decorators that can be applied to any HTML tag.

```
Element:
<button appRipple>Save</button>

Under the hood:
Directive intercepts element ──> Attaches HostListeners (click/hover) ──> Updates HostBindings (style.background)
```

## How does it work?
1. **Component Directives**: A component is structurally a directive with an attached HTML template.
2. **Attribute Directives**: Change the appearance or behavior of an element (e.g. `NgStyle`, `NgClass`, custom highlight behavior).
3. **Structural Directives**: Shape the DOM layout by adding, removing, or swapping element subtrees. They are recognized by the asterisk prefix `*` (e.g. `*ngIf`, `*ngFor` in legacy syntax, and mapped to `@if` / `@for` compilers internally).
4. **Host Decoration**:
   - `@HostBinding`: Binds a host element property (e.g., class names, style attributes) directly to a directive property.
   - `@HostListener`: Listens for events on the host element (e.g., clicks, hover, scroll) and executes handler methods.

## Impact
* **Application Architecture**: Decouples DOM behavior from component presentation, creating modular utility classes.
* **Performance**: Lightweight and compiler-optimized. They compile directly to surgical DOM adjustments.
* **Scalability**: Custom validation, event listeners, and tracking triggers can be written once and shared across teams.

## Real World Example
A directive like `appClickOutside` can be applied to a popup menu to close it automatically when a user clicks anywhere else on the screen.

## Syntax
* **Applying an attribute directive**: `<p appHighlight>Content</p>`
* **Host Binding**: `@HostBinding('style.color') textColor = 'blue';`
* **Host Listener**: `@HostListener('click', ['$event']) onClick(event: Event) { ... }`

## Code Examples

Here are the complete implementations for the three types of directives in Angular.

### 1. Component Directive (A Directive with a Template)
Every Angular component is structurally a Directive with a visual HTML view.
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

### 2. Attribute Directive (Modifying Appearance & Behavior)
This custom attribute directive scales elements up on hover and changes the background color using parameters, `@HostBinding`, and `@HostListener`.
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

### 3. Structural Directive (Modifying HTML Layout & DOM Structure)
Custom structural directives require `TemplateRef` (the HTML content inside the element to render) and `ViewContainerRef` (the container location where it should be inserted). The asterisk `*` prefix in HTML tells Angular to translate the tag into a `<ng-template>`.
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

### 4. Demo Component (Using All Three Directives)
Below is the integration component demonstrating how to import and apply all three types of directives in your templates:
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
      <!-- AlertBoxComponent acts as a custom HTML tag -->
      <app-alert-box>Your subscription is expiring soon!</app-alert-box>

      <hr>

      <h3>2. Attribute Directive Example</h3>
      <!-- appHoverScale modifies visual scale and style on hover -->
      <div class="card" appHoverScale [scaleFactor]="1.05" [hoverColor]="'#f0fdf4'">
        <h4>Hover over this card</h4>
        <p>This box will expand slightly and turn green.</p>
      </div>

      <hr>

      <h3>3. Structural Directive Example</h3>
      <!-- *appDelayRender delays the rendering of the paragraph in the DOM by 3 seconds -->
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

### Hinglish Explanation of Examples:
* **Attribute Directive (`appHoverScale`)**: Humne decorators `@HostBinding` aur `@HostListener` ka use kiya hai. Jaise hi mouse card par enter karta hai, listen event fire hota hai aur `backgroundColor` aur `transform` class variables badal jate hain, jisse direct browser element style modify ho jaldi hai.
* **Structural Directive (`*appDelayRender`)**: Angular jab asterisk (`*`) dekhta hai, toh background mein is section ko ek `<ng-template>` bana deta hai jo tab tak render nahi hota jab tak hum custom TS logic se container mein create node command fire na karein. Humne `ViewContainerRef.createEmbeddedView()` ka use karke 3 seconds baad template render kiya hai.


## Best Practices
1. **Always Use `Renderer2` or Host Decorators**: Do not access `element.style.color = ...` via raw DOM references (`nativeElement.style`), as this breaks server-side rendering (SSR) environments.
2. **Prefix Selectors**: Always use a camelCase prefix (such as your app name, e.g. `appHighlight`) to prevent collisions with future native HTML elements.
3. **Clean Up Listeners**: While `@HostListener` cleans up automatically, if you set event listeners manually, ensure you destroy them to prevent memory leaks.

## Common Mistakes
* **Using structural syntax on custom attributes**: Attempting to call an attribute directive as `<div *appHighlight>`. If the directive does not use `TemplateRef` and `ViewContainerRef`, it will throw a compile error.
* **Adding Directives with the Same Name as Native Attributes**: Creating a directive with a generic selector like `[class]`, which can conflict with native class assignments.

## Interview Questions & Answers
### Q: What is the difference between a Component and a Directive?
**A**: A component is structurally a directive that has an associated HTML template and style definitions. A directive is a class without a template that attaches styles or behavior to existing DOM elements.

### Q: What are `@HostBinding` and `@HostListener` used for?
**A**: `@HostBinding` binds a directive property to a DOM property of the host element, allowing the directive to update host properties. `@HostListener` binds a host element event to a directive handler method, allowing the directive to respond to user interactions on that element.

## Summary
Directives extend template capabilities by modifying styles, behaviors, and layout structures. Attribute directives change element appearance and behavior, while structural directives modify the DOM tree. Host decorators connect directive logic directly to host element properties and events.

---

Previous : [Pipes](./06_Pipes.md) | Index : [Home](./00_index.md) | Next : [Component Lifecycle](./08_Component_Lifecycle.md)
