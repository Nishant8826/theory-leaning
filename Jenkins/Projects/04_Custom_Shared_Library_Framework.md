# 🏗️ Custom Shared Library Framework

## 📌 Topic Name
Project Blueprint: Building an Enterprise Shared Library Framework

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Writing a bunch of reusable Jenkins code so 50 different teams don't have to copy-paste the same 100-line Jenkinsfile.
*   **Expert**: In an enterprise with hundreds of microservices, managing individual `Jenkinsfile`s is an anti-pattern that leads to massive configuration drift, security vulnerabilities, and impossible migration paths. A Staff engineer builds a **Global Shared Library Framework** that abstracts the entire declarative pipeline into a single method call (an internal DSL). This framework enforces compliance (security scanning, standardized deployments), handles complex Kubernetes pod provisioning dynamically, and shields developers from the intricacies of the CPS engine, Groovy sandboxing, and caching strategies.

## 🏗️ Mental Model
Think of the Shared Library as a **Restaurant Menu**.
- **Without Library (Cooking at home)**: Every developer has to know how to buy ingredients (Docker), chop vegetables (Compile), cook the meat (Test), and plate the food (Deploy). Most make a mess.
- **With Library (Ordering at a Restaurant)**: The developer just writes: `standardJavaMicroservice(name: 'auth-api', javaVersion: '17')`. The kitchen (Shared Library) handles exactly *how* that is cooked, ensuring health standards (Security Scans) are always met.

## ⚡ Architecture Diagram

```mermaid
graph TD
    subgraph Developer Repo (e.g., auth-api)
        JF[Jenkinsfile]
        JF -.->|Calls| LibEntry[standardJavaMicroservice()]
    end

    subgraph Global Shared Library (jenkins-lib.git)
        subgraph vars/ (Entry Points)
            LibEntry
            LibNode[standardNodeMicroservice()]
            LibPython[standardPythonMicroservice()]
        end
        
        subgraph src/com/corp/ (Object-Oriented Logic)
            PodBuilder[KubernetesPodBuilder.groovy]
            Security[SecurityScanner.groovy]
            Cache[S3CacheManager.groovy]
            Deploy[ArgoCDTrigger.groovy]
        end
        
        LibEntry --> PodBuilder
        LibEntry --> Cache
        LibEntry --> Security
        LibEntry --> Deploy
    end

    %% Flow
    PodBuilder -->|Generates YAML| K8s[Kubernetes Cluster]
    Security -->|Runs SonarQube| Jenkins[Jenkins CPS Engine]
```

## 🔬 Component Deep Dive & Implementation

### 1. The Entry Point (`vars/`)
*   **Purpose**: Expose a clean, declarative-looking DSL to the developer.
*   **File**: `vars/standardJavaMicroservice.groovy`
*   **Logic**: This file implements `def call(Map config)`. It takes parameters from the developer, validates them, and then dynamically constructs a Declarative `pipeline { }` block or a Scripted pipeline flow.

### 2. The Core Engine (`src/com/myorg/`)
*   **Purpose**: Move complex, Sandbox-violating code out of `vars/` and into compiled Java/Groovy classes.
*   **Structure**: 
    *   `src/com/myorg/k8s/PodTemplates.groovy`: Returns massive YAML strings for Kubernetes agents based on the requested language version.
    *   `src/com/myorg/security/Sonar.groovy`: Handles the complex logic of calling SonarQube, waiting for Webhooks, and parsing Quality Gates.
    *   `src/com/myorg/utils/Logger.groovy`: A standardized logging framework to ensure all pipelines print formatted, SIEM-friendly output.

### 3. Dependency Injection & Context
*   **The Problem**: Classes in `src/` cannot natively call Jenkins steps like `sh()` or `echo()`.
*   **The Solution**: You must pass the pipeline `script` context (often referenced as `this`) from `vars/` into the classes.
    ```groovy
    // vars/standardJavaMicroservice.groovy
    def call(Map config) {
        // Pass 'this' to the class so it can execute Jenkins steps
        def scanner = new com.myorg.security.SonarScanner(this)
        scanner.runScan()
    }
    ```

### 4. Testing the Library
*   **The Challenge**: Debugging Groovy by committing to Git, running a Jenkins build, and watching it fail is agonizingly slow.
*   **The Solution**: Use **JenkinsPipelineUnit**. Write JUnit tests that mock the Jenkins CPS engine, allowing you to test your library logic (e.g., verifying that passing `javaVersion: 11` generates the correct Pod YAML) entirely locally on your laptop in milliseconds.

## 💥 Implementation Failure Modes
1.  **The CPS Method Size Limit**: A developer writes a massive 2,000-line Groovy file in `vars/`. When the pipeline runs, it crashes with `MethodCodeTooLargeException`. The JVM limits a single method to 64KB of bytecode. The CPS engine's AST transformation heavily inflates bytecode. **Rule**: Break complex logic into smaller helper methods or object-oriented classes in `src/`.
2.  **The "Main Branch" Blackout**: An engineer pushes a syntax error (a missing bracket) directly to the `main` branch of the Shared Library. Instantly, every single pipeline in the entire company fails to start because Jenkins cannot compile the library upon checkout. **Rule**: All production Jenkinsfiles MUST pin to a specific tagged version of the library (e.g., `@Library('corp-lib@v1.2.0') _`), never to `main`.
3.  **State Leakage**: An engineer uses static variables in a `src/` class (e.g., `static List changedFiles = []`). Because the classloader might be shared or cached within the JVM depending on context, Build B running concurrently might read the files from Build A. **Rule**: Never use `static` state for pipeline execution data.

## ⚖️ Architectural Trade-offs
*   **Standardization vs Flexibility**: A heavily opinionated library guarantees that all 500 apps have security scans and proper caching. However, when Team X needs to install a rare OS package just for their app, the strict library blocks them. You must design "Escape Hatches" (e.g., allowing developers to inject custom shell steps before/after standard stages) without compromising security.

## 💼 Implementation Path
1.  **Design the Interface**: Do not write code yet. Write the *ideal* 10-line Jenkinsfile that you want developers to use.
2.  **Bootstrap the Repo**: Create the Git repo with `vars/`, `src/`, and `test/`. Setup `JenkinsPipelineUnit`.
3.  **Build the Pod Generator**: Write the Groovy classes that abstract Kubernetes PodTemplate YAML generation.
4.  **Implement the Pipeline**: Write the `call()` method in `vars/` that ties it all together into a Declarative structure.
5.  **Rollout**: Target one low-risk team. Replace their 200-line Jenkinsfile with your 5-line library call. Observe metrics.
