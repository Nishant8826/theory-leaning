# Handling Memory and API-Based Agents

---

### What
Previously, we stored memory in a simple `memory = []` array. If the server restarted, the memory was lost.
- **Handling Real Memory:** In production, memory must be tied to a specific User or Session ID and stored in a database (like MongoDB or Redis).
- **API-Based Agents:** A system where your frontend, mobile app, or external users can interface with your powerful backend Agent via standard REST APIs (`POST /api/chat`).

---

### Why
If you build a chatbot, a user expects that if they refresh the React page, the AI will still remember what they discussed. To achieve this, the Node.js backend must pull their chat history from a database *before* sending it to the LLM. Exposing this through an API makes your agent accessible from anywhere (Web, iOS, CLI).

---

### How
1. User sends message: `{ sessionId: "123", text: "Hello" }`
2. Backend queries Database for `sessionId: "123"`. Retrieves past 10 messages.
3. Backend appends the new "Hello" message to the array.
4. Backend sends the massive array to OpenAI.
5. OpenAI replies. Backend saves the updated array to the Database.
6. Backend returns answer to frontend.

---

### Implementation

Here is a conceptual architecture using Node.js/Express and a mock Database.

```typescript
import express, { Request, Response } from 'express';

const app = express();
app.use(express.json());

// Mock Database (In reality: MongoDB, Postgres, Redis)
const Database: Record<string, { role: string, content: string }[]> = {};

// Helper: Retrieves or creates memory for a user
function getMemory(sessionId: string) {
    if (!Database[sessionId]) {
        Database[sessionId] = [{ role: "system", content: "You are a helpful assistant." }];
    }
    return Database[sessionId];
}

// Our generic LLM Call mock
async function callLLM(messages: any[]) {
    return "I am the AI response based on your history.";
}

// THE API ROUTE (POST /chat)
app.post("/chat", async (req: Request, res: Response) => {
    const { sessionId, message } = req.body;

    if (!sessionId || !message) {
        return res.status(400).send({ error: "Missing sessionId or message" });
    }

    try {
        // 1. Fetch History from DB
        let history = getMemory(sessionId);

        // 2. Add current user input to History
        history.push({ role: "user", content: message });

        // 3. Send entire history to the AI Model
        const aiResponse = await callLLM(history);

        // 4. Add AI's response to History
        history.push({ role: "assistant", content: aiResponse });

        // 5. Update Database
        Database[sessionId] = history;

        // 6. Return response to front end
        res.status(200).send({ reply: aiResponse });

    } catch (err) {
        res.status(500).send({ error: "Agent Failed" });
    }
});

// app.listen(3000, () => console.log("Agent API running on port 3000"));
```

---

### Steps
1. Create a `messages` table/collection in your Database.
2. Require a unique identifier (User ID or Session ID) from the client on every request.
3. Fetch -> Append -> Call API -> Save -> Respond.
4. **Token Management:** Implement a sliding window (e.g., only pass the last 15 messages) so your array doesn't become 10,000 tokens long and bankrupt your API limits.

---

### Integration

* **React:** Store the `sessionId` in `localStorage` when the app mounts. Send it in the body of every `fetch` request to your API.
* **Next.js:** You can use Next.js `Route Handlers` (`app/api/chat/route.ts`) to do this exactly as shown above, using a database like Vercel KV (Redis) for ultra-fast memory fetching.
* **Node.js backend:** Because fetching memory requires hitting a database, make sure your database is highly optimized for read/writes (Redis is the industry standard for fast chat memory).

---

### Impact
Persistent memory changes the dynamic from a "tool" to an "assistant". It provides a personalized experience over time. Creating an API for your Agent means you can easily integrate it into Slack, WhatsApp, or standard web apps.

---

### Interview Questions
1. **If an LLM has no memory natively, how do chat apps like ChatGPT remember the conversation after you reload the page?**
   *Answer: The application backend stores every message in a database. Upon reload or new prompt, the backend retrieves that history and sends the entire conversation block to the LLM API.*
2. **What is a "Sliding Window" memory technique?**
   *Answer: Dropping the oldest messages from the array before sending it to the API to prevent exceeding token limits and saving costs, while retaining recent context.*

---

### Summary
* Real agents require memory stored in a persistent database.
* Always query memory using a User/Session ID before calling the LLM.
* Building your agent as an API allows any frontend or platform to hook into its capabilities.

---
Prev : [12_tool_and_function_calling_code.md](./12_tool_and_function_calling_code.md) | Next : [14_integrating_react_nextjs.md](./14_integrating_react_nextjs.md)
