# 🤖 Tokenization and Context Windows

## 📌 Overview

Computers and Neural Networks cannot directly process human words, letters, or sentences; they operate exclusively on numbers and linear algebra operations (matrices and vectors).

To bridge this gap, Large Language Models (LLMs) rely on a critical preprocessing layer called the **Tokenizer**. 

* **Tokenizer**: A specialized software program that converts raw human text into a sequence of numerical identifiers called **TokenIDs** (Encoding), and translates numerical TokenIDs back into human-readable text (Decoding).
* **Token**: The fundamental atomic unit of text processed by an LLM. A token is not necessarily a full word—it can be a single character, a subword fragment (e.g., `"un"`, `"trust"`, `"able"`), or a punctuation mark.
* **Context Window**: The maximum working memory capacity of an LLM, defined as the total number of tokens (Input Prompt + Chat History + Retrieved Documents + Generated Output) that a model can process in a single inference request.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│   Human Text    │ ──►   │    Tokenizer    │ ──►   │  Token ID List  │ ──►   │ Transformer LLM  │
│ "Untrustable"   │       │   (Encoder)     │       │ [500, 600, 700] │       │ (Weights Matrix) │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └──────────────────┘
```

---

## 🎯 Why This Matters

Understanding tokenization and context windows is essential for AI software engineering:
* **Cost & Billing**: Cloud LLM providers (OpenAI, Anthropic, Google) charge API usage strictly per **1,000 or 1,000,000 Tokens**, not per character or per word.
* **Multilingual Cost Bias**: Legacy tokenizers trained primarily on English data break non-English languages (e.g., Hindi, Arabic, Japanese) into significantly more tokens per word (**High Token Fertility**), making API calls more expensive and shrinking effective context memory for non-English users.
* **Context Management**: Exceeding a model's **Context Length** causes request crashes, input truncation, or conversational memory loss.
* **Performance & Prompt Quality**: Passing overly long context introduces the **"Lost in the Middle"** degradation effect, where the model misses critical information buried in central positions of a prompt.
* **Security**: System prompts, safety boundaries, and tool calls rely on **Special Tokens** (e.g., `<|im_start|>`, `<|im_end|>`). Flaws in handling these tokens can open apps to Prompt Injection attacks.

---

## 🧠 Prerequisites

| Concept | Explanation |
| :--- | :--- |
| **Vocabulary (Vocab)** | The master dictionary of all distinct subword pieces and special symbols recognized by a specific tokenizer (typically 30,000 to 100,000+ tokens). |
| **TokenID** | The unique numerical integer index assigned to each token in the vocabulary. |
| **Embedding Layer** | The first neural network layer that maps integer TokenIDs into high-dimensional dense floating-point vectors (e.g., a vector of 4,096 numbers representing semantic meaning). |
| **Encoding / Decoding** | **Encoding**: Text $\rightarrow$ TokenIDs. **Decoding**: TokenIDs $\rightarrow$ Text. |

---

## 🔍 Deep Dive: Tokenization Mechanics & Context Limits

---

### Part 1: The Translation Problem (Words vs Characters vs Subwords)

Why don't LLMs just tokenize full words or individual characters?

```
                               Text: "Untrustable"
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  Word Tokenization   │    │ Character Tokenization│   │ Subword Tokenization │
│   ["Untrustable"]    │    │["U","n","t",...]     │    │["Un","trust","able"] │
└──────────┬───────────┘    └──────────┬───────────┘    └──────────┬───────────┘
           │                           │                           │
  - Huge Vocab (>1M+)         - Tiny Vocab (~100)         - Optimal Vocab (32k-100k)
  - Out of Vocabulary (OOV)   - Long Sequences            - Efficient balance
  - Cannot handle typos       - Loss of word semantics    - Handles rare words & typos
