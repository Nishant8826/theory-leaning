# 🚀 Shared Libraries

## 📌 Topic Name
Jenkins Shared Libraries: Reusability, Classpaths, and Trusted Code

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Put common Jenkins code in a central Git repo so everyone can share it.
*   **Expert**: Global Shared Libraries are dynamically loaded Java/Groovy codebases injected directly into the Jenkins CPS execution engine at runtime. They serve two critical functions: **DRY (Don't Repeat Yourself)** for organization-wide pipelines, and **Security Escapes**, as Global libraries execute *outside* the Groovy Sandbox. A Staff engineer leverages them to create internal DSLs, standardize deployment wrappers, and separate complex Java-esque logic from declarative orchestrations.

## 🏗️ Mental Model
Think of a Shared Library as a **Custom Expansion Pack for Jenkins**.
- **Jenkins Core**: Comes with standard tools (`sh`, `git`).
- **The Library**: A toolkit you build (`deployToEKS`, `notifySlackWithFormatting`).
- **The Injection**: When a pipeline runs `@Library('my-lib')`, Jenkins downloads the toolkit from Git, compiles it, and dumps the tools onto the developer's workbench, ready to use.

## ⚡ Actual Behavior
- **Dynamic Retrieval**: By default, Jenkins checks out the library from SCM every single time a pipeline runs. This adds a few seconds of latency to the start of every build.
- **Trusted vs Untrusted**:
    - **Global Libraries** (configured in "Manage Jenkins"): Run *outside* the Sandbox (Trusted). Can use any Java API.
    - **Folder Libraries**: Run *inside* the Sandbox (Untrusted).

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Classpath Injection**: When `@Library` is encountered, the Controller checks out the code to a hidden workspace, compiles the Groovy files into bytecode, and adds them to the CPS Classloader for that specific pipeline run.
2.  **Directory Structure**:
    - `src/`: Standard Java/Groovy classes (e.g., `com.myorg.utils`). Object-oriented, good for helper classes.
    - `vars/`: Global Variables (e.g., `buildApp.groovy`). Exposes functions directly to the Jenkinsfile DSL.
    - `resources/`: Static files (e.g., JSON templates, bash scripts) loaded via `libraryResource()`.
3.  **The `call()` method**: Inside `vars/myStep.groovy`, defining a `def call(Map args) {}` method allows the pipeline to execute `myStep(a: 1)` seamlessly.

## 🔁 Execution Flow
1.  **Trigger**: Pipeline starts.
2.  **Parsing**: Controller reads `@Library('my-lib@v1.0') _` at the top of the Jenkinsfile.
3.  **SCM Fetch**: Controller pulls `v1.0` of `my-lib` from Git.
4.  **Compilation**: Controller compiles the library classes.
5.  **Execution**: Pipeline executes. When it hits `myStep()`, it executes the compiled code from the library.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Git Thrashing**: If you have 100 concurrent builds using the same library, the Controller might execute 100 `git clone` operations against your SCM provider, potentially hitting API rate limits.
- **Memory Overhead**: Each run gets its own classloader instance for the library to prevent state leakage, consuming minor Heap space.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINSFILE ]
@Library('my-lib') _
deployApp()
      |
      V
[ CLASSLOADER INJECTION ] <---- [ GIT REPO: my-lib ]
                                  /vars/deployApp.groovy
                                  /src/org/corp/Utils.groovy
      |
      V
[ CPS ENGINE ]
(Executes deployApp() as if it were a native Jenkins step)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Repository: my-shared-lib
// File: vars/standardPipeline.groovy
def call(Map config) {
    pipeline {
        agent { label 'docker' }
        stages {
            stage('Build') {
                steps {
                    sh "npm install ${config.appName}"
                }
            }
        }
    }
}

// -----------------------------------------
// Repository: my-app
// File: Jenkinsfile
@Library('my-shared-lib@main') _

// One-line pipeline! The library handles the rest.
standardPipeline(appName: 'frontend-ui')
```

## 💥 Production Failures
1.  **The "Main Branch" Outage**: Everyone imports `@Library('my-lib@main')`. A junior dev pushes a syntax error to the `main` branch of the library. Instantly, every pipeline in the entire company fails to start. **Solution**: Always pin libraries to specific tags/versions in production Jenkinsfiles.
2.  **State Leakage**: A developer uses a static variable in a `src/` class (e.g., `static List logs = []`). Because classes might be cached or shared depending on the execution context, data from Build A leaks into Build B. **Solution**: Never use static state in Jenkins Shared Libraries.
3.  **SCM Rate Limiting**: GitHub bans the Jenkins Controller's IP because it polled the Shared Library repo 5,000 times in an hour. **Solution**: Enable "Cache fetched versions on Controller" in the library settings.

## 🧪 Real-time Q&A
*   **Q**: What does the underscore `_` mean in `@Library('lib') _`?
*   **A**: It's a Groovy hack. `@Library` is an annotation. In Groovy, annotations must be attached to something (a class, a method, or an import). The `_` acts as a dummy import statement so the syntax is valid.
*   **Q**: Can a library load another library?
*   **A**: Yes, using the `@Library` annotation inside the library's classes.

## ⚠️ Edge Cases
*   **Overriding Native Steps**: If you create a file named `vars/sh.groovy`, you will override the native Jenkins `sh` step. This is incredibly dangerous and breaks everything.
*   **`libraryResource` limits**: Loading massive files via `libraryResource` pulls them directly into the Controller's RAM.

## 🏢 Best Practices
1.  **Version Pinning**: Enforce `my-lib@v1.2.0` in all production pipelines.
2.  **Unit Testing**: Use frameworks like `JenkinsPipelineUnit` to mock and test your shared library code locally before pushing.
3.  **Use `vars/` for entry points**: Keep `vars/` scripts small. Delegate heavy logic to Object-Oriented classes in `src/`.

## ⚖️ Trade-offs
*   **Shared Libraries**: Drastically reduces duplicated code and standardizes security, but creates a massive Single Point of Failure and a steep learning curve for developers trying to debug them.

## 💼 Interview Q&A
*   **Q**: You have a complex Groovy script that parses XML, but the Sandbox keeps rejecting it. How do you fix this permanently for all teams?
*   **A**: I would move the XML parsing logic into a class inside the `src/` directory of a Global Shared Library. Because Global Shared Libraries run outside the Sandbox as "Trusted Code," it can use standard Java XML libraries without triggering `ScriptApproval` rejections. I would then expose a simple wrapper function in `vars/` for teams to call.

## 🧩 Practice Problems
1.  Create a Shared Library with a `vars/sayHello.groovy` file that takes a `name` parameter and prints "Hello, [name]". Use it in a pipeline.
2.  Configure the "Retriever" method for a Shared Library to use "Modern SCM" and explore the caching options.

---
Prev: [03_Groovy_Sandbox.md](../Pipelines/03_Groovy_Sandbox.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [05_Stage_Execution_and_Parallelism.md](../Pipelines/05_Stage_Execution_and_Parallelism.md)
---
