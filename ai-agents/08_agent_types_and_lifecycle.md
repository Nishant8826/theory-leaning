# Types of Agents and the Agent Lifecycle

---

### What
- **Types of Agents:** Agents are categorized by their capabilities. Some only react, others plan ahead.
- **Agent Lifecycle:** The continuous cycle of operations an agent follows from the moment it is given a task to the moment it completes it.

---

### Why
Not every task needs a highly complex, planning agent. A simple customer service bot reacting to FAQs doesn't need to "plan" multiple steps. By understanding what types of agents exist, you can build the most cost-effective and efficient architecture for your app. The lifecycle helps us structure our code.

---

### How

**Types of Agents:**
1. **Simple Reflex Agents:** React strictly based on a written rule (If user says "refund", trigger refund function). Very rigid, no true intelligence.
2. **Learning Agents:** Improve their performance based on past interactions.
3. **Goal-Based / Autonomous Agents:** You give them a final destination. They figure out the route on their own.

**Agent Lifecycle Loop:**
- **Perceive:** Take in user input and current environment state.
- **Plan:** Decide what needs to be done.
- **Act:** Execute the function or tool.
- **Observe Result:** Check if the action worked. (If yes, finish. If no, go back to Plan).

---

### Implementation

Here is a simplified TypeScript representation of an Autonomous Agent's Lifecycle Loop.

```typescript
// The Agent Lifecycle Loop
async function agentLifecycle(goal: string) {
    let isTaskComplete = false;
    let agentMemory: string[] = [`Initial Goal: ${goal}`];

    console.log("--- Starting Agent Lifecycle ---");

    // The Loop: Persevere until complete
    while (!isTaskComplete) {
        // 1. Plan (We mock the LLM 'deciding' what to do)
        console.log("Agent: Thinking about next step...");
        const nextAction = await mockLLMDecision(agentMemory);

        // 2. Act
        if (nextAction === "SEARCH_WEB") {
            console.log("Agent Action: Searching the web.");
            agentMemory.push("Action taken: Searched web. Result: Found relevant data.");
            
        } else if (nextAction === "FINISH") {
            // 3. Complete
            console.log("Agent Action: Task is complete!");
            isTaskComplete = true;
            break;
        }

        // Failsafe to prevent infinite loops (important in real apps to save money)
        if (agentMemory.length > 5) break; 
    }
    
    console.log("--- Agent Done ---");
}

// Mocking the LLM's brain
async function mockLLMDecision(memory: string[]): Promise<string> {
    // If it just started, search. If it searched, finish.
    return memory.length === 1 ? "SEARCH_WEB" : "FINISH";
}

agentLifecycle("Find the capital of France");
```

---

### Steps
1. Determine if your task needs a basic rules-engine (Reflex) or an LLM (Autonomous).
2. Code an event loop (`while(!done)`).
3. Ensure you have a maximum iteration limit so the agent doesn't loop infinitely and cost thousands of dollars in API fees.
4. Pass the history of what the agent has done back into the LLM on every loop.

---

### Integration

* **React:** Since an agent might loop 10 times over 30 seconds, display an ongoing "Logs" UI in React so the user sees: "Searching Web...", "Reading Article...", "Formatting Response..."
* **Next.js:** You can use Next.js API Routes, but remember serverless functions usually timeout after 10-60 seconds. A complex Goal-Based agent may need a dedicated continuously running server environment.
* **Node.js backend:** Use standard `while` loops combined with try/catch blocks. If a tool fails inside the loop, push the error into the `agentMemory` array so the LLM perceives the error on its next cycle.

---

### Impact
Understanding agent types optimizes cost. Knowing the lifecycle provides a standard blueprint (Perceive -> Plan -> Act) for all AI architectures you build, making debugging much easier.

---

### Interview Questions
1. **What is an Autonomous/Goal-Based Agent?**
   *Answer: An agent where you provide the final goal, and it dynamically plans the intermediary steps required to get there, altering its path if it encounters errors.*
2. **What are the main stages of the Agent Lifecycle?**
   *Answer: Perceive (taking input), Plan (deciding action), Act (executing action), Observe (evaluating the outcome of the action).*
3. **Why is an iteration limit (max loops) critical when building AI Agents?**
   *Answer: Because LLM API calls cost money. If an agent gets stuck in a loop trying the same failing action repeatedly, it will drain credentials and lock resources.*

---

### Summary
* Simple Reflex agents follow strict rules; Goal-Based agents figure things out.
* The lifecycle is a continuous loop of thinking, doing, and checking.
* Always enforce loop limiters to prevent infinite AI errors.

---
Prev : [07_what_are_ai_agents.md](./07_what_are_ai_agents.md) | Next : [09_tools_memory_and_planning.md](./09_tools_memory_and_planning.md)