```

1. **Word-Level Tokenization**:
   * *How it works*: Maps every unique word in a dictionary to an ID (e.g., `"apple"` $\rightarrow$ `101`, `"banana"` $\rightarrow$ `102`).
   * *The Problem*: Human languages contain millions of words, inflections, slang, and typos. The vocabulary size becomes massive ($>1,000,000+$ entries), requiring huge memory matrices. Any unseen word causes an **Out-of-Vocabulary (OOV)** crash.
2. **Character-Level Tokenization**:
   * *How it works*: Maps each single letter to an ID (e.g., `"U"` $\rightarrow$ `21`, `"n"` $\rightarrow$ `55`).
   * *The Problem*: Vocabulary is small ($\approx 100-250$ characters), but sequence lengths explode! A 500-word essay becomes 3,000+ characters, exhausting attention computation ($O(N^2)$ complexity) and destroying semantic groupings.
3. **Subword Tokenization (The Standard)**:
   * *How it works*: Commonly used words remain single tokens (`"This"`, `"boy"`), while rare, complex, or compound words are broken into reusable subword fragments (`"Un"` + `"trust"` + `"able"`).
   * *The Benefit*: Achieves an optimal trade-off: manageable vocabulary sizes ($32,000-100,000$ tokens), short sequence lengths, and **zero Out-of-Vocabulary errors** (unseen words are safely split into smaller known sub-units).

---

### Part 2: Tokenization Algorithms (BPE, WordPiece, Unigram)

Modern tokenizers construct their vocabulary automatically from large text corpora using statistical algorithms:

```
                          SUBWORD TOKENIZATION ALGORITHMS
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ Byte Pair Encoding   │     │      WordPiece       │     │       Unigram        │
│        (BPE)         │     │                      │     │                      │
│ - Bottom-up merge    │     │ - Likelihood merge   │     │ - Top-down prune     │
│ - Used by OpenAI,    │     │ - Used by BERT       │     │ - Used by Sentence   │
│   LLaMA, Mistral     │     │                      │     │   Piece, T5          │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

#### 1. Byte Pair Encoding (BPE)
Used by OpenAI (GPT-2, GPT-3.5, GPT-4), LLaMA, and Mistral.
* **Mechanism**: Starts with individual characters as the base vocabulary. It iteratively counts all adjacent pairs of symbols in the training corpus and merges the most **frequently occurring pair** into a new single token.
* **Example**:
  * Step 1: Base characters: `L`, `o`, `w`, `e`, `r`, `s`, `t`
  * Step 2: Frequently pair `"e"` + `"r"` $\rightarrow$ Merge into token `"er"`
  * Step 3: Frequently pair `"e"` + `"s"` + `"t"` $\rightarrow$ Merge into token `"est"`
  * Tokenized Results:
    * `"Low"` $\rightarrow$ `["Low"]` (Token ID: `15`)
    * `"Lower"` $\rightarrow$ `["Low", "er"]` (Token IDs: `[15, 35]`)
    * `"Lowest"` $\rightarrow$ `["Low", "est"]` (Token IDs: `[15, 20]`)

#### 2. WordPiece
Used by Google's BERT and RoBERTa.
* **Mechanism**: Similar to BPE by merging subword pairs bottom-up, but instead of choosing the most frequent pair, it merges the pair that **maximizes the probability/likelihood** of the training data when added to the vocabulary.

#### 3. Unigram
Used by SentencePiece, T5, and ALBERT.
* **Mechanism**: The exact opposite of BPE. It starts with a massive candidate set of all possible subwords and substrings, evaluates the loss impact of removing each token, and iteratively **prunes less useful pieces** until reaching the target vocabulary size.

---

### Part 3: Tokenization Quirks, Multilingual Bias, & Special Tokens

Tokenization behavior creates surprising edge cases that every AI engineer must know:

#### 1. Multilingual Bias & Token Fertility Ratio
* **Token Fertility Ratio**: $\frac{\text{Total Number of Tokens}}{\text{Total Number of Words}}$

Because legacy LLMs were pre-trained on datasets composed of $>85\%$ English text, the tokenizer's vocabulary is optimized for English root words.

```text
English Sentence:
"I cannot help you with that"
Tokens: ["I", " cannot", " help", " you", " with", " that"]
Total: 6 Words ──► 6 Tokens (Fertility: 1.0)

Hindi Translation:
"मैं आपकी मदद नहीं कर सकता"
Tokens: ["मैं", " आप", "की", " मद", "द", " नहीं", " कर", " सक", "ता"]
Total: 6 Words ──► 12+ Tokens (Fertility: 2.0+)
```

* **Production Impact**: A non-English prompt consumes **2x to 4x more tokens** for the exact same semantic content, leading to higher API costs and consuming context memory up to 4x faster!

