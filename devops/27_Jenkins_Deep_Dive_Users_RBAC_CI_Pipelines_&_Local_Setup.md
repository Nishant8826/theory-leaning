# 27 – Jenkins Deep Dive: Users, RBAC, CI Pipelines & Local Setup

---

## Table of Contents

1. [Jenkins User Management & Security](#1-jenkins-user-management--security)
2. [Role-Based Access Control (RBAC)](#2-role-based-access-control-rbac)
3. [Continuous Integration – Automated Triggers](#3-continuous-integration--automated-triggers)
4. [Java Application Build & Deployment in Jenkins](#4-java-application-build--deployment-in-jenkins)
5. [Jenkins Local Installation (WAR File Method)](#5-jenkins-local-installation-war-file-method)
6. [Plugin Lifecycle Management](#6-plugin-lifecycle-management)
7. [Real-Time DevOps Mindset](#7-real-time-devops-mindset)
8. [Visual Diagrams](#8-visual-diagrams)
9. [Scenario-Based Q&A](#9-scenario-based-qa)
10. [Interview Q&A](#10-interview-qa)

---

## 1. Jenkins User Management & Security

### What
Jenkins has a built-in **user management system** that lets you create individual accounts for every person who needs access to Jenkins. Each user can have their own login credentials and, through security settings, different levels of access.

### Why
In a real company, Jenkins is connected to your production pipelines. You cannot give everyone admin-level access:
- A **developer** should be able to trigger builds — not delete them
- An **L1 support** team member might only need to *view* build logs — not configure jobs
- An **admin** manages everything

Without user management, Jenkins would either be wide open (dangerous) or locked to one shared account (no accountability, no audit trail).

### How – Creating a New User

```
Step 1: Log in as admin
Step 2: Go to → Dashboard → Manage Jenkins → Users
Step 3: Click → "Create User"
Step 4: Fill in:
         - Username   (e.g., balaji)
         - Password
         - Full Name
         - Email
Step 5: Click → "Create User"
Step 6: Test in incognito window:
         - Open new incognito tab
         - Go to Jenkins URL
         - Log in with new credentials
         - Verify access works correctly
```

> 💡 **Why incognito?** Your main browser is already logged in as admin. Incognito starts a fresh session with no cookies — it lets you test the new user's login without logging out of your admin session.

### Impact

| Without User Management | With User Management |
|------------------------|---------------------|
| Everyone shares one login | Individual accountability |
| No audit trail (who did what?) | Full activity log per user |
| One mistake affects everyone | Scoped access limits damage |
| Security risk in production | Controlled, role-based access |

---

## 2. Role-Based Access Control (RBAC)

### What
**RBAC** is a security model where permissions are assigned based on a person's **role**, not their individual identity. You define roles (like "developer", "L1-support", "admin"), set what each role can do, then assign users to roles.

> 💡 **Analogy:** In a hospital, doctors can prescribe medicine, nurses can administer it, and receptionists can only view appointments. Same building, very different access — based on role.

### Why
Jenkins by default gives all users either no access or full admin access. RBAC allows **fine-grained permission control** — exactly what's needed in real DevOps environments where teams have different responsibilities.

### How – Step-by-Step RBAC Setup

#### Step 1: Install the Plugin
```
Manage Jenkins → Plugins → Available Plugins
Search: "Role-based Authorization Strategy"
Click: Install
Restart Jenkins if prompted
```

#### Step 2: Enable RBAC as the Authorization Strategy
```
Manage Jenkins → Security → Authorization
Select: "Role-based matrix authorization strategy"
Save
```

#### Step 3: Create Roles
```
Manage Jenkins → Manage and Assign Roles → Manage Roles

Create roles, for example:
  - "developer"   → Can: Build, Configure, Read
  - "l1-support"  → Can: Read only (view logs, status)
  - "admin"       → Can: Everything
```

#### Step 4: Assign Users to Roles
```
Manage Jenkins → Manage and Assign Roles → Assign Roles

Map users to roles:
  - balaji    → developer
  - support1  → l1-support
  - jenkins   → admin
```

#### Step 5: Verify
Log in as each user (in incognito) and confirm they can only do what their role permits.

---

### Role Permission Matrix (Real-World Example)

| Permission | Admin | Developer | L1 Support |
|-----------|-------|-----------|-----------|
| View jobs/builds | ✅ | ✅ | ✅ |
| Trigger builds | ✅ | ✅ | ❌ |
| Configure jobs | ✅ | ✅ | ❌ |
| Create new jobs | ✅ | ❌ | ❌ |
| Install plugins | ✅ | ❌ | ❌ |
| Manage users | ✅ | ❌ | ❌ |
| Delete jobs | ✅ | ❌ | ❌ |
| View console logs | ✅ | ✅ | ✅ |

### Impact

| Without RBAC | With RBAC |
|-------------|----------|
| All-or-nothing access | Granular permission control |
| Junior dev can delete production pipelines | Scoped to only what's needed |
| No separation of responsibilities | Clear role boundaries |
| Security audit fails | Compliant with security standards |

---

## 3. Continuous Integration – Automated Triggers

### What
This is the **heart of CI** — instead of manually clicking "Build Now" in Jenkins, the build **triggers automatically** every time a developer pushes code to GitHub. No human needs to start it.

### Why
Manual triggering defeats the purpose of CI. The whole point is that the pipeline runs **immediately and automatically** after every code push — giving the developer instant feedback without any extra action on their part.

### How – Two Ways to Trigger Automatically

#### Method 1: Poll SCM (what was used in class)
Jenkins **periodically checks GitHub** to see if any new commits exist. If yes, it runs the build.

##### Setting up Poll SCM:
```
Job → Configure → Build Triggers
Check: "Poll SCM"
Enter a cron expression in the Schedule field
```

##### Understanding Cron Expressions
A cron expression has **5 fields**, each separated by a space:

```
┌───────────── minute       (0–59)
│ ┌─────────── hour         (0–23)
│ │ ┌───────── day of month (1–31)
│ │ │ ┌─────── month        (1–12)
│ │ │ │ ┌───── day of week  (0–7, 0=Sunday)
│ │ │ │ │
* * * * *
```

##### Examples from class:

| Cron Expression | Meaning |
|----------------|---------|
| `* * * * *` | Every minute |
| `*/10 * * * *` | Every 10 minutes |
| `*/10 8 * * *` | Every 10 minutes, but only during the 8 AM hour |
| `0 9 * * 1-5` | At 9:00 AM, Monday to Friday only |
| `0 0 * * *` | Once a day at midnight |

> ⚠️ **Poll SCM drawback:** Jenkins keeps checking GitHub even when nothing changed — wasteful. The better production approach is **Webhooks** (GitHub pushes a notification to Jenkins the instant code is pushed), but Poll SCM is simpler to set up for learning.

#### Method 2: GitHub Webhook (Production Best Practice)
```
GitHub Repo → Settings → Webhooks → Add Webhook
Payload URL: http://JENKINS_URL/github-webhook/
Content type: application/json
Trigger: "Just the push event"
```
Now GitHub calls Jenkins *instantly* on every push — no polling delay.

---

### Git Repository Integration in Jenkins

```
Job → Configure → Source Code Management
Select: Git
Repository URL: https://github.com/username/repo.git
Credentials: Add GitHub username + Personal Access Token
Branch: */main (or */feature-*)
```

Once connected, Jenkins pulls the latest code automatically on each trigger.

### Impact

| Without Automated Triggers | With Poll SCM / Webhooks |
|--------------------------|------------------------|
| Developer must manually trigger builds | Happens automatically on push |
| Delays between code push and feedback | Feedback within minutes (or seconds) |
| Builds get forgotten or skipped | Every push is validated, no exceptions |
| CI is only as good as people's habits | CI is enforced by the system |

---

## 4. Java Application Build & Deployment in Jenkins

### What
Jenkins can compile and run Java programs as part of a build job. In class, a **Hello World Java program** was used to demonstrate the full compile-execute-verify cycle inside Jenkins.

### How – Configuring the Build Step

#### The Java HelloWorld Setup

Assume the GitHub repo contains:
```java
// HelloWorld.java
public class Simple {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

> 🔑 **Important distinction from class:** The **filename** is `HelloWorld.java` but the **class name** inside is `Simple`. Java requires these to match in most cases — but the key lesson is: when *running* the program, you use the **class name** (`java Simple`), not the filename.

#### Jenkins Build Step (Execute Shell)
```bash
# Compile the Java file
javac HelloWorld.java

# Run using the class name (not the file name)
java Simple
```

#### What Jenkins Does Step by Step
```
1. Trigger fires (manual click or Poll SCM detects new commit)
2. Jenkins pulls latest code from GitHub into workspace
3. Jenkins runs: javac HelloWorld.java
   → Produces: Simple.class (bytecode file)
4. Jenkins runs: java Simple
   → JVM executes Simple.class
   → Output: "Hello, World!" printed to console
5. Build status: SUCCESS ✅
6. Console log saved and viewable in UI
```

### Verifying in Build Logs
Always check the Console Output after a build:
```
Dashboard → [Job Name] → Build #N → Console Output
```

A successful run shows:
```
Started by an SCM change
[hello-world-java] $ /bin/sh -xe /tmp/jenkins...
+ javac HelloWorld.java
+ java Simple
Hello, World!
Finished: SUCCESS
```

### Impact

| Skipping build verification | Checking build logs |
|----------------------------|---------------------|
| Assuming code works | Confirmed it compiles and runs |
| Bugs reach testing/production | Caught at compile stage |
| "Works on my machine" problem | Verified in clean CI environment |

---

## 5. Jenkins Local Installation (WAR File Method)

### What
Instead of installing Jenkins on a server/VM via `apt`, you can run Jenkins directly from its **WAR (Web Application Archive) file** on your local Windows or Mac machine. This is useful for learning, testing, or offline demos.

> 💡 **What is a WAR file?** A `.war` file is a packaged Java web application — similar to a `.zip` but for web apps. Jenkins is distributed as a WAR file you can run directly.

### Why
- No need for a cloud VM or Linux server
- Quick setup for learning and experimentation
- Great for running Jenkins offline or during development

### Prerequisites

Java must be installed (Jenkins 2.504 requires **Java 21**):
```bash
# Verify Java version before starting
java -version
# Must show version 21+ for Jenkins 2.504
```

> ⚠️ **Version Compatibility Issue (from class):** Jenkins 2.504 (latest as of class) requires **Java 21**. If you only have Java 17, you'll get a startup error. Two solutions:
> 1. Upgrade Java to 21
> 2. Download an older Jenkins version (e.g., January 2025 release) that still supports Java 17

---

### Step-by-Step WAR File Setup (Windows)

#### Step 1: Download jenkins.war
```
Go to: https://www.jenkins.io/download/
Download: jenkins.war (LTS version recommended)
```

#### Step 2: Place in a Clean Directory
```
Create folder: C:\bin\
Move file to:  C:\bin\jenkins.war
```

#### Step 3: Open Command Prompt and Launch Jenkins
```cmd
cd C:\bin
java -jar jenkins.war --httpPort=8082
```

> 💡 **Why port 8082?** Port 8080 might already be used by another service on your local machine. `--httpPort=8082` tells Jenkins to use 8082 instead. You can use any available port.

#### Step 4: Wait for Startup
You'll see output like:
```
Jenkins initial setup is required.
Please use the following password to proceed to installation:
a1b2c3d4e5f6...   ← Copy this!
Jenkins is fully up and running
```

#### Step 5: Access Jenkins in Browser
```
http://localhost:8082
```

#### Step 6: Unlock and Complete Setup
```
Paste the initial admin password from the terminal
Install suggested plugins
Create admin user
Done! ✅
```

---

### WAR Method vs apt Install – Comparison

| | WAR File (Local) | apt Install (Server) |
|--|-----------------|---------------------|
| **Where** | Your laptop/desktop | Linux VM or server |
| **Best for** | Learning, testing, offline | Production, team use |
| **Port** | Configurable (e.g., 8082) | Default 8080 |
| **Persistence** | Runs while terminal is open | Runs as system service |
| **Start command** | `java -jar jenkins.war` | `systemctl start jenkins` |
| **Stop** | Ctrl+C in terminal | `systemctl stop jenkins` |

---

## 6. Plugin Lifecycle Management

### What
Plugins are **add-ons that extend Jenkins' functionality**. Jenkins core is minimal by design — plugins add almost everything: Git support, Maven builds, Slack alerts, Docker integration, RBAC, and thousands more.

### Full Plugin Lifecycle

```
Available → Install → Active → Disable → Enable → Uninstall
```

| Action | Where | Effect |
|--------|-------|--------|
| **Install** | Manage Jenkins → Plugins → Available | Downloads and activates the plugin |
| **Enable** | Manage Jenkins → Plugins → Installed | Re-activates a disabled plugin |
| **Disable** | Manage Jenkins → Plugins → Installed | Deactivates without removing |
| **Uninstall** | Manage Jenkins → Plugins → Installed | Removes plugin files permanently |

> 💡 **Tip:** Disable before uninstall — it lets you test that nothing breaks before fully removing a plugin. In production, never uninstall without testing the disable state first.

### Key Plugins to Know

| Plugin | Purpose |
|--------|---------|
| **Git Plugin** | Connect Jenkins to GitHub/GitLab |
| **Maven Integration** | Build Java/Maven projects |
| **Role-based Authorization Strategy** | RBAC user permissions |
| **Pipeline** | Write pipelines as code (Jenkinsfile) |
| **Blue Ocean** | Modern, visual pipeline UI |
| **SonarQube Scanner** | Code quality analysis |
| **Docker Pipeline** | Build and push Docker images |
| **Slack Notification** | Send alerts to Slack channels |
| **Email Extension** | Send build results via email |
| **GitHub Integration** | Enable webhooks from GitHub |

---

## 7. Real-Time DevOps Mindset

These are the professional principles the instructor emphasized — not just technical knowledge, but how to **think** in a real DevOps role.

---

### "Production is Production"
> **"You can't change the production environment — you must adapt your application to fit it."**

In real companies, the production environment is locked down. You can't say "let me install Java 17 on the prod server" — it has Java 21, and your application must work with that. This is why version compatibility checks and testing in environment-matching setups matter so much.

---

### Troubleshooting Approach
When something breaks:
```
Step 1: Read the error message carefully (most answers are there)
Step 2: Search official documentation
Step 3: Search Google with exact error text
Step 4: Use ChatGPT / AI tools for explanation
Step 5: Try one solution at a time (don't change multiple things)
Step 6: Document what you tried and what worked
```

> 💡 **Key DevOps skill:** Self-sufficient troubleshooting. You won't always have a senior around — knowing how to find answers is as important as knowing the answers.

---

### Version Compatibility Mindset
The Java 17 vs Jenkins 2.504 (needs Java 21) conflict from class is a perfect real-world example:
- Read the release notes for version requirements
- Check compatibility matrices before upgrading anything
- When you can't upgrade the environment, downgrade the application version
- This happens constantly in production: "We can't use that library version because our runtime is too old"

---

## 8. Visual Diagrams

### Diagram 1: Jenkins User & RBAC Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      JENKINS                            │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │               USER ACCOUNTS                     │   │
│  │  admin (you)   balaji (dev)   support1 (L1)     │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │ Assigned to                     │
│  ┌────────────────────▼─────────────────────────────┐   │
│  │                  ROLES (RBAC)                    │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌────────────┐  ┌─────────────┐  │   │
│  │  │  admin   │  │ developer  │  │  l1-support  │  │   │
│  │  │          │  │            │  │             │  │   │
│  │  │ All      │  │ Build      │  │ View only   │  │   │
│  │  │ perms    │  │ Configure  │  │ Read logs   │  │   │
│  │  │          │  │ Read       │  │             │  │   │
│  │  └──────────┘  └────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

### Diagram 2: CI Automated Trigger Flow

```
POLL SCM METHOD:
─────────────────
Jenkins (every N minutes)           GitHub
       │                               │
       │── "Any new commits?" ────────►│
       │◄── "No" ──────────────────────│  (do nothing)
       │                               │
       │── "Any new commits?" ────────►│
       │◄── "Yes! commit abc123" ──────│
       │                               │
       │  Trigger build pipeline       │
       ▼                               │
  [Compile → Test → Deploy]            │


WEBHOOK METHOD (Production):
──────────────────────────────
Developer           GitHub              Jenkins
    │                  │                   │
    │── git push ─────►│                   │
    │                  │── POST /webhook ─►│
    │                  │                   │── Trigger build immediately
    │                  │                   ▼
    │                  │            [Compile → Test → Deploy]
```

---

### Diagram 3: Cron Expression Breakdown

```
Expression:  */10  8  *  *  *
              │    │  │  │  │
              │    │  │  │  └── Day of week (*)  = any day
              │    │  │  └───── Month (*)         = any month
              │    │  └──────── Day of month (*)  = any day
              │    └─────────── Hour (8)           = 8 AM only
              └──────────────── Minute (*/10)      = every 10 min

Result: Runs every 10 minutes, but only during the 8 o'clock hour (8:00, 8:10, 8:20, 8:30, 8:40, 8:50)
```

---

### Diagram 4: WAR File Local Setup Flow

```
[jenkins.war downloaded]
         │
         │  java -jar jenkins.war --httpPort=8082
         ▼
[JVM starts Jenkins]
         │
         │  Jenkins initializes...
         ▼
[Terminal shows: initial admin password: abc123xyz]
         │
         │  Open browser
         ▼
[http://localhost:8082]
         │
         │  Paste admin password
         ▼
[Install plugins]
         │
         │  Create admin user
         ▼
[Jenkins ready ✅]
```

---

### Diagram 5: Java Compile-Run in Jenkins

```
GitHub Repo
├── HelloWorld.java    ← filename
│   └── class Simple  ← class name (used for running)

Jenkins pulls code
         │
         ▼
javac HelloWorld.java
         │
         ▼ produces
Simple.class           ← bytecode file (class name = filename)
         │
         ▼
java Simple            ← run using CLASS name, not file name
         │
         ▼
Console: "Hello, World!"
Status:   SUCCESS ✅
```

---

### Diagram 6: Plugin Lifecycle

```
Available Plugins
      │
      │ Install
      ▼
Installed & Active ──── Disable ────► Disabled
      │                                  │
      │ Uninstall                        │ Enable
      ▼                                  │
   Removed                         Installed & Active
                                         │
                                         │ Uninstall
                                         ▼
                                      Removed
```

---

## 9. Scenario-Based Q&A

---

🔍 **Scenario 1:** You've just joined a company as a DevOps engineer. There are 15 developers, 5 QA engineers, and 3 L1 support staff. The CTO says "everyone needs Jenkins access but with appropriate restrictions." How do you set this up?

✅ **Answer:** Install the "Role-based Authorization Strategy" plugin. Create three roles:
- `developer` — Build, Configure, Read permissions
- `qa-engineer` — Build (to trigger tests), Read permissions
- `l1-support` — Read only (view logs and build history)

Then create Jenkins user accounts for all 23 people and assign them to their respective roles via Manage Roles → Assign Roles. Test each role in incognito to verify permissions are correct.

---

🔍 **Scenario 2:** A developer asks "why does my Jenkins build trigger only every 10 minutes? Can it be faster?" What's the proper solution?

✅ **Answer:** Poll SCM with `*/10 * * * *` means Jenkins checks GitHub every 10 minutes — there's inherent delay. The proper production solution is to switch to **GitHub Webhooks**. Configure the webhook in your GitHub repo settings pointing to `http://JENKINS_URL/github-webhook/`. Now GitHub notifies Jenkins the *instant* a push happens — zero polling delay, no wasted checks when nothing changed.

---

🔍 **Scenario 3:** You're setting up Jenkins locally for a demo. You run `java -jar jenkins.war` but get an error saying Jenkins requires Java 21 and you have Java 17. Your laptop can't get a Java 21 installer today. What do you do?

✅ **Answer:** Download an older Jenkins LTS release (e.g., the January 2025 version) that supports Java 17. Jenkins releases are available with version notes specifying minimum Java requirements. This is exactly the "production is production" principle — you adapt the application to the environment, not the other way around. Use `java -jar jenkins-old.war --httpPort=8082` to run on a non-conflicting port.

---

🔍 **Scenario 4:** Your Poll SCM build is running successfully but it's triggering even when nothing changed in the code. Why, and how do you fix it?

✅ **Answer:** This is a known limitation of Poll SCM — it checks for changes but can sometimes misfire. The real fix is switching to **Webhooks** (GitHub triggers Jenkins only on actual pushes). If you must keep Poll SCM, ensure the Git plugin is updated and the polling log (Dashboard → Job → Git Polling Log) is reviewed to see what changes it's detecting. Often, the issue is tracking the wrong branch or picking up metadata changes.

---

🔍 **Scenario 5:** A new developer on your team ran `java HelloWorld` instead of `java Simple` and got a "class not found" error even though the code compiled fine. How do you explain this?

✅ **Answer:** In Java, the **class name** and the **file name** don't have to match (though best practice says they should). The `javac HelloWorld.java` command compiles the file and produces a `.class` file named after the **class** defined inside — in this case, `Simple.class`. When running, Java looks for the class name, not the file name. So the correct command is `java Simple`. This is a common beginner mistake — always run Java using the class name as it appears in the `public class` declaration.

---

🔍 **Scenario 6:** A manager wants to know which developer ran a build at 2 AM and deleted an important job. Is there a way to find out in Jenkins?

✅ **Answer:** Yes — Jenkins maintains an **audit log** when proper user management is configured. Each action (builds triggered, jobs deleted, configuration changes) is tagged with the user who performed it. This is one of the key reasons individual user accounts matter over a shared login. Navigate to Manage Jenkins → System Log or use the "Audit Trail" plugin for a searchable history of all user actions.

---

🔍 **Scenario 7:** You installed a new plugin and now Jenkins is behaving strangely — some jobs aren't working right. What's your troubleshooting process?

✅ **Answer:** First, **disable** the plugin (don't uninstall yet) via Manage Jenkins → Plugins → Installed → find the plugin → Disable → Restart Jenkins. If the problem goes away, the plugin was the cause. Check for compatibility issues (plugin version vs Jenkins version). If confirmed, uninstall it. If you need the functionality, look for an alternative plugin or a compatible version. Always test plugin changes on a non-production Jenkins instance first.

---

## 10. Interview Q&A

---

**Q1. What is RBAC in Jenkins and why is it important?**

**A:** RBAC (Role-Based Access Control) is a security model where permissions are assigned based on roles rather than individual users. In Jenkins, it's implemented via the "Role-based Authorization Strategy" plugin. You define roles (admin, developer, L1 support), assign permissions to each role, then assign users to roles.

It's important because Jenkins often controls production deployment pipelines. Without RBAC, a junior developer could accidentally delete a critical job or modify a production pipeline. RBAC enforces the principle of least privilege — everyone has exactly the access they need and nothing more. It also ensures compliance with security standards in enterprise environments.

---

**Q2. What is Poll SCM in Jenkins and how does it differ from a webhook?**

**A:** Poll SCM is a Jenkins trigger where Jenkins **periodically checks** the Git repository for new commits on a cron schedule. For example, `*/5 * * * *` checks every 5 minutes. If new commits are found, the build runs.

A Webhook is the reverse — GitHub **notifies Jenkins immediately** when a push event occurs. Jenkins doesn't need to poll; GitHub calls Jenkins' webhook endpoint the instant code is pushed.

Poll SCM is simpler to configure but adds delay and wastes resources checking when nothing changed. Webhooks are the production best practice — real-time, efficient, and zero delay. The trade-off: webhooks require Jenkins to be publicly reachable (or use a tunnel), while Poll SCM works even on private networks.

---

**Q3. How do you run Jenkins locally without installing it as a system service?**

**A:** Download the `jenkins.war` file from jenkins.io and run it directly with Java:
```bash
java -jar jenkins.war --httpPort=8082
```
This starts Jenkins on port 8082 (or any port you specify). Access it at `http://localhost:8082`. Jenkins runs as long as the terminal window is open. This approach requires only Java to be installed — no `apt install`, no system service, no admin privileges on the machine. It's ideal for local development, learning, or demos.

---

**Q4. What is the difference between `javac HelloWorld.java` and `java Simple`?**

**A:** `javac HelloWorld.java` is the **compilation** step — it reads the source file and produces bytecode. The output file is named after the **class defined inside** the file, not the file itself. If the file contains `public class Simple { }`, the output is `Simple.class`.

`java Simple` is the **execution** step — it tells the JVM to load and run the class named `Simple`. You use the **class name**, not the filename. This distinction matters in Jenkins build scripts: always compile using the filename (`javac FileName.java`) and run using the class name (`java ClassName`).

---

**Q5. What are the steps to install and configure RBAC in Jenkins?**

**A:**
1. Go to Manage Jenkins → Plugins → Available Plugins
2. Search for and install "Role-based Authorization Strategy"
3. Go to Manage Jenkins → Security → Authorization
4. Select "Role-based matrix authorization strategy" and save
5. Go to Manage Jenkins → Manage and Assign Roles → Manage Roles
6. Create roles (e.g., developer, l1-support, admin) and set permission checkboxes for each
7. Go to Assign Roles and map Jenkins users to their appropriate roles
8. Test by logging in as each user type (use incognito) and verifying their access level

---

**Q6. What is a Jenkins plugin and what are some essential ones to know?**

**A:** A Jenkins plugin is an add-on that extends Jenkins' core functionality. Jenkins ships minimal by design — plugins add almost everything. Essential plugins include:

- **Git Plugin** — connects Jenkins to GitHub/GitLab repositories
- **Role-based Authorization Strategy** — enables RBAC for user permissions
- **Pipeline** — enables writing pipelines as code in a Jenkinsfile
- **Maven Integration** — supports building Java projects with Maven
- **SonarQube Scanner** — integrates code quality analysis
- **Docker Pipeline** — builds and pushes Docker images
- **Slack Notification / Email Extension** — sends build alerts

Plugins are managed at Manage Jenkins → Plugins, where you can install, disable, enable, and uninstall them.

---

**Q7. What does the cron expression `*/10 8 * * *` mean in Jenkins Poll SCM?**

**A:** Breaking it down by field (minute, hour, day-of-month, month, day-of-week):
- `*/10` — every 10 minutes
- `8` — only during hour 8 (8 AM)
- `*` — any day of month
- `*` — any month
- `*` — any day of week

So it runs at: 8:00, 8:10, 8:20, 8:30, 8:40, and 8:50 — six times total, only during the 8 AM hour, every day. This is useful for scheduled morning builds that check if overnight commits to a branch are valid.

---

**Q8. What is a WAR file and why is Jenkins distributed as one?**

**A:** A WAR (Web Application Archive) file is a packaged Java web application — essentially a `.zip` file with a specific structure that a Java web server can run directly. Jenkins is distributed as a WAR file because it's built on Java, which means it can run on any operating system that has a JVM — Windows, Mac, Linux — without OS-specific packaging.

Running `java -jar jenkins.war` works because Java's built-in web server (Winstone/Jetty) is bundled inside the WAR file itself. This makes Jenkins extremely portable — same WAR file works anywhere Java is installed.

---

**Q9. What does "least privilege" mean in the context of Jenkins access control?**

**A:** Least privilege is a security principle where every user is given **only the permissions they need to do their job** — nothing more. In Jenkins:
- An L1 support engineer needs to read logs → give Read access only
- A developer needs to trigger builds and configure jobs → give Build + Configure + Read
- An admin manages the system → give full access

This limits the blast radius of mistakes or malicious actions. If a developer account is compromised, the attacker can only trigger builds — not delete pipelines or access credentials. RBAC in Jenkins is the technical implementation of this principle.

---

← Previous: [`26_Introduction_to_CICD_and_Jenkins.md`](26_Introduction_to_CICD_and_Jenkins.md) | Next: [`28_Java,_Spring_Boot_Maven_&_Jenkins_Build_Pipeline.md`](28_Java,_Spring_Boot_Maven_&_Jenkins_Build_Pipeline.md) →