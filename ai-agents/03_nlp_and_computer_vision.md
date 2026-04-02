# Natural Language Processing (NLP) & Computer Vision

---

### What
- **Natural Language Processing (NLP):** How computers give meaning to human language (text and speech). It allows AI to read, understand, translate, and generate text just like a human.
- **Computer Vision (CV):** How computers gain high-level understanding from digital images or videos. It gives machines "eyes" to see and understand the visual world.

---

### Why
Humans communicate mostly through words and sight. If we want AI to interact with us naturally, read our documents, or drive our cars, it absolutely needs to understand language (NLP) and see its surroundings (CV).

---

### How
- **NLP:** Turns words into numbers. It checks grammar, finds root words, figures out the sentiment (happy/sad), and guesses the next logical word.
- **Computer Vision:** Turns images into a grid of pixels (numbers). It uses Neural Networks to find borders, colors, and shapes, eventually recognizing complete objects like faces or stop signs.

---

### Implementation

You usually consume NLP/CV via APIs. Let's look at a Node.js/TypeScript example of calling a mock NLP API to do Sentiment Analysis (checking if text is positive or negative).

```typescript
// Mock API call to an NLP service
async function analyzeSentiment(text: string): Promise<string> {
    // In reality, this would be a fetch() call to OpenAI, Google NLP, etc.
    console.log(`Analyzing: "${text}"`);
    
    const positiveWords = ["happy", "great", "excellent", "love"];
    const negativeWords = ["sad", "terrible", "bad", "hate"];
    
    let score = 0;
    const words = text.toLowerCase().split(" ");
    
    words.forEach(word => {
        if (positiveWords.includes(word)) score++;
        if (negativeWords.includes(word)) score--;
    });
    
    if (score > 0) return "POSITIVE";
    if (score < 0) return "NEGATIVE";
    return "NEUTRAL";
}

// Usage
async function run() {
    const result = await analyzeSentiment("I love building AI Agents, it is great!");
    console.log(`Sentiment: ${result}`); // Output: Sentiment: POSITIVE
}
run();
```

---

### Steps
1. For NLP, start with cleaning textual data (removing punctuation, lowering case).
2. Use an NLP model (like BERT or GPT) to process text.
3. For CV, resize images to standard formats.
4. Pass the images through a Vision Model (like YOLO or ResNet) to detect objects.

---

### Integration

* **React:** Allow users to upload receipts. Display a loading spinner while processing.
* **Next.js:** Send the receipt to a Next.js API route. Use an OCR (Optical Character Recognition - a part of CV) tool to extract the text.
* **Node.js backend:** Receive the extracted text, use NLP to find the "Total Amount" and "Store Name", and save it to the database.

---

### Impact
- **NLP:** Powers Google Translate, Grammarly, chatbots, and voice assistants.
- **CV:** Powers Face ID on phones, medical tumor detection in X-rays, and security cameras that track intrusions.

---

### Interview Questions
1. **What is Sentiment Analysis?**
   *Answer: An NLP technique that identifies if a piece of text expresses a positive, negative, or neutral emotion.*
2. **How does an AI "see" an image?**
   *Answer: It sees the image as a massive matrix (grid) of numbers, where each number represents the color intensity of a specific pixel.*
3. **What is OCR?**
   *Answer: Optical Character Recognition. It's a Computer Vision task that extracts printed/handwritten text from images.*

---

### Summary
* NLP helps computers read, write, and understand human language.
* Computer Vision gives computers the ability to process and analyze visual images.
* They convert human inputs (words, images) into numeric data that Neural Networks can process.

---
Prev : [02_machine_learning_deep_learning.md](./02_machine_learning_deep_learning.md) | Next : [04_generative_ai_and_llms.md](./04_generative_ai_and_llms.md)