#### 2. Whitespace, Capitalization, & Code
* **Capitalization**: `"Apple"` (Capitalized) and `"apple"` (lowercase) are stored as **two completely distinct TokenIDs** in most BPE vocabularies.
* **Whitespace**: Leading spaces are attached directly to tokens (e.g., `" is"` is tokenized differently than `"is"`).
* **Code Syntax**: Dense code snippets like `if(true) return "sd"; else "sdc"` contain unusual symbol juxtapositions, producing higher token counts per line than plain English prose.
* **Emojis**: Emojis are complex multi-byte Unicode sequences. A simple emoji might be 1 token, while a complex emoji with skin-tone modifiers (e.g., 🙋🏽‍♂️) can split into 3 to 7 tokens!

#### 3. Special Tokens (Control Tokens)
Tokenizers reserve unique, non-printable control tokens used by the model architecture to delineate structure:

```text
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
Hello!<|im_end|>
<|im_start|>assistant
```

* `<|im_start|>` / `<|im_end|>`: Delineate conversational roles (System, User, Assistant).
* `<|endoftext|>` / `<eos>`: Signal the end of generation.
* `<|tool_call|>` / `<|tool_response|>`: Structure agentic tool executions.

---

### Part 4: Context Window vs. Context Length

Developers often use these terms interchangeably, but they represent distinct concepts:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CONTEXT LENGTH (Hardware Limit)                       │
│  The absolute maximum ceiling of tokens the architecture can process.        │
│  Example: GPT-4o (128,000 Tokens) | Claude 3.5 Sonnet (200,000 Tokens)        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CONTEXT WINDOW (Active Payload)                       │
│  The total count of tokens currently populated in a specific API request.   │
│                                                                             │
│  ┌─────────────────┬──────────────────┬─────────────────┬────────────────┐  │
│  │ System Prompt   │ Chat History     │ Retrieved RAG   │ Generated      │  │
│  │ (500 Tokens)    │ (2,500 Tokens)   │ Docs (4,000)    │ Output (1,000) │  │
│  └─────────────────┴──────────────────┴─────────────────┴────────────────┘  │
│  Total Active Context Window = 8,000 Tokens / 128,000 Ceiling               │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Context Length**: The architectural limit imposed by positional embeddings and GPU memory capacity (e.g., 8k, 32k, 128k, 1M, or 2M tokens).
* **Context Window**: The shared working space of active tokens sent in a single inference call. **The input prompt and generated output share the exact same context window ceiling!**

---

### Part 5: Context Overflow Strategies (When Context Window Fills)

When conversational history or document retrieval exceeds the maximum Context Length, the system will crash unless managed. Production applications implement specific overflow strategies:

```
                             Context Overflow Detected
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│   Sliding Window     │     │ Context Summarization│     │   RAG Filtering      │
│  (FIFO Pruning)      │     │  (LLM Compression)   │     │(Selective Vector Search)│
│ Drops oldest chat    │     │ Summarizes older     │     │ Only retrieves top-K │
│ messages iteratively │     │ history into 1 block │     │ relevant chunks      │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

1. **Request Rejection / Error**: Returning a `400 Bad Request` (`context_length_exceeded`).
2. **Input Truncation**: Hard-cutting text from the beginning or end of the input string.
3. **Sliding Window (FIFO Pruning)**: Automatically deleting the oldest user/assistant message pairs from chat history while preserving the System Prompt.
4. **Context Summarization**: Periodically triggering a background LLM call to compress past dialogue into a concise bulleted summary paragraph.
5. **RAG Selective Retrieval**: Dynamically reducing top-K retrieved document chunks when chat history grows.
6. **Task Chunking**: Splitting a massive task (e.g., analyzing a 500-page book) into smaller parallel requests (MapReduce pattern).

---

### Part 6: The "Lost in the Middle" Effect & Long Prompt Degradation

A major industry misconception is that a larger context window (e.g., 1 Million Tokens) guarantees flawless memory recall across all tokens.

```
                    RECALL ACCURACY ACROSS CONTEXT POSITION
    100% ──┐                                                     ┌── 100%
           │ Primacy Effect                              Recency │
           │ (Beginning of Prompt)                        Effect │
     50% ──┤                                       (End of Prompt)
           │                                                     │
           │                  Lost in the Middle                 │
      0% ──┴───────────────────────────┬─────────────────────────┴── 0%
                                   Position
