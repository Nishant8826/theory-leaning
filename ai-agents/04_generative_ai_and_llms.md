# Generative AI & Large Language Models (LLMs)

---

### What
- **Generative AI:** A type of AI that can create completely *new* content—like text, images, music, or code—instead of just analyzing existing data.
- **Large Language Models (LLMs):** Massive AI models (like ChatGPT, Claude, Gemini) specifically designed to understand and generate human-like text. They are a subset of Generative AI. 

---

### Why
Before Generative AI, AI was mostly used to classify things (e.g., "Is this a spam email?"). Generative AI allows machines to be creative helpers. LLMs allow us to talk to computers using plain English instead of coding languages.

---

### How
LLMs "read" billions of pages on the internet. By doing this, they build a massive statistical map of how humans use language. When you ask a question, the LLM doesn't "think" like a human; instead, it purely calculates the **most probable next word** over and over again until the sentence is complete. 

---

### Implementation

Using an LLM in code usually involves hitting an API provided by companies like OpenAI (creators of LLMs).

```typescript
// Simulating an LLM API Request in Node.js
interface LLMRequest {
  prompt: string;
  temperature: number; // How creative the model should be
}

async function callLLM(request: LLMRequest): Promise<string> {
  console.log(`Sending to LLM API (Temp: ${request.temperature}): "${request.prompt}"`);
  
  // Simulated network delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Fake response
  return "I am an AI generated response based on probability!";
}

// Usage
async function app() {
  const answer = await callLLM({
    prompt: "Write a poem about coding.",
    temperature: 0.7 // 0.0 is very strict, 1.0 is very creative
  });
  console.log("LLM:", answer);
}
app();
```

---

### Steps
1. Sign up for an API key from an LLM provider (OpenAI, Anthropic).
2. Securely store your API key in a `.env` file.
3. Send a prompt (text) from your server to the API.
4. Wait for the response and stream it back to the user.

---

### Integration

* **React:** Build a UI with a "Chat" interface. Use modern React hooks to handle the streaming response (so words appear one by one, like ChatGPT).
* **Next.js:** Next.js API Routes are perfect for hiding your LLM API keys. You can use the Vercel AI SDK to easily handle LLM text streaming.
* **Node.js backend:** Use Node.js to receive user input, add context from your database to the prompt, and then forward it to the LLM.

---

### Impact
LLMs have fundamentally changed how we work. Instead of googling and reading 10 articles, LLMs instantly synthesize the exact answer. They generate boilerplate code for developers, write marketing emails, and power customer support bots.

---

### Interview Questions
1. **Explain what an LLM does at its core.**
   *Answer: At its core, an LLM predicts the next most probable word (or token) in a sequence based on the context of the words before it.*
2. **What does the 'temperature' setting do in an LLM?**
   *Answer: It controls the randomness. Low temperature (0) makes the output predictable and focused. High temperature (1) makes it more random and creative.*
3. **What is a "hallucination" in Generative AI?**
   *Answer: When an AI confidently generates false, incorrect, or nonsensical information because it is simply predicting words without true logical grounding.*

---

### Summary
* Generative AI creates new content from scratch.
* LLMs are Generative AI specifically for text.
* They work by mathematically guessing the next word.

---
Prev : [03_nlp_and_computer_vision.md](./03_nlp_and_computer_vision.md) | Next : [05_tokens_embeddings_and_vectors.md](./05_tokens_embeddings_and_vectors.md)
