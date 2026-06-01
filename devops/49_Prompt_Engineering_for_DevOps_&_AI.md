# 49 – Prompt Engineering for DevOps & AI

> **Batch-43 | Prompt Engineering + AI Types + GitHub Copilot Setup**

---

## Table of Contents

1. [The AI Landscape — More Than Just ChatGPT](#1-the-ai-landscape--more-than-just-chatgpt)
2. [What is Prompt Engineering?](#2-what-is-prompt-engineering)
3. [The CRAFT Model](#3-the-craft-model)
4. [Key Prompt Engineering Principles](#4-key-prompt-engineering-principles)
5. [Types of AI Explained](#5-types-of-ai-explained)
6. [Agentic AI vs AI Agent](#6-agentic-ai-vs-ai-agent)
7. [Tools Setup — VS Code + GitHub Copilot](#7-tools-setup--vs-code--github-copilot)
8. [Visual Diagrams](#8-visual-diagrams)
9. [Scenario-Based Q&A](#9-scenario-based-qa)
10. [Interview Q&A](#10-interview-qa)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Code / Practical Examples](#12-code--practical-examples)
13. [Navigation Footer](#navigation-footer)

---

## 1. The AI Landscape — More Than Just ChatGPT

### What
Most people think "AI = ChatGPT." That's like saying "the internet = Google." ChatGPT is just one **visible product** built on top of AI. The actual AI landscape is much broader.

```
AI (Artificial Intelligence)
    │
    ├── Machine Learning (ML)
    │       └── Deep Learning
    │               └── Neural Networks
    │
    ├── Computer Vision (image recognition)
    ├── Natural Language Processing (NLP)
    ├── Robotics
    │
    └── Generative AI  ← This is what ChatGPT, Claude, Gemini are
            └── Large Language Models (LLMs)
```

### Why This Matters for DevOps Engineers
As a DevOps engineer, you'll interact with AI at multiple levels:
- **Generative AI** — Write IaC, shell scripts, pipelines using Copilot / ChatGPT
- **Agentic AI** — Automate multi-step DevOps workflows
- **AI in cloud** — AWS Bedrock, GCP Vertex AI, Azure OpenAI for custom automation

Understanding the full map prevents you from being limited to one tool and helps you make better architecture decisions.

---

## 2. What is Prompt Engineering?

### What
**Prompt Engineering** is the practice of **designing, structuring, and refining the inputs (prompts) you give to an AI model** to get the most accurate, useful, and relevant outputs.

> Simply put: **Better questions → Better answers. Vague questions → Useless answers.**

A prompt is not just a question — it's a full instruction set that gives the AI:
- Context (who, what, where)
- A role (who should it act as)
- An action (what to do)
- A format (how to respond)
- A tone (how to communicate)

### Why
AI models like GPT, Claude, and Gemini are trained on enormous amounts of data. They can respond in a thousand different ways to the same question. **Prompt engineering is the steering wheel** — it controls which of those thousand responses you actually get.

| Bad Prompt | Good Prompt |
|---|---|
| "Write a script" | "Write a Bash script that checks disk usage on a Linux server, alerts if > 80%, and logs to /var/log/disk_check.log" |
| "Explain Docker" | "Explain Docker to a fresher with no containerization background, using a restaurant analogy, in 5 bullet points" |
| "Fix my code" | "I'm getting a `ModuleNotFoundError: boto3` in Python 3.12 on Ubuntu 22.04. Here's the error: [paste]. How do I fix it?" |

### How (Iterative Prompting)

```
1. Start with your goal (what do you want?)
2. Add context (what's the environment/situation?)
3. Define the role (who should AI act as?)
4. Specify the format (how should the answer look?)
5. Review the output
6. If not right → refine the prompt and try again
```

> Prompt engineering is **iterative** — your first prompt is rarely perfect. Each refinement gets you closer.

### Impact

| With Good Prompts | With Vague Prompts |
|---|---|
| Get production-ready scripts on first try | Get generic boilerplate that needs hours of editing |
| AI acts as a specialized expert | AI gives generic textbook answers |
| Consistent, reusable prompt templates | Inconsistent results every time |
| AI becomes a force multiplier | AI becomes a frustrating search engine |

---

## 3. The CRAFT Model

### What
**CRAFT** is a 5-part framework for writing structured, effective prompts. Each letter is a layer you add to your prompt to give the AI more precision.

```
C – Context / Constraint
R – Role
A – Action
F – Format
T – Tone
```

Think of it as writing a **job description for the AI** — the more specific, the better the output.

---

### C — Context / Constraint

**What:** Set the background, environment, and any limitations for the AI.

**Why:** Without context, AI makes assumptions — often wrong ones. Context eliminates ambiguity.

```
❌ Without context:  "Write a deployment script"
✅ With context:     "I have a Node.js 20 app on AWS EC2 (Ubuntu 22.04),
                      deployed using PM2, behind Nginx.
                      The app runs on port 3000."
```

**Constraint examples:**
- "Do not use Docker in the solution"
- "The script must work on both Ubuntu 20.04 and 22.04"
- "Keep the response under 50 lines"
- "Only use AWS free-tier services"

---

### R — Role

**What:** Tell the AI who it should act as — what expertise, perspective, and personality to adopt.

**Why:** The same question answered by a "senior DevOps engineer" vs a "beginner tutor" will be completely different in depth, vocabulary, and structure.

```
❌ Without role:  "Explain Kubernetes"
✅ With role:     "You are a senior Kubernetes administrator with 8 years of
                   experience. Explain Kubernetes to a developer who
                   understands Docker but has never used K8s."
```

**Useful DevOps roles:**
- "You are a senior DevOps engineer specializing in AWS and Terraform"
- "You are a Linux sysadmin with 10 years of experience"
- "You are a security-focused cloud architect reviewing this Terraform code"
- "You are a technical interviewer at a top product company"

---

### A — Action

**What:** Clearly define the **specific task** you want the AI to perform. Use strong action verbs.

**Why:** Vague actions produce vague results. The AI needs to know exactly what to do.

```
❌ Vague action:   "Help me with Jenkins"
✅ Specific action: "Write a Jenkins declarative pipeline that:
                     1. Checks out code from GitHub
                     2. Runs npm test
                     3. Builds a Docker image
                     4. Pushes it to AWS ECR
                     5. Deploys to EC2 via SSH"
```

**Strong action verbs for DevOps prompts:**
`Write`, `Generate`, `Debug`, `Optimize`, `Explain`, `Convert`, `Review`, `Create`, `List`, `Compare`, `Summarize`, `Fix`, `Refactor`

---

### F — Format

**What:** Specify exactly how you want the output structured.

**Why:** AI can respond in paragraphs, tables, JSON, YAML, scripts, bullet points, numbered lists, etc. Without specifying, it guesses — and often guesses wrong for your use case.

```
❌ No format:    "What are the best practices for Dockerfile?"
✅ With format:  "List the top 10 Dockerfile best practices as a
                  numbered list, with a one-line explanation and
                  a ✅/❌ example for each."
```

**Format options for DevOps:**
- `"Return as a valid JSON object"`
- `"Write as a complete, runnable Bash script"`
- `"Format as a Markdown table"`
- `"Output as a Jenkinsfile (declarative syntax)"`
- `"Give me a YAML file for Kubernetes deployment"`
- `"Respond in bullet points, max 5 per section"`

---

### T — Tone

**What:** Define the communication style of the response.

**Why:** A deeply technical response with jargon is perfect for an expert but useless for a fresher. Tone controls the complexity and language level.

```
❌ No tone:    "Explain what a VPC is"
✅ With tone:  "Explain what a VPC is in simple language,
                as if I'm completely new to cloud networking.
                Use an analogy."
```

**Tone options:**
- `"Professional and concise"`
- `"Simple language for beginners, no jargon"`
- `"Explain like I'm 10 years old"`
- `"Hindi mein samjhao (explain in Hindi)"`
- `"Use a real-world analogy"`
- `"Be direct — bullet points only, no preamble"`

---

### CRAFT in Action — Full Example

**Goal:** Get a Terraform script for creating an S3 bucket.

```
[C - Context]
I am setting up infrastructure for a Node.js app on AWS.
I need an S3 bucket to store build artifacts from Jenkins.
The bucket should be private, versioning-enabled, and in ap-south-1.

[R - Role]
You are a senior AWS DevOps engineer with deep Terraform expertise.

[A - Action]
Write a complete Terraform configuration that creates this S3 bucket.

[F - Format]
Return as a single main.tf file with inline comments explaining each block.
Include a terraform.tfvars example at the end as a comment.

[T - Tone]
Professional. Include a comment at the top explaining the purpose.
```

**What you get:** A production-ready, commented Terraform file tailored exactly to your needs — not a generic tutorial snippet.

---

## 4. Key Prompt Engineering Principles

### Principle 1: Be Specific, Short, and Clear

More words ≠ better prompts. Precise words = better prompts.

```
❌ "Can you maybe help me understand how I could potentially use
    Python with AWS to do something with files?"

✅ "Write a Python script using boto3 that uploads all .log files
    from /var/log/myapp/ to an S3 bucket named 'myapp-logs',
    with today's date as a folder prefix."
```

---

### Principle 2: Break Big Tasks into Small Prompts

AI models have a **context window** (memory limit). Big, multi-part requests often get partially fulfilled or lose quality toward the end.

**Instead of one monster prompt:**
```
Write me a complete CI/CD pipeline with Terraform, Jenkins, Docker,
AWS, monitoring, alerting, logging, and auto-scaling.
```

**Do this (separate prompts/projects):**
```
Prompt 1: "Write Terraform for a 3-tier VPC in AWS"
Prompt 2: "Write a Dockerfile for this Node.js app"
Prompt 3: "Write a Jenkinsfile for build → test → push to ECR"
Prompt 4: "Write a CloudWatch alarm for CPU > 80%"
```

Each prompt is focused, gets a quality response, and you compose them together.

---

### Principle 3: Use Separate Projects Per Use Case

Most AI platforms (ChatGPT, Claude) support **Projects** — separate conversation spaces with their own context and custom instructions.

| Project | Custom Instructions | Purpose |
|---|---|---|
| **Work / Office** | "You are familiar with our tech stack: Node.js, AWS, PostgreSQL, Jenkins" | Day-to-day work tasks |
| **Learning** | "Explain everything from scratch. I'm learning DevOps." | Study and course work |
| **Job Search** | "You are a senior tech recruiter and resume coach" | Resume, interview prep |
| **Code Review** | "You are a security-focused code reviewer" | Reviewing scripts and IaC |

Benefits:
- No context bleed between use cases
- AI "remembers" your project's specific stack
- More consistent, relevant answers

---

### Principle 4: NEVER Share Confidential Data with Public AI

**This is a critical professional and legal boundary.**

❌ **Never put these in a public AI prompt:**
- Company source code or proprietary algorithms
- Customer names, emails, personal data (PII)
- Internal server IPs, hostnames, credentials
- Database schemas with real table/column names
- AWS account IDs, access keys, secrets
- Business strategy or unreleased product plans

✅ **Safe alternatives:**
- Use placeholder names: `[COMPANY_NAME]`, `DB_HOST`, `API_KEY`
- Ask about the concept, not the actual implementation
- Use self-hosted / enterprise AI tools for sensitive work (AWS Bedrock, Azure OpenAI with private deployment)

```
❌ BAD:  "Here is our production RDS connection string:
         postgresql://admin:SuperSecret123@prod-db.abc123.ap-south-1.rds.amazonaws.com"

✅ GOOD: "Show me how to securely connect to an RDS PostgreSQL database
         in a Node.js app using environment variables and AWS Secrets Manager."
```

---

## 5. Types of AI Explained

### ANI — Artificial Narrow Intelligence

**What:** AI designed to do **one specific task** extremely well. It cannot do anything outside its domain.

**Why it exists:** Solving a single, well-defined problem at scale and speed no human can match.

| Tool | What it does | What it can't do |
|---|---|---|
| Google Maps | Navigation, traffic prediction | Answer your email |
| Netflix recommendations | Suggest movies you'll like | Book you a taxi |
| Spam filters | Classify emails as spam/not | Write code |
| Face ID | Recognize your face | Understand language |
| Chess engines (Stockfish) | Play chess perfectly | Play checkers |

**Impact:** ANI is already deeply embedded in modern software. Every recommendation engine, fraud detection system, and autocomplete feature is ANI.

---

### AGI — Artificial General Intelligence

**What:** AI that can perform **any intellectual task a human can** — reasoning, writing, coding, planning, learning new domains without retraining.

**Current state:** **LLMs (Large Language Models) like GPT-4, Claude, Gemini** are considered the current stage of AGI progress. They're not fully AGI (they have limitations in reasoning, memory, real-world action) but they're the closest we've reached.

**Why it matters for DevOps:**
- Write Terraform, Bash, Python, Dockerfiles in natural language
- Debug errors by describing symptoms
- Design architectures from requirements
- Study and explain complex concepts

**Examples:** ChatGPT, Claude, Gemini, LLaMA, Mistral

**Impact:** AGI-level tools are already changing how DevOps engineers work — shifting from "write every line of code" to "architect + review + prompt."

---

### ASI — Artificial Super Intelligence

**What:** AI that **surpasses the best human intelligence in every domain** — science, creativity, social skills, strategy. It could solve problems humans can't even conceptualize.

**Current state:** **Does not yet exist.** This is a future possibility, widely discussed in AI safety research.

**Why it's relevant:** ASI is why companies like Anthropic (Claude) and OpenAI say their core mission is AI safety. An ASI without human-aligned values could be the most consequential technology ever created.

---

### Generative AI

**What:** A category of AI that **creates new content** — text, images, audio, video, code — in response to prompts. It doesn't just classify or predict; it **generates**.

**How it works (simplified):**
1. Trained on billions of text/image examples
2. Learns patterns and relationships in language
3. Given a prompt → predicts the most probable useful continuation
4. Returns generated content

**Examples:** ChatGPT (text), DALL-E (images), GitHub Copilot (code), Suno (music), Runway (video)

**DevOps use cases:** Writing Dockerfiles, Terraform, Bash scripts, Kubernetes manifests, Jenkins pipelines, architecture diagrams (from text description)

---

### Agentic AI

**What:** AI systems that can **coordinate multiple AI agents, tools, and steps** to complete a complex, multi-part goal — refining outputs as they go, using tools like web search, code execution, file access.

**How it's different from a single AI chat:**

```
Single AI Chat:               Agentic AI:
You → Prompt → Response       You → Goal
                              Orchestrator Agent
                                  ├── Research Agent (searches web)
                                  ├── Code Agent (writes & tests code)
                                  ├── Reviewer Agent (checks quality)
                                  └── Output refined & delivered
```

**Examples:** AutoGPT, CrewAI, LangGraph, Claude's Projects with tools, GitHub Copilot Workspace

**DevOps use case:** "Set up a complete CI/CD pipeline for my Node.js app" → Agentic AI reads your repo, generates Dockerfile, Jenkins pipeline, Terraform, tests it, and delivers the final output.

---

### AI Agent

**What:** A single AI entity that can **take autonomous actions** in the real world — not just answer questions, but do things.

**How it works:**
1. Given a goal ("book a flight from Delhi to Bangalore on June 10")
2. Has access to tools (browser, API calls, calendar)
3. Takes actions step by step until goal is achieved
4. Can make decisions along the way

**Examples:** Claude's computer use, Devin (AI software engineer), browser-based agents that fill forms

---

## 6. Agentic AI vs AI Agent

### The Key Distinction

This is a common source of confusion. Here's the clearest breakdown:

| | **Agentic AI** | **AI Agent** |
|---|---|---|
| **Scope** | A system / framework | A single entity |
| **Function** | Orchestrates multiple agents | Takes autonomous actions |
| **Analogy** | Project Manager | Worker |
| **Example** | CrewAI orchestrating 4 specialized agents | One agent browsing the web to find prices |
| **Output** | Coordinated multi-step result | Completed single task |

### Real-World Analogy

```
Agentic AI = The entire kitchen in a restaurant
  - Orchestrates: chef, sous-chef, prep cook, dishwasher
  - Each person (agent) does their part
  - Output: the complete meal

AI Agent = One chef
  - Receives order: "make pasta"
  - Takes actions: boil water, cook pasta, make sauce, plate
  - Output: the pasta dish
```

### DevOps Example

```
AI Agent:
  "Check if all EC2 instances in us-east-1 have the 'Environment' tag.
   If not, add it with value 'production'."
  → Single agent, single task, takes autonomous action via AWS API

Agentic AI:
  "Set up a complete monitoring and alerting system for my 3-tier app."
  → Orchestrator spawns:
      Agent 1: Analyzes current infra
      Agent 2: Writes CloudWatch alarm configs
      Agent 3: Writes SNS + Lambda notification code
      Agent 4: Writes Terraform to deploy it all
      Agent 5: Reviews all outputs for consistency
  → Final: complete monitoring stack
```

---

## 7. Tools Setup — VS Code + GitHub Copilot

### What
**GitHub Copilot** is an AI coding assistant built into VS Code (and other IDEs). It uses the same LLM technology as ChatGPT, but it's **context-aware of your code** — it sees your open files, project structure, and coding patterns.

### Why
- Code completion in real-time (as you type)
- Inline chat: ask questions without leaving your editor
- Generate entire files from a comment description
- Explain code, fix bugs, write tests
- Works with IaC: Terraform, YAML, Dockerfiles, Jenkinsfiles

### Setup Steps

```
Step 1: Install VS Code
  → https://code.visualstudio.com/download

Step 2: Install GitHub Copilot Extension
  → Open VS Code
  → Ctrl+Shift+X (Extensions panel)
  → Search "GitHub Copilot"
  → Install "GitHub Copilot" (by GitHub)
  → Install "GitHub Copilot Chat" (by GitHub)

Step 3: Sign in
  → Copilot requires a GitHub account
  → Sign in when prompted (uses OAuth)
  → GitHub Copilot requires a paid subscription
    (Free tier: 2000 completions/month + 50 chat messages)

Step 4: Open Copilot Chat
  → Shortcut: Ctrl + Shift + I   ← Remember this!
  → Or: click the Copilot icon in the sidebar
```

### Additional Extensions Installed in Session

| Extension | Purpose |
|---|---|
| **Kubernetes Template** | YAML templates for K8s Deployments, Services, Ingress |
| **YAML** (Red Hat) | YAML validation, auto-complete, schema checking |

### Using CRAFT Model in VS Code Copilot

The CRAFT model works identically in Copilot Chat. Open with `Ctrl+Shift+I` and write:

```
[Context]  I have a Node.js 20 app, running on EC2 Ubuntu 22.04 behind Nginx.
[Role]     Act as a senior DevOps engineer.
[Action]   Write a Bash script that:
           1. Pulls latest code from GitHub main branch
           2. Runs npm ci
           3. Restarts the PM2 process named 'myapp'
           4. Checks if the app is healthy on port 3000
[Format]   Return as a complete, runnable .sh file with comments.
[Tone]     Production-grade. Include error handling with set -e.
```

### Copilot in Code (Inline Suggestions)

```javascript
// Type a comment describing what you want — Copilot autocompletes it
// Function to upload a file to S3 and return the public URL
async function uploadToS3(filePath, bucketName) {
    // ← Copilot suggests the entire function here
}
```

```bash
# Bash: check if a service is running and restart if not
# ← Copilot writes the if/systemctl block
```

---

## 8. Visual Diagrams

### The AI Landscape Map

```
ARTIFICIAL INTELLIGENCE
        │
        ├── Machine Learning
        │       ├── Supervised Learning (classification, regression)
        │       ├── Unsupervised Learning (clustering)
        │       └── Reinforcement Learning (games, robotics)
        │
        ├── ANI (Narrow AI) — TODAY
        │       ├── Google Maps (navigation)
        │       ├── Netflix (recommendations)
        │       ├── Face ID (recognition)
        │       └── Spam filters (classification)
        │
        ├── AGI (General AI) — CURRENT FRONTIER
        │       ├── GPT-4o (OpenAI)
        │       ├── Claude 3 (Anthropic)
        │       ├── Gemini (Google)
        │       └── LLaMA (Meta)
        │              │
        │              ├── Generative AI (creates content)
        │              └── Agentic AI (orchestrates agents)
        │
        └── ASI (Super AI) — FUTURE (not yet achieved)
```

---

### CRAFT Model Visual

```
┌──────────────────────────────────────────────────────────────┐
│                    CRAFT PROMPT FRAMEWORK                    │
├──────────┬───────────────────────────────────────────────────┤
│    C     │  CONTEXT / CONSTRAINT                             │
│          │  "I have a Node.js app on EC2 Ubuntu 22.04,       │
│          │   behind Nginx, deployed with PM2..."             │
├──────────┼───────────────────────────────────────────────────┤
│    R     │  ROLE                                             │
│          │  "You are a senior DevOps engineer with           │
│          │   8 years of AWS experience..."                   │
├──────────┼───────────────────────────────────────────────────┤
│    A     │  ACTION                                           │
│          │  "Write a Bash deployment script that:            │
│          │   1. Pulls code  2. Runs tests  3. Restarts PM2"  │
├──────────┼───────────────────────────────────────────────────┤
│    F     │  FORMAT                                           │
│          │  "Return as a complete .sh file with              │
│          │   inline comments on each section"                │
├──────────┼───────────────────────────────────────────────────┤
│    T     │  TONE                                             │
│          │  "Production-grade. Include set -e                │
│          │   and error handling. No preamble."               │
└──────────┴───────────────────────────────────────────────────┘
                              │
                              ▼
              High-quality, targeted AI output
```

---

### Prompt Quality Spectrum

```
VAGUE ◄────────────────────────────────────────► PRECISE

"write a script"              "write a bash script that monitors
                               disk usage on ubuntu 22.04, alerts
                               if / is > 80%, logs to
                               /var/log/disk_check.log, and
                               sends a Slack webhook notification"

    │                                             │
    ▼                                             ▼
Generic boilerplate                   Production-ready output
Needs heavy editing                   Usable in 5 minutes
Often wrong stack/syntax              Correct environment assumed
```

---

### Agentic AI vs AI Agent Architecture

```
AI AGENT (single worker)
─────────────────────────
Goal: "Tag all untagged EC2 instances"
        │
        ▼
    [AI Agent]
        │
        ├── calls AWS API: list instances
        ├── filters: finds 12 untagged
        ├── calls AWS API: apply tags
        └── reports: "12 instances tagged"


AGENTIC AI (orchestrated system)
──────────────────────────────────
Goal: "Build complete monitoring for my app"
        │
        ▼
  [Orchestrator / Planner Agent]
        │
        ├──▶ [Research Agent]
        │         reads current infra, identifies gaps
        │
        ├──▶ [CloudWatch Agent]
        │         writes alarm configs for CPU, disk, memory
        │
        ├──▶ [Notification Agent]
        │         writes SNS + Lambda alert code
        │
        ├──▶ [IaC Agent]
        │         writes Terraform to deploy everything
        │
        └──▶ [Review Agent]
                  checks all outputs, ensures consistency
                  assembles final deliverable
```

---

### VS Code + Copilot Workflow for DevOps

```
VS Code Editor
        │
        ├── Ctrl+Shift+I  →  Copilot Chat sidebar opens
        │                    │
        │                    ├── Ask with CRAFT model
        │                    ├── Attach files: @workspace, @file
        │                    ├── Run in terminal from chat
        │                    └── Insert code into editor
        │
        ├── Type in editor  →  Inline autocomplete suggestions
        │                    (Tab to accept, Esc to dismiss)
        │
        ├── Select code + right-click  →  Copilot: Explain
        │                                 Copilot: Fix
        │                                 Copilot: Generate tests
        │
        └── Comment-driven generation:
            # Create a Kubernetes deployment for nginx with 3 replicas
            ← Copilot writes the entire YAML below the comment
```

---

## 9. Scenario-Based Q&A

---

🔍 **Scenario 1:** You paste an error message into ChatGPT and ask "fix this" — but the response is generic and doesn't help. What did you do wrong and how do you fix it?

✅ **Answer:** The prompt lacks context and role. Apply CRAFT:
- **C:** "I'm running a Python 3.12 script on Ubuntu 22.04. Error: `ModuleNotFoundError: No module named 'boto3'`. I installed it with `pip install boto3`."
- **R:** "You are a senior Python DevOps engineer."
- **A:** "Diagnose why the error persists despite installation and give me the exact commands to fix it."
- **F:** "Step-by-step numbered list."
- **T:** "Simple and direct — I need to fix this now."

Now the AI knows your OS, Python version, what you already tried, and exactly what kind of answer to give.

---

🔍 **Scenario 2:** Your team uses GitHub Copilot. A junior engineer copy-pasted their AWS access keys into a Copilot prompt while asking how to debug an S3 connection error. What's the risk?

✅ **Answer:** This is a critical security incident. GitHub Copilot (like any public AI) transmits your input to external servers. Access keys in prompts can be logged, potentially exposed, or misused. Immediately: revoke those keys in IAM, generate new ones, rotate any secrets that were visible. Going forward: use placeholder text (`YOUR_ACCESS_KEY`) in prompts. For sensitive debugging, use private/enterprise AI deployments or redact all credentials before sharing.

---

🔍 **Scenario 3:** You're learning Kubernetes and ask Copilot: "Write a Kubernetes deployment." You get a generic deployment YAML that doesn't match your app. How do you improve the prompt?

✅ **Answer:** Apply CRAFT:
```
[C] I'm deploying a Node.js 20 API on Kubernetes (EKS 1.29).
    The app runs on port 3000, needs 3 replicas, and requires
    an environment variable DB_HOST from a Kubernetes Secret.
[R] You are a senior Kubernetes engineer.
[A] Write a complete Kubernetes Deployment and Service manifest.
[F] Single YAML file with --- separator. Include resource requests/limits.
[T] Production-grade with comments explaining each section.
```
Result: a deployment that matches your exact app, environment, and cluster version.

---

🔍 **Scenario 4:** Your manager asks you to research and implement AWS cost optimization strategies for 15 services. Asking one massive prompt returns a shallow, rushed answer. What's your strategy?

✅ **Answer:** Break it into small focused prompts — one per service or area:
- Prompt 1: "Cost optimization for EC2 (Reserved Instances, Savings Plans, right-sizing)"
- Prompt 2: "Cost optimization for RDS (instance types, Aurora Serverless, snapshot scheduling)"
- Prompt 3: "Cost optimization for S3 (lifecycle policies, storage classes)"
- ...and so on

Each prompt gets deep, quality output. You compile the responses into a single report. This is the **"break big tasks into small prompts"** principle in action.

---

🔍 **Scenario 5:** You want GitHub Copilot to consistently generate code that matches your team's style — Node.js with Express, PostgreSQL via pg library, async/await patterns, and always including JSDoc comments. How do you set this up?

✅ **Answer:** Use a **Copilot project-level context** or a `.github/copilot-instructions.md` file at your repo root:
```markdown
# Copilot Instructions
- Always use Node.js with Express framework
- Database: PostgreSQL using the `pg` library (not ORM)
- Use async/await (no callbacks or raw .then())
- Every function must have a JSDoc comment
- Error handling: try/catch with next(err) in Express routes
- Config via environment variables, never hardcoded values
```
Now every Copilot suggestion in this repo follows your team's conventions.

---

🔍 **Scenario 6:** You're building a multi-cloud Python ATS (Applicant Tracking System) that needs to run on both AWS and GCP. You want AI to help design the architecture. How do you use CRAFT effectively?

✅ **Answer:**
```
[C] I'm building an ATS (Applicant Tracking System) in Python.
    It needs to run on both AWS and GCP. AWS for compute (EC2/Lambda),
    GCP for AI features (Vertex AI for resume screening).
    Storage: S3 (AWS) + GCS (GCP). Database: PostgreSQL on RDS.
[R] You are a multi-cloud solutions architect with Python expertise.
[A] Design a high-level architecture showing how AWS and GCP services
    connect, with the Python services acting as the glue layer.
[F] ASCII architecture diagram + bullet-point service list with justification.
[T] Technical but clear. This is for a DevOps learning project.
```

---

## 10. Interview Q&A

---

**Q1. What is prompt engineering and why is it important for a DevOps engineer?**

**A:** Prompt engineering is the practice of designing structured, precise inputs for AI models to get high-quality, relevant outputs. For DevOps engineers, it's important because AI tools (Copilot, ChatGPT, Claude) are now part of the workflow for writing IaC, scripts, pipelines, and debugging. A well-crafted prompt can produce production-ready Terraform or Bash code in seconds. Poor prompts produce generic code that requires hours of editing or doesn't work at all. It's essentially the skill of "talking to your AI tools effectively."

---

**Q2. Explain the CRAFT model with a DevOps example.**

**A:** CRAFT stands for Context, Role, Action, Format, Tone. Example:
- **C:** "I have a Jenkins server on AWS EC2, Ubuntu 22.04, and a Node.js app in a GitHub repo."
- **R:** "Act as a senior Jenkins/DevOps engineer."
- **A:** "Write a declarative Jenkins pipeline with stages: Checkout, Test, Build Docker, Push to ECR, Deploy to EC2."
- **F:** "Return as a complete Jenkinsfile (declarative syntax) with inline comments."
- **T:** "Production-ready. Include environment variable handling and post{} failure/success blocks."

This produces a complete, usable Jenkinsfile tailored to the exact environment.

---

**Q3. What is the difference between ANI, AGI, and ASI?**

**A:**
- **ANI (Narrow):** Single-task AI. Expert at one thing, useless outside it. Google Maps, Netflix recommendations, spam filters.
- **AGI (General):** Can perform any intellectual task. Current LLMs (GPT, Claude, Gemini) are approaching this. Writes code, explains concepts, plans, reasons across domains.
- **ASI (Super):** Beyond human intelligence in every domain. Does not exist yet. Future possibility with significant safety implications.

---

**Q4. What is the difference between Generative AI and Agentic AI?**

**A:** Generative AI creates content (text, code, images) in response to a single prompt — it's a one-shot interaction. Agentic AI uses multiple AI agents coordinated by an orchestrator to complete complex, multi-step goals. Generative: "Write a Dockerfile" → one response. Agentic: "Set up a complete CI/CD pipeline" → orchestrates multiple agents (infra agent, code agent, test agent, review agent) that each do their part, with outputs feeding into each other, to deliver the complete pipeline.

---

**Q5. What is the difference between Agentic AI and an AI Agent?**

**A:** An AI Agent is a single entity that takes autonomous actions (e.g., one agent browsing the web to book a flight). Agentic AI is a system or framework that orchestrates multiple AI agents to accomplish a complex goal. AI Agent = one worker. Agentic AI = the project manager + team of workers. In DevOps: an AI Agent might tag untagged EC2 instances autonomously; Agentic AI might design and deploy an entire monitoring system by coordinating multiple specialized agents.

---

**Q6. Why should you never paste company code or credentials into public AI tools?**

**A:** Public AI models (ChatGPT, Claude.ai, Copilot free tier) transmit input to external servers and may use it for model training or logging. Pasting credentials exposes them to potential breach. Pasting proprietary code violates IP agreements and NDAs. Pasting customer PII violates data protection laws (GDPR, IT Act). Best practice: replace real values with placeholders, ask conceptually, or use enterprise/private AI deployments (AWS Bedrock, Azure OpenAI) where data stays within your organization's control.

---

**Q7. How does GitHub Copilot differ from ChatGPT for a DevOps engineer?**

**A:** GitHub Copilot is deeply integrated into the IDE (VS Code) and is context-aware — it can see your open files, project structure, and coding patterns, making suggestions that fit your existing code. ChatGPT is a standalone chat interface without code context. For DevOps: Copilot is better for inline code completion, writing IaC in your active project, and generating code that matches your existing patterns. ChatGPT/Claude are better for architecture discussions, long explanations, and tasks that don't need file context.

---

**Q8. How would you use AI tools to accelerate your DevOps work without compromising security?**

**A:** Three rules:
1. **Sanitize inputs** — Replace real IPs, credentials, and company names with placeholders before pasting anything into a public AI.
2. **Use CRAFT model** — Structured prompts get production-ready outputs that need minimal editing, reducing the chance of introducing insecure patterns.
3. **Always review AI output** — Never blindly deploy AI-generated scripts or IaC. Check for hardcoded values, insecure defaults (open security groups, `chmod 777`), missing error handling, and logic that doesn't fit your actual environment.

For sensitive work, use enterprise deployments (AWS Bedrock, GitHub Copilot Business with data privacy mode) where inputs are not used for training.

---

**Q9. What are some practical DevOps use cases for prompt engineering?**

**A:**
- Generate complete Terraform modules from a description of the architecture
- Write Dockerfiles optimized for your specific language and version
- Debug shell script errors by pasting the error and script
- Convert a manual runbook into a Bash automation script
- Write Jenkins/GitHub Actions pipelines from stage descriptions
- Generate Kubernetes manifests (Deployment, Service, Ingress) for your app
- Create CloudWatch alarm configs and SNS notification setups
- Explain a complex Terraform error in plain language
- Review a security group config for common vulnerabilities

---

## 11. Tech Stack Mapping

### AI Tools in the DevOps Workflow

| Stage | AI Tool | How It Helps |
|---|---|---|
| **Planning** | ChatGPT / Claude | Architecture design, tech stack selection, cost estimation |
| **IaC Writing** | Copilot / Cursor | Terraform, CloudFormation, Pulumi generation |
| **Scripting** | Copilot / ChatGPT | Bash, Python, PowerShell automation scripts |
| **CI/CD Pipelines** | Copilot | Jenkinsfiles, GitHub Actions YAMLs, GitLab CI |
| **Kubernetes** | Copilot + K8s Extension | Deployment, Service, Ingress YAML generation |
| **Debugging** | ChatGPT / Claude | Error explanation, root cause analysis |
| **Documentation** | ChatGPT / Claude | README, runbooks, architecture docs |
| **Code Review** | Copilot | Inline suggestions, security checks |
| **Monitoring** | Claude / ChatGPT | CloudWatch alarm JSON, Grafana dashboard queries |

---

### AI-Assisted DevOps Deployment Flow

```
Requirement: "Deploy Node.js app on AWS with CI/CD"
        │
        ├── Prompt Copilot (CRAFT):
        │   "Write Terraform for: VPC + EC2 + RDS + ALB"
        │   → Get main.tf, variable.tf, outputs.tf
        │
        ├── Prompt Copilot (CRAFT):
        │   "Write Dockerfile for Node.js 20 app"
        │   → Get optimized, multi-stage Dockerfile
        │
        ├── Prompt Copilot (CRAFT):
        │   "Write Jenkinsfile: checkout → test → build → push ECR → deploy"
        │   → Get complete Jenkinsfile
        │
        ├── Review all outputs (critical step — never skip)
        │   - Check for hardcoded values
        │   - Verify security groups aren't open
        │   - Test in staging before production
        │
        └── Deploy: terraform apply → Jenkins build → Live
```

---

### Tech Stack for Tomorrow's Multi-Cloud ATS Project

| Component | Technology | AI Tool Used |
|---|---|---|
| Backend | Python (FastAPI / Flask) | Copilot for API routes |
| AWS | EC2 / Lambda / S3 / RDS | Copilot for boto3 scripts |
| GCP | Vertex AI / GCS | Copilot for GCP SDK calls |
| Resume Parsing | Python + LLM API | Prompt-engineered parsing |
| Storage | S3 (resumes) + PostgreSQL (data) | Copilot for schema + queries |
| Deployment | Terraform (multi-cloud) | Copilot for module writing |
| CI/CD | Jenkins / GitHub Actions | Copilot for pipeline YAML |

---

## 12. Code / Practical Examples

### Example 1: CRAFT Prompts for Common DevOps Tasks

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT: Write a Dockerfile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[C] My app is a Node.js 20 REST API using Express.
    It has a build step (npm run build → dist/ folder).
    Production runs: node dist/server.js on port 3000.

[R] Act as a Docker expert focused on production best practices.

[A] Write a multi-stage Dockerfile:
    Stage 1: install deps and build
    Stage 2: production image (smaller, no dev deps)

[F] Single Dockerfile with comments on each stage.
    Include HEALTHCHECK instruction.

[T] Production-grade. Minimize image size. Non-root user.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT: Debug a Terraform error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[C] I'm running Terraform 1.8 with AWS provider ~> 5.0,
    targeting ap-south-1. Running: terraform apply

[R] You are a senior Terraform and AWS engineer.

[A] Diagnose this error and give me the exact fix:
    Error: creating RDS DB Instance: InvalidParameterCombination:
    Cannot find version 15.4 for mysql8.0

[F] Numbered steps: (1) what caused it, (2) exact fix in code.

[T] Direct. No preamble. Just diagnosis and fix.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT: Write a monitoring Bash script
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[C] Ubuntu 22.04 EC2 instance running Nginx and a Node.js app.
    I want to monitor CPU, disk, memory, and service status.

[R] Act as a senior Linux sysadmin.

[A] Write a Bash monitoring script that:
    1. Checks CPU, memory, disk (alert if > 80%)
    2. Checks if nginx and node-app are running
    3. Sends a Slack webhook alert if any check fails
    4. Logs all checks to /var/log/monitor.log

[F] Complete .sh file. Include color-coded terminal output.
    Include the cron entry needed to run it every 5 minutes.

[T] Production-grade. set -e. Error handling throughout.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Example 2: Copilot Instructions File (`.github/copilot-instructions.md`)

```markdown
# GitHub Copilot Instructions for This Project

## Project Context
This is a multi-cloud DevOps + AI Python application (ATS system).
- Backend: Python 3.12 with FastAPI
- AWS: boto3 for EC2, S3, Lambda, RDS (PostgreSQL)
- GCP: google-cloud-aiplatform for Vertex AI
- Database: PostgreSQL via asyncpg
- Testing: pytest with async support

## Code Style Rules
- Always use async/await (no synchronous blocking calls)
- Type hints on all function parameters and return types
- Docstrings on every function (Google style)
- Error handling: raise HTTPException for FastAPI routes
- Environment variables via os.getenv(), never hardcoded values
- Logging: use structlog for structured JSON logs

## AWS Patterns
- Always use IAM roles (never hardcode AWS credentials)
- Use boto3 session with explicit region: boto3.Session(region_name='ap-south-1')
- S3 keys follow: {environment}/{service}/{YYYY/MM/DD}/{filename}

## GCP Patterns  
- Authenticate via Application Default Credentials (ADC)
- Use Vertex AI SDK, not raw REST calls

## Security
- Never generate examples with hardcoded secrets
- Always use AWS Secrets Manager or GCP Secret Manager for sensitive values
- Input validation on all API endpoints
```

---

### Example 3: AI-Generated Multi-Stage Dockerfile (Result of CRAFT Prompt)

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies (cached separately from source code)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# ─────────────────────────────────────────────────────────
# Stage 2: Production image
FROM node:20-alpine AS production

# Security: run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy only production dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy built output from stage 1
COPY --from=builder /app/dist ./dist

# Set ownership
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000

# Health check for container orchestrators and ALB
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

---

### Example 4: Jenkins Pipeline with AI-Assisted Stages

```groovy
// Jenkinsfile
// Generated with CRAFT prompt + reviewed and adjusted

pipeline {
    agent any

    environment {
        ECR_REPO        = "123456789.dkr.ecr.ap-south-1.amazonaws.com/myapp"
        AWS_REGION      = "ap-south-1"
        DEPLOY_HOST     = credentials('ec2-deploy-ip')
        EC2_KEY         = credentials('ec2-ssh-key')
        SLACK_WEBHOOK   = credentials('slack-webhook-url')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/myapp.git'
            }
        }

        stage('Test') {
            steps {
                sh 'npm ci && npm test'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      --target production \
                      -t $ECR_REPO:$BUILD_NUMBER \
                      -t $ECR_REPO:latest \
                      .
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                      docker login --username AWS --password-stdin $ECR_REPO
                    docker push $ECR_REPO:$BUILD_NUMBER
                    docker push $ECR_REPO:latest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    ssh -i $EC2_KEY -o StrictHostKeyChecking=no ubuntu@$DEPLOY_HOST "
                        docker pull $ECR_REPO:latest
                        docker stop myapp 2>/dev/null || true
                        docker rm myapp 2>/dev/null || true
                        docker run -d --name myapp -p 3000:3000 \
                          --env-file /etc/myapp/.env \
                          $ECR_REPO:latest
                    "
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 15
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
                        http://$DEPLOY_HOST:3000/health)
                    [ "$STATUS" = "200" ] || exit 1
                    echo "✅ Health check passed"
                '''
            }
        }
    }

    post {
        success {
            sh """
                curl -s -X POST '$SLACK_WEBHOOK' \
                  -d '{"text":"✅ Deploy #${BUILD_NUMBER} to production succeeded"}'
            """
        }
        failure {
            sh """
                curl -s -X POST '$SLACK_WEBHOOK' \
                  -d '{"text":"❌ Deploy #${BUILD_NUMBER} FAILED — check Jenkins"}'
            """
        }
    }
}
```

---

### Example 5: Python Script Using AI-Generated Boto3 Pattern

```python
# ats_s3_resume_upload.py
# Part of Multi-Cloud ATS project (Python + AWS + GCP)
# Generated skeleton via Copilot CRAFT prompt, reviewed and expanded

import boto3
import os
import hashlib
from datetime import datetime
from pathlib import Path


def get_s3_client():
    """
    Returns a boto3 S3 client.
    Uses IAM role in production (no hardcoded keys).
    """
    return boto3.client(
        's3',
        region_name=os.getenv('AWS_REGION', 'ap-south-1')
    )


def upload_resume(local_file_path: str, candidate_id: str) -> dict:
    """
    Uploads a resume file to S3.

    Args:
        local_file_path: Path to the resume file (PDF/DOCX)
        candidate_id: Unique ID of the candidate

    Returns:
        dict with s3_key, bucket, and upload timestamp
    """
    bucket = os.getenv('RESUME_BUCKET')
    if not bucket:
        raise EnvironmentError("RESUME_BUCKET environment variable not set")

    file_path = Path(local_file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {local_file_path}")

    # Generate a consistent, organized S3 key
    date_prefix = datetime.now().strftime("%Y/%m/%d")
    file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()[:8]
    s3_key = f"resumes/{date_prefix}/{candidate_id}/{file_hash}_{file_path.name}"

    s3 = get_s3_client()

    s3.upload_file(
        str(file_path),
        bucket,
        s3_key,
        ExtraArgs={
            'ContentType': 'application/pdf',
            'ServerSideEncryption': 'AES256',   # encrypt at rest
            'Metadata': {
                'candidate_id': candidate_id,
                'uploaded_at': datetime.now().isoformat()
            }
        }
    )

    print(f"✅ Resume uploaded: s3://{bucket}/{s3_key}")
    return {
        's3_key': s3_key,
        'bucket': bucket,
        'timestamp': datetime.now().isoformat()
    }


if __name__ == "__main__":
    result = upload_resume("./sample_resume.pdf", "CAND-2026-001")
    print(result)
```

---

### Example 6: Prompt Chaining — Building the ATS Architecture Step by Step

```
# Step 1: Architecture Design
──────────────────────────────
Prompt: "Design a high-level architecture for a Python ATS system
         that uses AWS (EC2, S3, RDS PostgreSQL) for compute/storage
         and GCP Vertex AI for resume screening. Show data flow
         from resume upload to screening result. ASCII diagram."

# Step 2: Database Schema
──────────────────────────────
Prompt: "Based on this ATS architecture [paste Step 1 output],
         write the PostgreSQL schema for:
         - candidates table
         - applications table
         - screening_results table
         Return as CREATE TABLE SQL with indexes and foreign keys."

# Step 3: FastAPI Routes
──────────────────────────────
Prompt: "Using this schema [paste Step 2 output], write FastAPI
         routes for:
         POST /candidates (create candidate)
         POST /applications (submit application + upload resume to S3)
         GET /applications/{id}/screening (get AI screening result)
         Use async/await, boto3, asyncpg. Include type hints."

# Step 4: Vertex AI Integration
──────────────────────────────
Prompt: "Write a Python function that:
         1. Downloads a resume from S3 (given s3_key)
         2. Sends it to GCP Vertex AI for text extraction
         3. Returns a screening score (0-100) and key skills list
         Use boto3 for S3, google-cloud-aiplatform for Vertex.
         Handle errors gracefully."

# Step 5: Terraform
──────────────────────────────
Prompt: "Write Terraform to provision the AWS side of this ATS:
         VPC, EC2 (t3.medium), RDS PostgreSQL (db.t3.micro),
         S3 bucket (private, versioning on), IAM role for EC2.
         Region: ap-south-1. Modular structure."
```

---

## Navigation Footer

← Previous: [`48_Shell_Scripting_with_Linux.md`](48_Shell_Scripting_with_Linux.md) | Next: [`50_Prompt_Engineering_for_DevOps_&_AI.md`](50_Prompt_Engineering_for_DevOps_&_AI.md) →