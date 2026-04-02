# Real Tool & Function Calling Implementation

---

### What
In the previous file, we used a hacky method (`ACTION: getWeather`) to call tools. Real Function Calling uses the official APIs provided by OpenAI, Anthropic, or Gemini. You send a strict JSON Schema describing your functions, and the LLM guarantees it will reply with a beautifully structured JSON object representing the function parameters.

---

### Why
Using Regex to parse `ACTION: toolName` is fragile. If the AI replies `ACTION getWeather in London` (missing a colon), your app crashes. Using official Function Calling ensures rigid, reliable, and type-safe integration between the AI and your backend code.

---

### How
When calling the OpenAI API, you pass an array called `tools`. Each tool has a `name`, a `description`, and a `parameters` object (JSON Schema) that defines what inputs the tool expects.

---

### Implementation

This is how a real Function Calling payload looks in TypeScript using the OpenAI standard.

```typescript
// 1. We define our actual code function
function fetchStockPrice(ticker: string) {
    if(ticker === "AAPL") return "$150.00";
    return "Unknown";
}

// 2. We define the Schema that tells the AI HOW to use our function
const toolDefinitions = [
    {
        type: "function",
        function: {
            name: "get_stock_price",
            description: "Get the current stock price of a given company ticker symbol.",
            parameters: {
                type: "object",
                properties: {
                    ticker: {
                        type: "string",
                        description: "The stock ticker symbol, e.g. AAPL for Apple"
                    }
                },
                required: ["ticker"]
            }
        }
    }
];

// Mocking OpenAI's response when we pass the above toolDefinitions
async function generateAIResponse() {
    // The AI recognized it should use the tool based on the user asking "Apple stock"
    // OpenAI responds with a specific 'tool_calls' object, NOT standard text.
    return {
        tool_calls: [
            {
                function: {
                    name: "get_stock_price",
                    // Notice how it intelligently figured out the ticker is AAPL
                    arguments: '{"ticker": "AAPL"}' 
                }
            }
        ]
    };
}

async function app() {
    console.log("User: What is the price of Apple stock?");
    
    // Simulate API Call
    const response = await generateAIResponse();

    // 3. Our backend parses the AI's structured request
    if (response.tool_calls) {
        const toolCall = response.tool_calls[0].function;
        console.log(`\nAI wants to run: ${toolCall.name}`);
        
        // Parse the secure JSON
        const args = JSON.parse(toolCall.arguments);
        console.log(`With arguments: ${args.ticker}`);

        // 4. Execute the actual function
        if (toolCall.name === "get_stock_price") {
            const result = fetchStockPrice(args.ticker);
            console.log(`\nExecution Result: The price is ${result}`);
            // (You would then send this result BACK to the AI to form a human sentence)
        }
    }
}

app();
```

---

### Steps
1. Write standard TypeScript/Node functions for your tools.
2. Construct a strict JSON Schema detailing exactly what arguments your function requires.
3. Pass both the User's Message and the `tools` array to the LLM API.
4. Check if the LLM response contains `tool_calls`.
5. Run the requested function, append the result to the messages array, and send it back to the LLM.

---

### Integration

* **React:** Just send standard text. Function calling should exclusively be a backend concern.
* **Next.js:** The Vercel AI SDK has incredible built-in support for `tool` properties, automatically mapping and executing your Next.js server-side functions when the LLM requests them.
* **Node.js backend:** You can use a library like `Zod` to define your schemas in TypeScript. OpenAI actually supports passing Zod schemas to guarantee type safety!

---

### Impact
Structured Function Calling bridges the gap between conversational AI and traditional software engineering. It allows AI to safely manipulate databases, send emails, or update user profiles without the risk of parsing errors.

---

### Interview Questions
1. **What is a JSON Schema in the context of AI tools?**
   *Answer: It is a structured format that describes exactly what parameters a function expects (e.g., string, number, required fields), so the AI knows how to construct its request.*
2. **Why is native Function Calling better than asking the AI to return a specific string?**
   *Answer: Because native Function Calling is trained directly into the model's architecture, heavily reducing hallucinations and guaranteeing parsable, structured JSON outputs.*

---

### Summary
* Real function calling relies on strict JSON schemas.
* The API returns a special `tool_calls` object instead of a text message.
* You execute the tool on your server, not the client.

---
Prev : [11_building_basic_agent.md](./11_building_basic_agent.md) | Next : [13_memory_and_api_agents.md](./13_memory_and_api_agents.md)
