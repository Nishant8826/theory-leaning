# 29 – Jenkins Pipelines: Declarative, Scripted & CI Integration

---

## Table of Contents

1. [Freestyle Jobs vs Pipelines – Why Upgrade?](#1-freestyle-jobs-vs-pipelines--why-upgrade)
2. [Two Ways to Define a Pipeline](#2-two-ways-to-define-a-pipeline)
3. [Declarative vs Scripted Pipeline](#3-declarative-vs-scripted-pipeline)
4. [Pipeline Syntax – Every Block Explained](#4-pipeline-syntax--every-block-explained)
5. [Pipeline Syntax Generator](#5-pipeline-syntax-generator)
6. [Building a Java Pipeline – Step by Step](#6-building-a-java-pipeline--step-by-step)
7. [Real Project Pipeline – Freestyle to Pipeline Migration](#7-real-project-pipeline--freestyle-to-pipeline-migration)
8. [Foreground vs Background Processes – The nohup Fix](#8-foreground-vs-background-processes--the-nohup-fix)
9. [CI Configuration with Poll SCM](#9-ci-configuration-with-poll-scm)
10. [Key Jenkins Plugins Reference](#10-key-jenkins-plugins-reference)
11. [Visual Diagrams](#11-visual-diagrams)
12. [Scenario-Based Q&A](#12-scenario-based-qa)
13. [Interview Q&A](#13-interview-qa)

---

## 1. Freestyle Jobs vs Pipelines – Why Upgrade?

### What
A **Jenkins Pipeline** is a way to define your entire CI/CD build process as **code** — written in a file called a `Jenkinsfile`. Instead of clicking through forms in the Jenkins UI (Freestyle), you write the build steps as a script that Jenkins reads and executes.

> 💡 **Analogy:** Freestyle jobs are like filling out a paper form every time you want to build something. Pipelines are like writing a recipe once and letting anyone follow it exactly, every time, forever.

### Why Pipelines Replace Freestyle Jobs
Freestyle projects work for simple setups, but they have serious limitations in real teams:

| Problem with Freestyle | How Pipeline Solves It |
|-----------------------|----------------------|
| Config lives only in Jenkins UI | Config lives in code (Jenkinsfile in GitHub) |
| No version history of pipeline changes | Every change to Jenkinsfile is tracked in Git |
| Hard to review "who changed the pipeline" | Git blame/history shows exactly who changed what |
| Can't reuse across projects easily | Jenkinsfile can be copied and adapted |
| Complex multi-stage flows are painful to configure | Stages are natural in pipeline code |
| If Jenkins server crashes, config is lost | Jenkinsfile is safely in your Git repo |

### Impact

| Without Pipelines | With Pipelines |
|------------------|----------------|
| Build config is tribal knowledge in the UI | Build config is documented as code |
| Pipeline changes have no audit trail | Every change tracked in version control |
| Onboarding a new project takes hours of clicking | Copy the Jenkinsfile and you're done |
| Complex workflows need workarounds | Multi-stage, parallel, conditional flows are native |

---

## 2. Two Ways to Define a Pipeline

### What
Jenkins gives you two options for where the pipeline code lives. Understanding the difference is critical.

---

### Option 1: Pipeline Script (Inline)
- **What:** You write the pipeline code directly inside the Jenkins job configuration UI
- **Where it lives:** Inside Jenkins itself (not in your code repository)
- **Good for:** Quick experiments, learning, demos
- **Bad for:** Real projects — no version control, lost if Jenkins crashes

```
Jenkins Job → Configure → Pipeline → Definition: "Pipeline Script"
→ Write Groovy code directly in the text box
```

---

### Option 2: Pipeline from SCM ✅ (Recommended)
- **What:** The pipeline code lives in a file called `Jenkinsfile` inside your GitHub repository
- **Where it lives:** Your Git repository, alongside your application code
- **Good for:** Everything real — versioned, reviewable, recoverable
- **SCM** = Source Code Management (Git, GitHub, GitLab, etc.)

```
Jenkins Job → Configure → Pipeline → Definition: "Pipeline Script from SCM"
→ SCM: Git
→ Repository URL: https://github.com/yourname/your-repo.git
→ Branch: */main
→ Script Path: Jenkinsfile   ← the filename in your repo
```

Your repository structure looks like this:
```
your-project/
├── Jenkinsfile          ← Pipeline definition lives HERE
├── src/
│   └── HelloWorld.java
├── pom.xml
└── README.md
```

### Why "From SCM" is Always Preferred in Production

> 💡 **The golden rule:** Treat your pipeline as code. If it's not in version control, it doesn't exist.

- If Jenkins server dies → Jenkinsfile is safe in GitHub
- If someone changes the pipeline → Git history shows who, what, and when
- Code review for pipeline changes → PR process applies to Jenkinsfile too
- Multiple environments → different branches can have different Jenkinsfiles

---

## 3. Declarative vs Scripted Pipeline

### What
Jenkins pipelines can be written in two styles — **Declarative** and **Scripted**. Both are written in Groovy (a Java-based scripting language), but they have different syntax and philosophy.

---

### Declarative Pipeline ✅ (Recommended for Most Teams)

#### What
A structured, opinionated syntax that enforces a specific format. Always starts with the `pipeline` keyword.

#### Why
- Easier to read and understand
- Better error messages when something goes wrong
- Enforces best practices (you can't write random code anywhere)
- Supported by the Blue Ocean visual UI
- What most companies use

#### Structure
```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'java -jar target/app.jar'
            }
        }
    }
}
```

---

### Scripted Pipeline (Advanced / Legacy)

#### What
An older, more flexible syntax that starts with the `node` keyword. Gives you full programmatic control — loops, conditionals, complex logic anywhere.

#### Why it exists
Before Declarative Pipeline was introduced, Scripted was the only option. Some teams still use it for complex workflows that Declarative can't handle cleanly.

#### Structure
```groovy
node {
    stage('Build') {
        sh 'mvn clean package'
    }
    stage('Test') {
        sh 'mvn test'
    }
    stage('Deploy') {
        sh 'java -jar target/app.jar'
    }
}
```

---

### Declarative vs Scripted – Side by Side

| | Declarative | Scripted |
|--|------------|---------|
| **Starts with** | `pipeline {` | `node {` |
| **Structure** | Enforced, structured | Freeform |
| **Complexity** | Simpler to read/write | More powerful but complex |
| **Error messages** | Clearer | Harder to debug |
| **Recommended for** | Most pipelines | Complex custom workflows |
| **Blue Ocean support** | ✅ Full | ⚠️ Limited |
| **Best practice** | ✅ Yes | Use only when needed |

> 💡 **Rule:** Start with Declarative. Switch to Scripted only if Declarative genuinely can't do what you need.

---

## 4. Pipeline Syntax – Every Block Explained

Let's break down every keyword in a Declarative Pipeline so you understand exactly what each piece does.

```groovy
pipeline {               // ← Root block. Everything lives inside this.
    agent any            // ← WHERE to run. "any" = use any available Jenkins agent/node

    environment {        // ← (Optional) Define environment variables
        APP_NAME = 'my-app'
        JAVA_HOME = '/usr/lib/jvm/java-21'
    }

    triggers {           // ← (Optional) When to auto-run
        pollSCM('* * * * *')   // Check GitHub every minute
    }

    stages {             // ← Container for all your stages

        stage('Clone') { // ← A named step. Shows up as a box in the UI
            steps {      // ← The actual commands to run inside this stage
                git branch: 'main',
                    url: 'https://github.com/yourname/repo.git'
            }
        }

        stage('Compile') {
            steps {
                sh 'javac HelloWorld.java'   // sh = run a shell command
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Package') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Deploy') {
            steps {
                sh 'nohup java -jar target/app.jar &'
            }
        }
    }

    post {               // ← (Optional) Actions after all stages complete
        success {
            echo 'Build succeeded! 🎉'
        }
        failure {
            echo 'Build failed! ❌ Check the logs.'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}
```

---

### Key Keywords Reference

| Keyword | What it does |
|---------|-------------|
| `pipeline` | Root block — everything goes inside this |
| `agent any` | Run on any available Jenkins node/machine |
| `agent none` | Don't assign a global agent — each stage picks its own |
| `agent { label 'linux' }` | Run on a specific agent with the label "linux" |
| `stages` | Container that holds all the stage blocks |
| `stage('Name')` | A named phase of the build — shows up visually in Jenkins UI |
| `steps` | The actual commands inside a stage |
| `sh '...'` | Run a shell (bash) command on Linux/Mac |
| `bat '...'` | Run a batch command on Windows |
| `echo '...'` | Print a message to the console log |
| `environment` | Define variables available to the whole pipeline |
| `triggers` | Define when the pipeline auto-runs |
| `post` | Define actions after the pipeline finishes |

---

## 5. Pipeline Syntax Generator

### What
Jenkins has a built-in tool called the **Snippet Generator** (or Pipeline Syntax Generator) that helps you generate the correct Groovy syntax for any pipeline step without memorizing it.

### Why
Pipeline syntax can be complex — especially for steps like checking out from Git, archiving artifacts, or sending notifications. The generator produces the exact code you need.

### How to Use It

```
Jenkins Dashboard
→ [Your Pipeline Job]
→ Configure
→ Scroll to Pipeline section
→ Click "Pipeline Syntax" link (opens Snippet Generator)

In the generator:
1. Select the step you want (e.g., "git: Git")
2. Fill in the form fields (Repository URL, branch, credentials)
3. Click "Generate Pipeline Script"
4. Copy the generated code into your Jenkinsfile
```

### Example – Generating a Git Checkout Step

```
Step: git: Git
Repository URL: https://github.com/Nishant8826/javaspringboot-ecommerce.git
Branch: main
Credentials: (select your GitHub credentials)

Generated output:
git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/Nishant8826/javaspringboot-ecommerce.git'
```

Paste this directly into your `stage('Clone') { steps { ... } }` block.

### Impact

| Without Snippet Generator | With Snippet Generator |
|--------------------------|----------------------|
| Memorize complex Groovy syntax | Generate it in 30 seconds |
| Trial and error on syntax errors | First attempt is correct |
| Look up documentation constantly | Everything in one UI |

---

## 6. Building a Java Pipeline – Step by Step

### The Pipeline We Built in Class

This pipeline takes a simple Java Hello World program from GitHub, compiles it, and runs it.

#### The Java Code (in GitHub)
```java
// HelloWorld.java
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class HelloWorld {
    public static void main(String[] args) {
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        System.out.println("Hello, World! Real-time Execution: " + dtf.format(LocalDateTime.now()));
    }
}
```

#### The Jenkinsfile

```groovy
pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourname/hello-java.git'
            }
        }

        stage('Compile') {
            steps {
                sh 'javac HelloWorld.java'
                // Produces: HelloWorld.class
            }
        }

        stage('Run') {
            steps {
                sh 'java HelloWorld'
                // Output: Hello, World! Real-time Execution: 2026-04-27 10:15:30
            }
        }

    }
}
```

#### What Jenkins Does at Each Stage

```
Stage: Clone
  → Jenkins runs: git clone https://github.com/yourname/hello-java.git
  → Code now in: /var/lib/jenkins/workspace/[job-name]/

Stage: Compile
  → Jenkins runs: javac HelloWorld.java
  → Produces: HelloWorld.class (bytecode)
  → Error here = BUILD FAILURE (syntax error in Java)

Stage: Run
  → Jenkins runs: java HelloWorld
  → Console shows: Hello, World! Real-time Execution: 2026-04-27 10:15:30
  → Build: SUCCESS ✅
```

#### How to Create This Job in Jenkins

```
Step 1: Dashboard → New Item
Step 2: Name: hello-java-pipeline
Step 3: Type: Pipeline → OK
Step 4: Scroll to Pipeline section
Step 5: Definition: Pipeline Script
Step 6: Paste the Jenkinsfile code
Step 7: Save → Build Now
Step 8: Click build #1 → Console Output to verify
```

---

## 7. Real Project Pipeline – Freestyle to Pipeline Migration

### What Was Converted
The shopping cart Java Spring Boot project from the previous class was migrated from a Freestyle job to a proper Pipeline with multiple stages.

### Why Migrate?
- Freestyle had no version history
- Adding stages (test → sonar → deploy) was becoming messy in UI forms
- Team needs pipeline-as-code going forward

### The Full Shopping Cart Pipeline

```groovy
pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')   // Check GitHub every minute
    }

    stages {

        stage('Clone Code') {
            steps {
                git url: 'https://github.com/Nishant8826/javaspringboot-ecommerce.git', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Run') {
            steps {
                sh 'java -jar /var/lib/jenkins/workspace/pipeline/target/Shopping_Cart-0.0.1-SNAPSHOT.jar --server.port=4000 '
            }
        }

        stage('Deploy') {
            steps {
                sh 'nohup java -jar target/Shopping_Cart-0.0.1-SNAPSHOT.jar &'
                // Runs in background so Jenkins job can complete
            }
        }

    }

    post {
        success {
            echo '✅ Shopping cart deployed successfully!'
        }
        failure {
            echo '❌ Build failed — check the logs above.'
        }
    }
}
```

### Stage-by-Stage Walkthrough

#### Stage 1: Clone Code
- Jenkins pulls the latest code from GitHub
- Code lands in: `/var/lib/jenkins/workspace/pipeline/`
- If branch doesn't exist or URL is wrong → stage fails immediately

#### Stage 2: Build (`mvn clean package`)
- `clean`: Deletes old `target/` folder
- `package`: Compiles → runs tests → creates JAR
- Output: `target/Shopping_Cart-0.0.1-SNAPSHOT.jar`
- If tests fail → stage fails, Deploy stage never runs (this is the safety gate)

#### Stage 3: Run
- Executes the built Spring Boot JAR file directly in the **foreground** using its absolute workspace path.
- Explicitly binds the application to port 4000 (`--server.port=4000`).
- ⚠️ **Warning:** Because this command runs in the foreground without `nohup` or `&`, it will cause Jenkins to hang indefinitely waiting for the process to finish (which leads perfectly into the explanation in Section 8).

#### Stage 4: Deploy
- Runs the JAR as a background process (`nohup ... &`)
- App starts on configured port (4000 or 8080)
- Jenkins job completes successfully

> 💡 **Key Concept: Are `Run` and `Deploy` doing the same thing?**
> Yes and No! Both stages execute the application, but they behave fundamentally differently in a pipeline:
> - **The `Run` Stage (Foreground):** Jenkins waits for the command to finish. Since a Spring Boot app never stops, Jenkins **hangs forever** and the build eventually fails. This is a common beginner mistake.
> - **The `Deploy` Stage (Background):** The `nohup` and `&` detach the process. Jenkins fires the command, moves on immediately, and the build **succeeds** while your app stays online in the background.

---

## 8. Foreground vs Background Processes – The nohup Fix

### The Problem
This is one of the most common beginner mistakes with Jenkins pipelines.

When you run `java -jar app.jar` in a Jenkins step, the application starts and **keeps running** — it never exits. Jenkins waits for the command to finish before moving to the next stage. Since a running Spring Boot app never exits on its own, **Jenkins hangs forever**.

```
Stage: Deploy
  → sh 'java -jar target/Shopping_Cart-0.0.1-SNAPSHOT.jar'
  → App starts...
  → Jenkins waits...
  → Jenkins waits...
  → Jenkins waits...  (forever — job never completes)
```

### Why This Happens
Shell commands in Jenkins pipeline `sh` steps run in the **foreground** — Jenkins waits until the process exits to mark the step as complete. A web application runs continuously and never exits voluntarily.

### Solution 1: Background Process with `&`
The `&` at the end of a command tells the shell to run it in the **background** — the shell moves on immediately without waiting.

```groovy
sh 'java -jar target/Shopping_Cart-0.0.1-SNAPSHOT.jar &'
// The & detaches the process → Jenkins step completes immediately
// App continues running in the background
```

### Solution 2: `nohup` + `&` (More Robust) ✅

```groovy
sh 'nohup java -jar target/Shopping_Cart-0.0.1-SNAPSHOT.jar &'
```

- **`nohup`** = "No Hang Up" — tells the process to keep running even if the terminal/Jenkins session that started it closes
- **`&`** = runs in background
- Combined: the app starts, detaches completely from Jenkins, and keeps running even after the pipeline finishes

### Solution 3: Port Override with nohup

```groovy
sh 'nohup java -jar -Dserver.port=4000 target/Shopping_Cart-0.0.1-SNAPSHOT.jar &'
```

### When to Use What

| Situation | Command |
|-----------|---------|
| App should run briefly then stop | `sh 'java -jar app.jar'` (no `&`) |
| App should keep running, simple | `sh 'java -jar app.jar &'` |
| App should keep running even after Jenkins finishes | `sh 'nohup java -jar app.jar &'` ✅ |
| App needs a specific port | `sh 'nohup java -jar -Dserver.port=4000 app.jar &'` |

### Impact

| Without nohup/& | With nohup & |
|----------------|-------------|
| Jenkins job hangs indefinitely | Pipeline completes successfully |
| Build timeout eventually kills job | App runs independently after pipeline |
| No way to know if deploy succeeded | Post-stage confirms success |
| Manual killing of stuck jobs required | Clean, automated pipeline |

---

## 9. CI Configuration with Poll SCM

### What
Poll SCM in a Pipeline is configured inside the `triggers` block — it tells Jenkins to automatically check GitHub for new commits and trigger the pipeline if changes are found.

### How to Configure in a Declarative Pipeline

```groovy
pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')       // Check every minute
        // pollSCM('*/5 * * * *')  // Check every 5 minutes
        // pollSCM('H/10 * * * *') // Every 10 min (H = hash-based, avoids thundering herd)
    }

    stages {
        // ... your stages
    }
}
```

### The `H` (Hash) Syntax – Pro Tip
Using `H` instead of `*` tells Jenkins to distribute builds evenly across time, preventing all jobs from running at exactly :00 every hour:

```groovy
pollSCM('H/10 * * * *')   // Every 10 min, but offset per job (not all at :00, :10, :20)
pollSCM('H 8 * * 1-5')    // Once in the 8 AM hour, weekdays only
```

### Alternative: Webhook Trigger (Production Best Practice)
Instead of polling, configure GitHub to *push* a notification to Jenkins when code is pushed:

```groovy
triggers {
    githubPush()   // Requires GitHub Integration plugin + webhook configured in GitHub
}
```

### Full CI Pipeline Behavior

```
Developer pushes commit to GitHub
         │
         │ (Poll SCM fires every minute)
         ▼
Jenkins detects new commit
         │
         ▼
Pipeline triggers automatically:
  Stage 1: Clone  (pulls latest code)
  Stage 2: Build  (mvn clean package)
  Stage 3: Deploy (nohup java -jar ...)
         │
         ▼
Developer gets result (SUCCESS or FAILURE)
without ever clicking "Build Now"
```

---

## 10. Key Jenkins Plugins Reference

These plugins were discussed in class as essential for a real CI/CD setup.

| Plugin | What it enables | When you need it |
|--------|----------------|-----------------|
| **Pipeline** | Jenkinsfile pipeline support | Always — required for pipelines |
| **Git** | Connect to Git repositories | Always — needed to clone code |
| **GitHub** | GitHub-specific integration (webhooks, PR status) | When using GitHub |
| **Maven Integration** | Build Java/Maven projects | Any Java project using Maven |
| **Docker Pipeline** | Build/push Docker images in pipelines | When containerizing apps |
| **SonarQube Scanner** | Code quality analysis stage | When adding quality gates |
| **Credentials** | Securely store tokens, passwords, SSH keys | Always — keep secrets out of Jenkinsfile |
| **Build Timeout** | Automatically kill hung builds | Prevents the foreground-process hang problem |
| **Blue Ocean** | Visual pipeline UI | When you want a pretty pipeline visualization |
| **Role-based Authorization** | RBAC user permissions | Multi-user Jenkins environments |

### How to Install Any Plugin
```
Manage Jenkins → Plugins → Available Plugins
Search for plugin name → Check the box → Install
Restart Jenkins if required
```

### The Credentials Plugin – Critical Security Note
Never hardcode passwords, tokens, or SSH keys in your Jenkinsfile. Use the Credentials plugin:

```
Manage Jenkins → Credentials → (global) → Add Credentials
Kind: Secret text (for tokens) or Username/Password
ID: github-token   ← You reference this ID in Jenkinsfile
```

Then in your Jenkinsfile:
```groovy
environment {
    GITHUB_TOKEN = credentials('github-token')  // Safe — never exposed in logs
}
```

---

## 11. Visual Diagrams

### Diagram 1: Freestyle Job vs Pipeline Job

```
FREESTYLE JOB                          PIPELINE JOB
─────────────                          ────────────
Config lives in Jenkins UI             Config lives in Jenkinsfile (GitHub)
       │                                      │
       ▼                                      ▼
  Click forms                          Write Groovy code
       │                                      │
No version history                    Git tracks every change
       │                                      │
Hard to reuse                         Copy Jenkinsfile to any project
       │                                      │
Limited multi-stage flow              Natural multi-stage, parallel, conditional
       │                                      │
Jenkins crash = lost config            Jenkins crash = Jenkinsfile safe in Git
```

---

### Diagram 2: Pipeline Script vs Pipeline from SCM

```
OPTION 1: Pipeline Script              OPTION 2: Pipeline from SCM ✅
────────────────────────               ────────────────────────────
Jenkins Job UI                         GitHub Repository
┌────────────────────┐                 ┌────────────────────┐
│ pipeline {         │                 │ your-project/      │
│   agent any        │                 │ ├── Jenkinsfile ◄──│── Jenkins reads this
│   stages {         │                 │ ├── src/           │
│     ...            │                 │ ├── pom.xml        │
│   }                │                 │ └── README.md      │
│ }                  │                 └────────────────────┘
└────────────────────┘
         │                                        │
  Lives in Jenkins                         Lives in Git
  Not versioned                            Fully versioned
  Lost if Jenkins dies                     Safe forever
  No peer review                           PR process applies
```

---

### Diagram 3: Declarative Pipeline Anatomy

```
pipeline {                    ← Root block (required)
    │
    ├── agent any             ← Where to run (any node)
    │
    ├── environment { }       ← (Optional) Variables
    │
    ├── triggers { }          ← (Optional) Auto-run rules
    │
    ├── stages {              ← Container for all stages
    │     │
    │     ├── stage('Clone')  ← Stage 1: named phase
    │     │     └── steps { git ... }
    │     │
    │     ├── stage('Build')  ← Stage 2
    │     │     └── steps { sh 'mvn ...' }
    │     │
    │     └── stage('Deploy') ← Stage 3
    │           └── steps { sh 'nohup ...' }
    │
    └── post { }              ← (Optional) After all stages
          ├── success { }
          ├── failure { }
          └── always { }
}
```

---

### Diagram 4: Java Pipeline Execution Flow

```
GitHub Repo                    Jenkins (Pipeline Execution)
─────────────                  ─────────────────────────────
HelloWorld.java                Stage 1: Clone
                               → git pull from GitHub
                               → files in workspace/

                               Stage 2: Compile
                               → sh 'javac HelloWorld.java'
                               → Produces: HelloWorld.class

                               Stage 3: Run
                               → sh 'java HelloWorld'
                               → Console: "Hello, World!"

                               BUILD: SUCCESS ✅
```

---

### Diagram 5: The Foreground Process Problem & Fix

```
WITHOUT nohup:                        WITH nohup &:
──────────────                        ─────────────
Stage: Deploy                         Stage: Deploy
  sh 'java -jar app.jar'                sh 'nohup java -jar app.jar &'
       │                                      │
       ▼                                      ▼
  App starts...                         App starts...
       │                                      │
  Jenkins waits...                      & → detaches process
       │                                      │
  Jenkins waits... (forever)            nohup → survives session end
       │                                      │
  ❌ Build Timeout Error                ✅ Step completes immediately
                                              │
                                        Stage: Deploy → SUCCESS
                                              │
                                        App still running on server
```

---

### Diagram 6: Full CI Pipeline Flow

```
Developer                    GitHub                    Jenkins
────────                     ──────                    ───────
  │                             │                         │
  │── git push ────────────────►│                         │
  │                             │                         │
  │                             │◄── pollSCM (every min) ─│
  │                             │                         │
  │                             │── "new commit found" ──►│
  │                             │                         │
  │                             │                Trigger pipeline:
  │                             │                  Stage 1: Clone ✅
  │                             │                  Stage 2: Build ✅
  │                             │                  Stage 3: Deploy ✅
  │                             │                         │
  │◄── Console notification ────────────────────────────── │
       "BUILD SUCCESS"
```

---

### Diagram 7: Declarative vs Scripted Structure

```
DECLARATIVE                           SCRIPTED
────────────                          ─────────
pipeline {                            node {
    agent any                             stage('Build') {
    stages {                                  sh 'mvn package'
        stage('Build') {                  }
            steps {                       stage('Test') {
                sh 'mvn package'              sh 'mvn test'
            }                             }
        }                             }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}

More structured ✅                    More flexible
Easier to read ✅                     More complex
Recommended ✅                        Use only when needed
```

---

## 12. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your team's Jenkins server crashed and had to be rebuilt from scratch. All your Freestyle job configurations are gone. How do you prevent this from happening again with your next pipeline?

✅ **Answer:** Switch all jobs to **Pipeline from SCM**. Create a `Jenkinsfile` in every GitHub repository containing the pipeline definition. When Jenkins is rebuilt, you simply create new Pipeline jobs that point to the repository — Jenkins reads the `Jenkinsfile` and the complete pipeline configuration is restored in minutes. The pipeline config lives in Git, not Jenkins. A Jenkins crash becomes a minor inconvenience instead of a disaster.

---

🔍 **Scenario 2:** Your pipeline's Deploy stage is hanging and eventually timing out. The console log just shows the Spring Boot startup banner and then nothing. What's wrong and how do you fix it?

✅ **Answer:** The Spring Boot application is starting in the **foreground** — the `sh 'java -jar app.jar'` command doesn't return because the app keeps running. Jenkins waits for it to exit, which never happens. Fix it by running the process in the background with `nohup`: `sh 'nohup java -jar target/app.jar &'`. The `nohup` ensures the process survives after the step completes, and the `&` detaches it immediately so Jenkins can mark the step as done and move on.

---

🔍 **Scenario 3:** A junior DevOps engineer writes a Jenkinsfile and hardcodes a GitHub personal access token directly in the pipeline script. What's the risk and how should it be done correctly?

✅ **Answer:** Hardcoding credentials in a Jenkinsfile is a critical security risk — the token is visible to anyone who can view the Jenkins job or the GitHub repository (if the Jenkinsfile is committed). The correct approach: store the token in Jenkins using the **Credentials plugin** (Manage Jenkins → Credentials → Add → Secret Text → ID: `github-token`), then reference it safely in the Jenkinsfile using `credentials('github-token')`. Jenkins automatically masks the value in console logs so it's never exposed.

---

🔍 **Scenario 4:** Your manager asks you to add a quality gate to the pipeline — no deployment unless the code passes SonarQube analysis. How do you add this as a pipeline stage?

✅ **Answer:** Add a `stage('Quality Gate')` between Build and Deploy in the Jenkinsfile. Install the SonarQube Scanner plugin in Jenkins and configure the SonarQube server URL in Jenkins settings. Then:
```groovy
stage('Quality Gate') {
    steps {
        withSonarQubeEnv('SonarQube') {
            sh 'mvn sonar:sonar'
        }
        timeout(time: 5, unit: 'MINUTES') {
            waitForQualityGate abortPipeline: true
        }
    }
}
```
If SonarQube gives a "Fail" rating, `abortPipeline: true` stops the pipeline before Deploy runs. No deployment unless code quality passes.

---

🔍 **Scenario 5:** You've set up `pollSCM('* * * * *')` but your builds are still running even when no code was pushed. Why might this happen?

✅ **Answer:** Poll SCM checks if there are *any* new commits since the last build — including commits on other branches, tags, or even changes to the repository metadata. Check the **Git Polling Log** (Job → Git Polling Log) to see exactly what change Jenkins detected. Common causes: pushing to a different branch that the pipeline is also watching (`*/main` vs `*/*`), committing the Jenkinsfile itself triggering a new build, or a misconfigured branch specifier. Consider using `githubPush()` with a webhook instead of polling to get more precise trigger control.

---

🔍 **Scenario 6:** You want the pipeline to send a Slack message on failure but not on success. How do you configure this in the `post` section?

✅ **Answer:** Use the `post` block's `failure` condition with the Slack Notification plugin:
```groovy
post {
    failure {
        slackSend channel: '#devops-alerts',
                  color: 'danger',
                  message: "❌ Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
    }
    success {
        echo '✅ Build passed — no Slack alert needed'
    }
}
```
The `failure` block only runs when the pipeline fails. The `success` block only runs on success. `always` would run in both cases. `env.JOB_NAME`, `env.BUILD_NUMBER`, and `env.BUILD_URL` are built-in Jenkins environment variables available in every pipeline.

---

## 13. Interview Q&A

---

**Q1. What is a Jenkins Pipeline and how is it different from a Freestyle job?**

**A:** A Jenkins Pipeline is a way to define your entire CI/CD process as code in a file called `Jenkinsfile`. Unlike Freestyle jobs — where you configure build steps by clicking through UI forms — a Pipeline is written in Groovy and stored in your source code repository. The key advantages of Pipelines: version control (every change to the pipeline is tracked in Git), recoverability (survives Jenkins server crashes), code review (pipeline changes go through the PR process), and support for complex multi-stage workflows with native stage visualization. Freestyle is appropriate for simple, one-off tasks; Pipelines are the standard for any real CI/CD workflow.

---

**Q2. What is the difference between Declarative and Scripted pipelines?**

**A:** Both are ways to write Jenkins pipeline code in Groovy, but with different structure and philosophy:
- **Declarative** starts with `pipeline {` and enforces a structured format. It's easier to read, produces clearer error messages, and is recommended for most use cases. The pipeline structure (agent, stages, post) is defined and predictable.
- **Scripted** starts with `node {` and gives complete programmatic freedom — you can write arbitrary Groovy code anywhere. It's more powerful for complex custom logic but harder to maintain and debug.

Recommendation: always start with Declarative. Only switch to Scripted if Declarative genuinely can't handle a specific requirement.

---

**Q3. What is a Jenkinsfile and where should it live?**

**A:** A Jenkinsfile is a text file containing the pipeline definition written in Groovy. It should live in the root of your application's Git repository, checked in alongside your source code. This approach — Pipeline from SCM — is the industry best practice because it means the pipeline definition is version-controlled, peer-reviewed through pull requests, and recoverable if Jenkins crashes. Never store your Jenkinsfile only in Jenkins UI (Pipeline Script) for production workloads. Treat your Jenkinsfile as code: it deserves the same review and version control discipline as application code.

---

**Q4. What does `agent any` mean in a Jenkins Pipeline?**

**A:** `agent any` tells Jenkins to run the pipeline on any available build agent (node). In a single-server Jenkins setup, that's the Jenkins master itself. In a Master-Slave (Controller-Agent) setup with multiple build nodes, Jenkins will pick whichever agent is free. The `agent` directive can also be more specific: `agent { label 'linux' }` runs only on agents tagged "linux", `agent { docker 'maven:3.8' }` runs inside a specific Docker container, and `agent none` means no global agent — each stage must define its own. For beginners with a single Jenkins server, `agent any` is always the right choice.

---

**Q5. Why do Spring Boot applications hang Jenkins pipeline deploy stages, and how do you fix it?**

**A:** When Jenkins runs `sh 'java -jar app.jar'`, it waits for the process to exit before marking the step as complete. Spring Boot applications run continuously as web servers — they never exit on their own. Jenkins waits indefinitely, eventually hitting the Build Timeout.

Fix: use `nohup java -jar app.jar &`
- `&` runs the process in the background, so the shell returns immediately
- `nohup` ensures the process keeps running even after the Jenkins session that started it closes

This is a fundamental Linux process management concept: foreground processes block the terminal; background processes let it move on.

---

**Q6. What is the `post` block in a Declarative Pipeline and what are its conditions?**

**A:** The `post` block defines actions to take after all stages complete, regardless of outcome. It supports several conditions:
- `success` — runs only when the pipeline succeeds
- `failure` — runs only when the pipeline fails
- `always` — runs no matter what (cleanup tasks, notifications)
- `unstable` — runs when the build is marked unstable (some tests failed but didn't abort)
- `changed` — runs when the result is different from the previous build (e.g., fixed a failing build)
- `aborted` — runs when the pipeline was manually stopped

Common uses: sending Slack/email notifications on failure, archiving test reports, cleaning up temporary files.

---

**Q7. What is the Pipeline Syntax Generator and when do you use it?**

**A:** The Pipeline Syntax Generator (Snippet Generator) is a built-in Jenkins tool that generates correct Groovy syntax for pipeline steps without requiring memorization. Access it from any Pipeline job: Configure → Pipeline → "Pipeline Syntax" link. You select the step type (e.g., `git: Git`), fill in the form fields (URL, branch, credentials), click "Generate Pipeline Script," and copy the output directly into your Jenkinsfile. Use it whenever you need to: add a Git checkout step, archive build artifacts, send notifications, integrate with external tools, or use any step whose exact syntax you don't know. It eliminates trial-and-error syntax debugging.

---

**Q8. What are the `sh` and `bat` steps in a Jenkins Pipeline? When do you use each?**

**A:** `sh` executes a shell (bash) command on Linux or macOS build agents. `bat` executes a Windows batch command on Windows build agents. In a typical DevOps environment running Linux-based Jenkins servers, `sh` is used almost exclusively. Examples:
```groovy
sh 'mvn clean package'           // Linux: run Maven
sh 'javac HelloWorld.java'       // Linux: compile Java
bat 'mvn clean package'          // Windows: same Maven command
```
If your pipeline must support both OS types, use the `isUnix()` function: `if (isUnix()) { sh '...' } else { bat '...' }`. In practice, CI/CD servers are almost always Linux, so `sh` is the standard.

---

**Q9. What is the difference between `pollSCM` and a GitHub webhook for triggering pipelines?**

**A:**
- **`pollSCM`** — Jenkins periodically checks the Git repository for new commits on a cron schedule. Simple to configure, works on private networks, but introduces polling delay and wastes resources checking when nothing changed.
- **GitHub Webhook** — GitHub calls Jenkins immediately when a push event occurs. Real-time (sub-second trigger), no wasted polling, but requires Jenkins to be publicly reachable (or use a reverse proxy/tunnel).

In production, **webhooks are preferred** because they're real-time and efficient. Poll SCM is acceptable for learning environments, internal networks where webhooks aren't feasible, or as a fallback when webhooks fail. Configure webhooks in GitHub: Repo Settings → Webhooks → Add Webhook → Payload URL: `http://JENKINS_URL/github-webhook/`.

---

← Previous: [28_Java,_Spring_Boot_Maven_&_Jenkins_Build_Pipeline.md](28_Java,_Spring_Boot_Maven_&_Jenkins_Build_Pipeline.md) | Next: [`30_Jenkins_Master_Slave_Architecture_&_Node_Configuration.md](30_Jenkins_Master_Slave_Architecture_&_Node_Configuration.md) →