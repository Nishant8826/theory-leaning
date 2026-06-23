# Setup and Environment

## What is it?
Angular environment setup karne me Node.js, npm (Node Package Manager), aur Angular Command Line Interface (CLI) install karna shamil hai. Yeh tools TypeScript compile karte hain, external libraries manage karte hain, local development servers start karte hain, aur production ke liye code bundle karte hain.

## Why do we need it?
Browsers native roop se TypeScript, Angular templates, ya modern CSS formats (SASS) ko nahi samajhte. Hamein ek development environment chahiye taaki:
1. Files ko standard JavaScript, CSS, aur HTML me compile kiya ja sake.
2. Dependencies (jaise RxJS, Tailwind, Angular Material) ko manage kiya ja sake.
3. Quick iteration ke liye Hot Module Replacement (HMR) ke sath local development server run kiya ja sake.

```
Development:
[TS Files + Styles] ──> Angular CLI ──> Vite/Webpack compiler ──> Browser Execution (HTML/JS/CSS)
```

## How does it work?
1. **Node.js**: Yeh runtime environment hai jo browser ke bahar developer tools ko execute karta hai.
2. **npm**: Yeh registry repository hai jahan se hum Angular core aur secondary packages download karte hain.
3. **Angular CLI**: Command-line orchestration tool jo code generate karta hai (components, services), dev server start karta (`ng serve`), application build karta (`ng build`), aur tests run karta (`ng test`).

## Impact
* **Application Architecture**: Poori team ke liye ek standard project folder layout ensure karta hai.
* **Performance**: Dev mode me fast build ke liye CLI Vite ka use karta hai aur production build ke liye Webpack/esbuild use karta hai.
* **Maintainability**: `ng update` command ke zariye Angular major versions ke beech smooth migration possible hota hai.

## Real World Example
Ek professional team environment me, naye developers sirf ek single command (`npm install` aur uske baad `ng serve`) chala kar apna workspace setup kar lete hain aur kuch hi minutes me local application run karne lagte hain.

## Syntax
Basic CLI commands:
```bash
# Install CLI globally
npm install -g @angular/cli

# Create a new standalone application
ng new my-app --standalone --routing --style=css

# Run development server
ng serve

# Build production assets
ng build
```

## Code Examples
Ek typical Angular setup me `package.json` file aisi dikhti hai:

```json
{
  "name": "angular-academy",
  "version": "0.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test"
  },
  "dependencies": {
    "@angular/animations": "^18.0.0",
    "@angular/common": "^18.0.0",
    "@angular/compiler": "^18.0.0",
    "@angular/core": "^18.0.0",
    "@angular/forms": "^18.0.0",
    "@angular/platform-browser": "^18.0.0",
    "@angular/platform-browser-dynamic": "^18.0.0",
    "@angular/router": "^18.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.0"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^18.0.0",
    "@angular/cli": "^18.0.0",
    "@angular/compiler-cli": "^18.0.0",
    "typescript": "~5.4.0"
  }
}
```

## Best Practices
1. **Local Node Version**: Developers ke beech Node.js versions ko synchronous rakhne ke liye Node Version Manager (`nvm`) ka use karein.
2. **Run via npm Scripts**: Global CLI ko directly use karne ke bajaye, `npm run start` ya `npm run build` jaise local scripts use karein taaki CI/CD platforms par versions consistent rahein.
3. **Keep CLI updated**: CLI version ko humesha Angular framework version ke sath align rakhein.

## Common Mistakes
* **Global/Local CLI Mismatches**: Ek globally outdated CLI par commands run karna jo local project packages ke sath conflict kare. Ise door karne ke liye `npx ng <command>` ka use karein.
* **Not using standard folders**: Manually files banana ke bajaye CLI generator commands (`ng generate`) use karein, nahi toh files connect karne me galti ho sakti hai.

## Interview Questions & Answers
### Q: What is the command to create a component, and why should you use CLI?
**A**: Command `ng generate component component-name` (ya `ng g c component-name`) hai. CLI use karna isliye recommended hai kyunki yeh component ki TS, HTML, CSS, aur test (spec) files automatically bana deta hai, dependencies register kar deta hai, aur standard naming conventions follow karta hai.

### Q: What is the difference between global npm installation and local dependencies?
**A**: Global installation (`npm i -g`) command-line binaries ko pure system me available banata hai. Local dependencies (`node_modules` me stored) yeh ensure karti hain ki project `package.json` me locked exact dependency version ke sath compile ho, taaki build servers par breaks na hon.

## Summary
Angular workspace setup karne ke liye Node.js, npm, aur Angular CLI ki zaroorat hoti hai. CLI Angular project ka nervous system hai, jo scaffolding, compilation, testing, aur final builds ko aasan banata hai.

---

Previous : [Introduction to Angular](./01_Introduction_to_Angular.md) | Index : [Home](./00_index.md) | Next : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md)