```

* **The Problem**: Research (*Liu et al.*) proves that LLMs exhibit high accuracy at retrieval for facts placed at the **very beginning** (Primacy Effect) or **very end** (Recency Effect) of a prompt.
* **Degradation in the Center**: Facts placed in the middle of a massive 50k+ token prompt experience significant accuracy drops ("Lost in the Middle").
* **Takeaway**: **Longer Prompts $\neq$ Better Results**. Keep prompts lean, focused, and structured.

---

### Part 7: 7 Common Token & Context Misconceptions

| Misconception | Reality |
| :--- | :--- |
| **1. "1 Token = 1 Word"** | 1 Token is roughly **0.75 words** in English. In non-English languages or code, 1 word can equal 2 to 5+ tokens. |
| **2. "All models use the same Tokenizer"** | Each LLM family (OpenAI `cl100k_base` / `o200k_base`, LLaMA, Claude, Gemini) has a proprietary tokenizer and distinct vocabulary. |
| **3. "TokenID carries intrinsic semantic meaning"** | A TokenID is merely an integer table index (e.g., `1543`). Semantic meaning is generated when the TokenID is converted into a vector in the **Embedding Layer**. |
| **4. "1 Visible Emoji = 1 Token"** | Emojis with skin-tone modifiers or gender variants split into multiple Unicode sub-tokens. |
| **5. "Larger Vocabulary is always better"** | Larger vocabularies shorten sequence lengths but increase the parameter footprint of the model's input/output embedding matrices. |
| **6. "Larger Context Window means perfect memory"** | Attention mechanisms suffer from the "Lost in the Middle" recall degradation as context length grows. |
| **7. "Longer prompts produce better answers"** | Irrelevant context dilutes attention, increases latency, raises API costs, and degrades reasoning accuracy. |
| **8. "A model learns new facts from prompt tokens"** | Prompt context is transient working memory for a single inference call. It does **not** update frozen network weights. |

---

### Part 8: Bridge to Transformer Architecture

Tokenization is the first step of the Transformer input pipeline:

$$\text{Raw Text} \xrightarrow{\text{Tokenizer}} \text{TokenIDs} \xrightarrow{\text{Embedding Matrix}} \text{Dense Vectors} \xrightarrow{\text{Positional Encoding}} \text{Self-Attention Layers}$$

In upcoming lessons, we will explore how these dense vector representations pass through the **Self-Attention Mechanism** to calculate relationships between every token in the context window.

---

## 📊 Summary Comparison: Tokenization Algorithms

| Feature | Byte Pair Encoding (BPE) | WordPiece | Unigram |
| :--- | :--- | :--- | :--- |
| **Direction** | Bottom-up (Merge) | Bottom-up (Merge) | Top-down (Prune) |
| **Merge Criterion** | Pair Frequency | Maximum Likelihood | Loss Minimization |
| **Popular Models** | GPT-3.5, GPT-4, LLaMA, Mistral | BERT, RoBERTa | SentencePiece, T5 |
| **OOV Handling** | 100% Coverage (Falls back to bytes/chars) | 100% Coverage (`[UNK]` or subwords) | 100% Coverage |

---

## 💡 Simple Example: Step-by-Step Token Breakdown

```text
Input Word: "Untrustable"

Step 1: Tokenizer receives raw string "Untrustable".
Step 2: Checks vocabulary for exact match "Untrustable" -> Not found.
Step 3: Splits into subwords:
        - "Un"    (Prefix - Token ID: 500)
        - "trust" (Root   - Token ID: 600)
        - "able"  (Suffix - Token ID: 700)
Step 4: Output Token ID Array: [500, 600, 700]

Multilingual Example:
English: "I cannot help you"  -> ["I", " cannot", " help", " you"] (4 tokens)
Hindi:   "मैं मदद नहीं कर सकता" -> ["मैं", " मद", "द", " नहीं", " कर", " सक", "ता"] (7 tokens)
```

---

## 🏗️ Real-World Example: Context Window Manager Architecture

In production Node.js applications, a Context Manager maintains conversation length within safe limits:

```
                          User Input Message
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │   Calculate Token Count │
                     │   (Tiktoken / Tokenizer)│
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │ Context Limit Check     │
                     │ Current + New > Ceiling?│
                     └────────────┬────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │ YES                           │ NO
                  ▼                               ▼
     ┌──────────────────────────┐    ┌──────────────────────────┐
     │ Sliding Window FIFO      │    │  Append Message & Send   │
     │ Evict oldest User/       │    │  Directly to LLM API     │
     │ Assistant pair           │    └──────────────────────────┘
     └────────────┬─────────────┘
                  │
                  ▼
     ┌──────────────────────────┐
     │ Send Trimmed Context     │
     └──────────────────────────┘
