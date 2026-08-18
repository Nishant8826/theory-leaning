# What Are AI Agents? (AI Models vs AI Agents)

---

### What
- **AI Models:** An AI model (like ChatGPT) is a brain in a jar. You ask it a question, it replies. It cannot *do* anything. It cannot browse your emails, it cannot execute code, it rests silently until invoked.
- **AI Agents:** An AI Agent is a brain given hands, a memory, and a to-do list. An agent takes an overall goal, uses an AI model to break that goal into steps, and uses **Tools** to execute those steps autonomously in the real world.

---

### Why
Models are great for writing emails or answering questions, but terrible for getting real work done. If you say to a Model: "Book me a flight", it says "I can't do that." If you say to an Agent: "Book me a flight", the Agent will browse Expedia, check your calendar, enter your credit card details, and give you the receipt. Agents move AI from "Chatbots" to "Digital Employees."

---

### How
An Agent operates in a loop:
1. **Understand Goal:** Receives prompt.
2. **Think/Plan:** Uses LLM reasoning to decide the next step.
3. **Action:** Uses a tool (e.g., executing an API request).
4. **Observe:** Looks at the result of the tool.
5. **Repeat:** Keeps thinking and acting until the goal is met.

---

### Implementation

Think of the difference structurally in code. 

```typescript
// AI MODEL - Simply returns text
async function runModel(prompt: string) {
    return "You want the weather? I'm sorry, I don't have internet access.";
}

// AI AGENT - Uses the model, but executes tools dynamically
class WeatherAgent {
    async executeGoal(goal: string) {
        console.log(`Agent Goal: ${goal}`);
        
        // 1. The LLM 'Thinks' and realizes it needs weather for New York
        const locationToSearch = "New York"; 
        
        // 2. The Agent uses a TOOL (Internet API)
        const currentTemp = await this.getWeatherTool(locationToSearch);
        
        // 3. The Agent analyzes the tool output and gives the final answer
        console.log(`Final Result: It is currently ${currentTemp} degrees in ${locationToSearch}.`);
    }

    // A Tool the Agent has access to
    async getWeatherTool(location: string): Promise<number> {
        // Imaginary API call 
        return 72; 
    }
}

const myAgent = new WeatherAgent();
myAgent.executeGoal("Tell me the weather in New York!");
```

---

### Steps
1. Define the overall goal you want to achieve.
2. Provide the LLM with a hidden list of tools it is allowed to use.
3. Let the LLM output a "plan" indicating which tool to use first.
4. Your code reads the plan, runs the tool, and feeds the result *back* to the LLM so it can keep going.

---

### Integration

* **React:** Your user types "Create a landing page." React shows a generic loading state while the backend works, eventually rendering the generated code.
* **Next.js:** This loop can take minutes. Next.js server actions might time out. You often need to use WebSockets or background jobs to report intermediate Agent progress to the frontend.
* **Node.js backend:** This is where the Agent loop lives. Frameworks like LangChain or AutoGen in Node manage the Think -> Action -> Observe loop automatically.

---

### Impact
Agents are the future of software. Instead of clicking 15 buttons to configure a server, you will just ask your "DevOps Agent" to do it. Instead of reading docs to calculate taxes, an "Accounting Agent" will retrieve your Quickbooks data and file them autonomously. 

---

### Interview Questions
1. **Explain the fundamental difference between an AI Model and an AI Agent.**
   *Answer: A model provides information based on fixed training data. An agent uses a model as its brain to autonomously decide which tools to execute to achieve a real-world goal.*
2. **What happens if an Agent's tool fails during execution?**
   *Answer: Because agents operate in an observe-and-react loop, the error is fed back into the LLM. The LLM understands the error and attempts a different tool or alternative strategy to fix it.*
3. **Why do Agents take longer to respond than Chatbots?**
   *Answer: Agents often do multiple iterations (Think, Act, Observe, Think, Act, Observe) behind the scenes before resolving the final answer for the user.*

---

### Summary
* Models = Brain (Text in -> Text out).
* Agents = Brain + Hands (Text in -> Actions -> Actions -> Final Result).
* Agents work autonomously in loops until the goal is achieved.

---
Prev : [06_prompt_engineering_and_limitations.md](./06_prompt_engineering_and_limitations.md) | Next : [08_agent_types_and_lifecycle.md](./08_agent_types_and_lifecycle.md)
