# GitHub Actions

## What You Will Learn
* The structural components of GitHub Actions (Workflows, Jobs, Steps, Actions, and Runners).
* Defining pipeline triggers: `push`, `pull_request`, and `workflow_dispatch`.
* Setting up the Node.js runner environment using `actions/setup-node`.
* Caching `node_modules` dependencies to optimize build speeds.
* Writing a complete CI workflow configuration file.

## Why This Matters
GitHub Actions integrates CI/CD automation directly into your GitHub repository. You do not need to manage external build servers (like Jenkins) or configure complex webhooks. By writing a simple YAML file in `.github/workflows/`, GitHub automatically executes tests, audits code, and builds containers on every pull request, protecting your codebase from bugs.

## Theory

### Workflows, Jobs, Steps, and Runners
* **Workflow**: An automated process defined in a YAML file inside the `.github/workflows/` directory.
* **Job**: A set of steps executed sequentially on a clean instance of a runner virtual machine. By default, multiple jobs defined in a workflow run concurrently in parallel.
* **Step**: An individual task that runs a command (e.g. `run: npm test`) or executes an Action.
* **Action**: A reusable package of code that performs common tasks (like checking out code or configuring Node.js).
* **Runner**: The virtual machine host provided by GitHub (running Linux, Windows, or macOS) that executes the workflow jobs.

### Triggering Events
You can configure workflows to trigger on specific events:
* **`push`**: Runs whenever code is pushed to specific branches (e.g. `main` or `release`).
* **`pull_request`**: Runs when pull requests are created, updated, or merged.
* **`workflow_dispatch`**: Enables developers to trigger the workflow manually using the GitHub website dashboard interface.

## Deep Dive

### Caching Dependencies
Downloading and installing npm packages on clean runner virtual machines on every build consumes significant bandwidth and adds build latency.
* **`actions/setup-node` caching**: Modern setup actions include built-in caching. By setting `cache: 'npm'`, the runner caches the npm download cache directory between runs. If the dependencies in `package-lock.json` have not changed, the runner restores the packages instantly, reducing build times.

## Visual Explanation

### GitHub Actions Workflow Execution
```text
Developer pushes code to branch 'feature/auth'
         │
         ▼ (Triggers GitHub Runner Event)
[ Spin up Clean virtual machine: ubuntu-latest ]
         │
         ▼ (Step 1: Check out code)
[ Action: actions/checkout@v4 ]
         │
         ▼ (Step 2: Initialize Node.js + Read cache)
[ Action: actions/setup-node@v4 ] ── Checks cache ──> Cache Hit?
                                                       ├── YES ──> Restore packages instantly
                                                       └── NO  ──> Run: npm ci (Download from registry)
         │
         ▼ (Step 3: Run Linters & Tests)
[ Run command: npm run lint ] ──> [ Run command: npm test ]
         │
         ▼
[ Build Passed! (Pull Request approved for merge) ]
```

## Real-World Example
Consider a team of developers collaborating on a repository. You want to ensure that no developer can merge code into the `main` branch unless the tests pass. You create a workflow file `ci.yml` that runs on `pull_request`. You configure GitHub branch protection rules to require this check to pass before merging, preventing broken code from entering the stable branch.

## Code Examples

### A Complete CI Workflow Configuration for Node.js Applications

