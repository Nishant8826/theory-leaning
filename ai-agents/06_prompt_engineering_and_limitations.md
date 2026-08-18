# Prompt Engineering and Limitations of AI

---

### What
- **Prompt Engineering:** The skill of providing clear, direct, and structured instructions (prompts) to an AI model to get the exact output you want. It's the "programming language" for LLMs.
- **Limitations of AI:** The boundaries where AI currently fails. It is not perfect; it can make up facts, forget things in long conversations, and requires huge computing power.

---

### Why
An AI model is like an incredibly smart intern on their first day. If you give them a vague instruction ("Write an article"), you'll get a vague result. If you engineer a great prompt ("Write a 300-word article about React aimed at beginners, using bullet points"), you get high-quality work instantly. Knowing its limitations ensures you don't blindly trust incorrect outputs in production environments.

---

### How
- **Role assignments:** "Act as a Senior Developer..."
- **Context:** "...We are building a Next.js application..."
- **Instructions:** "...Write a function to format dates..."
- **Formatting:** "...Output ONLY the raw code, no explanations."

---

### Implementation

Let's look at how adding context changes the AI prompt in code using TypeScript string interpolation.

```typescript
// A function that dynamically engineers a high-quality prompt
function buildPrompt(userTopic: string, targetAudience: string): string {
    // Bad Prompt: `Tell me about ${userTopic}`
    
    // Engineered Prompt:
    return `
    Role: You are an expert teacher with 20 years of experience.
    Task: Explain the given topic comprehensively.
    Audience: ${targetAudience}
    Format: Use markdown headings, bullet points, and simple language.
    Topic: ${userTopic}
    `.trim();
}

console.log(buildPrompt("TypeScript Basics", "Absolute beginners"));
```

---

### Steps
1. Give the AI a clearly defined role.
2. Provide all necessary background context.
3. Be explicitly clear about what NOT to do.
4. If testing, read the output. If it hallucinates (invents facts), refine your prompt to be stricter (e.g., "Answer ONLY using the provided text").

---

### Integration

* **React:** Store the raw user input, but before sending it to the backend, you can let the user select a "Persona" from a dropdown. 
* **Next.js:** Inside the API Route, combine the user's short input with a massive hidden System Prompt that the user never sees, governing how the AI must respond.
* **Node.js backend:** Create a template system in Node to dynamically inject variables (like user preferences from a DB) directly into the hidden system prompt.

---

### Impact
Good prompt engineering can save companies thousands of dollars in API costs. If a prompt is precise, the AI gets the answer right on the first try, reducing the need for costly follow-up questions and manual editing.

---

### Interview Questions
1. **What is Prompt Engineering?**
   *Answer: Combining context, roles, and strict formatting rules to guide an LLM to generate the exact required output.*
2. **What is an AI Hallucination?**
   *Answer: When an LLM confidently generates information that is factually incorrect or nonexistent.*
3. **What is a "System Prompt"?**
   *Answer: A background instruction given to an AI (usually invisible to the user) that defines its baseline behavior and rules for the entire conversation.*

---

### Summary
* Prompt engineering is how you extract value from LLMs.
* Better context = Better results.
* AI has critical limitations: it hallucinates, lacks real-time logic, and cannot truly reason.

---
Prev : [05_tokens_embeddings_and_vectors.md](./05_tokens_embeddings_and_vectors.md) | Next : [07_what_are_ai_agents.md](./07_what_are_ai_agents.md)
