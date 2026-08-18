# Tokens, Embeddings, and Vectors

---

### What
- **Tokens:** AI doesn't read words; it reads tokens. A token can be a whole word, a syllable, or just a single letter. (e.g., "Hamburger" might become "Ham", "bur", "ger").
- **Vectors:** These are lists of numbers in mathematics. In AI, they represent features or meanings.
- **Embeddings:** This is the process of translating a token (word) into a powerful vector (a list of hundreds of numbers). This list captures the *actual meaning* of the word.

---

### Why
Computers only understand math. If we want an AI to know that "Dog" and "Puppy" mean similar things, we can't just use text. Embeddings turn words into coordinates in a massive mathematical space. In this space, the coordinate for "Dog" is mathematically very close to the coordinate for "Puppy"!

---

### How
1. You pass the word "Apple" to an Embedding Model.
2. The model outputs a huge array of numbers (the vector), like `[0.12, -0.44, 0.89, ...]`.
3. You pass the word "Banana" to the model, getting `[0.11, -0.42, 0.88, ...]`.
4. Because the numbers are incredibly similar, the AI understands that both are related (fruits).

---

### Implementation

You can think of calculating semantic similarity by comparing two arrays of numbers.

```typescript
// A highly simplified concept of comparing Vectors
type Vector = number[];

// Fake embeddings representing words
const vectorDog: Vector   = [0.9, 0.8, 0.1]; // Pet, Furry, Machinery
const vectorPuppy: Vector = [0.9, 0.9, 0.1]; // Pet, Furry, Machinery
const vectorCar: Vector   = [0.1, 0.0, 0.9]; // Pet, Furry, Machinery

// Simple function to see how close two vectors are (using fake math)
function getDifference(v1: Vector, v2: Vector): number {
  let diff = 0;
  for (let i = 0; i < v1.length; i++) {
    diff += Math.abs(v1[i] - v2[i]);
  }
  return diff;
}

console.log("Dog vs Puppy diff:", getDifference(vectorDog, vectorPuppy)); // Very low difference (0.1) -> Similar!
console.log("Dog vs Car diff:", getDifference(vectorDog, vectorCar));     // High difference (2.4) -> Not similar!
```

---

### Steps
1. Count tokens accurately, because LLM APIs charge you **per token**, not per word (100 tokens ~= 75 words).
2. Take user text and convert it to embeddings using an Embedding API (like OpenAI's `text-embedding-3-small`).
3. Store these vectors in a Vector Database.
4. When searching for context, compare the math vectors to find the most "meaning-related" matches.

---

### Integration

* **React:** Do not handle tokens or embeddings directly on the frontend. The math is too heavy, and exposing API keys is a risk.
* **Next.js:** Write an API route `/api/embed`. Send text from the frontend here, get the embedding vector from OpenAI, and return it.
* **Node.js backend:** Use a library like `tiktoken` to count how many tokens a users string has before sending it to the LLM, ensuring they don't surpass rate limits.

---

### Impact
Embeddings revolutionized search engines. Instead of searching for exact keyword matches (which fails if the user makes a typo or uses a synonym), systems now search for "meaning". Connecting embeddings to LLMs is the foundation of powerful AI features.

---

### Interview Questions
1. **What is a Token in the context of LLMs?**
   *Answer: A token is the fundamental unit of data an LLM processes. It's often a piece of a word. Roughly, 1 token is 4 characters in English.*
2. **What is an Embedding?**
   *Answer: An embedding converting text into a high-dimensional vector (array of numbers) that captures the semantic meaning of that text.*
3. **How does an AI know that "King" minus "Man" plus "Woman" equals "Queen"?**
   *Answer: Because of Vectors! Words are placed in geometric space. Moving backwards on the "gender" vector from King and moving forwards results directly pointing at the mathematical location for Queen.*

---

### Summary
* Tokens are chunks of words (AI's alphabet).
* Vectors are lists of numbers mapping out coordinates.
* Embeddings convert text to Vectors to capture absolute meaning, ignoring exact spelling.

---
Prev : [04_generative_ai_and_llms.md](./04_generative_ai_and_llms.md) | Next : [06_prompt_engineering_and_limitations.md](./06_prompt_engineering_and_limitations.md)
