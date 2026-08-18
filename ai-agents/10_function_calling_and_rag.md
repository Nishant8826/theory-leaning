# Function Calling and Retrieval-Augmented Generation (RAG)

---

### What
- **Function Calling:** A special feature inside modern LLMs designed specifically to trigger Tools. You describe your code's functions to the AI, and the AI will output perfectly formatted JSON telling your code to run that function.
- **RAG (Retrieval-Augmented Generation):** Giving the AI a massive external library (a Vector Database) so it can search for facts before answering. It stops the AI from hallucinating because it uses facts provided by you.

---

### Why
- **Function Calling:** Standard text outputs from an LLM are messy. Extracting data from them using Regex is a nightmare. Function Calling guarantees the AI provides structural JSON data so your Node app doesn't crash.
- **RAG:** You cannot train an LLM on your company's private wiki—it's too expensive and insecure. RAG lets you "inject" your private company documents into the conversation right before the LLM answers.

---

### How

**How RAG Works:**
1. A user asks: "What is our company's refund policy?"
2. **Retrieval:** Your Node app converts that question into an embedding and searches the Vector DB for similar documents.
3. It finds a document titled "Internal_refunds.pdf" and extracts the text.
4. **Augmented Generation:** Your app sends a prompt to the LLM: 
    * "Answer the user based ONLY on this text. [paste PDF text here]. User: What is the refund policy?"
5. The LLM answers flawlessly using your company data!

---

### Implementation

RAG relies heavily on Vector Databases. A Vector DB stores those mathematical Arrays (Embeddings) we discussed earlier.

```typescript
// Concept of how a RAG pipeline looks in code
async function queryRAG(userQuestion: string) {
    // 1. Turn the user's question into math
    const questionVector = await getEmbedding(userQuestion);

    // 2. Retrieve the top 3 closest documents from the Vector Database
    // (Imagine this searches thousands of company PDF files instantly)
    const contextDocuments = await mockVectorDatabaseSearch(questionVector);

    // 3. Augment the Prompt. Inject the documents directly in to the text!
    const prompt = `
      You are an assistant. Answer the user's question using ONLY the following context.
      --- Context ---
      ${contextDocuments.join("\n")}
      ---------------
      Question: ${userQuestion}
    `;

    // 4. Generate Answer
    const finalAnswer = await mockCallLLM(prompt);
    console.log(finalAnswer);
}

// Helpers
async function getEmbedding(text: string) { return [0.1, 0.4]; }
async function mockVectorDatabaseSearch(vector: number[]) { 
    return ["Fact 1: Refunds take 5-7 business days."]; 
}
async function mockCallLLM(prompt: string) { 
    return "Based on your company documents, refunds take 5-7 business days."; 
}

queryRAG("How long do refunds take?");
```

---

### Steps (To build a RAG System)
1. Chop your large PDF/Docs into small text chunks.
2. Turn each chunk into Vectors.
3. Save them in a Vector DB (like Pinecone, Weaviate, or pgvector).
4. When a user asks a question, turn their question into a Vector.
5. Search the DB for closest chunks, grab the text, inject into prompt, and call LLM.

---

### Integration

* **React:** Just provide the search box. The user has no idea RAG is occurring.
* **Next.js / Node.js backend:** The massive pipeline logic happens here. Your backend must connect to the Vector Database API, query it, format the string, and orchestrate the LLM call.

---

### Impact
RAG is currently the most widely built AI application in the enterprise software world. It allows chatbots to safely and accurately summarize gigantic internal datasets (legal documents, codebases, wikis) without leaking data to the public. Function calling ensures that if the user wants to trigger a workflow based on those documents, the system outputs safe JSON to trigger the API.

---

### Interview Questions
1. **What Problem does RAG solve?**
   *Answer: It solves model hallucinations and the inability to access private, up-to-date data, without requiring the expensive process of retraining a model.*
2. **What role does a Vector Database play in RAG?**
   *Answer: It stores document embeddings allowing for extremely fast semantic similarity search based on the user's query.*
3. **Why use Function Calling instead of just telling the AI to return text?**
   *Answer: Function Calling strictly enforces a JSON schema output. This guarantees your backend code can safely parse the response (`JSON.parse()`) and execute internal functions without runtime errors.*

---

### Summary
* Function calling converts LLM reasoning into actionable JSON for your code.
* RAG retrieves private facts from a Vector DB and injects them into the prompt.
* Together, they create highly accurate, capable enterprise tools.

---
Prev : [09_tools_memory_and_planning.md](./09_tools_memory_and_planning.md) | Next : [11_building_basic_agent.md](./11_building_basic_agent.md)
