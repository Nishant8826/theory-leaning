# 🚀 Declarative vs Scripted Pipelines

## 📌 Topic Name
Jenkins Pipelines: Declarative vs Scripted Syntax and Execution

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Two ways to write your Jenkinsfile. Declarative is stricter and easier; Scripted is just pure code.
*   **Expert**: Both syntaxes compile down to the same underlying **Continuation Passing Style (CPS)** execution engine. **Scripted Pipeline** is a raw Groovy execution environment bound by the Jenkins Sandbox, offering imperative, Turing-complete flexibility. **Declarative Pipeline** is an abstraction layer (a custom Groovy DSL) built *on top* of Scripted. It enforces a strict structural schema (AST validation), pre-flight linting, and opinionated error handling, at the cost of dynamic execution flexibility. A Staff engineer uses Declarative for 95% of workloads to enforce organizational standards and relies on Shared Libraries to abstract away complex Scripted logic.

## 🏗️ Mental Model
- **Scripted Pipeline**: **Driving a Manual Transmission Car on a Dirt Road**. You can go anywhere, shift gears whenever you want, but if you make a mistake, you'll drive off a cliff.
- **Declarative Pipeline**: **Riding a Bullet Train**. You must stay on the tracks (the Schema). You can only get off at predefined stations (`stages`, `post`). But it has built-in safety brakes (syntax validation) and is highly predictable.

## ⚡ Actual Behavior
- **Validation Phase**: Declarative pipelines are fully parsed and validated *before* any code executes. If you have a syntax error in Stage 10, the pipeline fails immediately. Scripted pipelines will run Stages 1-9 successfully and then crash at Stage 10.
- **Restartability**: Declarative natively supports "Restart from Stage," leveraging the predictable AST structure. Scripted does not natively support this without complex custom logic.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **AST (Abstract Syntax Tree)**: When Jenkins receives a Declarative Jenkinsfile, it doesn't just run it. It parses it into an AST, validates it against the Declarative schema, and then dynamically translates it into underlying Scripted blocks (`node`, `catchError`, etc.) before passing it to the CPS engine.
2.  **The `script {}` Block**: The escape hatch in Declarative. It temporarily disables the strict AST schema validation and drops the parser back down to the raw Scripted Groovy engine.
3.  **Post Conditions**: Declarative `post` blocks (always, success, failure) are implemented under the hood as massive `try/catch/finally` blocks wrapping the entire pipeline or stage.

## 🔁 Execution Flow
**Declarative Flow**:
1. Controller reads `Jenkinsfile`.
2. AST Parser validates syntax.
3. Controller allocates Flyweight Executor.
4. Top-level `agent` definition triggers node allocation.
5. Stages execute sequentially.
6. `post` conditions are evaluated based on final `currentBuild.result`.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **CPU**: Declarative parsing has a very slight CPU overhead at the start of the build compared to Scripted.
- **Memory**: Both consume significant heap space via the CPS engine, keeping the entire variable scope in memory so it can be serialized to disk.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINSFILE (Declarative) ]
          |
  [ AST VALIDATOR ] ---(Fail Fast if Syntax Error)
          |
[ TRANSLATION LAYER ] (Converts 'pipeline{}' to 'node{}')
          |
  [ CPS ENGINE ] (Groovy Sandbox)
          |
  [ EXECUTION ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// DECLARATIVE SYNTAX
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make'
            }
        }
    }
    post {
        failure { echo "Failed!" }
    }
}

// EQUIVALENT SCRIPTED SYNTAX
node {
    try {
        stage('Build') {
            sh 'make'
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        echo "Failed!"
        throw e
    }
}
```

## 💥 Production Failures
1.  **Dynamic Stage Generation**: A developer tries to use a `for` loop inside a Declarative `stages` block to dynamically create stages based on an array. The build fails immediately with a syntax error because Declarative does not allow dynamic structure generation at runtime. **Solution**: Use `matrix` blocks or a `script{}` block (though `script` won't render individual stages cleanly in the UI).
2.  **The "Late" Failure**: In Scripted, a typo in a teardown script at the end of a 2-hour build isn't caught until the end. The build fails and the environment is left dirty. Declarative would have caught the typo in second 1.

## 🧪 Real-time Q&A
*   **Q**: Can I mix them?
*   **A**: Yes. You can put a `script {}` block inside a Declarative `steps {}` block. You CANNOT put a Declarative `pipeline {}` block inside a Scripted `node {}` block.
*   **Q**: Which one is faster?
*   **A**: Neither. They both run on the same CPS engine. Performance limits are tied to shell steps and network I/O, not the DSL syntax.

## ⚠️ Edge Cases
*   **Environment Variable Scope**: In Declarative, `environment` blocks at the top level are applied to every stage. In Scripted, you must explicitly use `withEnv([]) {}` wrappers.

## 🏢 Best Practices
1.  **Enforce Declarative**: Mandate Declarative pipelines across the organization. It forces developers to write standard, predictable CI/CD flows rather than unmaintainable spaghetti code.
2.  **Limit `script{}` blocks**: If a `script{}` block is more than 10 lines long, extract it into a Shared Library.
3.  **Use Matrix**: Instead of dynamic loops, use the Declarative `matrix` directive for cross-platform/cross-browser testing.

## ⚖️ Trade-offs
*   **Declarative**: Highly readable, safe, and UI-friendly (Blue Ocean works best with it), but rigid.
*   **Scripted**: Infinite flexibility (e.g., dynamically parallelizing 100 tasks based on an API call), but difficult to read, maintain, and secure.

## 💼 Interview Q&A
*   **Q**: A team needs to build a dynamic pipeline that queries a database at the start of the build, gets a list of 10 microservices, and then dynamically creates 10 parallel stages to build them. Should they use Declarative or Scripted?
*   **A**: They must use **Scripted** (or a `script{}` block within Declarative). Declarative requires the structure of the pipeline (the stages) to be known and defined *at compile time* before the code executes. Because the list of services is determined *at runtime*, the strict AST validation of Declarative will fail.

## 🧩 Practice Problems
1.  Rewrite a complex Scripted pipeline containing `try/catch/finally` into a Declarative pipeline using `post` conditions.
2.  Trigger a Declarative pipeline with an intentional syntax error in the very last stage and observe how fast it fails.

---
Prev: [08_System_Performance_Limits.md](../Core/08_System_Performance_Limits.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_Jenkinsfile_Execution_Model.md](../Pipelines/02_Jenkinsfile_Execution_Model.md)
---
