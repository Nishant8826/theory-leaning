# Beginner Interview Prep

## What is it?
Beginner Interview Preparation un foundational concepts, syntax conventions, aur framework features ka compilation hai jo developers ko entry-level Angular roles ke liye interview dete waqt pata hone chahiye.

## Why do we need it?
Structured preparation ke bina interview dena challenging ho sakta. Core concepts—jaise component structure, interpolation, direct bindings, aur setup CLI tools—ko review karne se developers ko confidence ke sath questions ke answers dene aur apne solid technical foundations ko demonstrate karne me help milti hai.

```
Preparation Flow:
Review Core Definitions ──> Study Direct Bindings ──> Practice CLI Commands ──> Build Simple Demos ──> Ace the Interview
```

## How does it work?
1. **Foundations Check**: Yeh cover karta hai ki Angular kya hai, single-page application (SPA) architectures, aur setup tools.
2. **Template Binding**: Interpolation, property/event binding, aur directive properties ki knowledge ko test karta hai.
3. **TypeScript Integration**: Variables, classes, aur interfaces ke basic understandings ko verify karta hai.

## Impact
* **Application Architecture**: Component-driven code layouts ki solid understanding ko establish karta hai.
* **Performance**: Angular CLI aur clean bindings ke use ko promote karta hai taaki common performance pitfalls se bacha ja sake.
* **Scalability**: Developers ko basic components ko sahi tareeqe se structure karne me help karta hai, jisse aage chalkar bade applications banana easy ho jata hai.

## Real World Example
Ek entry-level candidate se technical interview ke dauran component aur template ke beech ka difference pucha jata hai. Candidate explain karta hai ki components behavior ko manage karte hain jabki templates layout ko define karte hain, jo framework ki architecture ke baare me ek clear understanding ko demonstrate karta hai.

## Syntax
Ek basic component structure:
```typescript
@Component({
  selector: 'app-hello',
  standalone: true,
  template: `<p>Hello, {{ name }}!</p>`
})
export class HelloComponent {
  name = 'World';
}
```

## Code Examples
Neeche ek basic component ka implementation diya gaya hai jo interpolation, click events, aur list directives ko cover karta hai.

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-greet-box',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="greet-card">
      <h2>Hello, {{ guestName }}!</h2>
      <button (click)="changeName()">Greet Admin</button>
      
      <h4>Core Frameworks:</h4>
      <ul>
        <li *ngFor="let item of frameworks">{{ item }}</li>
      </ul>
    </div>
  `,
  styles: [`
    .greet-card { border: 1px solid #10b981; padding: 15px; border-radius: 6px; max-width: 250px; }
  `]
})
export class GreetBoxComponent {
  guestName = 'Guest';
  frameworks = ['Angular', 'React', 'Vue'];

  changeName() {
    this.guestName = 'Admin';
  }
}
```

## Best Practices
1. **Always Use the Angular CLI**: Standard structures ko maintain karne ke liye components, services, aur directives ko scaffold karne ke liye CLI generator commands ka use karein.
2. **Enable Strict TypeScript Mode**: Common runtime errors se bachne ke liye strict checking values ke liye TypeScript ko configure karein.
3. **Write Thin Component Classes**: Data fetching aur business calculations ko services ko delegate karein, taaki components strictly presentation par hi focus karein.

## Common Mistakes
* **Mutating DOM Elements Directly**: Component classes ke andar native DOM APIs (jaise `document.getElementById`) ka use karna. Yeh Angular ke change detection ko bypass karta hai aur rendering bugs create kar sakta hai.
* **Forgetting Parentheses in Interpolation**: Class me bina property define kiye template me `{{ myProperty }}` likh dena, jisse compilation errors aate hain.

## Interview Questions & Answers

### Q1: What is Angular and what are its main features?
**A**: Angular ek component-based front-end framework hai jise Google ne banaya hai. Isme routing, forms management, dependency injection, aur API requests ke liye HttpClient out-of-the-box built-in milte hain. Yeh koii third-party packages ke bina Single Page Applications (SPAs) banane ke liye full-featured environment hai.

### Q2: What is the difference between a Component and a Directive?
**A**: Component ke paas apna khud ka ek HTML template aur CSS styles hote hain (yeh UI page ka visual block represent karta hai). Directive ke paas apna koi HTML template nahi hota, yeh pehle se bane kisi HTML tag par lag kar uske attributes, styles ya behavior ko update karne ke kaam aata hai (jaise hover event par dynamic styles lagana).

### Q3: What is Interpolation and how is it written?
**A**: Interpolation ek direct data representation method hai jiske zariye component class ke variables ya calculations ko template (HTML) me show kiya jata hai. Iska syntax double curly braces `{{ variableName }}` hota hai. Angular internally is value ko text string me badal kar display kar deta hai.

### Q4: What are the main bindings available in templates?
**A**: 
1. **Interpolation**: Normal variables ko template me display karne ke liye: `{{ name }}`.
2. **Property Binding**: Element attributes me dynamic variables pass karne ke liye: `[src]="imageUrl"`.
3. **Event Binding**: Browser click ya press events capture karne ke liye: `(click)="save()"`.
4. **Two-Way Binding**: Input elements aur component variables ko aapas me dynamically sync (do-tarfa) rakhne ke liye: `[(ngModel)]="name"`.

### Q5: What is the purpose of the Angular CLI?
**A**: Angular CLI ek utility command-line assistant hai jo developer ke basic repetitive tasks ko automatic handle karta hai. Iska use project setup, naye components ya services generate karne (`ng generate`), local server test run karne (`ng serve`), aur final production build compile karne (`ng build`) me hota hai.

### Q6: Explain what Standalone Components are.
**A**: Standalone Components bina kisi extra container module (`NgModule`) ke direct execute ho sakte hain. Inhe component metadata me `standalone: true` set karke define kiya jata hai, aur inki dependencies ko direct `imports: [...]` block me import kar liya jata hai, jisse code reuse aur modular layout setup easy ho jata hai.

## Summary
Beginner level interviews core foundations jaise CLI tools, component setups, interpolation, aur template bindings par focus karte hain. In concepts ko review karne se candidates ko unki solid technical baselines demonstrate karne me help milti hai.

---

Previous : [Real World E-Commerce Project](./27_Real_World_ECommerce_Project.md) | Index : [Home](./00_index.md) | Next : [Intermediate Interview Prep](./29_Interview_Prep_Intermediate.md)
