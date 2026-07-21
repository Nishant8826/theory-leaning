# Chapter 12: Prompt Engineering Basics

**Estimated Reading Time**: 20 minutes  
**Difficulty**: Beginner  
**Prerequisites**: Chapters 1–11.  
**Learning Objectives**:
1. Structure prompts using the Role-Context-Constraint-Input pattern.
2. Implement Few-Shot Prompting to guide output styling.
3. Construct dynamic prompt templates in TypeScript.
4. Escaping user input variables using clear XML-like delimiters.

---

## Introduction

Writing prompts for a production application is different from typing queries into a web chatbot. In an application, prompts are part of the codebase. They must compile dynamic runtime variables (like user inputs or database logs) and consistently produce predictable, structured results.

**Prompt Engineering** is the practice of designing and formatting prompts to get reliable outputs from a probabilistic model.

In this chapter, we cover basic prompting patterns and build a dynamic query template builder in TypeScript.

---

## Theory: Roles, Context, and Prompt Templates

A production-grade prompt template contains four core sections:
1. **System Persona (Role)**: Instructs the model on who it is (e.g., `"You are a Senior React Developer."`).
2. **Context**: Background facts or data schemas the model needs.
3. **Constraints**: Boundaries the model must respect (e.g., `"Do NOT output introductory text, return ONLY JSON."`).
4. **User Input Variables**: Dynamic inputs injected at runtime.

### Few-Shot Prompting
If instructions alone are not enough to guide the model, you provide **Examples** (shots) of inputs and expected outputs within the prompt. This allows the model to learn the pattern and apply it to the new user input.
* **Tip**: Use 3 to 5 examples. Ensure they are diverse and use identical formatting.

---

## Real-World Analogy: Hiring a Contractor

Think of prompt engineering as **writing a contract for a specialized contractor**:
* **Bad prompt**: "Fix my sink." (Result: The contractor might use wrong parts, make a mess, or charge too much.)
* **Good prompt**:
  * **Role**: "You are a licensed plumber."
  * **Context**: "Here is the layout diagram of the pipes."
  * **Constraints**: "Do not change the main drain pipe. Keep the budget below $200. Clean up when finished."
  * **Examples**: "Here is a photo of how the pipes should look when complete (Few-Shot)."

---

## Architecture Diagram: Dynamic Prompt Compilation

This diagram shows how static templates and dynamic variables are combined inside the backend to compile the final prompt sent to the LLM.

```mermaid
graph TD
    SystemTemplate[System Template: 'You are a DBA. Schema: {{schema}}'] --> Compile[Compile Engine]
    SchemaVar[Database Schema: 'users table'] --> Compile
    
    UserTemplate[User Template: 'Write query for: {{query}}'] --> Compile
    UserVar[User input: 'June signups'] --> Compile
    
    Compile --> FinalPrompt[Final Prompt sent to LLM]
    FinalPrompt --> LLM[LLM API]
```

---

## Code Example: Few-Shot Prompt Query Builder (TypeScript)

Let's build a class `FewShotPromptBuilder` that compiles dynamic variables and formatting examples into a structured prompt.

Create `prompt_builder.ts`:

```typescript
interface FewShotExample {
  input: string;
  output: string;
}

class FewShotPromptBuilder {
  private role: string;
  private instructions: string;
  private examples: FewShotExample[] = [];

  constructor(role: string, instructions: string) {
    this.role = role;
    this.instructions = instructions;
  }

  // Add an example to the prompt
  public addExample(example: FewShotExample) {
    this.examples.push(example);
  }

  // Compile the final prompt string
  public compile(userInput: string): string {
    let prompt = `Role: ${this.role}\n`;
    prompt += `Instructions: ${this.instructions}\n\n`;
    
    prompt += "--- Examples ---\n";
    this.examples.forEach((ex, idx) => {
      prompt += `Example ${idx + 1}:\n`;
      prompt += `Input: ${ex.input}\n`;
      prompt += `Output: ${ex.output}\n\n`;
    });

    prompt += "--- Active User Request ---\n";
    prompt += `Input: ${userInput}\n`;
    prompt += "Output: ";

    return prompt;
  }
}

// Ingestion and Setup
const builder = new FewShotPromptBuilder(
  "You are a SQL query compiler.",
  "Translate natural language requests into valid SQL queries targeting a 'users' table with columns (id, name, created_at)."
);

// Add Few-Shot Examples
builder.addExample({
  input: "Show me all users registered today",
  output: "SELECT * FROM users WHERE created_at::date = CURRENT_DATE;"
});
builder.addExample({
  input: "Find user John",
  output: "SELECT * FROM users WHERE name = 'John';"
});

// Compile dynamic prompt
const compiledPrompt = builder.compile("Show me users registered in June");

console.log("--- Compiled Dynamic Few-Shot Prompt ---");
console.log(compiledPrompt);
```

Run this file:
```bash
npx tsx prompt_builder.ts
```

---

## Best Practices, Production & Security Considerations

### 1. Order Prompts Strategically
Place your instructions (roles, constraints) at the beginning or end of the prompt. Models pay the most attention to tokens at the start and end of context windows (Primacy/Recency effects), while tokens in the middle can be ignored.

---

## Common Mistakes

1. **Using vague adjectives**: Saying "Be quick" or "Write a short summary" instead of specifying measurable constraints ("Keep the response below 3 sentences" or "Output exactly 50 words").

---

## Exercises & Mini Project

### Exercise 1: Delimiter Escape
Write a helper function that escapes HTML/XML tags in user input strings before they are injected into templates to prevent system instruction breakout.

### Mini Project: Few-Shot Sentiment API
Use your prompt builder class to create an API prompt template for a sentiment analyzer. Add three few-shot examples (positive, negative, neutral) and build a test query.

---

## Interview Questions

1. **Q**: What is Few-Shot Prompting, and when is it preferred over Zero-Shot Prompting?
   * **A**: Few-shot prompting provides input-output examples within the prompt context before user input. It is preferred over zero-shot prompting (instructions only) when the task involves complex formatting rules, tone mimicry, or custom translation formats that are hard to describe in abstract rules.
2. **Q**: Why should user inputs be wrapped in delimiters inside prompts?
   * **A**: Wrapping inputs in delimiters (e.g. `<user_input>text</user_input>`) clearly separates untrusted user text from system instructions, preventing prompt injection attacks where the model treats user text as new instructions.

---

## Navigation

**Prev:** [Chapter 11: Multimodal Models](./11_Multimodal_Models.md) | **Index:** [Course Overview](./00_Index.md) | **Next:** [Chapter 13: Prompt Engineering Advanced](./13_Prompt_Engineering_Advanced.md)
