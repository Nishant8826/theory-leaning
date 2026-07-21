# Chapter 33: Interview Preparation and Coding Challenges

**Estimated Reading Time**: 30 minutes  
**Difficulty**: Expert  
**Prerequisites**: Chapters 1–32.  
**Learning Objectives**:
1. Crack technical interview questions on LLM execution, RAG, and state graphs.
2. Solve system design challenges for AI integrations.
3. Master dynamic prompt pruning strategies under strict token budgets.
4. Implement a message pruner function in TypeScript.

---

## Introduction

As companies integrate AI into their stacks, they need engineers who understand first principles: attention bottlenecks, vector indexing tradeoffs, semantic caching, and multi-agent state machines.

This chapter compiles technical interview questions, system design tasks, and coding challenges with detailed answers.

---

## Technical Interview Questions

### Question 1: What is the difference between RAG and Fine-Tuning?
* **Answer**: RAG retrieves relevant documents from external databases and injects them into the prompt context at runtime, making it ideal for access to dynamic data. Fine-Tuning updates model weights on a training dataset, making it ideal for styling, formatting, and behavioral changes.

### Question 2: Why does the computational cost of self-attention scale quadratically?
* **Answer**: In self-attention, every token in a sequence is compared to every other token to compute relationship weights. For a sequence of size $N$, this requires building an $N \times N$ matrix, resulting in quadratic ($O(N^2)$) time and space complexity scaling.

### Question 3: How does the HNSW index optimize vector search?
* **Answer**: HNSW organizes vectors as a multi-layered proximity graph. It traverses sparse connections at top layers for fast spatial jumps, and dense connections at bottom layers for precise local searches, reducing query complexity to $O(\log N)$.

---

## System Design Challenge: Enterprise Copilot

### Scenario
Design a Slack bot that answers employee questions about company benefits. The company has 10,000 pages of PDF manuals, and documents are updated weekly. The bot must respect document permissions (e.g. Sales reps cannot read HR salary files).

### Solution Blueprint
1. **Ingestion**: A background worker parses PDFs, splits them into parent-child chunks, generates embeddings, and saves them to a PostgreSQL database with `pgvector`.
2. **Access Control**: When inserting embeddings, save metadata fields containing allowed roles: `{ allowed_roles: ['HR', 'Admin'] }`.
3. **Retrieval**: Retrieve the user's role from the Slack payload, and run a vector search using a metadata filter:
   ```sql
   SELECT parent_text FROM docs WHERE allowed_roles && $1 ORDER BY embedding <=> $2 LIMIT 3;
   ```
4. **Generation**: Inject context into the prompt, call the LLM, and stream the response to Slack.

---

## Coding Challenge: Token Pruning Utility (TypeScript)

Implement a utility function `pruneMessages` in TypeScript. It must accept an array of chat messages and a token budget, returning the most recent messages that fit within the budget, always preserving the system message.

Create `interview_challenge.ts`:

```typescript
import { encodingForModel } from "js-tiktoken";

interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

const encoder = encodingForModel("gpt-4o-mini");

function countMessageTokens(message: ChatMessage): number {
  return encoder.encode(message.content).length + 4; // Add formatting overhead
}

export function pruneMessages(
  messages: ChatMessage[],
  maxTokens: number
): ChatMessage[] {
  const systemMsg = messages.find(m => m.role === 'system');
  const systemTokens = systemMsg ? countMessageTokens(systemMsg) : 0;

  if (systemTokens > maxTokens) {
    throw new Error("System prompt alone exceeds the maximum token limit.");
  }

  const pruned: ChatMessage[] = [];
  let currentTokens = systemTokens;

  // Iterate backwards through messages (excluding the system prompt)
  const conversationMsgs = messages.filter(m => m.role !== 'system');
  
  for (let i = conversationMsgs.length - 1; i >= 0; i--) {
    const msg = conversationMsgs[i];
    const tokens = countMessageTokens(msg);

    if (currentTokens + tokens <= maxTokens) {
      pruned.unshift(msg); // Prepend to maintain correct chronological order
      currentTokens += tokens;
    } else {
      break; // Stop adding older messages
    }
  }

  // Prepend the system message if it exists
  if (systemMsg) {
    pruned.unshift(systemMsg);
  }

  console.log(`[Pruner] Kept ${pruned.length}/${messages.length} messages. Budget: ${currentTokens}/${maxTokens} tokens.`);
  return pruned;
}

// Test Runner
const mockMessages: ChatMessage[] = [
  { role: 'system', content: 'You are a database expert.' },
  { role: 'user', content: 'Here is my SQL table structure. It has 20 columns...' },
  { role: 'assistant', content: 'Thanks, I see the database design.' },
  { role: 'user', content: 'How do I optimize queries on the created_at field?' },
  { role: 'assistant', content: 'You should add a B-Tree index on the created_at column.' },
  { role: 'user', content: 'Can you show me the exact SQL syntax?' }
];

const budget = 50; 
const result = pruneMessages(mockMessages, budget);
console.log("Pruned Conversation Result:\n", JSON.stringify(result, null, 2));
```

Run this file:
```bash
npx tsx interview_challenge.ts
```

---

## Navigation

**Prev:** [Chapter 32: Redis Caching and Rate Limiting](file:///d:/learning/theory/AI-tut/32_Production_Redis_Caching_and_Rate_Limiting.md) | **Index:** [Course Overview](file:///d:/learning/theory/AI-tut/README.md) | **Next:** [Chapter 34: Capstone Projects](file:///d:/learning/theory/AI-tut/34_Capstone_Projects.md)
