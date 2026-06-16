# Environment Setup

Installing Node.js globally using a direct installer leads to version conflicts, permission issues on Unix-based systems (forcing the usage of `sudo npm install`), and environment drift across local environments, staging, and production. Standardizing version control and configuring tools prevents "it works on my machine" bugs.

Production-ready backend environments require absolute determinism. A small variation in the minor or patch version of Node.js can introduce changes in the V8 engine compilation phase or differences in experimental APIs. 

To achieve determinism, we use:
1. **Node Version Managers**: Tools that download and run isolated Node.js binary environments locally without modifying system root folders.
2. **Engine Locking**: Configuring constraints in `package.json` to instruct npm/yarn/pnpm to reject running the project if the wrong engine is active.
3. **Environment Isolation**: Managing runtime environment variables via configuration layers (`.env` files) rather than hardcoding credentials inside codebase modules.

## Deep Dive
Let's analyze Node Version Manager operations under the hood:

### How NVM/FNM Works
When you switch Node.js versions (e.g., `nvm use 20.11.0`), NVM does not reinstall Node globally. It dynamically alters your operating system's `PATH` environment variable. By placing the directory of the selected Node.js binary version at the front of the `PATH` array, any shell command executing `node` or `npm` queries that specific folder instead of system-level directories.

### .npmrc Configuration
The `.npmrc` file is an understated, yet critical, configuration file that dictates dependency resolution policies:
* **save-exact=true**: Automatically saves dependency versions in `package.json` as exact releases rather than permitting semantic range upgrades (e.g., locking `express: "4.18.2"` instead of `express: "^4.18.2"`). This protects production builds from breaking changes in third-party patches.
* **engine-strict=true**: Instructs Node.js to abort installation if the active Node.js version fails to match the `engines` parameters inside the application's `package.json`.

## Visual Explanation

### PATH Variable Redirection
```text
Default System PATH:
[ C:\Windows\System32 ] ---> [ C:\Program Files\nodejs\node.exe (v18.0.0) ]

Executing: nvm use 20.11.0

Modified PATH (Prepend active version folder):
[ C:\Users\User\.nvm\versions\node\v20.11.0\bin ] ---> [ C:\Windows\System32 ] ---> ...
                      |
                      v
          Executing 'node' resolves to v20.11.0 binary directory first!
```

## Real-World Example
Suppose a developer updates their local global Node version to Node 22, while the production servers run Node 20 LTS. An experimental method utilized in Node 22 (such as `Array.fromAsync`) passes local development checks but crashes instantly on the production server with a `TypeError`. Setting `engine-strict=true` inside `.npmrc` prevents this by blocking the project from starting on the local system unless the developer switches back to Node 20.

## Code Examples

### Standard package.json Engine Configuration
```json
{
  "name": "production-grade-node-app",
  "version": "1.0.0",
  "description": "Secure, version-locked Node.js API",
  "main": "server.js",
  "engines": {
    "node": ">=20.11.0 <21.0.0",
    "npm": ">=10.2.4"
  },
  "scripts": {
    "start": "node server.js",
    "check-env": "node -e 'console.log(`Running Node.js version: ${process.version}`)'"
  }
}
```

### Dynamic Version Enforcement Script
Include this pre-install check script in your workflow if you do not want to rely solely on package manager warnings:

```javascript
// scripts/check-node-version.js
const semver = require('semver');
const pkg = require('../package.json');

const requiredVersion = pkg.engines.node;
const currentVersion = process.version;

if (!semver.satisfies(currentVersion, requiredVersion)) {
  console.error(`\x1b[31m[ERROR] Required Node.js version is ${requiredVersion}.`);
  console.error(`You are currently running version ${currentVersion}.\x1b[0m`);
  console.error('Please run: nvm use OR fnm use to switch to the correct version.');
  process.exit(1); // Aborts execution with error code
}

console.log(`\x1b[32m[SUCCESS] Node.js version check passed: ${currentVersion}\x1b[0m`);
```

## Best Practices
* **Use FNM (Fast Node Manager)**: Written in Rust, FNM is significantly faster than shell-based NVM implementations.
* **Store `.node-version` / `.nvmrc`**: Keep a `.node-version` file containing the version number (e.g. `20.11.0`) at the root of the repository so IDE terminals and runners switch automatically.
* **Always run npm config settings**: Add `save-exact=true` and `engine-strict=true` to your project's `.npmrc`.
* **Lock node_modules via lockfile**: Check `package-lock.json` or `pnpm-lock.yaml` directly into your git repository.

## Interview Questions

**Q:** What is the purpose of NVM or FNM, and why is it preferred over direct installers?

> **Answer:**
> Node Version Managers download isolated runtime environments, allowing developers to switch between multiple versions easily. This avoids system permission errors (which occur when writing global packages to root folders like `/usr/local`) and prevents runtime mismatch issues when working on multiple projects.

**Q:** How can you ensure that every member of a development team runs the exact same Node.js version?

> **Answer:**
> Define the targeted version in the `engines` property of the `package.json` file, create a `.node-version` or `.nvmrc` file at the root, and configure `.npmrc` with `engine-strict=true`. This setup causes the package manager to fail immediately if a developer attempts to install packages using an incompatible Node.js version.

**Q:** Explain how dependencies are resolved in package-lock.json and why the lockfile must be committed to git.

> **Answer:**
> `package-lock.json` records the exact version of every dependency and nested dependency installed, along with a cryptographic hash (integrity check) of the packages fetched from the registry. Committing this file ensures that the build pipeline, local development environments, and production servers install the exact same dependency tree, preventing bugs caused by semantic-range auto-updates.

**Q:** Discuss how version drift can cause subtle failures in highly scaled production clusters when migrating from Node.js 18 to Node.js 20. What migration strategy would you enforce?

> **Answer:**
> Node.js upgrades introduce new V8 memory profiles, modified HTTP parsing rules, and deprecations of experimental APIs. An upgrade can cause memory leaks if closures perform differently, or connection drops if HTTP parser tolerances change.
> To migrate safely:
> 1. Enforce engine constraints in `.npmrc`.
> 2. Implement local checking scripts before testing builds.
> 3. Deploy to staging, checking heap profiles and memory footprints under simulated load tests.
> 4. Perform a canary deployment to production, route 5% of traffic to the new Node.js 20 container, and monitor latency spikes, 5xx errors, and error logs before rolling out to the rest of the cluster.

---
Previous : [01_Introduction_to_NodeJS.md](01_Introduction_to_NodeJS.md) | Index : [00_index.md](00_index.md) | Next : [03_JavaScript_Fundamentals_for_NodeJS.md](03_JavaScript_Fundamentals_for_NodeJS.md)
