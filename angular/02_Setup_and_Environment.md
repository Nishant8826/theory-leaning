# Setup and Environment

## What is it?
Setting up an Angular development environment involves installing Node.js, npm (Node Package Manager), and the Angular Command Line Interface (CLI). These tools work together to compile TypeScript, manage external libraries, run local development servers with live reload, and bundle optimized assets for production.

## Why do we need it?
Web browsers cannot natively execute TypeScript, Angular template syntax, or modern CSS preprocessors (such as SCSS). A dedicated development environment is required to:
1. Compile modern TypeScript, SCSS, and template files into standard JavaScript, CSS, and HTML.
2. Manage project dependencies (such as RxJS, Tailwind CSS, or Angular Material) cleanly.
3. Host a local development server with Hot Module Replacement (HMR) for fast feedback during development.

```
Development Workflow:
[TypeScript Files + Styles] ──> Angular CLI ──> Vite/Webpack Compiler ──> Browser Execution (HTML/JS/CSS)
```

## How does it work?
1. **Node.js**: The JavaScript runtime environment that executes developer build tools outside of the web browser.
2. **npm**: The package registry from which we download the core Angular framework, CLI packages, and third-party libraries.
3. **Angular CLI**: The official command-line tool that automates project scaffolding, generates boilerplate code (components, services, guards), runs the dev server (`ng serve`), executes unit tests (`ng test`), and compiles production builds (`ng build`).

## Impact
* **Application Architecture**: Enforces a consistent, standardized project folder structure across engineering teams.
* **Performance**: Utilizes Vite for blazing-fast local development and esbuild/Webpack for optimized, minified production bundles.
* **Maintainability**: Makes upgrading between major Angular versions effortless and automated via the `ng update` command.

## Real World Example
In a professional enterprise team, a new engineer can clone the repository, run `npm install` followed by `ng serve`, and have a fully functioning local development environment running in just a few minutes.

## Syntax
Essential Angular CLI commands:

```bash
# Install Angular CLI globally
npm install -g @angular/cli

# Create a new standalone application with routing and CSS styling
ng new my-app --standalone --routing --style=css

# Start the local development server with auto-reload
ng serve --open

# Compile optimized production assets into the dist/ directory
ng build --configuration production
```

## Code Examples
Here is what a typical `package.json` looks like in a modern Angular project:

```json
{
  "name": "angular-academy",
  "version": "1.0.0",
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
1. **Manage Node Versions with NVM**: Use Node Version Manager (`nvm`) or `.nvmrc` to ensure all team members and CI/CD pipelines run the exact same Node.js LTS version.
2. **Use npm Scripts**: Instead of relying on a globally installed CLI binary, run commands via `npm start`, `npm run build`, or `npx ng` to prevent version mismatches.
3. **Keep the CLI Synchronized**: Always keep your Angular CLI version aligned with your project's `@angular/core` version to avoid configuration warnings and deprecated build options.

## Common Mistakes
* **Global vs. Local CLI Version Mismatches**: Running an outdated global CLI against a newer local project can cause build failures. Use `npx ng <command>` to ensure you execute the project-specific local CLI.
* **Manually Creating Files**: Manually creating component or service files without the CLI can lead to typos in class names, missing test files, or forgotten imports. Always prefer `ng generate` commands.

## Interview Questions & Answers
### Q: What is the command to create a component, and why is using the CLI recommended?
**A**: The command is `ng generate component <component-name>` (or `ng g c <name>`). Using the CLI is recommended because it automatically creates the TypeScript logic, HTML template, CSS styling, and unit test (`.spec.ts`) files, registers necessary dependencies, and enforces consistent naming conventions.

### Q: What is the difference between global npm packages and local project dependencies?
**A**: Global packages (`npm i -g`) make command-line utilities available across your entire operating system. Local dependencies (stored in `node_modules` and listed in `package.json`) ensure that the project compiles using the exact locked versions, preventing build breaks in continuous integration (CI) environments.

## Summary
Setting up an Angular workspace requires Node.js, npm, and the Angular CLI. The CLI serves as the backbone of an Angular project, managing code generation, development servers, testing suites, and production optimizations.

---

Previous : [Introduction to Angular](./01_Introduction_to_Angular.md) | Index : [Home](./00_index.md) | Next : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md)