```

---

## ⚠️ Common Mistakes & Pitfalls

* **Mistake 1: Estimating API costs using word count instead of token count**
  * *Correction*: Always measure cost using tokenizer libraries (`tiktoken` for OpenAI) rather than `text.split(' ').length`.
* **Mistake 2: Hardcoding substring slicing without respecting token boundaries**
  * *Correction*: Splitting text strings by character index can slice mid-token or mid-Unicode emoji, causing invalid UTF-8 rendering or broken prompt structures.
* **Mistake 3: Neglecting Special Token Security (Prompt Injection)**
  * *Correction*: Ensure user-supplied input text does not contain unescaped raw control strings (like `<|im_end|>`), which can trick the model into exiting system prompt instructions.

---

## 🔥 Important Points to Remember

* **Computers only understand numbers**; tokenization translates text into numerical **TokenIDs**.
* **Subword tokenization** is the optimal balance between huge word vocabularies and long character sequences.
* **OpenAI & LLaMA use BPE (Byte Pair Encoding)**, which greedily merges frequent adjacent character pairs.
* **Multilingual Fertility Bias**: Non-English text yields higher token-per-word ratios, increasing cost and consuming context memory faster.
* **Context Length is the hard ceiling**; **Context Window is the active payload size** shared between prompt and generation.
* **The "Lost in the Middle" effect** degrades recall accuracy when critical information is buried in the center of long prompts.
* **Special Tokens** (`<|im_start|>`, `<|im_end|>`) control structural execution and security boundaries.

---

## 💻 Code / Commands / Configuration

### Production-Grade JavaScript (Node.js) Token & Context Window Utilities

```javascript
// =====================================================================
// 1. Conceptual Byte Pair Encoding (BPE) Simulation in JavaScript
// =====================================================================
function simulateBpeTokenization(text) {
  // Vocabulary dictionary mapping subwords to Token IDs
  const vocabulary = {
    "This": 101,
    "is": 102,
    "a": 103,
    "simple": 104,
    "Un": 201,
    "trust": 202,
    "able": 203,
    " sentence": 105
  };

  // Simple subword split simulation
  const rawWords = text.split(" ");
  const tokens = [];
  const tokenIds = [];

  for (const word of rawWords) {
    if (vocabulary[word]) {
      tokens.push(word);
      tokenIds.push(vocabulary[word]);
    } else if (word === "Untrustable") {
      // Decompose subwords
      tokens.push("Un", "trust", "able");
      tokenIds.push(vocabulary["Un"], vocabulary["trust"], vocabulary["able"]);
    } else {
      // Fallback subword breakdown
      tokens.push(word);
      tokenIds.push(999); // Generic subword token ID
    }
  }

  return { tokens, tokenIds };
}

console.log("=== BPE Tokenization Result ===");
console.log(simulateBpeTokenization("Untrustable"));


// =====================================================================
// 2. Multilingual Token Fertility Calculator
// =====================================================================
function calculateTokenFertility(text, estimatedTokenCount) {
  const wordCount = text.trim().split(/\s+/).length;
  const fertilityRatio = (estimatedTokenCount / wordCount).toFixed(2);
  
  return {
    wordCount,
    estimatedTokenCount,
    fertilityRatio: parseFloat(fertilityRatio)
  };
}

const englishStats = calculateTokenFertility("I cannot help you with that", 6);
const hindiStats = calculateTokenFertility("मैं आपकी मदद नहीं कर सकता", 12);

console.log("\n=== Token Fertility Comparison ===");
console.log("English Fertility:", englishStats);
console.log("Hindi Fertility:  ", hindiStats);


// =====================================================================
// 3. Sliding Window Context Buffer Manager (Node.js Pattern)
// =====================================================================
class ContextWindowManager {
  constructor(maxContextLength = 4090, maxResponseTokens = 500) {
    this.maxContextLength = maxContextLength;
    this.maxResponseTokens = maxResponseTokens;
    this.systemPrompt = { role: "system", content: "You are a helpful AI assistant." };
    this.messages = [];
  }

