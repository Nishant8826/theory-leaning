# Integrating Agents in React & Next.js

---

### What
Connecting your backend AI logic to a frontend interface. 
- **React:** Handling state, loading spinners, and chat UI.
- **Next.js:** Utilizing modern server-side architecture (Server Actions, Server-Sent Events, Streaming) to handle slow AI operations gracefully.

---

### Why
An AI Agent is useless if users can't interact with it. Because Agents involve Think/Act loops, their response times can range from 2 seconds to 2 minutes! Standard `fetch()` calls might time out. You need a robust UI to assure the user the AI is "working on it".

---

### How
1. Use standard form submissions to gather user text.
2. Show an optimistic UI updates ("User: Check my emails").
3. Show a skeleton loader or a "Thinking..." animation.
4. Ideally, stream the text chunks back to React so the user reads as the AI generates (like ChatGPT).

---

### Implementation

A basic React component integrating with our Node.js AI API.

```tsx
import React, { useState } from 'react';

// Basic React Chat Interface
export default function AgentChat() {
  const [messages, setMessages] = useState<{role: string, text: string}[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // 1. Optimistic UI update
    const newMessages = [...messages, { role: 'user', text: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      // 2. Call the Agent API
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: "user-1", message: input }),
      });
      
      const data = await res.json();
      
      // 3. Update UI with Agent response
      setMessages([...newMessages, { role: 'agent', text: data.reply }]);
    } catch (error) {
      setMessages([...newMessages, { role: 'agent', text: "Error connecting to Agent." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto' }}>
      <div className="chat-window" style={{ height: '300px', overflowY: 'scroll', border: '1px solid gray' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.role === 'user' ? 'right' : 'left', padding: '10px' }}>
            <strong>{msg.role}: </strong> {msg.text}
          </div>
        ))}
        {isLoading && <div style={{ color: 'gray' }}>Agent is thinking and using tools...</div>}
      </div>

      <form onSubmit={sendMessage} style={{ marginTop: '10px' }}>
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Ask the agent..." 
        />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
}
```

---

### Steps
1. Create state for `messages`, `input`, and `isLoading`.
2. Map over the `messages` array to render the UI.
3. On submit, append the user message, clear input, set loading to true.
4. Await the fetch request to your Next.js/Node API.
5. Append the AI's response and remove the loading state.

---

### Integration

* **React:** The above code is perfect for Vite/React applications.
* **Next.js:** In Next.js App Router, instead of a standard `fetch`, you should use the `@vercel/ai` SDK (`useChat` hook). It automatically handles the React State, the streaming logic, and the backend route connection in about 5 lines of code.

---

### Impact
A clean integration ensures users aren't frustrated by agent delays. While an agent is looping through 5 different tools behind the scenes, dynamic UI indicators keep the user engaged.

---

### Interview Questions
1. **Why is streaming preferred in AI Chat interfaces over standard Request/Response architecture?**
   *Answer: Because AI models generate text token-by-token. Streaming allows the user to read the beginning of the sentence immediately, reducing perceived latency, rather than waiting 10 seconds for the entire block to finish generating.*
2. **How does the `@vercel/ai` SDK improve React integrations?**
   *Answer: It abstracts all the complex state management (messages array, loading state, streaming chunk concatenation) into a single clean `useChat()` hook.*

---

### Summary
* Treat AI calls like any async data fetching in React, but expect longer delays.
* Use `isLoading` effectively to explain the agent is executing tools.
* Next.js provides incredible libraries to make streaming UI trivial.

---
Prev : [13_memory_and_api_agents.md](./13_memory_and_api_agents.md) | Next : [15_integrating_nodejs_backend.md](./15_integrating_nodejs_backend.md)
