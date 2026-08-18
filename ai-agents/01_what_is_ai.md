# What is Artificial Intelligence (AI) and Its Types?

---

### What
Artificial Intelligence (AI) is the ability of a computer program or a machine to think, learn, and perform tasks that typically require human intelligence. Instead of just following strict rules, AI can recognize patterns, solve problems, and adapt to new information. 

**Types of AI:**
1. **Narrow AI (Weak AI):** AI trained for one specific task (e.g., Siri, self-driving cars, Netflix recommendations). This is what we have today.
2. **General AI (AGI):** AI that is as smart as a human across all areas. It can think, understand, and learn any intellectual task a human can. (Currently theoretical).
3. **Super AI (ASI):** AI that is far smarter than the brightest human minds in every field. (Also theoretical).

---

### Why
AI is important because it automates repetitive tasks, finds insights in massive amounts of data much faster than humans, and helps solve complex problems in medicine, finance, and engineering. It makes our apps smarter and our lives easier.

---

### How
AI works by feeding large amounts of data into complex algorithms. The algorithms look for patterns and use those patterns to make decisions or predictions. When it makes a mistake, it "learns" from it and adjusts its calculations to do better next time.

---

### Implementation

Even a simple keyword-based bot is a rudimentary form of AI (rule-based). Let's see a simple TypeScript example of a rule-based "Narrow AI" chatbot.

```typescript
// A very basic "Narrow AI" that responds to greetings
class SimpleBot {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  // The bot 'thinks' by checking the input against patterns
  respond(input: string): string {
    const lowerInput = input.toLowerCase();

    if (lowerInput.includes("hello") || lowerInput.includes("hi")) {
      return `Hello! I am ${this.name}, a simple AI.`;
    } else if (lowerInput.includes("weather")) {
      return "I don't have internet access, but I hope it's sunny!";
    } else {
      return "I only understand greetings and basic weather questions.";
    }
  }
}

// Usage
const myBot = new SimpleBot("Alpha");
console.log(myBot.respond("Hi there!")); // Output: Hello! I am Alpha, a simple AI.
```

---

### Steps
1. Identify the problem you want the AI to solve (e.g., classifying emails as spam).
2. Gather data related to the problem.
3. Choose an AI model or API (like OpenAI) suitable for the task.
4. Pass the data through the model to get a prediction or response.

---

### Integration

* **React:** You can build a chat interface and pass the user's message to an AI backend, then display the AI's response in state.
* **Next.js:** Use Server Actions or API routes securely to call external AI APIs so your secret keys don't leak.
* **Node.js backend:** Create an Express endpoint `POST /api/chat` that takes user input, communicates with Python scripts or AI APIs, and returns the AI's answer.

---

### Impact
AI has revolutionized industries. In healthcare, it detects diseases from X-rays. In finance, it detects fraud. In software, GitHub Copilot helps write code faster, saving millions of hours of developer time.

---

### Interview Questions
1. **Explain the difference between Narrow AI and General AI?** 
   *Answer: Narrow AI is designed for one specific task (like chess), while General AI has human-like intelligence across all domains.*
2. **Is ChatGPT an example of General AI?**
   *Answer: No, it is still advanced Narrow AI because it predicts text and doesn't possess true human understanding or consciousness.*
3. **What is the main requirement for an AI to learn?**
   *Answer: High-quality Data and computational power (Algorithms).*

---

### Summary
* AI makes machines simulate human intelligence.
* We currently only have Narrow AI (specialized tools).
* General and Super AI are concepts for the future.
* AI algorithms learn from data to make predictions or decisions.

---
Prev : [Start] | Next : [02_machine_learning_deep_learning.md](./02_machine_learning_deep_learning.md)
