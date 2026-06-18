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

### Q: What is the difference between global npm installation and local dependencies?
**A**: Global installation (`npm i -g`) makes command-line binaries available system-wide. Local dependencies (stored in `node_modules`) ensure that project compiles with the exact locked dependency version listed in `package.json`, preventing breaks on build machines.

## Summary
Setting up an Angular workspace requires Node.js, npm, and the Angular CLI. The CLI is the nervous system of an Angular project, facilitating scaffolding, compiling, testing, and builds.

---

Previous : [Introduction to Angular](./01_Introduction_to_Angular.md) | Index : [Home](./00_index.md) | Next : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md)
