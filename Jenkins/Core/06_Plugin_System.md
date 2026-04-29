# ⚙️ Plugin System

## 📌 Topic Name
Jenkins Plugin Architecture: Classloaders, Injection, and Global Namespace

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Plugins add features to Jenkins, like connecting to AWS or Slack.
*   **Expert**: The Jenkins plugin system is the source of its immense power and its greatest instability. It relies on a custom **Classloader Hierarchy** and **Extension Points** annotated with `@Extension`. Plugins are packaged as `.hpi`/`.jpi` files. Because all plugins eventually run within the single Controller JVM, they share the same heap and can cause catastrophic global conflicts (Dependency Hell) if they require different versions of the same core Java libraries.

## 🏗️ Mental Model
Think of Jenkins Core as a **Smartphone OS** and Plugins as **Apps**.
- **Extension Points**: The OS provides "Hooks" (e.g., "Add a button to the Job screen").
- **Injection**: When the OS boots, it finds all Apps that have registered for that hook and injects their code.
- **The Problem**: Unlike an iPhone where apps are strictly isolated in sandboxes, Jenkins plugins are more like shared browser extensions. If Plugin A brings an outdated version of a critical library (like Jackson JSON), and Plugin B needs the new version, the entire browser (Jenkins) might crash.

## ⚡ Actual Behavior
- **Dynamic Loading**: Plugins can theoretically be loaded without restarting Jenkins, but in practice, modifying classloaders at runtime causes memory leaks. Always restart after plugin changes.
- **The Uber-Classloader Leak**: While Jenkins attempts to give each plugin its own Classloader, Java's delegation model means plugins often inadvertently share transitive dependencies through the parent classloader, leading to `NoSuchMethodError`.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **HPI Format**: A plugin is a JAR file renamed to `.hpi` (Hudson Plugin Interface). It contains compiled `.class` files, Jelly/Groovy UI templates, and a `META-INF/MANIFEST.MF` that declares dependencies.
2.  **Guice & `@Extension`**: Jenkins scans the classpath on startup for classes annotated with `@Extension`. It uses Guice to instantiate them and register them into the global registry.
3.  **Classloader Topology**: 
    - `Core Classloader`: Loads Jenkins base classes.
    - `Plugin Classloader`: One per plugin. It checks its own JAR first, then asks the Core Classloader, then asks its declared Plugin Dependencies.

## 🔁 Execution Flow (Startup Plugin Load)
1.  **Discovery**: Jenkins scans `$JENKINS_HOME/plugins/*.jpi`.
2.  **Dependency Graph**: It reads all Manifests and builds a Directed Acyclic Graph (DAG) to determine load order.
3.  **Classloader Instantiation**: Creates a custom Classloader for each plugin.
4.  **Bytecode Parsing**: Uses the `SezPoz` library to rapidly scan bytecode for `@Extension` annotations without fully loading the classes into memory.
5.  **Registration**: Instantiates the classes and maps them to Extension Points (e.g., `SCM`, `BuildStep`, `Publisher`).

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Metaspace Exhaustion**: Every loaded Java class resides in JVM Metaspace (formerly PermGen). Loading 200 massive plugins can exhaust Metaspace, causing the JVM to crash.
- **Startup CPU**: Building the dependency graph and scanning annotations is heavily CPU bound during boot.

## 📐 ASCII Diagrams (MANDATORY)
```text
+---------------------------------------------------+
|               JVM METASPACE / HEAP                |
|                                                   |
|  [ CORE CLASSLOADER ]                             |
|      | (Provides Jenkins API)                     |
|      |                                            |
|      +----------+--------------------+            |
|      |          |                    |            |
| [ PLUGIN A ]  [ PLUGIN B ]      [ PLUGIN C ]      |
| Classloader   Classloader       Classloader       |
| (Needs Libv1) (Needs Plugin A)  (Needs Libv2)     |
|                                     |             |
|                                   (CRASH! Class   |
|                                   Conflict)       |
+---------------------------------------------------+
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```java
// Example of a Java Plugin implementation
import hudson.Extension;
import hudson.model.RootAction;

// The @Extension annotation tells Jenkins to inject this at boot
@Extension
public class MyCustomUIEndpoint implements RootAction {
    @Override
    public String getIconFileName() { return "gear.png"; }

    @Override
    public String getDisplayName() { return "My Custom Dashboard"; }

    @Override
    public String getUrlName() { return "my-dashboard"; }
}
```

## 💥 Production Failures
1.  **Jar Hell (Dependency Conflict)**: Plugin X uses `aws-java-sdk v1`. Plugin Y uses `aws-java-sdk v2`. Jenkins tries to load both. A pipeline calling AWS suddenly throws `java.lang.NoSuchMethodError` because the Classloader grabbed the v1 class instead of the v2 class. **Solution**: Use the "Plugin BOM" (Bill of Materials) to align versions, or wait for the maintainers to update.
2.  **Memory Leaks via ThreadLocals**: A poorly written plugin stores data in a `ThreadLocal` variable but forgets to clear it. Because Jetty reuses HTTP threads, the data persists forever, eventually causing an `OutOfMemoryError`.
3.  **The "Pinning" Trap**: An admin manually uploads an old `.hpi` file, "pinning" it. Jenkins updates the core, which requires a newer version of the plugin. Jenkins refuses to boot because the pinned plugin breaks the dependency graph.

## 🧪 Real-time Q&A
*   **Q**: How do I safely update plugins?
*   **A**: Never click "Update All" in production. Always test plugin updates in a staging environment. Plugins are code executing in the core JVM; an update can break the entire system.
*   **Q**: What is a "Detached Plugin"?
*   **A**: A feature that used to be built into Jenkins Core but was moved into its own plugin to reduce core bloat (e.g., Maven integration).

## ⚠️ Edge Cases
*   **Security Vulnerabilities**: Because plugins run in the Controller JVM, a vulnerability in ANY plugin (like an unescaped UI field) gives the attacker RCE (Remote Code Execution) on the Controller itself.

## 🏢 Best Practices
1.  **Minimalism**: Install the absolute minimum number of plugins required. More plugins = larger heap, slower boot, and higher vulnerability surface.
2.  **Plugin Manager CLI**: Manage plugins via code using the `jenkins-plugin-cli` tool to ensure deterministic environments.
3.  **Audit Regularly**: Remove plugins that haven't been updated by their authors in over 2 years.

## ⚖️ Trade-offs
*   **Extensibility vs Stability**: The lack of strict sandboxing means plugins can do almost anything (Extensibility), but it also means a single bad plugin can crash the whole system (Instability).

## 💼 Interview Q&A
*   **Q**: Your Jenkins instance crashes on boot with `java.lang.NoClassDefFoundError`. What is the likely cause and how do you fix it?
*   **A**: This is a severe plugin dependency issue. A plugin was loaded, but a Java class it requires is missing from the Classpath. This usually happens after a botched upgrade. To fix it, I would bypass the UI (which is dead), SSH into the server, check the `jenkins.log` to identify the failing plugin, and manually remove or downgrade that specific `.hpi` file in the `$JENKINS_HOME/plugins` directory, then restart the service.

## 🧩 Practice Problems
1.  Use the `jenkins-plugin-cli` tool to generate a `plugins.txt` file listing all installed plugins and their specific versions.
2.  Locate the `.hpi` files in the `$JENKINS_HOME/plugins` directory, unzip one of them, and inspect its `META-INF/MANIFEST.MF` to see its dependencies.
