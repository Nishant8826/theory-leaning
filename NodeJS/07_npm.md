# npm (Node Package Manager)

## What You Will Learn
* How npm operates as a registry, CLI client, and package manager.
* Understanding `package.json` configurations and dependency categories.
* The internal structure and role of `package-lock.json`.
* Semantic Versioning (SemVer) operators (`^`, `~`, exact versioning).
* Executing audits and dependency checks.

## Why This Matters
An application's stability depends on its third-party packages. A poor understanding of npm configuration leads to security risks, broken production builds when patches release, and bloated deployment containers. Knowing how to lock versions and audit dependencies protects your supply chain.

## Theory

### Node Package Manager Core Role
**npm** consists of three distinct components:
1. **The Registry**: A public database of open-source Node.js packages.
2. **The Command Line Interface (CLI)**: The tool developers run in their terminal to interact with the registry.
3. **The Package Manager**: Resolves package dependency trees and downloads them into the local `node_modules` directory.

### Semantic Versioning (SemVer)
Version numbers follow a three-part format: `MAJOR.MINOR.PATCH` (e.g., `4.18.2`):
* **MAJOR**: Includes breaking API changes. (Requires developer code updates).
* **MINOR**: Adds backwards-compatible features.
* **PATCH**: Fixes bugs in a backwards-compatible manner.

Operators dictate how npm updates packages:
* **Caret (`^`)**: Installs minor and patch updates (e.g., `^4.18.2` allows `4.19.0` and `4.18.3`, but blocks `5.0.0`).
* **Tilde (`~`)**: Installs patch updates only (e.g., `~4.18.2` allows `4.18.3`, but blocks `4.19.0`).
* **Exact (No Operator)**: Locks the package to that exact release (e.g., `4.18.2`).

## Deep Dive

### package-lock.json under the hood
While `package.json` defines semantic ranges (e.g., `"express": "^4.18.2"`), `package-lock.json` stores the exact dependency tree installed.
When you run `npm install`, npm references the lockfile to download the exact same versions.
Key properties in `package-lock.json`:
* **version**: The exact version installed.
* **resolved**: The URL of the registry registry registry where the package archive was downloaded.
* **integrity**: A Subresource Integrity (SRI) cryptographic hash (e.g. SHA-512) validating that the package code downloaded matches the registry copy and was not altered in transit.

### Dependency Types
1. **dependencies**: Packages required to run the application in production (e.g., `express`, `mongoose`).
2. **devDependencies**: Packages required during development and building, but not in production (e.g., `jest`, `eslint`, `nodemon`).
3. **peerDependencies**: Informs the installer that your package requires a parent library installed at a specific version (common in plugins).
4. **optionalDependencies**: Dependencies whose installation failures will not abort the installation process.

## Visual Explanation

### Dependency Resolution Path
```text
[ Developer runs: npm install ]
               │
               ▼
   [ Does package-lock.json exist? ]
         ├── YES ──> [ Install exact versions listed in lockfile ] ──> Validate integrity hashes
         │
         └── NO  ──> [ Read package.json dependency ranges ]
                           │
                           ▼
                     [ Query npm Registry for matching versions ]
                           │
                           ▼
                     [ Resolve dependency tree, download modules, write package-lock.json ]
```

## Real-World Example
Suppose you deploy a service to production. If your `package.json` contains `"dependency": "^1.2.0"`, and the library author releases a buggy patch `1.2.1` that breaks compilation, running `npm install` during deployment without a `package-lock.json` file will fetch the buggy version and break the server. Committing `package-lock.json` prevents this by forcing the build server to fetch version `1.2.0` exactly.

## Code Examples

### package.json Configurations

```json
{
  "name": "production-service",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "node dist/server.js",
    "dev": "nodemon src/server.js",
    "test": "jest",
    "lint": "eslint src/**/*.js"
  },
  "dependencies": {
    "cors": "2.8.5",
    "express": "4.18.2",
    "helmet": "7.1.0"
  },
  "devDependencies": {
    "eslint": "8.56.0",
    "jest": "29.7.0",
    "nodemon": "3.0.2"
  }
}
```

### Scripted Auditing and CI Checks
You can enforce security checks in your CI/CD pipeline using npm commands:

```bash
# 1. Clean install based exactly on package-lock.json (Recommended for pipelines)
# This will fail if package.json and package-lock.json are out of sync.
npm ci

# 2. Check for known security vulnerabilities in your dependencies
# Returns non-zero exit codes if critical issues are found, stopping CI/CD builds.
npm audit --audit-level=high

# 3. List outdated dependencies to check for technical debt
npm outdated
```

## Best Practices
* **Use npm ci in Pipelines**: Always use `npm ci` instead of `npm install` on build servers and CI/CD pipelines to guarantee exact replication and speed up installation.
* **Keep package-lock.json in Git**: Never add `package-lock.json` to `.gitignore`. It is your guarantee of reproducible environments.
* **Enforce Strict SemVer**: Use exact versions or `.npmrc` options (`save-exact=true`) to avoid unexpected dependency updates in production.
* **Run Regular Audits**: Incorporate `npm audit` check stages into your pull request workflows to catch security flaws early.

## Interview Questions

### Beginner
* **What is the difference between dependencies and devDependencies in package.json?**
  *Answer*: `dependencies` are libraries required for the application to run in production (e.g. web frameworks, database ORMs). `devDependencies` are only needed during development or build stages (e.g. compilers, testing frameworks, linters) and are excluded from production builds.

### Intermediate
* **What is the difference between package.json and package-lock.json, and why is the latter important?**
  *Answer*: `package.json` defines metadata, scripts, and target version ranges of direct dependencies. `package-lock.json` locks the exact version, download source, and cryptographic hash of every dependency and nested dependency installed. This ensures consistent, reproducible environments across all developer machines and servers.

### Advanced
* **Explain how `npm ci` works, how it differs from `npm install`, and why you should use it in CI/CD pipelines.**
  *Answer*: `npm ci` (Clean Install) is optimized for automated environments. It differs from `npm install` in several ways:
  1. It requires a `package-lock.json` to exist; otherwise, it throws an error.
  2. If the lockfile is out of sync with `package.json`, it aborts rather than modifying the lockfile.
  3. It deletes the existing `node_modules` directory entirely before downloading dependencies.
  4. It does not write to `package.json` or `package-lock.json`. This ensures absolute consistency and prevents dynamic updates during build runs.

### Senior Architect
* **Describe the security risks associated with npm dependencies (e.g., typo-squatting, package hijacking). How do you secure a enterprise CI/CD pipeline against these supply chain attacks?**
  *Answer*: Risks include typo-squatting (malicious packages named similarly to popular ones), dependency confusion (uploading internal packages to public registries), and package hijacking (compromised maintainer accounts releasing malicious updates).
  To secure a pipeline:
  1. Run a private registry mirror (like Nexus or Artifactory) to control package additions.
  2. Enforce `npm ci` using verified lockfile integrity hashes (SHA-512 check).
  3. Integrate automated static analysis security testing (SAST) tools like Snyk or `npm audit` into the build process, blocking commits with critical vulnerabilities.
  4. Implement policy checks that restrict the licensing types of dependencies and require approval for packages that have not been vetted.

---
Previous : [06_Event_Loop_Basics.md] | Index : [00_index.md] | Next : [08_npx.md]
