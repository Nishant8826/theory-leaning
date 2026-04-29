# 31 – Jenkins Day-to-Day Operations, Parameterized Jobs & AWS Core Services

---

## Table of Contents

1. [Jenkins Real-World Problems & Solutions](#1-jenkins-real-world-problems--solutions)
2. [Jenkins Restart Methods](#2-jenkins-restart-methods)
3. [Parameterized Jobs – One Job, Many Environments](#3-parameterized-jobs--one-job-many-environments)
4. [Jenkins Credentials Management](#4-jenkins-credentials-management)
5. [Amazon Aurora – Enterprise Cloud Database](#5-amazon-aurora--enterprise-cloud-database)
6. [Amazon CloudFront – CDN](#6-amazon-cloudfront--cdn)
7. [AWS IAM Policies – Permissions as Code](#7-aws-iam-policies--permissions-as-code)
8. [Interview Mindset – What the Industry Expects](#8-interview-mindset--what-the-industry-expects)
9. [Tech Stack Mapping](#9-tech-stack-mapping)
10. [Visual Diagrams](#10-visual-diagrams)
11. [Code & Practical Examples](#11-code--practical-examples)
12. [Scenario-Based Q&A](#12-scenario-based-qa)
13. [Interview Q&A](#13-interview-qa)

---

## 1. Jenkins Real-World Problems & Solutions

### What
Day-to-day Jenkins management means you're not just setting it up once — you're actively monitoring, troubleshooting, and maintaining it. This section covers the most common problems that appear in real jobs.

> 💡 **Key mindset:** Every Jenkins problem starts with one action — **check the logs**. 90% of answers are there.

---

### Problem 1: Job Failures

#### What
A Jenkins job returns `BUILD FAILURE`. The red ball appears in the dashboard.

#### Common Causes

| Cause | What it looks like | How to fix |
|-------|--------------------|-----------|
| **Configuration error** | Wrong Git URL, wrong branch, missing credentials | Fix job config, verify credentials |
| **Environment problem** | Java not found, Maven not installed, wrong PATH | Install missing tool, set PATH in job |
| **Dependency error** | `mvn package` fails, `npm install` fails | Check pom.xml, package.json, network access to registries |
| **Compile error** | Code has syntax error, test failed | Developer fixes the code, re-trigger build |
| **Disk space full** | "No space left on device" | Clear workspace, delete old builds, add disk |

#### How to Diagnose

```
Step 1: Click the failed build number (e.g., #7 ❌)
Step 2: Click "Console Output"
Step 3: Scroll to the bottom — look for "ERROR" or "FAILED"
Step 4: Read the lines ABOVE the error — context explains the cause
Step 5: Google the exact error message if needed
Step 6: Fix the root cause, re-run
```

---

### Problem 2: Performance Issues (Slow Builds)

#### What
Builds that used to take 5 minutes now take 25. Or Jenkins UI is sluggish.

#### Common Causes & Solutions

| Cause | Solution |
|-------|---------|
| Too many builds running on one machine | Add slave agents (Master-Slave) |
| Insufficient RAM (builds compete for memory) | Use a larger instance (more RAM) |
| CPU maxed out during compilation | More CPUs on agent or split across agents |
| Disk I/O bottleneck (slow storage) | Use SSD volumes on cloud VM |
| Too many concurrent executors on one node | Reduce executors, add more nodes |
| Workspace not cleaned between builds | Add `mvn clean` or workspace cleanup step |

#### Quick Diagnostic Commands (on Jenkins Linux server)

```bash
# Check CPU usage
top
htop

# Check RAM
free -h

# Check disk space
df -h

# Check Jenkins workspace disk usage
du -sh /var/lib/jenkins/workspace/*
```

---

### Problem 3: Agent/Slave Nodes Going Offline

#### What
Slave nodes disappear (go offline) and jobs are stuck in pending queue.

#### Why It Happens
- Slave machine rebooted
- Network interruption between master and slave
- `agent.jar` process was killed
- Jenkins master restarted (resets all connections)
- Java memory issue on slave caused process crash

#### Resolution Steps

```bash
# 1. Check which node is offline:
Jenkins → Manage Jenkins → Nodes → Look for ⚠️ Offline

# 2. On the slave machine, reconnect:
java -jar agent.jar \
  -url http://MASTER_IP:8080/ \
  -secret YOUR_SECRET_KEY \
  -name "your-node-name" \
  -webSocket \
  -workDir "/path/to/slave/workspace"

# 3. Verify node is online in Jenkins UI
# 4. Pending jobs will start automatically
```

---

### Problem 4: Plugin Management Issues

#### What
Plugins are the lifeblood of Jenkins — but outdated or conflicting plugins cause instability.

#### Common Plugin Problems

| Problem | Symptoms | Solution |
|---------|----------|---------|
| Plugin outdated | Feature doesn't work, UI warnings | Update via Manage Jenkins → Plugins → Updates |
| Plugin conflict | Jenkins error on startup | Check Plugin Manager for conflict warnings |
| Security vulnerability | CVE warnings in UI | Update affected plugin immediately |
| Missing dependency | "Plugin X requires Plugin Y" | Install the dependency first |
| Plugin broke after update | Builds fail after update | Downgrade to previous version (download .jpi file) |

#### Regular Plugin Maintenance

```
Manage Jenkins → Plugins → Updates tab
  → Select all outdated plugins
  → Click "Update"
  → Check "Restart Jenkins after download"
```

> ⚠️ **Best practice:** Never update all plugins at once in production. Update one at a time and test builds between each update.

---

### Problem 5: Log Management & Disk Space

#### What
Jenkins stores every build's console log. Over months, this fills up your disk — causing "no space left on device" errors.

#### Solutions

```
Option 1: Configure Log Rotation per job
  Job → Configure → General
  → Check: "Discard old builds"
  → Days to keep builds: 30
  → Max # of builds to keep: 50

Option 2: Delete workspace manually
  Job → Workspace → Wipe Out Current Workspace

Option 3: Clean up from command line
  sudo rm -rf /var/lib/jenkins/workspace/[job-name]/

Option 4: Global log rotation
  Manage Jenkins → System → Build Record Root Directory
  → Configure global retention policy
```

---

## 2. Jenkins Restart Methods

### What
Sometimes Jenkins needs a restart — after plugin updates, configuration changes, or when it becomes unresponsive.

### Why Different Methods Exist
- **Graceful restart** waits for running builds to finish (preferred)
- **Force restart** stops everything immediately (use only when Jenkins is stuck)
- **System restart** restarts the underlying OS (last resort)

### All Restart Methods

#### Method 1: Via URL (Graceful — Recommended)
```
Safe restart (waits for running builds to finish):
http://YOUR_JENKINS_URL/safeRestart

Force restart (immediate — active builds are aborted):
http://YOUR_JENKINS_URL/restart
```

#### Method 2: Via Jenkins UI
```
Manage Jenkins → Reload Configuration from Disk
(reloads config without full restart)

Or: Manage Jenkins → Prepare for Shutdown
→ No new builds accepted → existing builds finish → then restart manually
```

#### Method 3: Linux CLI
```bash
# If installed as service (apt install):
sudo systemctl restart jenkins

# Check status after restart:
sudo systemctl status jenkins

# If running from WAR file:
pkill -f jenkins.war
java -jar jenkins.war &
```

#### Method 4: Windows Service
```powershell
Restart-Service -Name jenkins

# Or via Services UI:
# services.msc → Jenkins → Restart
```

### When to Use Which

| Situation | Method |
|-----------|--------|
| Plugin update installed | Safe Restart via URL |
| Jenkins UI frozen/unresponsive | systemctl restart (Linux) |
| Config file changed manually | Reload Configuration from Disk |
| Server needs OS-level restart | systemctl restart after OS reboot |
| Jenkins WAR file update | Stop WAR → replace jar → restart |

---

## 3. Parameterized Jobs – One Job, Many Environments

### What
A **Parameterized Job** is a Jenkins job that accepts input variables (parameters) before each build. Instead of creating three separate jobs for Dev, QA, and Production deployments, you create ONE job with a parameter (like `ENVIRONMENT`) and the job behaves differently based on the value chosen.

> 💡 **Analogy:** It's like a travel booking website. Instead of three separate websites for economy, business, and first class — one website with a dropdown that changes what gets booked.

### Why
Without parameterized jobs:
- 3 environments = 3 separate jobs = 3x the maintenance
- Change something → update 3 jobs
- Risk of inconsistency between jobs

With parameterized jobs:
- 1 job handles all environments
- Change something → update once
- Consistent behavior guaranteed

### How – Setting Up a Parameterized Freestyle Job

```
Job → Configure → General
→ Check: "This project is parameterized"
→ Click: "Add Parameter"
```

#### Parameter Types

| Type | Use Case | Example |
|------|----------|---------|
| **String** | Free text input | Branch name, version number |
| **Choice** | Dropdown list | Dev / QA / Prod |
| **Boolean** | True/False checkbox | Run tests? Yes/No |
| **Password** | Masked input | API keys (though use Credentials instead) |
| **File** | Upload a file | Config file upload |

#### Example: Choice Parameter for Environment

```
Parameter Type: Choice Parameter
Name: ENVIRONMENT
Choices:
  dev
  qa
  prod
Description: "Select the target deployment environment"
```

When someone clicks "Build with Parameters," they see a dropdown with dev/qa/prod.

#### Using the Parameter in Build Steps

```bash
# In Execute Shell:
echo "Deploying to: $ENVIRONMENT"

if [ "$ENVIRONMENT" = "prod" ]; then
    java -jar -Dserver.port=8080 shopping-cart.jar
elif [ "$ENVIRONMENT" = "qa" ]; then
    java -jar -Dserver.port=8081 shopping-cart.jar
else
    java -jar -Dserver.port=8082 shopping-cart.jar
fi
```

### How – Parameterized Pipeline (Jenkinsfile)

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'qa', 'prod'],
            description: 'Select target environment'
        )
        string(
            name: 'VERSION',
            defaultValue: 'latest',
            description: 'Docker image tag or JAR version'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run test suite before deployment?'
        )
    }

    stages {
        stage('Deploy') {
            steps {
                echo "Deploying version ${params.VERSION} to ${params.ENVIRONMENT}"

                script {
                    if (params.ENVIRONMENT == 'prod') {
                        // Extra safety check for production
                        input message: 'Confirm production deployment?', ok: 'Deploy'
                    }
                }

                sh """
                    java -jar -Dspring.profiles.active=${params.ENVIRONMENT} \
                    target/shopping-cart-${params.VERSION}.jar &
                """
            }
        }

        stage('Test') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                sh 'mvn test'
            }
        }
    }
}
```

### Impact

| Without Parameterized Jobs | With Parameterized Jobs |
|---------------------------|------------------------|
| Separate job per environment | One job handles all |
| 3x maintenance overhead | Update once, works everywhere |
| Hard to trace who deployed what | Parameters logged in build history |
| Risk of env-specific config drift | Consistent logic, variable values |
| Developers need to know job names | One job, clear dropdown |

---

## 4. Jenkins Credentials Management

### What
Jenkins has a built-in **Credentials Store** — a secure vault where you keep sensitive information (passwords, API keys, SSH keys, certificates) that your pipelines need. Credentials are **encrypted at rest** and **never appear in console logs** — even if someone tries to print them.

### Why
Hardcoding passwords in Jenkinsfiles or build scripts is a critical security mistake:
- Anyone with Git access can see the password
- Credentials get committed to version history (impossible to fully erase)
- Rotating passwords requires updating every script

Jenkins Credentials Management centralizes and secures this.

### Types of Credentials

| Type | Used For | Example |
|------|---------|---------|
| **Username with Password** | GitHub login, Docker Hub, database | `git clone` with auth |
| **SSH Username with Private Key** | Server access, Git SSH | `ssh user@server` |
| **Secret Text** | API tokens, personal access tokens | AWS API key, GitHub PAT |
| **Secret File** | Config files, kubeconfig | AWS credentials file |
| **Certificate** | SSL/TLS certificates | HTTPS certificates |

### How to Add Credentials

```
Manage Jenkins → Credentials → System → Global credentials → Add Credentials

Kind: Secret text
Scope: Global
Secret: [paste your token here]
ID: github-token          ← You reference this ID in Jenkinsfile
Description: GitHub Personal Access Token
→ OK
```

### How to Use Credentials in a Pipeline

```groovy
pipeline {
    agent any

    environment {
        // Binds credential to environment variable
        GITHUB_TOKEN = credentials('github-token')
        DB_CREDS = credentials('database-credentials')  // username:password pair
    }

    stages {
        stage('Clone') {
            steps {
                // Token is automatically masked in logs as ****
                sh 'git clone https://${GITHUB_TOKEN}@github.com/yourname/repo.git'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'database-credentials',
                    usernameVariable: 'DB_USER',
                    passwordVariable: 'DB_PASS'
                )]) {
                    sh 'deploy.sh --db-user $DB_USER --db-pass $DB_PASS'
                    // $DB_PASS will show as **** in console output
                }
            }
        }
    }
}
```

### Credential Scopes

| Scope | Visibility |
|-------|-----------|
| **Global** | Available to all jobs on the Jenkins instance |
| **System** | Only available to Jenkins internal use (not jobs) |
| **Folder** | Available only to jobs within a specific folder |

### Impact

| Hardcoded Credentials | Jenkins Credentials Store |
|----------------------|--------------------------|
| Visible in Git history | Encrypted, never in Git |
| Visible in console logs | Masked as `****` |
| Rotation requires code change | Update once in credential store |
| Security audit failure | Compliant with security standards |
| Shared with everyone who has repo access | Access controlled by RBAC |

---

## 5. Amazon Aurora – Enterprise Cloud Database

### What
**Amazon Aurora** is AWS's own cloud-native relational database engine. It's built from the ground up for the cloud — not just a regular MySQL or PostgreSQL running on EC2. It's part of the Amazon RDS family but is significantly more advanced.

> 💡 **Analogy:** Standard MySQL on EC2 is like driving a regular car. Amazon Aurora is like driving a Tesla — same concept (a car), but rebuilt from scratch with modern technology, much faster, self-healing, and with features the old design couldn't support.

### Why
Enterprise applications have demanding database requirements:
- Need to handle millions of transactions per second
- Cannot afford downtime (financial systems, e-commerce, healthcare)
- Must scale read traffic without killing the primary database
- Need automatic failover when hardware fails
- Oracle is expensive — Aurora is a cost-effective alternative

### Key Features vs Standard MySQL/PostgreSQL

| Feature | Standard MySQL | Amazon Aurora |
|---------|---------------|---------------|
| **Performance** | Baseline | 5x faster (MySQL compatible), 3x faster (PostgreSQL compatible) |
| **Storage** | Fixed allocation | Auto-grows up to 64TB |
| **Replication lag** | Variable (seconds) | < 10ms (near real-time) |
| **Read replicas** | 5 max | 15 read replicas |
| **Failover time** | Minutes | < 30 seconds |
| **Availability** | Single AZ typical | Multi-AZ cluster by default |
| **Backup** | Manual or RDS backup | Continuous, to S3 |
| **Cost vs Oracle** | — | 90% cheaper |

### Aurora Architecture

Aurora separates **compute** from **storage** — a major architectural difference:
- The storage layer spans **6 copies across 3 Availability Zones** automatically
- Even if one AZ fails completely, the database keeps running
- Read replicas share the SAME storage volume (no replication lag copying data around)
- A writer endpoint handles all writes; a reader endpoint load-balances across replicas

### Aurora Cluster Components

```
Aurora Cluster
│
├── Primary Instance (Writer)
│   └── Handles all INSERT, UPDATE, DELETE operations
│
├── Read Replica 1
├── Read Replica 2    ← Up to 15 replicas
├── ...
└── Read Replica 15
    └── Handle SELECT queries (read traffic)

All instances share the same distributed storage layer
→ No data copying between instances
→ < 10ms replication lag
```

### Aurora vs RDS vs EC2 MySQL

| | EC2 MySQL | RDS MySQL | Amazon Aurora |
|--|-----------|-----------|---------------|
| **Management** | You manage everything | AWS manages OS/patches | AWS manages + optimized |
| **Performance** | Standard | Standard | 5x faster |
| **Failover** | Manual | ~2-3 minutes | < 30 seconds |
| **Storage** | Fixed EBS | Fixed to 64TB | Auto-scaling to 64TB |
| **Cost** | EC2 + EBS + admin time | Higher than EC2 | Higher than RDS, justified by performance |
| **Best for** | Dev/learning | Standard production | High-scale enterprise production |

### When to Use Aurora in DevOps

- Your application reads data far more than it writes → add read replicas
- You need 99.99% uptime SLA → multi-AZ Aurora cluster
- Migrating from Oracle (cost reduction) → Aurora PostgreSQL compatible
- Your RDS MySQL is becoming a bottleneck → upgrade to Aurora
- Regulatory compliance requires continuous backup → Aurora has this built in

### Impact

| Without Aurora (standard RDS/EC2 MySQL) | With Aurora |
|----------------------------------------|------------|
| Failover takes minutes | Failover in < 30 seconds |
| 5 read replicas max | 15 read replicas |
| Manual storage scaling | Automatic up to 64TB |
| High Oracle licensing costs | 90% cheaper |
| Single AZ risk | 6 copies across 3 AZs |

---

## 6. Amazon CloudFront – CDN

### What
**Amazon CloudFront** is AWS's **Content Delivery Network (CDN)**. A CDN is a global network of servers that stores copies (caches) of your content close to users around the world.

> 💡 **Analogy:** Imagine your website is a library in New York. Without CloudFront, someone in Mumbai has to request a book from New York — it takes a long time. CloudFront is like having a library branch in Mumbai, London, Tokyo, and 400 other cities. Mumbai users get books from the local branch in milliseconds.

### Why
Without a CDN:
- Every user request goes to your origin server (e.g., EC2 in us-east-1)
- Users in Asia, Europe, South America experience high latency
- Your origin server handles ALL traffic — it can get overwhelmed
- Slow load times = users leave = lost revenue

With CloudFront:
- Content is cached at **edge locations** (400+ worldwide)
- Users get content from the nearest edge — dramatically lower latency
- Origin server only handles requests for uncached/dynamic content
- DDoS protection built in (AWS Shield)

### How CloudFront Works

```
First request (cache miss):
User in Mumbai → CloudFront Edge (Mumbai) → "Not cached" → 
Origin (EC2 in US) → Content fetched → Stored at Mumbai edge → Served to user

All subsequent requests:
User in Mumbai → CloudFront Edge (Mumbai) → "Cached! ✅" → Served instantly
```

### What CloudFront Caches

| Content Type | Cache Duration | Example |
|-------------|---------------|---------|
| **Static files** | Days/weeks | Images, CSS, JavaScript, fonts |
| **Videos** | Hours/days | Product demo videos, tutorials |
| **API responses** | Seconds/minutes | Search results, product listings |
| **Dynamic HTML** | Not recommended | Shopping cart, user profile |

### CloudFront Key Concepts

| Term | Meaning |
|------|---------|
| **Edge Location** | A CloudFront server near users (400+ worldwide) |
| **Origin** | Your actual server/S3 bucket where real content lives |
| **Distribution** | A CloudFront configuration defining origin + cache behavior |
| **Cache Hit** | Content found at edge — served instantly |
| **Cache Miss** | Content not at edge — fetched from origin, then cached |
| **TTL** | Time-To-Live — how long content stays cached |
| **Invalidation** | Force CloudFront to clear cached content (after a deployment) |

### CloudFront in a DevOps Pipeline

```
Developer deploys new version
→ New files uploaded to S3 / deployed to EC2
→ Old files still cached at CloudFront edges worldwide!
→ Must invalidate cache:

aws cloudfront create-invalidation \
  --distribution-id EXXXXXXXXXX \
  --paths "/*"

→ Edges fetch fresh content on next request
→ Users see new version
```

### Real-World Architecture: Static Website with CloudFront

```
User Request
     │
     ▼
CloudFront Distribution (Global)
     │
     ├── Edge Location (Mumbai) ──────► Cache Hit → Response in < 10ms
     ├── Edge Location (London) ──────► Cache Hit → Response in < 10ms
     └── Edge Location (Tokyo)  ──────► Cache Miss → Fetch from S3 → Cache
                                                             │
                                                     S3 Bucket (us-east-1)
                                                     (Static website files)
```

### Impact

| Without CloudFront | With CloudFront |
|-------------------|-----------------|
| All traffic hits origin server | 90%+ served from edge cache |
| High latency for distant users | < 50ms globally |
| Origin can be overwhelmed | Origin gets 10x less traffic |
| No built-in DDoS protection | AWS Shield Basic included |
| No HTTPS without cert setup | Free SSL via ACM |
| Slow website = poor SEO | Fast website = better Google ranking |

---

## 7. AWS IAM Policies – Permissions as Code

### What
**IAM (Identity and Access Management)** is AWS's permission system. It controls who (or what) can do what in your AWS account. **IAM Policies** are the rules that define permissions — written in JSON format.

> 💡 **Analogy:** IAM is like a building's security system. Users are the employees with badges. Roles are job titles (receptionist, manager, engineer). Policies are the rules written in the access control system ("Receptionists can access floors 1-3, Managers can access all floors, Engineers can access the server room").

### The Three Core IAM Concepts – Clarified

| Concept | What it is | Analogy |
|---------|-----------|---------|
| **User** | An identity (person or service) | An employee |
| **Role** | A function that defines access level | A job title |
| **Policy** | A set of permission rules | The access control rulebook |

> 🔑 **Critical distinction from class:**
> - A **User** is the IDENTITY (who you are)
> - A **Role** is the FUNCTION (what job you're doing)
> - A **Policy** is the RULES (what actions are allowed)
>
> A User can ASSUME a Role. A Policy is ATTACHED to a User or Role.

### IAM Policy Structure (JSON Format)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-company-bucket",
        "arn:aws:s3:::my-company-bucket/*"
      ]
    },
    {
      "Sid": "DenyDeleteAnything",
      "Effect": "Deny",
      "Action": "s3:DeleteObject",
      "Resource": "*"
    }
  ]
}
```

### JSON Field Breakdown

| Field | Required? | What it means |
|-------|-----------|--------------|
| `Version` | Yes | Always `"2012-10-17"` (the current policy language version) |
| `Statement` | Yes | Array of permission rules |
| `Sid` | No | Statement ID — a label for the rule (your choice) |
| `Effect` | Yes | `"Allow"` or `"Deny"` |
| `Action` | Yes | Which AWS API operations (`s3:GetObject`, `ec2:StartInstances`) |
| `Resource` | Yes | Which specific AWS resources (ARN format, or `*` for all) |
| `Condition` | No | Optional — add conditions (e.g., only from specific IP) |

### Common Policy Examples

#### EC2 Full Access Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
```

#### Read-Only S3 for Specific Bucket
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ]
    }
  ]
}
```

#### Deny Access Outside Business Hours (with Condition)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```

### IAM Policy Types

| Type | What it is | Attached to |
|------|-----------|------------|
| **AWS Managed** | Pre-built by AWS (e.g., `AmazonS3FullAccess`) | Users, Roles, Groups |
| **Customer Managed** | You write and own the JSON | Users, Roles, Groups |
| **Inline** | Embedded directly into a user/role (not reusable) | One specific entity |
| **Resource-based** | Attached to a resource (e.g., S3 bucket policy) | AWS resources |

### The Visual Policy Editor
For beginners who don't want to write JSON:
```
IAM → Policies → Create Policy → Visual Editor
→ Service: S3
→ Actions: GetObject, PutObject
→ Resources: Specific ARN
→ Click "JSON" tab to see the generated JSON
→ Review + Create
```

### Principle of Least Privilege
> Always grant the **minimum permissions needed** and nothing more.

```
❌ Bad: Grant a Lambda function "AdministratorAccess"
✅ Good: Grant it only "s3:GetObject" on the specific bucket it needs

❌ Bad: Give a developer IAM user "ec2:*" on all resources
✅ Good: Give "ec2:StartInstances" and "ec2:StopInstances" on specific instance IDs
```

### Impact

| Without Proper IAM Policies | With Proper IAM Policies |
|----------------------------|-------------------------|
| Breached account = full AWS compromise | Breached account = limited blast radius |
| Anyone can delete production database | Only authorized roles can modify prod |
| Audit fails (no access records) | CloudTrail logs every action |
| Cost overruns from accidental resource creation | Prevent unauthorized resource creation |
| Compliance violations | Meets SOC2, HIPAA, PCI requirements |

---

## 8. Interview Mindset – What the Industry Expects

### Key Principles Emphasized in Class

#### 1. Continuous Delivery, NOT Continuous Deployment
In interviews, say you work on **Continuous Delivery** — not Deployment.

| Continuous Delivery | Continuous Deployment |
|--------------------|----------------------|
| Pipeline delivers a tested, ready artifact | Every commit auto-deploys to production |
| **Human approves** production deployment | No human approval — fully automated |
| Used in 90% of real companies | Used by only the most mature DevOps teams |
| Safer, more controlled | Requires very high test coverage |

> 💡 "Our Jenkins pipeline builds, tests, and delivers artifacts to staging. Production deployments require manager approval through the change management process."

#### 2. Jenkins is Dev/QA, Not Production
Jenkins is used to BUILD and TEST — not to run production applications. Production runs on:
- Kubernetes clusters
- Auto Scaling Groups
- ECS tasks
- Serverless (Lambda)

Jenkins' job is to produce the artifact (JAR, Docker image) and optionally trigger deployment tools.

#### 3. Document Everything
- GitHub repos with real pipelines and Jenkinsfiles
- Screenshots of actual Jenkins setups
- README files explaining what each pipeline does
- Link these in your resume/portfolio

#### 4. Speak About Real Scenarios
Don't just say "I know Jenkins." Say:

> "I set up a multi-node Jenkins environment with one master on GCP and slave agents on both AWS and on-premise Windows machines. I configured parameterized pipelines that deploy to Dev, QA, and staging environments based on a choice parameter. Build results trigger Slack notifications on failure."

#### 5. Explain the "Why"
Interviewers don't just want to know what you did — they want to know why. For every configuration decision, be ready to explain the reasoning.

---

## 9. Tech Stack Mapping

### Jenkins in a Real DevOps Stack

```
Developer (VS Code / IntelliJ)
         │ git push
         ▼
GitHub Repository
         │ webhook / pollSCM
         ▼
Jenkins Master (GCP Ubuntu)
         │ distributes jobs
    ┌────┴────┐
    ▼         ▼
Build Agent  QA Agent
(Ubuntu)     (Ubuntu)
    │              │
    │ mvn package  │ mvn test + SonarQube
    ▼              ▼
shopping-cart.jar  Test Results
    │
    ▼
Artifact Repository (Nexus/S3)
    │
    ▼
[Human Approval Gate — Continuous Delivery]
    │
    ▼
Deployment Tool (Kubernetes / Ansible / ECS)
    │
    ├── Dev Environment (port 3000)
    ├── QA Environment (port 8081)
    └── Staging Environment (port 80)
```

### AWS Services in a Modern Application Stack

| Layer | AWS Service | Role |
|-------|------------|------|
| **CDN** | CloudFront | Cache and serve static content globally |
| **Frontend** | S3 (static website) | Host React/Next.js build output |
| **API** | EC2 / ECS / Lambda | Run Node.js/Spring Boot API |
| **Database** | Amazon Aurora | Store application data |
| **Cache** | ElastiCache (Redis) | Cache frequent queries |
| **Queue** | SQS | Async processing |
| **Storage** | S3 | Files, images, artifacts |
| **Permissions** | IAM | Control who can do what |
| **Secrets** | Secrets Manager | Store credentials securely |

---

## 10. Visual Diagrams

### Diagram 1: Jenkins Common Problems Flowchart

```
Build Failed ❌
      │
      ▼
Check Console Output
      │
      ├── "No space left on device" ──────────► Clean workspace / Add disk
      │
      ├── "Cannot connect to Git" ────────────► Check credentials / URL
      │
      ├── "Tests failed: X" ──────────────────► Developer fixes code
      │
      ├── "Agent disconnected" ────────────────► Reconnect slave node
      │
      ├── "Plugin not found" ──────────────────► Install missing plugin
      │
      ├── "java: command not found" ───────────► Install Java on agent
      │
      └── Unknown error ───────────────────────► Google exact error message
                                                  Check Jenkins system log
```

---

### Diagram 2: Parameterized Job Flow

```
User clicks "Build with Parameters"
             │
             ▼
Jenkins shows parameter form:
┌──────────────────────────────┐
│ ENVIRONMENT: [Dev ▼]         │  ← dropdown: Dev / QA / Prod
│ VERSION: [latest    ]        │  ← text input
│ RUN_TESTS: [✅ checked]      │  ← boolean checkbox
│                              │
│        [Build]               │
└──────────────────────────────┘
             │
             ▼
Jenkins runs pipeline with:
  params.ENVIRONMENT = "dev"
  params.VERSION = "latest"
  params.RUN_TESTS = true
             │
             ▼
Stage: Deploy
  → "Deploying latest to dev environment"
  → java -jar -Dspring.profiles.active=dev app.jar

Stage: Test (runs because RUN_TESTS = true)
  → mvn test
```

---

### Diagram 3: Amazon Aurora Architecture

```
                    AURORA CLUSTER
                    ─────────────
         ┌─────────────────────────────────────┐
         │                                     │
         │  Writer Instance (Primary)          │
         │  Handles: INSERT, UPDATE, DELETE    │
         │                                     │
         │  Reader 1  Reader 2 ... Reader 15   │
         │  Handles: SELECT queries            │
         │                                     │
         └──────────────┬──────────────────────┘
                        │
                        │ All instances share
                        ▼ same storage layer
         ┌─────────────────────────────────────┐
         │     Distributed Storage Layer       │
         │  (6 copies across 3 AZs)           │
         │                                     │
         │  AZ-1: Copy1, Copy2                 │
         │  AZ-2: Copy3, Copy4                 │
         │  AZ-3: Copy5, Copy6                 │
         │                                     │
         │  Auto-scales up to 64TB             │
         │  Continuous backup to S3            │
         └─────────────────────────────────────┘

Failover: If Primary fails → Replica promoted in < 30 seconds
```

---

### Diagram 4: CloudFront Cache Flow

```
FIRST REQUEST (Cache MISS)                SUBSEQUENT REQUESTS (Cache HIT)
──────────────────────────                ────────────────────────────────
User (Mumbai)                             User (Mumbai)
    │                                          │
    ▼                                          ▼
CloudFront Edge                           CloudFront Edge
(Mumbai)                                  (Mumbai)
    │                                          │
    │ "Not cached"                             │ "Found in cache! ✅"
    ▼                                          ▼
Origin (S3/EC2 in us-east-1)              Response to User
    │                                     (~5-20ms)
    │ Fetch content
    ▼
Content returned
    │
    ├── Cached at Mumbai edge
    │   (stored for TTL duration)
    │
    └── Served to User
        (~200-400ms this time)
```

---

### Diagram 5: IAM User vs Role vs Policy

```
┌───────────────────────────────────────────────────────┐
│                     AWS Account                       │
│                                                       │
│  ┌──────────┐      ┌──────────┐      ┌────────────┐  │
│  │   USER   │      │   ROLE   │      │   POLICY   │  │
│  │          │      │          │      │            │  │
│  │ John     │ ──── │ Developer│ ───► │ Allow:     │  │
│  │ (identity│ uses │ (function│      │  ec2:*     │  │
│  │  badge)  │      │  /title) │      │  s3:Get*   │  │
│  └──────────┘      └──────────┘      │            │  │
│                                      │ Deny:      │  │
│  ┌──────────┐                        │  iam:*     │  │
│  │  SERVICE │                        │            │  │
│  │          │      ┌──────────┐      │ (the rules)│  │
│  │ EC2/     │ ──── │  Role    │ ───► └────────────┘  │
│  │ Lambda   │ uses │ (function│                       │
│  │          │      │  /title) │                       │
│  └──────────┘      └──────────┘                       │
└───────────────────────────────────────────────────────┘

USER = Who you are
ROLE = What job you're doing
POLICY = What rules apply to that job
```

---

### Diagram 6: Jenkins Credentials Security

```
❌ WITHOUT Credentials Management:
────────────────────────────────
Jenkinsfile:
  sh 'git clone https://john:PASSWORD123@github.com/company/repo.git'
                                  ↑
  Visible in: Git history, console logs, anyone with file access

✅ WITH Credentials Management:
────────────────────────────────
Jenkins Credentials Store (encrypted):
  ID: github-token
  Value: ghp_xxxxxxxxxxxxx  (never leaves the store unmasked)

Jenkinsfile:
  environment { GITHUB_TOKEN = credentials('github-token') }
  sh 'git clone https://${GITHUB_TOKEN}@github.com/company/repo.git'
                                ↑
  Console log shows: 'git clone https://****@github.com/company/repo.git'
```

---

## 11. Code & Practical Examples

### Example 1: Complete Parameterized Jenkins Pipeline

```groovy
// Jenkinsfile — Multi-environment deployment pipeline

pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'qa', 'prod'],
            description: 'Target deployment environment'
        )
        string(
            name: 'APP_VERSION',
            defaultValue: 'latest',
            description: 'Version tag to deploy'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Execute test suite?'
        )
    }

    environment {
        GITHUB_TOKEN = credentials('github-token')
        APP_NAME     = 'shopping-cart'
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: 'https://github.com/yourname/shopping-cart.git'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
                echo "Built version: ${params.APP_VERSION}"
            }
        }

        stage('Test') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }

        stage('Approval Gate') {
            when {
                expression { params.ENVIRONMENT == 'prod' }
            }
            steps {
                input message: "Deploy to PRODUCTION?",
                      ok: 'Approve',
                      submitter: 'manager,lead-engineer'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def port = [dev: '8082', qa: '8081', prod: '8080'][params.ENVIRONMENT]
                    sh "nohup java -jar -Dserver.port=${port} \
                        -Dspring.profiles.active=${params.ENVIRONMENT} \
                        target/${env.APP_NAME}.jar &"
                    echo "✅ Deployed to ${params.ENVIRONMENT} on port ${port}"
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment to ${params.ENVIRONMENT} succeeded!"
        }
        failure {
            echo "❌ Deployment FAILED. Check the logs above."
        }
    }
}
```

---

### Example 2: IAM Policy for a Jenkins EC2 Deploy Agent

This policy gives a Jenkins EC2 agent just enough permission to deploy to ECS and read from S3 — nothing more:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowECSDeployment",
      "Effect": "Allow",
      "Action": [
        "ecs:UpdateService",
        "ecs:DescribeServices",
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowECRImagePush",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:us-east-1:123456789012:repository/shopping-cart"
    },
    {
      "Sid": "AllowS3ArtifactRead",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::company-artifacts",
        "arn:aws:s3:::company-artifacts/*"
      ]
    }
  ]
}
```

---

### Example 3: CloudFront Cache Invalidation in Jenkins Pipeline

```groovy
stage('Invalidate CloudFront Cache') {
    steps {
        withCredentials([[
            $class: 'AmazonWebServicesCredentialsBinding',
            credentialsId: 'aws-credentials',
            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        ]]) {
            sh """
                aws cloudfront create-invalidation \
                  --distribution-id ${CLOUDFRONT_DISTRIBUTION_ID} \
                  --paths "/*"
                echo "✅ CloudFront cache invalidated"
            """
        }
    }
}
```

---

### Example 4: Jenkins System Log Cleanup Script

```bash
#!/bin/bash
# Run on Jenkins master to clean up old build logs

JENKINS_HOME="/var/lib/jenkins"
DAYS_TO_KEEP=30
JOB_NAME="shopping-cart"

echo "Current disk usage:"
df -h /

echo "Cleaning builds older than ${DAYS_TO_KEEP} days for job: ${JOB_NAME}"
find "${JENKINS_HOME}/jobs/${JOB_NAME}/builds/" \
  -maxdepth 1 \
  -type d \
  -mtime +${DAYS_TO_KEEP} \
  -exec rm -rf {} \;

echo "Cleaning all workspaces:"
du -sh ${JENKINS_HOME}/workspace/*
# Uncomment to delete all workspaces (be careful):
# rm -rf ${JENKINS_HOME}/workspace/*

echo "Disk usage after cleanup:"
df -h /
```

---

## 12. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your company deploys to three environments — Dev, QA, and Production. Currently there are three separate Jenkins jobs, all nearly identical. A new environment variable was added and someone updated Dev and QA but forgot to update Production. The production deploy broke. How do you prevent this from happening again?

✅ **Answer:** Convert the three separate jobs into one **parameterized pipeline** with an `ENVIRONMENT` choice parameter (Dev/QA/Prod). The single Jenkinsfile handles all three environments — any change to the pipeline automatically applies to all three. The environment-specific settings (ports, Spring profiles, connection strings) come from the parameter value. Optionally, add an `input` approval gate so Production requires a manager's click before deploying. One job, zero inconsistency.

---

🔍 **Scenario 2:** Your application's database is MySQL on an EC2 instance. It's becoming slow during peak hours, read queries are bottlenecking the primary, and you had a 2-hour downtime last month when the EC2 instance failed. Your CTO asks for recommendations. What do you suggest?

✅ **Answer:** Migrate to **Amazon Aurora MySQL-compatible**. It addresses all three problems: (1) Performance — Aurora is 5x faster than standard MySQL and supports up to 15 read replicas with < 10ms lag — you can offload all SELECT queries to replicas, relieving the primary; (2) Availability — Aurora's cluster architecture stores 6 copies across 3 Availability Zones. If the primary fails, automatic failover to a replica completes in < 30 seconds (vs. your 2-hour outage); (3) Scalability — storage auto-grows up to 64TB without manual intervention. This also eliminates the single point of failure that caused your downtime.

---

🔍 **Scenario 3:** You deployed new frontend files to S3, but users are still seeing the old website. The S3 files are definitely updated. What happened and what's the fix?

✅ **Answer:** CloudFront is serving cached old content from its edge locations. The S3 files updated, but CloudFront doesn't know because the cache TTL hasn't expired yet. Fix: create a **CloudFront invalidation** to force all edges to fetch fresh content: `aws cloudfront create-invalidation --distribution-id EXXXXXXXXXX --paths "/*"`. Going forward, add this as a stage in your Jenkins deployment pipeline immediately after the S3 upload step so cache invalidation is automatic on every deployment.

---

🔍 **Scenario 4:** A developer tells you "Jenkins is consuming all available disk space and builds are failing." What do you do immediately, and what do you put in place long-term?

✅ **Answer:** **Immediate fix:** SSH into the Jenkins server, run `df -h` to confirm disk is full, then `du -sh /var/lib/jenkins/workspace/*` to find the biggest culprits. Delete old workspaces: `rm -rf /var/lib/jenkins/workspace/[job-name]/`. Also check `jobs/*/builds/` for old build artifacts. **Long-term fix:** Configure **log rotation** on every job (Job → Configure → Discard old builds → set 30 days or 50 builds maximum). Set up a cron job that runs the cleanup script weekly. If disk keeps filling, attach a larger EBS volume or move the workspace directory to a separate volume.

---

🔍 **Scenario 5:** An intern accidentally created an IAM policy granting `"Action": "*"` on `"Resource": "*"` (admin access) and attached it to a service account used by the application. What are the risks and how do you fix it?

✅ **Answer:** This is a critical security violation — the service account can now do anything in your AWS account: delete databases, create IAM users, modify security groups, access all S3 buckets. If this account's credentials are compromised, the attacker has full AWS access. **Immediate fix:** Remove the overly permissive policy, replace with a least-privilege policy containing only the specific actions the application actually needs (e.g., `s3:GetObject` on the specific bucket, `ses:SendEmail` for email sending). Review CloudTrail logs to check if the account made any unexpected API calls while the permissive policy was attached. Enable **IAM Access Analyzer** going forward to automatically flag overly permissive policies.

---

🔍 **Scenario 6:** During your interview, the interviewer asks: "Tell me about a real Jenkins pipeline you've built." How do you answer this?

✅ **Answer:** Structure your answer around a real scenario: "In our DevOps training project, I built a parameterized Jenkins pipeline for a Spring Boot shopping cart application. The pipeline had five stages: Git clone from GitHub, Maven clean package, SonarQube quality gate analysis, parameterized deployment to Dev/QA/Staging with environment-specific ports and Spring profiles, and automatic Slack notification on failure. I configured the pipeline to run on a dedicated slave agent labeled 'build-java' on a separate Ubuntu VM, keeping the master free for orchestration. The master ran on GCP while one of the slave agents ran on an AWS EC2 instance — demonstrating multi-cloud CI/CD. I stored all credentials (GitHub token, SonarQube token) in Jenkins Credentials Store, never in the Jenkinsfile. The pipeline was defined as a Jenkinsfile stored in the application's GitHub repository for full version control."

---

## 13. Interview Q&A

---

**Q1. What are the most common Jenkins issues in production and how do you resolve them?**

**A:** The five most common: (1) **Job failures** — always start with Console Output, read the error, address root cause; (2) **Performance issues** — add slave agents to distribute load, use larger instance types for resource-intensive builds; (3) **Slave nodes going offline** — reconnect by re-running the `agent.jar` command, automate reconnection by running agent as a system service; (4) **Plugin issues** — keep plugins updated regularly, never update all at once in production, test after each update; (5) **Disk space exhaustion** — configure log rotation on all jobs, clean workspaces regularly, monitor disk usage with alerts. The golden rule: always check logs first.

---

**Q2. What is a parameterized Jenkins job and when would you use one?**

**A:** A parameterized job accepts user-defined inputs (parameters) before running. Instead of creating separate jobs for each environment, you create one parameterized job with a Choice parameter (Dev/QA/Prod). The pipeline uses `params.ENVIRONMENT` to control behavior — which port to deploy on, which Spring profile to activate, whether to require a manual approval gate. Use parameterized jobs when: multiple environments share the same build logic, you need on-demand version selection, you want to make tests optional, or you need a manual approval step before production. They reduce job duplication and ensure consistency across environments.

---

**Q3. What is Amazon Aurora and how does it differ from standard RDS MySQL?**

**A:** Aurora is AWS's cloud-native relational database engine, MySQL and PostgreSQL compatible. Key differences from standard RDS MySQL: Aurora is 5x faster due to a purpose-built storage layer; supports 15 read replicas (vs 5) with < 10ms replication lag; storage auto-scales to 64TB; data is stored in 6 copies across 3 AZs automatically; and failover completes in < 30 seconds vs. minutes for standard RDS. The architecture separates compute from storage — all instances share one distributed storage layer, eliminating the data-copying overhead of traditional replication. Aurora is the choice for high-availability, high-throughput production databases where RDS would bottleneck.

---

**Q4. What is CloudFront and why would you use it instead of serving content directly from S3 or EC2?**

**A:** CloudFront is AWS's CDN — a global network of 400+ edge locations that cache your content close to users. Serving from S3/EC2 directly means all users hit your origin server in one AWS region, creating high latency for users far from that region and putting all load on your origin. CloudFront solves this by caching content at edge locations worldwide — users get content from the nearest edge in < 50ms instead of 200-400ms from a distant origin. It also reduces origin load (90%+ of requests served from cache), provides DDoS protection (AWS Shield), and enables free HTTPS via ACM. In a DevOps pipeline, after deploying to S3, always run a CloudFront invalidation to ensure users get the fresh version.

---

**Q5. Explain the difference between IAM Users, Roles, and Policies.**

**A:** Three distinct concepts: A **User** is an identity — it represents a person or service account. It's WHO you are. A **Role** is a function — it defines a level of access that can be assumed by users or AWS services. It's WHAT JOB you're doing. A **Policy** is a set of permission rules — it defines what actions are allowed or denied on which resources. It's THE RULES. The relationship: you attach Policies to Roles, and Users assume Roles. Example: A Lambda function (service) assumes the Role "LambdaS3ReadRole" which has the Policy "AllowS3GetObject" attached. The Lambda can read from S3 but nothing else. The critical principle: always follow least privilege — grant only what's genuinely needed.

---

**Q6. How do Jenkins credentials work and why should you never hardcode passwords in a Jenkinsfile?**

**A:** Jenkins Credentials Store is an encrypted vault in the Jenkins home directory. You store sensitive values (GitHub tokens, database passwords, SSH keys) with an ID, and reference that ID in Jenkinsfiles using `credentials('my-id')`. Jenkins automatically masks the value as `****` in console logs. Hardcoding passwords in Jenkinsfiles is dangerous for three reasons: (1) the Jenkinsfile is committed to Git, exposing credentials to everyone with repo access; (2) credentials appear in plain text in console logs, visible to all Jenkins users; (3) rotating a password requires finding and updating every place it's hardcoded. With Credentials Store, rotation means updating one record — all pipelines using that credential ID automatically use the new value.

---

**Q7. What is the difference between Continuous Delivery and Continuous Deployment, and which is more common in enterprise settings?**

**A:** Continuous Delivery means the pipeline automatically builds, tests, and produces a deployment-ready artifact — but the actual push to production requires a human approval. Continuous Deployment extends this further: every commit that passes tests is automatically deployed to production with zero human intervention. In enterprise settings, Continuous Delivery is by far more common (~90% of companies). Regulated industries (banking, healthcare) often require change management approval before production changes. Even in tech companies, most teams want a human sanity check before touching production. In interviews, say you practice Continuous Delivery with an approval gate before production — this is the mature, professional answer.

---

**Q8. How would you troubleshoot a Jenkins job stuck in "pending" state?**

**A:** Pending means the job is waiting for an agent to become available. Diagnose in this order: (1) Check Manage Jenkins → Nodes — look for offline agents. If the assigned agent is offline, reconnect it by re-running `agent.jar` on the slave machine; (2) Check the job's label expression — if the job requires label `performance` but no online agent has that label, it waits forever. Temporarily change to `agent any` to unblock; (3) Check executor count — if all executors on the target agent are busy, the job queues until one finishes. You can add more executors to the node or add another agent with the same label; (4) Check if Jenkins master is low on memory — restart Jenkins via `http://JENKINS_URL/safeRestart` if the UI is sluggish.

---

**Q9. What should a Jenkins portfolio on GitHub include to impress interviewers?**

**A:** A strong Jenkins portfolio includes: (1) A real `Jenkinsfile` in a project repository showing multi-stage pipeline (Clone → Build → Test → Quality Gate → Deploy) with proper `post` blocks; (2) Evidence of Master-Slave setup — screenshots of node configuration, preferably multi-cloud (GCP master + AWS agent); (3) Parameterized pipeline with Dev/QA/Prod environments; (4) Screenshot of successful builds showing all stages green in Jenkins UI; (5) README explaining the architecture and decisions made; (6) Evidence of credentials management (Jenkinsfile references credential IDs, no hardcoded secrets); (7) If possible, integration with SonarQube or Slack notifications. The goal: show that you've actually run these pipelines, not just read about them.

---

← Previous: [`30_Jenkins_Master_Slave_Architecture_&_Node_Configuration.md`](30_Jenkins_Master_Slave_Architecture_&_Node_Configuration.md) | Next: [`32_Jenkins_Advanced_Concepts_&_Security.md`](32_Jenkins_Advanced_Concepts_&_Security.md) →