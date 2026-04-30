# 🚀 Groovy Sandbox

## 📌 Topic Name
Jenkins Groovy Sandbox: Security, AST Modification, and ScriptApproval

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Jenkins stops random code from breaking the server or stealing passwords.
*   **Expert**: The Groovy Sandbox is an execution interceptor. Because Jenkins pipelines are raw Groovy running inside the Controller JVM, unconstrained code could easily execute `System.exit(0)` or read `/etc/shadow`. The Sandbox uses an **AST (Abstract Syntax Tree) transformation** to intercept every single method call, property access, and object instantiation at runtime. It checks these operations against a strict "Whitelist" of approved signatures. A Staff engineer manages this delicate balance between developer velocity and platform security using **Script Approval** and **Shared Libraries**.

## 🏗️ Mental Model
Think of the Sandbox as a **Parole Officer observing an Inmate (The Script)**.
- **Without Sandbox**: The inmate can go anywhere and do anything.
- **With Sandbox**: Every time the inmate wants to take a step (call a method) or pick up an object (instantiate a class), the Parole Officer stops them, checks a list of "Allowed Actions", and either lets them proceed or tackles them to the ground (`RejectedAccessException`).

## ⚡ Actual Behavior
- **Performance Hit**: The Sandbox intercepts *everything*. This adds a significant CPU penalty to Groovy execution on the Controller.
- **Script Approval**: If a developer tries to use a non-whitelisted method (e.g., `java.util.UUID.randomUUID()`), the build fails, and the signature is added to an "In-Process Script Approval" queue. A Jenkins Administrator must manually review and approve the signature before the script can run successfully.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Script Security Plugin**: The core engine managing the Sandbox. It maintains a hardcoded whitelist of safe Java/Groovy methods (e.g., `String.length()`).
2.  **AST Transformation**: When the pipeline is compiled, the plugin injects a wrapper (`SandboxInterceptor`) around every AST node.
3.  `System.exit(0)` becomes `SandboxInterceptor.checkStaticMethod(System.class, "exit", 0)`.
4.  **Global Shared Libraries**: Code residing in a globally configured Shared Library runs **OUTSIDE** the Sandbox. It is fully trusted. Code defined in a Jenkinsfile runs **INSIDE** the Sandbox.

## 🔁 Execution Flow
1.  **Commit**: Developer pushes `Jenkinsfile`.
2.  **Compile**: Jenkins compiles the Groovy, applying the Sandbox AST transformation.
3.  **Execute**: Script attempts `new java.net.URL("http://evil.com")`.
4.  **Intercept**: `SandboxInterceptor.checkNewInstance()` is triggered.
5.  **Lookup**: Interceptor checks the whitelist for `new java.net.URL java.lang.String`.
6.  **Result**: Signature not found. `RejectedAccessException` is thrown.
7.  **Queue**: Signature is added to the Admin Approval queue.
8.  **Halt**: Build aborts.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **CPU**: Extremely high overhead for heavily nested loops or complex Groovy logic due to the constant interceptor checks.
- **Memory**: Approving too many broad signatures essentially defeats the purpose of the sandbox, turning the entire JVM into a potential attack surface.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINSFILE (Untrusted) ]
          |
    (Compilation)
          |
[ AST TRANSFORMATION ] ----> Injects Interceptor
          |
[ GROOVY EXECUTION ]
          |
  (Calls Method 'X')
          |
[ SANDBOX INTERCEPTOR ] ---> Checks Whitelist
          |
    +-----+-----+
    |           |
(Allowed)    (Denied)
    |           |
[ RUN ]   [ ABORT BUILD ] ---> [ ADD TO ADMIN APPROVAL QUEUE ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent any
    steps {
        script {
            // SAFE: Whitelisted by default
            def text = "Hello"
            echo text.toUpperCase() 
            
            // BLOCKED: Accessing internal Java reflection or OS calls
            // Fails with: org.jenkinsci.plugins.scriptsecurity.sandbox.RejectedAccessException: Scripts not permitted to use staticMethod java.lang.System getenv
            def env = System.getenv("PATH")
            
            // To get env vars safely in Jenkins, use the 'env' global variable:
            // def path = env.PATH
        }
    }
}
```

## 💥 Production Failures
1.  **The "Approval Death Spiral"**: A developer writes a complex script using 50 new Java methods. They run the build. It fails on method 1. Admin approves it. Run build. Fails on method 2. Admin approves. Repeat 50 times. **Solution**: Move complex code to a Global Shared Library.
2.  **The RCE Sandbox Escape**: An admin blindly approves a highly dangerous signature like `staticMethod java.lang.Runtime getRuntime`. A malicious developer uses this to execute arbitrary bash commands directly on the Controller OS, dumping the `$JENKINS_HOME/secrets` directory.
3.  **Out of Memory (OOM) via Whitelist**: A developer uses a whitelisted method to allocate massive byte arrays in a loop until the Controller heap crashes. The sandbox protects against *access*, not *resource exhaustion*.

## 🧪 Real-time Q&A
*   **Q**: How do I disable the sandbox?
*   **A**: In a "Pipeline script" job, there is a checkbox to "Use Groovy Sandbox". If unchecked, an Admin must approve the *entire script* once. If it's a "Pipeline script from SCM" (Jenkinsfile), the sandbox is **mandatory** and cannot be disabled.
*   **Q**: Why does my Shared Library not need approval?
*   **A**: Global Shared Libraries (configured in System Settings) are considered "Admin-provisioned" and run outside the sandbox as "Trusted Code".

## ⚠️ Edge Cases
*   **Folder-level Shared Libraries**: Libraries defined at the Folder level (not Global) run *inside* the sandbox because Folder admins are not assumed to have system-wide trust.

## 🏢 Best Practices
1.  **Never blindly approve scripts**. If it looks like a core Java API (`java.io.*`, `java.lang.reflect.*`), deny it.
2.  **Use Shared Libraries for Logic**: Shift all non-trivial Groovy code into a Global Shared Library to avoid the Sandbox tax and approval overhead.
3.  **Use native Steps**: Instead of Groovy XML parsers, use the `readJSON` / `readXML` steps provided by the Pipeline Utility Steps plugin.

## ⚖️ Trade-offs
*   **Security vs Friction**: The sandbox prevents massive security incidents, but introduces high friction for developers trying to write custom parsing logic in their Jenkinsfiles.

## 💼 Interview Q&A
*   **Q**: A developer asks you to approve the signature `method java.lang.Class forName java.lang.String`. Do you approve it?
*   **A**: **No, absolutely not.** That signature allows reflection. Once a script can use reflection, it can bypass the entire Sandbox and instantiate any class in the JVM, granting Remote Code Execution on the Controller. I would ask the developer what they are trying to achieve and provide a safe Jenkins-native step or put the logic in a Shared Library.

## 🧩 Practice Problems
1.  Try to generate a UUID in a Jenkinsfile using `java.util.UUID.randomUUID()`. Observe the failure, find the signature in the UI, and approve it.
2.  Refactor a Jenkinsfile that uses `java.io.File` to read a file into one that uses the Jenkins-native `readFile()` step to avoid Sandbox violations.

---
Prev: [02_Jenkinsfile_Execution_Model.md](../Pipelines/02_Jenkinsfile_Execution_Model.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Shared_Libraries.md](../Pipelines/04_Shared_Libraries.md)
---
