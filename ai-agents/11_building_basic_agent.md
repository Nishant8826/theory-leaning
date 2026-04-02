# Building a Basic Agent Architecture

---

### What
A basic agent architecture is the system of code that puts together an LLM, Memory, and Tools into a continuous loop. It acts as the orchestrator, taking user input and running the "Think -> Act -> Observe" cycle.

---

### Why
If you just send an API request to OpenAI, you only get back a block of text. To build an agent, you need to write the "glue" code that handles parsing what the LLM wants to do, executing the physical code (a tool), and feeding the data back until the task is marked Complete.

---

### How
The architecture typically consists of:
1. **The Brain:** The LLM API connection.
2. **The Tool Registry:** A dictionary of JavaScript/Node functions the AI is allowed to trigger.
3. **The Memory Bank:** An array storing the entire conversation history.
4. **The Executor Loop:** A `while` loop that handles the network requests and triggers the tools.

---

### Implementation

Here is a bare-bones implementation of a Basic Agent in TypeScript.

```typescript
// Define our allowed Tools (The Registry)
const Tools = {
  getWeather: (location: string) => `The weather in ${location} is 70 degrees.`,
  getTime: () => `The current time is ${new Date().toLocaleTimeString()}`
};

// The Agent Architecture
class SimpleAgent {
  memory: any[] = [];

  constructor() {
    this.memory.push({ 
        role: "system", 
        content: "You are a helpful agent. You can use tools: [getWeather, getTime]. " +
                 "If you need a tool, reply with exactly: ACTION: toolName, param. " +
                 "Otherwise, just answer." 
    });
  }

  async run(userInput: string) {
    this.memory.push({ role: "user", content: userInput });

    let isDone = false;
    let loopCount = 0;

    // The Executor Loop
    while (!isDone && loopCount < 5) {
      loopCount++;
      console.log(`\n--- Agent Loop ${loopCount} ---`);
      
      // 1. Brain: Get LLM Response (Mocked)
      const aiResponse = await this.mockLLMCall(this.memory);
      this.memory.push({ role: "assistant", content: aiResponse });
      console.log(`Agent Says: ${aiResponse}`);

      // 2. Parse if the AI wants to use a Tool
      if (aiResponse.startsWith("ACTION:")) {
        // Example: "ACTION: getWeather, London"
        const [_, toolName, param] = aiResponse.split(/[:,]/).map(s => s.trim());
        
        console.log(`Executing Tool: ${toolName}(${param})`);
        
        // 3. Execute Tool
        let toolResult = "";
        if (toolName === "getWeather") toolResult = Tools.getWeather(param);
        else if (toolName === "getTime") toolResult = Tools.getTime();
        
        // 4. Observe: Push result back into memory so AI sees it on next loop
        this.memory.push({ role: "system", content: `Tool Result: ${toolResult}` });
      } else {
        // If it didn't ask for an ACTION, it must be the final answer!
        isDone = true; 
        console.log("Goal Achieved!");
      }
    }
  }

  // Mocking the OpenAI API response based on what is in memory
  async mockLLMCall(memory: any[]) {
     const lastItem = memory[memory.length - 1].content;
     if (lastItem.includes("weather in London")) return "ACTION: getWeather, London";
     if (lastItem.includes("Tool Result: The weather in London is 70 degrees.")) {
         return "It is currently 70 degrees in London.";
     }
     return "I don't know how to do that.";
  }
}

// Running the Agent
const myAgent = new SimpleAgent();
myAgent.run("What is the weather in London?");
```

---

### Steps
1. Define the system prompt.
2. Initialize an empty memory array.
3. Map functions (tools) that your AI can use.
4. Establish the `while(!done)` loop.
5. Parse the LLM response. If it calls a tool, run it and loop again. If plain text, break the loop and return it.

---

### Integration

* **React:** The frontend should be blind to this loop. It just sends `"What is the weather in London?"` and waits.
* **Node.js backend:** The loop runs on the server. If this loop takes 15 seconds, you might want to use Server-Sent Events (SSE) to send updates back to React (e.g. `res.write("Executing weather tool...")`).

---

### Impact
This architecture is the foundational pattern for all autonomous systems. Even multi-million dollar platforms like Devin or specialized trading bots use variations of this exact `while` loop pattern. 

---

### Interview Questions
1. **Why does an Agent need an execution loop?**
   *Answer: Because solving complex problems requires intermediate step executions. The model needs a loop so it can view the results of its previous tool usage before deciding on the next step.*
2. **Where should your tools (functions) reside? Frontend or Backend?**
   *Answer: Tools should reside on the backend. Giving the frontend direct power to execute dynamic AI-driven actions introduces severe security risks and exposes API integrations.*
3. **How do you prevent an Agent from getting stuck in an infinite loop?**
   *Answer: By strictly implementing a maximum iteration counter (e.g., max_steps = 5) and breaking the loop gracefully if the count is exceeded.*

---

### Summary
* A basic architecture glues the LLM, memory, and tools.
* The Executor Loop runs until a final answer is determined.
* It is essential to use loop limits to prevent runaway logic.

---
Prev : [10_function_calling_and_rag.md](./10_function_calling_and_rag.md) | Next : [12_tool_and_function_calling_code.md](./12_tool_and_function_calling_code.md)
