# Handling Responses & Errors in the Backend

---

### What
When integrating AI agents heavily into a Node.js backend, you have to account for the chaotic nature of LLMs. 
- **Handling Responses:** Parsing markdown, handling malformed JSON, and formatting data for the frontend.
- **Error Handling:** Dealing with API rate limits, API timeouts, invalid tool schemas, and agent infinite loops.

---

### Why
If you build a standard CRUD API, the database reliably returns the data structure you asked for. LLMs are non-deterministic (they produce varied outputs). Even with Function Calling, an LLM might hallucinate a tool name, forget a required parameter, or the heavy OpenAI API might crash. If your backend doesn't elegantly catch these, your servers will crash.

---

### How
- Wrap all LLM calls in `try/catch` and utilize Fallbacks.
- Implement Retry logic for 429 (Rate Limit) errors.
- Always validate the JSON output from an LLM using a tool like Zod before passing it further into your code.

---

### Implementation

An example of Defensive Programming when dealing with an Agent in Node.js.

```typescript
import { z } from 'zod';

// We expect the AI to return this structure: { answer: string, confidence: number }
const ExpectedSchema = z.object({
  answer: z.string(),
  confidence: z.number()
});

async function safeLLMCall(prompt: string) {
    try {
        // Mock API call that could fail or return bad JSON
        console.log("Calling OpenAI...");
        
        // Simulate a network failure
        // throw new Error("API Timeout");
        
        // Simulated response from AI
        const messyJSONResult = `{"answer": "Paris is the capital", "confidence": 99}`;

        // 1. Defensively Parse JSON
        const rawObject = JSON.parse(messyJSONResult);
        
        // 2. Defensively Validate Schema
        const validatedData = ExpectedSchema.parse(rawObject);
        
        return validatedData;

    } catch (error: any) {
        console.error("Agent Error Caught!");
        
        // Handle specific API Rate Limits
        if (error.status === 429) {
            return { answer: "I'm receiving too many requests. Please try again later.", confidence: 0 };
        }
        
        // Handle JSON Parse errors
        if (error instanceof SyntaxError) {
             return { answer: "Agent returned malformed data.", confidence: 0 };
        }
        
        // Generic Fallback
        return { answer: "Agent encountered a critical error.", confidence: 0 };
    }
}

async function app() {
    const result = await safeLLMCall("What is the capital of France?");
    console.log(result.answer);
}
app();
```

---

### Steps
1. Never trust the LLM to output perfect syntax. Always use `try...catch` around `JSON.parse()`.
2. Use exponential backoff (retry after 1s, then 2s, then 4s) if the LLM API is throttling you.
3. If the Agent loops and errors out, format a clean "I am sorry, I couldn't complete that" string to send to the UI, rather than breaking the React application.

---

### Integration

* **React/Next.js:** Expect the API to return a cleanly structured `{ error: string }` if the backend catches an error. Display a toast notification to the user.
* **Node.js backend:** Centralize your LLM API calls into a helper library so you only have to write your Retry and JSON validation logic once, applying it globally to all your agents.

---

### Impact
Proper error handling prevents user frustration. Due to the high latencies of AI, waiting 20 seconds just to crash the app is a terrible user experience. Graceful fallbacks ensure the app stays alive and communicates the issue.

---

### Interview Questions
1. **Why is defensive programming crucial when working with LLM responses?**
   *Answer: Because LLMs are probabilistic models, meaning their output structures are never 100% guaranteed, and external APIs are prone to high latencies and rate limits.*
2. **What is Zod and why is it useful in AI architectures?**
   *Answer: Zod is a TypeScript-first schema declaration and validation library. It is used to ensure the JSON returned by the AI exactly matches the structure expected by your codebase.*

---

### Summary
* LLM APIs fail often (Timeouts, Rate Limits, Overloaded).
* LLMs occasionally generate invalid JSON strings.
* Always wrap agent calls in Try/Catch and validate schemas strictly before propagating data.

---
Prev : [14_integrating_react_nextjs.md](./14_integrating_react_nextjs.md) | Next : [16_n8n_guide.md](./16_n8n_guide.md)