```yaml
# .github/workflows/ci.yml
name: Node.js Continuous Integration

# 1. Define Pipeline Triggers
on:
  push:
    branches: [ main, release ]
  pull_request:
    branches: [ main ]
  # Allow manual execution from GitHub Action tab UI
  workflow_dispatch:

# 2. Define Jobs to Execute
jobs:
  test_and_audit:
    # Use the latest Ubuntu runner
    runs-on: ubuntu-latest

    # Define matrix to run tests across multiple Node.js versions concurrently
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    # Step 1: Check out the repository code
    - name: Checkout Repository Code
      uses: actions/checkout@v4

    # Step 2: Set up target Node.js version and configure caching
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm' # Automatically caches npm packages between runs

    # Step 3: Install dependencies using clean install (npm ci)
    - name: Install Project Dependencies
      run: npm ci

    # Step 4: Run ESLint to verify code formatting rules
    - name: Run Linter
      run: npm run lint

    # Step 5: Run security scan on dependency tree
    - name: Run Security Audit
      run: npm audit --audit-level=high

    # Step 6: Execute Jest test suites
    # Use environment variables injected from GitHub secrets if needed
    - name: Run Jest Test Suites
      env:
        NODE_ENV: test
        JWT_SECRET: ${{ secrets.TEST_JWT_SECRET }}
      run: npm test
```

## Best Practices
* **Enable NPM Cache**: Always configure the `cache: 'npm'` option in the `actions/setup-node` step to reduce dependency installation times and speed up builds.
* **Test Across LTS Versions**: Use build matrix configurations (`matrix.node-version`) to test your application across multiple Node.js LTS versions, verifying compatibility before deployments.
* **Use Specific Action Tags**: Pin specific version tags on actions (e.g. `actions/checkout@v4`) rather than using branches like `@main` or `@master` to protect your pipeline from breaking changes in third-party actions.
* **Secure secrets access**: Use GitHub repository secrets to store credentials. Never print secrets to the console during pipeline runs.

## Interview Questions

### Beginner
* **What is a Workflow and a Job in GitHub Actions?**
  *Answer*: A workflow is an automated process defined in a YAML configuration file inside the `.github/workflows/` directory. A job is a set of execution steps (commands or actions) that runs on a clean instance of a runner virtual machine.

### Intermediate
* **How do you cache `node_modules` dependencies in GitHub Actions, and why is this useful?**
  *Answer*: You cache dependencies by setting `cache: 'npm'` in the `actions/setup-node` step. This is useful because it stores the downloaded packages in a cache folder between runs. If `package-lock.json` has not changed, the runner restores the packages instantly instead of downloading them from the npm registry, saving bandwidth and reducing build times.

### Advanced
* **Explain how matrix builds work in GitHub Actions and how you would configure one to test an API across different operating systems and Node.js versions.**
  *Answer*: A matrix build allows you to run multiple configurations of a job concurrently by defining variables (like OS and Node versions) in a matrix. GitHub automatically generates and runs separate jobs for every possible combination:
  ```yaml
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest]
      node-version: [18.x, 20.x]
  runs-on: ${{ matrix.os }}
  ```
  This configuration runs 4 parallel jobs testing the application across Ubuntu/Windows and Node 18/20, ensuring cross-platform compatibility.

### Senior Architect
* **How would you architecture a deployment pipeline in GitHub Actions that builds a Docker image and deploys it to AWS EKS (Kubernetes), ensuring secrets are injected securely without storing static AWS Access Keys in the repository?**
  *Answer*: To deploy to EKS without static AWS keys:
  1. **Configure OIDC**: Set up an OpenID Connect (OIDC) trust relationship between your AWS IAM account and GitHub Actions. This allows GitHub to authenticate with AWS dynamically.
  2. **Assume IAM Role**: In your workflow file, use the official `aws-actions/configure-aws-credentials` action to assume an IAM Role dynamically using short-lived tokens:
     ```yaml
     - name: Configure AWS credentials
       uses: aws-actions/configure-aws-credentials@v4
       with:
         role-to-assume: arn:aws:iam::1234567890:role/github-actions-deploy-role
         aws-region: us-east-1
         audience: sts.amazonaws.com
     ```
  3. **Build and Push**: Authenticate with AWS ECR using the resolved session and push the Docker image.
  4. **Deploy**: Configure `kubectl` to update the EKS deployment using the short-lived AWS session, completing the rollout safely without storing static credentials in GitHub.

---
Previous : [77_CI_CD.md] | Index : [00_index.md] | Next : [79_AWS_Deployment.md]
