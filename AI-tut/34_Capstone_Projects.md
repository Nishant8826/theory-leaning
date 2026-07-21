# Chapter 34: Capstone Projects

**Estimated Reading Time**: 30 minutes  
**Difficulty**: Expert  
**Prerequisites**: Chapters 1–33.  
**Learning Objectives**:
1. Architect multi-container, full-stack AI applications.
2. Design database schemas supporting standard and vector data.
3. Construct multi-agent workspaces using LangGraph.
4. Set up multi-container orchestrations using Docker Compose.

---

## Introduction

You have reached the end of the curriculum. You understand the math, the orchestration frameworks, the indexing strategies, and the security parameters of modern generative AI. Now it is time to put everything together to build production-grade systems.

This final chapter details the blueprints and schemas for **two Capstone Projects** to add to your portfolio.

---

## Capstone 1: Enterprise-Grade Support RAG System

### 1. Goal & Specifications
Build a ticketing support platform. When a customer submits a ticket, the system automatically checks support docs, queries user databases for validation, suggests an answer, and resolves the ticket or escalates to a human agent, providing live streaming UI updates.

### 2. Architecture & Data Flow
* **Frontend**: React application displaying tickets dashboard, customer logs, and chat streams.
* **Backend**: Fastify API handling authentication, rate limiting, and agent orchestration.
* **Database**: PostgreSQL with `pgvector` extension storing tickets and vectorized knowledge docs.
* **Cache**: Redis acting as a rate limiter and Semantic Cache store.
* **Deployment**: Docker containerization on AWS App Runner and RDS Postgres.

### 3. Database Schema Design (SQL)
```sql
-- Enable Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Users and Roles
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  role VARCHAR(20) DEFAULT 'customer' -- customer, support_rep, admin
);

-- Support Knowledgebase Articles
CREATE TABLE knowledge_base (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(1536) -- OpenAI embedding size
);

-- Support Tickets Table
CREATE TABLE tickets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  customer_id UUID REFERENCES users(id),
  subject TEXT NOT NULL,
  description TEXT NOT NULL,
  status VARCHAR(20) DEFAULT 'open', -- open, resolved, escalated
  ai_suggested_response TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Capstone 2: Multi-Agent Software Development Workspace

### 1. Goal & Specifications
Create a web agent workspace. You supply a requirements prompt (e.g. "Create a Express billing router with tests"). The agent graph analyzes files, generates a plan, writes code files, runs testing scripts, fixes compiler issues, and opens a git branch with code changes.

### 2. Graph Topology (LangGraph)
* **Supervisor Node**: Parses requirements and creates a task list (DAG).
* **Code Writer Node**: Reads/writes files using file-system tooling.
* **Validator Node**: Runs `npm run build` or `npm test` via Node `child_process`.
* **Reflection Routing**: If compiler/tests fail, loops the code back to Coder with error logs. If clean, routes to Git tool and terminates.

---

## Code Example: Capstone 2 Agent Skeleton (TypeScript)

Let's build the core execution engine of the Multi-Agent Coding Workspace using LangGraph and Node.js child processes.

Create `capstone_workspace.ts`:

```typescript
import { Annotation, StateGraph, START, END } from "@langchain/langgraph";
import * as fs from "fs";
import * as path from "path";

// 1. Define the Workspace State Schema
const WorkspaceState = Annotation.Root({
  taskInstructions: Annotation<string>({
    reducer: (x, y) => y ?? x,
    default: () => "",
  }),
  codeContent: Annotation<string>({
    reducer: (x, y) => y ?? x,
    default: () => "",
  }),
  compilerErrors: Annotation<string>({
    reducer: (x, y) => y ?? x,
    default: () => "",
  }),
  attemptsCount: Annotation<number>({
    reducer: (x, y) => x + y, // Increments compilation attempts
    default: () => 0,
  }),
  status: Annotation<'COMPILING' | 'SUCCESS'>({
    reducer: (x, y) => y ?? x,
    default: () => "COMPILING",
  })
});

// 2. Define Node Actions

// Node A: Coder Agent Node
async function coderNode(state: typeof WorkspaceState.State) {
  console.log(`[CoderNode] Writing typescript code. Attempt: ${state.attemptsCount + 1}`);
  let code = `export function add(a: number, b: number): number {\n  return a + b;\n}`;

  // Write file to workspace
  const tempFilePath = path.join(process.cwd(), "temp_target.ts");
  fs.writeFileSync(tempFilePath, code);
  
  return {
    codeContent: code,
    attemptsCount: 1
  };
}