  // Rough estimation: 1 word ~ 1.33 tokens
  estimateTokens(text) {
    return Math.ceil(text.trim().split(/\s+/).length * 1.33);
  }

  getTotalTokens() {
    let total = this.estimateTokens(this.systemPrompt.content);
    for (const msg of this.messages) {
      total += this.estimateTokens(msg.content);
    }
    return total;
  }

  addMessage(role, content) {
    this.messages.push({ role, content });
    this.enforceContextLimit();
  }

  enforceContextLimit() {
    const allowedLimit = this.maxContextLength - this.maxResponseTokens;

    // FIFO eviction: remove oldest user/assistant pairs if exceeding allowed limit
    while (this.getTotalTokens() > allowedLimit && this.messages.length > 1) {
      console.log(`[Context Window Overflow] Evicting oldest message: "${this.messages[0].content}"`);
      this.messages.shift(); // Remove oldest message
    }
  }

  getPayload() {
    return [this.systemPrompt, ...this.messages];
  }
}

// Example Usage
console.log("\n=== Sliding Window Context Buffer ===");
const manager = new ContextWindowManager(50, 10); // Small limit for testing
manager.addMessage("user", "Hello!");
manager.addMessage("assistant", "Hi there, how can I help you today?");
manager.addMessage("user", "Can you explain how tokenization works in LLMs?");
manager.addMessage("user", "Also explain context windows and sliding memory buffers!");

console.log("\nFinal Payload to LLM API:\n", manager.getPayload());
```

---

## 🎤 Interview Perspective

| Common Interview Question | What the Interviewer Is Really Testing | High-Scoring Answer Key Points |
| :--- | :--- | :--- |
| **"Why do modern LLMs use Subword Tokenization (BPE) instead of Word or Character tokenization?"** | Understanding of vocabulary size vs sequence length trade-offs. | Word tokenization creates huge vocabularies and fails on Out-of-Vocabulary (OOV) words. Character tokenization creates tiny vocabularies but causes sequence lengths to explode, destroying semantic context and spiking attention compute ($O(N^2)$). Subword tokenization (BPE) balances manageable vocabulary sizes ($32k-100k$) with zero OOV errors. |
| **"Explain the difference between Context Length and Context Window."** | Knowledge of hardware limits vs active API request payloads. | Context Length is the hard architectural/hardware limit of tokens a model can process in one pass (e.g., 128k tokens). Context Window is the active payload size populated in a specific request (System Prompt + History + RAG Docs + Generation Output). |
| **"What is the 'Lost in the Middle' effect in long-context models?"** | Practical experience with long-prompt degradation failure modes. | Research shows LLMs recall facts at the beginning (Primacy) and end (Recency) of long prompts with high accuracy, but experience significant recall degradation for information placed in the middle. Keeping prompts lean and structured yields better results than dumping massive documents. |
| **"Why is API usage for non-English languages more expensive?"** | Understanding of Token Fertility Ratio and vocabulary training bias. | Tokenizers are trained on predominantly English corpora. Non-English words split into smaller subword fragments, producing a higher Token Fertility Ratio ($\frac{\text{Tokens}}{\text{Words}}$). As a result, non-English prompts require more tokens for the exact same text, increasing API cost and consuming context memory faster. |

---

## 🧩 Connection With Previous Concepts

* **Connection to Season 01, Class 02**: In Class 02, we learned that LLMs predict the next word probabilistically ($P(w_{t} \mid w_{1}, \dots, w_{t-1})$). In Class 03, we uncovered *what* those words actually are under the hood—numerical **TokenIDs** generated by a **Tokenizer** operating within a fixed **Context Window**.
* **Bridge to Class 04**: In the next lesson, we will see how these TokenIDs are transformed into continuous mathematical vectors via **Embeddings** and passed into **Neural Network Architectures**.

---

Previous : [02. Search Engines vs LLMs and LLM Fundamentals](./02_Search_Engines_vs_LLMs_and_LLM_Fundamentals.md) | Index: [00_index.md](../00_index.md) | Next: [04. Vector Embeddings and Semantic Search](./04_Vector_Embeddings_and_Semantic_Search.md)
