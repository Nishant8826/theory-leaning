# Directives

## What is it?
Directives are classes that add new behaviors, styles, or DOM modifications to elements in your Angular templates. They act as instruction sets for Angular's HTML parser, instructing it to attach event handlers, toggle classes, or manipulate layout structures.

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
Below is an implementation of a custom **attribute directive** that changes background color and adds animations on mouse entry/exit.

```typescript
import { Directive, ElementRef, Renderer2, HostListener, HostBinding, Input, Component } from '@angular/core';

@Directive({
  selector: '[appHoverScale]',
  standalone: true
})
export class HoverScaleDirective {
  @Input() scaleFactor: number = 1.1;
  @Input() defaultColor: string = 'transparent';
  @Input() hoverColor: string = '#e0f2fe';

  // 1. HostBinding to dynamically set inline CSS properties
  @HostBinding('style.backgroundColor') backgroundColor: string = this.defaultColor;
  @HostBinding('style.transition') transition: string = 'transform 0.2s ease, background-color 0.2s';
  @HostBinding('style.transform') transform: string = 'scale(1)';

  constructor(private el: ElementRef, private renderer: Renderer2) {
    // Initial setup if needed
  }

  // 2. HostListener to intercept host events
  @HostListener('mouseenter') onMouseEnter() {
    this.backgroundColor = this.hoverColor;
    this.transform = `scale(${this.scaleFactor})`;
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.backgroundColor = this.defaultColor;
    this.transform = 'scale(1)';
  }
}

// Demo Component using the Directive
@Component({
  selector: 'app-directive-demo',
  standalone: true,
  imports: [HoverScaleDirective],
  template: `
    <div class="card" appHoverScale [scaleFactor]="1.05" [hoverColor]="'#f0fdf4'">
      <h4>Hover Scale Card</h4>
      <p>Hover over this card to watch the directive scale the container and swap its background color.</p>
    </div>
  `,
  styles: [`
    .card { border: 1px solid #10b981; padding: 16px; border-radius: 8px; max-width: 300px; cursor: pointer; }
  `]
})
export class DirectiveDemoComponent {}
```

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
