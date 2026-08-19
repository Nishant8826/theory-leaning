# Directives

## What is it?

### Core Definition:
* A **Component** is a **custom HTML tag** (e.g., `<app-profile-card>`) that defines an entire view section of your UI with its own dedicated HTML template, CSS styling, and TypeScript logic.
* A **Directive** is a **custom HTML attribute or marker** (e.g., `appHoverScale` in `<button appHoverScale>`) applied to **existing HTML elements** (such as `<button>`, `<p>`, or `<div>`) to extend their appearance, behavior, or DOM presence without rewriting the element.

## Why do we need it?
While components encapsulate entire visual blocks, developers frequently need to attach reusable behaviors to existing elements (such as tooltips, keyboard input masks, click-outside handlers, or ripple effects). Writing these behaviors inside every component creates massive code duplication. 

Directives solve this problem by encapsulating DOM-manipulation logic into standalone, reusable classes that can be attached to any HTML element.

```
Template Usage:
<button appRipple>Save</button>

Under the Hood:
Directive intercepts element ──> Attaches HostListeners (click/hover) ──> Updates HostBindings (style.background)
```

## How does it work?
1. **Component Directives**: Under the hood, a component is technically a directive that has an attached visual HTML template.
2. **Attribute Directives**: Modify the appearance or behavior of an existing element (e.g., `NgClass`, `NgStyle`, or custom hover/tooltip directives).
3. **Structural Directives**: Add, remove, or manipulate DOM nodes using `TemplateRef` and `ViewContainerRef`. They are denoted in template syntax with an asterisk prefix (e.g., legacy `*ngIf`, `*ngFor`, which compile to modern `@if` and `@for` control flow blocks).
4. **Host Decoration**:
   - `@HostBinding()`: Binds a directive class property directly to a property, style, or class on the host DOM element.
   - `@HostListener()`: Listens for native DOM events (such as `click`, `mouseenter`, `scroll`) on the host element and invokes the decorated directive method.

## Impact
* **Application Architecture**: Keeps DOM manipulation logic out of components, ensuring a clean and modular codebase.
* **Performance**: Directives are lightweight and compiler-optimized. They compile directly into high-efficiency DOM instruction calls.
* **Scalability**: Write custom validation rules, accessibility attributes, or tracking triggers once and reuse them across hundreds of templates.

## Real World Example
A custom `appClickOutside` directive attached to a dropdown or modal menu detects when a user clicks anywhere outside the designated container and automatically closes the dropdown.

## Syntax
* **Applying an attribute directive**: `<p appHighlight>Content</p>`
* **Host Binding**: `@HostBinding('style.color') textColor = 'blue';`
* **Host Listener**: `@HostListener('click', ['$event']) onClick(event: Event) { ... }`

## Code Examples
Below is a complete implementation featuring all three directive types:

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
    .alert { 
      padding: 12px; 
      background: #fee2e2; 
      border-left: 4px solid #ef4444; 
      border-radius: 4px; 
    }
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
  @Input() scaleFactor: number = 1.05;
  @Input() defaultColor: string = 'transparent';
  @Input() hoverColor: string = '#e0f2fe';

  // Connects directive properties directly to host element styles
  @HostBinding('style.backgroundColor') backgroundColor: string = this.defaultColor;
  @HostBinding('style.transition') transition: string = 'transform 0.2s ease, background-color 0.2s';
  @HostBinding('style.transform') transform: string = 'scale(1)';

  // Listens to native browser events on the host DOM element
  @HostListener('mouseenter') onMouseEnter(): void {
    this.backgroundColor = this.hoverColor;
    this.transform = `scale(${this.scaleFactor})`;
  }

  @HostListener('mouseleave') onMouseLeave(): void {
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
    private viewContainer: ViewContainerRef      // Represents the DOM container to render into
  ) {}

  @Input() set appDelayRender(timeMs: number) {
    // Clear container first
    this.viewContainer.clear();

    // Delay insertion into DOM
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
        <p>This box will smoothly expand and change background color.</p>
      </div>

      <hr>

      <h3>3. Structural Directive Example</h3>
      <div *appDelayRender="2500" class="delayed-content">
        <p>🎉 This content was delayed by 2.5 seconds before rendering into the DOM!</p>
      </div>
    </div>
  `,
  styles: [`
    .container { padding: 20px; font-family: sans-serif; }
    .card { border: 1px solid #10b981; padding: 16px; border-radius: 8px; max-width: 320px; cursor: pointer; }
    .delayed-content { padding: 12px; background: #e0e7ff; border-radius: 4px; color: #4338ca; font-weight: bold; }
  `]
})
export class DirectiveDemoComponent {}
```

## Best Practices
1. **Use `@HostBinding` and `@HostListener` Instead of Direct DOM APIs**: Avoid direct manipulation like `element.nativeElement.style.color = 'red'`. Direct DOM references can fail or crash in Server-Side Rendering (SSR) environments.
2. **Always Prefix Directive Selectors**: Use a custom prefix (such as `appHighlight` or `appClickOutside`) to avoid naming collisions with future standard HTML attributes.
3. **Clean Up Custom Event Handlers**: While `@HostListener` handles unbinding automatically when the directive is destroyed, any custom event listeners registered manually with `addEventListener` must be cleaned up in `ngOnDestroy` to prevent memory leaks.

## Common Mistakes
* **Using Asterisk `*` Syntax with Non-Structural Directives**: Adding `*` to an attribute directive (e.g., `*appHighlight`) triggers a compilation error unless the directive injects `TemplateRef` and `ViewContainerRef`.
* **Colliding with Native HTML Attributes**: Defining a selector like `[class]` or `[title]` that overrides native browser behavior and breaks standard styling.

## Interview Questions & Answers
### Q: What is the fundamental difference between a Component and a Directive?
**A**: A Component is a specialized directive that has an associated HTML template and view layout. A Directive does not have its own template; it is applied as an attribute or marker to existing HTML tags or components to modify their behavior, appearance, or presence in the DOM.

### Q: How do `@HostBinding` and `@HostListener` work?
**A**: `@HostBinding` allows a directive to bind one of its internal properties directly to a property, attribute, or style of the host DOM element. `@HostListener` attaches an event listener to the host element, intercepting user actions (such as clicks, mouse events, or keyboard strokes) and invoking a corresponding directive method.

## Summary
Directives are powerful tools for modifying element appearance, behavior, and DOM layout. Attribute directives dynamically alter styling and behavior, structural directives control DOM rendering, and host decorators maintain seamless communication between the directive logic and host HTML elements.

---

Previous : [Pipes](./06_Pipes.md) | Index : [Home](./00_index.md) | Next : [Component Lifecycle](./08_Component_Lifecycle.md)
