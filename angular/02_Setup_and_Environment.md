# Setup and Environment

## What is it?
Setting up the Angular environment involves installing Node.js, npm (Node Package Manager), and the Angular Command Line Interface (CLI). These tools compile TypeScript, manage external libraries, spin up development servers, and bundle code for production.

## Why do we need it?
Browsers do not natively understand TypeScript, Angular templates, or modern CSS formats (SASS). We need a development environment to:
1. Compile files into standard JavaScript, CSS, and HTML.
2. Manage dependencies (like RxJS, Tailwind, Angular Material).
3. Run a local development server with Hot Module Replacement (HMR) for quick iteration.

```
Development:
[TS Files + Styles] ──> Angular CLI ──> Vite/Webpack compiler ──> Browser Execution (HTML/JS/CSS)
```

## How does it work?
1. **Node.js**: The runtime environment executing developer tools outside the browser.
2. **npm**: The repository registry to download the Angular core and secondary packages.
3. **Angular CLI**: The command-line orchestration tool that generates code (components, services), starts development servers (`ng serve`), builds applications (`ng build`), and runs tests (`ng test`).

## Impact
* **Application Architecture**: Ensures standard project folder layout across the team.
* **Performance**: CLI leverages Vite (dev) and Webpack/esbuild (prod) for ultra-fast builds.
* **Maintainability**: Seamless migrations between Angular major versions using `ng update`.

## Real World Example
In a commercial team setting, new developers run a single command (`npm install` followed by `ng serve`) to set up their workspace and run the application locally within minutes.

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

## Hinglish Explanation

Angular application setup aur commands chalane ke liye kuch software tools zaroori hain.

### 1. Node.js aur npm (Gas stove aur Gas Cylinder)
* **Node.js:** Yeh background runtime environment hai jisse hamara system JavaScript ko machine par directly run kar sakta hai (jaise kitchen me stove ka hona).
* **npm (Node Package Manager):** Yeh ek shopping center ya app store ki tarah hai, jahan se hum bani-banayi dependencies (packages/libraries) download karte hain (jaise gas cylinder ya kitchen supplies lana).

### 2. Angular CLI (Hamara Personal Assistant)
CLI ka full form hai **Command Line Interface**. Yeh Angular ka official tool hai jo saare boring aur repetitive tasks seconds me kar deta hai.
* Agar component banana hai, toh manually files banana aur code connect karne ke bajaye hum simple bolte hain: `ng g c component-name`, aur CLI saari files aur connections auto-setup kar deta hai.
* Local server start karne ke liye: `ng serve`
* Production build banane ke liye: `ng build`

### 3. package.json aur node_modules (Shopping List vs Storage Box)
* **package.json:** Yeh hamare project ki recipe book hai jisme likha hota hai ki project ko chalane ke liye kaun-kaunsi dependencies aur unke kaunse versions zaroori hain.
* **node_modules:** Yeh wo storage folder hai jahan wo saari downloaded dependencies actual me store hoti hain. Yeh size me bohot bada hota hai, isliye ise Git par push nahi kiya jata (sirf `package.json` ko push karte hain aur dusre developers use `npm install` se local storage me fetch kar lete hain).

## Code Examples
Here is how your `package.json` configurations typically look in an Angular setup:

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

### 2. Angular CLI (Hamara Personal Assistant)
CLI ka full form hai **Command Line Interface**. Yeh Angular ka official tool hai jo saare boring aur repetitive tasks seconds me kar deta hai.
* Agar component banana hai, toh manually files banana aur code connect karne ke bajaye hum simple bolte hain: `ng g c component-name`, aur CLI saari files aur connections auto-setup kar deta hai.
* Local server start karne ke liye: `ng serve`
* Production build banane ke liye: `ng build`

### 3. package.json aur node_modules (Shopping List vs Storage Box)
* **package.json:** Yeh hamare project ki recipe book hai jisme likha hota hai ki project ko chalane ke liye kaun-kaunsi dependencies aur unke kaunse versions zaroori hain.
* **node_modules:** Yeh wo storage folder hai jahan wo saari downloaded dependencies actual me store hoti hain. Yeh size me bohot bada hota hai, isliye ise Git par push nahi kiya jata (sirf `package.json` ko push karte hain aur dusre developers use `npm install` se local storage me fetch kar lete hain).

## Best Practices
1. **Local Node Version**: Use Node Version Manager (`nvm`) to align Node.js versions among developers.
2. **Run via npm Scripts**: Instead of invoking global CLI directly, use local scripts via `npm run start` or `npm run build` to guarantee version consistency across CI/CD platforms.
3. **Keep CLI updated**: Keep CLI aligned with angular framework version.

## Common Mistakes
* **Global/Local CLI Mismatches**: Running commands on a globally outdated CLI that conflicts with the local project package versions. Resolve this by invoking `npx ng <command>`.
* **Not using standard folders**: Manually creating files instead of using CLI generator commands (`ng generate`), which can skip setting up proper component specifications.

## Interview Questions & Answers
### Q: What is the command to create a component, and why should you use CLI?
**A**: The command is `ng generate component component-name` (or `ng g c component-name`). Using the CLI is recommended because it automatically creates the TS, HTML, CSS, and spec test files, registers any necessary bindings, and ensures standard naming conventions.
* **Hinglish Explanation**: CLI (Command Line Interface) se component banane ki command `ng generate component component-name` hai. CLI use karne ka fayda yeh hai ki yeh automatic component ki TS file, HTML template, CSS styling aur test specifications (spec) file bana deta hai, aur file structure ko strict standard conventions ke mutabik set karta hai jisse aapko haath se file banana aur connect nahi karna padta.

### Q: What is the difference between global npm installation and local dependencies?
**A**: Global installation (`npm i -g`) makes command-line binaries available system-wide. Local dependencies (stored in `node_modules`) ensure that project compiles with the exact locked dependency version listed in `package.json`, preventing breaks on build machines.
* **Hinglish Explanation**: Global npm installation (`npm i -g`) se tool pure operating system me install ho jata hai aur aap terminal pe kahin se bhi us command ko chala sakte ho. Local dependencies (`node_modules` me jo store hoti hain) sirf usi specific project ke liye hoti hain. Isse yeh sure hota hai ki agar alag-alag projects me alag-alag versions hain, toh koi conflict na ho aur project build machine par sahi locked version par hi build ho.

## Summary
Setting up an Angular workspace requires Node.js, npm, and the Angular CLI. The CLI is the nervous system of an Angular project, facilitating scaffolding, compiling, testing, and builds.

---

Previous : [Introduction to Angular](./01_Introduction_to_Angular.md) | Index : [Home](./00_index.md) | Next : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md)