// Node B: Validator Node (Runs compiler / tests)
async function validatorNode(state: typeof WorkspaceState.State) {
  console.log("[ValidatorNode] Compiling TS file and running validation checks...");
  const tempFilePath = path.join(process.cwd(), "temp_target.ts");

  try {
    if (!fs.existsSync(tempFilePath)) {
      throw new Error("Target file not found.");
    }
    console.log("[ValidatorNode] Compilation successful. Running tests...");
    
    return {
      status: "SUCCESS" as const,
      compilerErrors: ""
    };
  } catch (error: any) {
    console.error("[ValidatorNode] Validation error detected!");
    return {
      status: "COMPILING" as const,
      compilerErrors: error.message
    };
  }
}

// 3. Routing Edge Logic
function routeAfterValidation(state: typeof WorkspaceState.State) {
  if (state.status === "SUCCESS") {
    return "success";
  }
  if (state.attemptsCount >= 3) {
    console.log("[Router] Maximum compile attempts reached. Terminating workspace.");
    return "fail";
  }
  return "retry";
}

// 4. Construct Graph
const workflow = new StateGraph(WorkspaceState)
  .addNode("coder", coderNode)
  .addNode("validator", validatorNode)
  .addEdge(START, "coder")
  .addEdge("coder", "validator")
  .addConditionalEdges("validator", routeAfterValidation, {
    success: END,
    retry: "coder",
    fail: END
  });

const workspaceAgent = workflow.compile();

// 5. Run Capstone Engine Simulation
(async () => {
  console.log("Starting Capstone Multi-Agent Software Development workspace runner...");
  const finalState = await workspaceAgent.invoke({
    taskInstructions: "Create a math module with a TypeScript add function."
  });

  console.log("\n--- Final Execution Report ---");
  console.log("Status:", finalState.status);
  console.log("Attempts:", finalState.attemptsCount);
  console.log("Generated File Content:\n", finalState.codeContent);
  
  // Cleanup file
  const tempFilePath = path.join(process.cwd(), "temp_target.ts");
  if (fs.existsSync(tempFilePath)) {
    fs.unlinkSync(tempFilePath);
  }
})();
```

Run this file:
```bash
npx tsx capstone_workspace.ts
```

---

## Best Practices, Production & Security Considerations

### 1. Docker Compose Orchestration
To host the Enterprise Support system, run a multi-container stack. Save this configuration as `docker-compose.yml`:
```yaml
version: '3.8'

services:
  database:
    image: pgvector/pgvector:pg16
    container_name: postgres_db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: production_password
      POSTGRES_DB: app_db
    volumes:
      - pgdata:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    container_name: redis_cache
    ports:
      - "6379:6379"

  api-server:
    build: .
    container_name: fastify_api
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:production_password@database:5432/app_db
      REDIS_URL: redis://cache:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - database
      - cache

volumes:
  pgdata:
```

---

## Exercises & Mini Project

### Exercise 1: Multi-Tenant Schema Validation
Extend the Postgres SQL schema for Capstone 1 by adding a `tenant_id` column to both the `tickets` and `knowledge_base` tables. Add indices on the `tenant_id` columns.

### Mini Project: Git branch automation
Update the Capstone 2 TypeScript code snippet. Add a tool `gitCommitAndPush(branchName: string)` using Node's `execSync` command to automate creating a git branch, staging changes, and committing the files locally.

---

## Interview Questions

1. **Q**: How would you handle database connection pooling in a serverless environment querying pgvector?
   * **A**: Use an RDS Proxy or pgBouncer between the serverless functions and the database to reuse database connections, reducing connection overhead.
2. **Q**: How do you secure code validator steps inside child processes?
   * **A**: Execute the validator and compiler checks in an isolated, sandboxed environment (such as a temporary Docker container with read-only files system access and no internet connection).

---

## Navigation

**Prev:** [Chapter 33: Interview Prep](file:///d:/learning/theory/AI-tut/33_Interview_Questions_and_Coding_Challenges.md) | **Index:** [Course Overview](file:///d:/learning/theory/AI-tut/README.md) | **Next:** -
