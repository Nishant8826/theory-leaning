# 🤖 Does ChatGPT Know or Does It Guess?

## 📌 Overview

When you type a question into ChatGPT and a fluent, authoritative answer appears on your screen within seconds, what is actually happening behind the scenes?

* Did it query a structured SQL database?
* Did it search the live internet in real time?
* Did it recall a memorized fact from digital memory?
* Does it truly **know** the answer, or is it merely **guessing**?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       THE CORE QUESTION OF GENERATION                       │
│                                                                             │
│      Prompt: "The capital of France is _____"                               │
│                                                                             │
│      Does the model "know" Paris?                                           │
│      - It does not look up a table: { "France": "Paris" }.                  │
│      - It calculates learned next-token probabilities:                      │
│        P("Paris") = 99.4%, P("Lyon") = 0.3%, P("Marseille") = 0.1%          │
│      - It generates "Paris" because training made that sequence probable!   │
└─────────────────────────────────────────────────────────────────────────────┘
```

The answer is neither a simple "it knows" nor a naive "it blindly guesses." Modern Large Language Models operate on **learned probability distributions over tokens**. To use and build AI systems effectively, software engineers must understand the fundamental difference between **Information Retrieval (Search Engines)** and **Probabilistic Generation (LLMs)**.

---

## 🎯 Why This Matters

Treating an LLM as a search engine or database leads to critical production failures:
* **The Hallucination Trap**: LLMs generate grammatically flawless prose even when facts are completely fabricated.
* **The Confidence Illusion**: Language models express fabricated answers with the exact same authoritative tone as established facts.
* **Architectural Decisions**: Helps engineers know when to use **Vector Databases & RAG**, when to use **External Tools/APIs**, and when to rely on the model's base parameters.
* **Security & Prompt Design**: Explains why models exhibit apparent self-knowledge (via System Prompts) and how safety guardrails intercept unsafe requests.

---

## 🧠 Prerequisites

| Concept | Explanation |
| :--- | :--- |
| **Information Retrieval** | The process of finding, indexing, and ranking existing documents from a storage system based on a user query. |
| **Next-Token Prediction** | The algorithmic task of estimating probability distributions for the next token given an existing sequence of tokens. |
| **Knowledge Cutoff** | The fixed date when a model's pre-training dataset was finalized; facts occurring after this date are unknown to the base weights. |
| **System Prompt** | Hidden developer instructions injected before user messages that govern model identity, persona, tool use, and safety boundaries. |

---

## 🔍 Deep Dive: Search Retrieval vs. LLM Generation

---

### Part 1: Four Live Demonstrations – Revealing the Difference

---

#### Experiment 1: The Factual Query (Dr. APJ Abdul Kalam)
* **Google Search**: Returns a ranked list of links (Wikipedia, official biographies, news articles). The user must click and read.
* **ChatGPT (GPT-4)**: Instantly generates a concise, readable narrative summarizing his presidency, contributions to science, and biography.
* *Impression*: ChatGPT feels like a faster, more convenient search engine.

---

#### Experiment 2: The Nonexistent Product ("Namaste AI Red Wine")
The instructor tested an intentionally absurd prompt:
> *"Why is Namaste AI red wine from the Himalayan region of India so expensive? Please explain briefly."*

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     THE NONEXISTENT WINE EXPERIMENT                         │
│                                                                             │
│  1. Google Search:                                                          │
│     - Query: "Namaste AI red wine Himalayan region"                         │
│     - Result: "No results found." (Accurate! The product does not exist).   │
│                                                                             │
│  2. Raw GPT-4 Base Generation:                                              │
│     - Result: "Namaste AI red wine is expensive due to:                     │
│                - High-altitude unique Himalayan vineyards                   │
│                - Hand-picked grape harvesting in steep terrain              │
│                - Limited batch production & special aging barrels           │
│                - State import/export luxury taxes and branding."            │
│     - Reality: Complete fabrication generated with absolute confidence!    │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Why this happens**: A search engine can only retrieve documents stored in its index. A language model, however, accepts the premise of the prompt and generates a statistically plausible sequence based on patterns associated with *"wine"*, *"Himalayas"*, *"altitude"*, and *"luxury pricing"*.

---

#### Experiment 3: Correct Identity, Wrong Age (Mixture of Fact and Fiction)
* **Prompt**: *"Who is Akshay Saini? How old is he?"*
* **Response**: Correctly identifies him as an Indian software engineer and educator (Namaste JavaScript). Correctly identifies his birthdate as March 7. **Hallucinates the birth year as 1983 and age as 43** (actual age at recording: 31).
* **Key Insight**: Hallucinations rarely present as pure gibberish. They disguise themselves within authentic facts, making them difficult to detect without external verification.

---

#### Experiment 4: The Dot-Counting Test (Tokenization vs. Tool Execution)
* **Prompt**: A string of 108 dots (`..................`) is submitted.
* **Raw GPT-4**: Confidently claims there are **100 dots**. When 10 more dots are appended, it predicts **110 dots** (expected: 118).
* **ChatGPT with Code Interpreter**: Executes a Python/code tool (`len(dots)`), correctly returning **108 dots** and **118 dots**.
* **Key Insight**: LLMs are text generators, not arithmetic calculators. Exact counting requires **computational tools**.

---

### Part 2: Retrieval vs. Generation (The Fundamental Comparison)

```
┌────────────────────────────────────────┐     ┌────────────────────────────────────────┐
│             SEARCH ENGINE              │     │             LANGUAGE MODEL             │
│               (Retrieve)               │     │               (Generate)               │
│                                        │     │                                        │
│  1. Accepts user Query                 │     │  1. Accepts user Prompt                │
│  2. Looks inside Inverted Index        │     │  2. Calculates next-token distribution │
│  3. Retrieves existing documents       │     │  3. Samples candidate token            │
│  4. Ranks candidates by credibility    │     │  4. Appends token and repeats loop     │
│  5. Returns links with source trails   │     │  5. Produces original synthesized text │
└────────────────────────────────────────┘     └────────────────────────────────────────┘
```

$$\text{Search Engines } \mathbf{\text{RETRIEVE}} \text{ existing text.} \quad \longleftrightarrow \quad \text{LLMs } \mathbf{\text{GENERATE}} \text{ new text.}$$

---

### Part 3: How Search Engines Work (The Textbook Index Analogy)

Imagine reading a 1,000-page physics book. To study thermodynamics, you do not read from page 1; you flip to the **Index at the back**, locate the topic, and jump directly to that page.

```
                        SEARCH ENGINE CRAWLING & INDEXING
                        
  Live Internet ──► [Web Crawlers / Spiders] ──► [Inverted Search Index] ──► [Ranking Engine]
  (New pages,       (Continuously discovering    (Keyword-to-URL mapping:    (Domain Authority,
   Earthquakes)      new & modified URLs)         "Delhi" -> [URL1, URL2])    PageSpeed, Backlinks)
```

#### Ranking Signals Used by Search Engines:
* **Domain Authority**: Perceived trust and historical credibility of the domain.
* **Page Speed & Mobile Performance**: Latency and rendering speed.
* **Dwell Time (Retention)**: Average duration users stay on the page.
* **Backlinks**: Quantity and quality of external sites linking to the page.
* **Recency / Freshness**: Timestamp of latest publication or update.

#### Search Engine Limitations & Strengths:
* **Limitations**: Indexed articles can still be biased, outdated, or factually incorrect.
* **The Golden Advantage – Traceability**: Search results leave a clear **source trail**. You can inspect the domain, review the author, check the publication date, and evaluate credibility.

---

### Part 4: Probabilistic Next-Token Generation

An LLM operates like a reader who has studied a vast library of books. The books are now closed. When asked a question, the model responds from patterns retained inside its parameters, rather than reopening a specific page.

```
                      NEXT-TOKEN PROBABILITY DISTRIBUTION
                      
  Prompt: "The capital of India is _____"
  
  Candidate Tokens:
  ┌─────────────────────────────────────────────────────────────┐
  │ "Delhi"       ████████████████████████████████████ 90.0%    │
  │ "New"         ████████                             18.0%    │
  │ "Punjab"      ▌                                     1.0%    │
  │ "Lucknow"     ▎                                     0.5%    │
  └─────────────────────────────────────────────────────────────┘
```

#### Is an LLM "Just Autocomplete"?
In lay terms, next-token prediction resembles phone keyboard autocomplete. However, calling an LLM "just autocomplete" misses its emergent depth:
* It tracks complex linguistic dependencies across thousands of words.
* It captures grammar, multi-step logic, code syntax, and reasoning patterns.
* It operates across dozens of human and programming languages.
* **A more accurate description**: **A very powerful, context-aware probabilistic reasoning engine.**

---

### Part 5: Base Model vs. AI Assistant (The Car Analogy)

A common mistake is assuming that GPT-4 or Claude is simply a single neural network.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THE CAR ENGINE ANALOGY                            │
│                                                                             │
│   1. The Base Model (The Engine):                                           │
│      - Raw text completion engine trained on trillions of tokens.           │
│      - If given: "Once upon a time", it continues a fairy tale.             │
│      - If given: "User: Hello\nAssistant:", it predicts conversational text.│
│                                                                             │
│   2. The Complete AI Assistant (The Complete Car):                          │
│      - Sits around the engine to provide a safe, drivable consumer vehicle: │
│        ├── Steering & Gears   ──► System Instructions & Chat Formatting     │
│        ├── Windshield & Brakes──► Safety Guardrails & Content Moderation    │
│        ├── GPS Navigation     ──► Live Web Search & RAG Retrieval           │
│        └── Onboard Computer   ──► Code Interpreter, Calculators & Tools     │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LAYERS OF AN AI ASSISTANT                          │
│                                                                             │
│  [User Prompt]                                                              │
│        │                                                                    │
│        ▼                                                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 1. Security & Guardrails (Intercepts malicious/harmful intent)        │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ 2. System Instructions (Identity, constraints, formatting rules)      │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ 3. Tool Dispatcher (Calls Web Search, Calculator, Python Sandbox)    │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ 4. Base LLM (Generates next-token text using prompt + tool context)   │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ 5. Output Safety Filters (Checks response before displaying to user)  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│        │                                                                    │
│        ▼                                                                    │
│  [Rendered Assistant Response]                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Part 6: Training vs. Inference

| Characteristic | Training Phase | Inference Phase (Runtime) |
| :--- | :--- | :--- |
| **Operation** | Adjusts billions of parameters using loss & backprop | Performs forward pass on frozen weights |
| **Compute / Hardware** | Massive GPU/TPU clusters running for weeks | Single GPU or shared cloud inference endpoint |
| **State of Weights** | **Mutable** (values change continuously) | **Frozen** (read-only matrices) |
| **Knowledge State** | Absorb patterns from training dataset | Bounded by fixed **Knowledge Cutoff** date |
| **Cost & Latency** | Millions of dollars; long execution times | Milliseconds; fractions of a cent per query |

---

### Part 7: Hallucinations – The Confidence Illusion

> **Formal Definition:**  
> **Hallucination** occurs when an AI model generates output that appears fluent and plausible, but is factually unsupported, incorrect, misleading, or completely fabricated.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE 4 RULES OF AI FACTUALITY                             │
│                                                                             │
│   1. Fake fluency is NOT truthfulness.                                      │
│   2. Language quality and factual accuracy are completely separate.         │
│   3. Authoritative tone is NOT evidence of factual certainty.               │
│   4. Never fall for an illusion of certainty in AI output.                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### The 7 Core Causes of Hallucinations:
1. **Insufficient Information**: The model lacks specific training data on the topic, but its objective function forces it to generate a continuation.
2. **Ambiguous or Conflicting Training Data**: Conflicting sources on the web produce blended, incoherent probability distributions.
3. **Outdated Knowledge (Cutoff)**: The queried event occurred after pre-training completed.
4. **False Assumptions in Prompts**: The prompt asserts a false premise (*"Himalayan wine"*); the model conditions on that premise rather than challenging it.
5. **Unreliable Internet Patterns**: Scraping vast internet text absorbs satire, marketing hyperbole, conspiracy theories, and errors.
6. **Optimization for Helpfulness**: Assistant tuning prioritizes providing an answer over repeatedly saying *"I don't know"*.
7. **Probabilistic Nature**: Sampling from probability distributions inherently introduces variance and non-zero chances of selecting incorrect tokens.

#### The 6 Common Types of Hallucinations:
* **Invented Facts**: Fabricating events, products, or historical details.
* **Invented Citations**: Generating realistic-looking but fake academic papers, DOIs, or URLs.
* **Incorrect Combinations**: Blending two real people, companies, or events together.
* **Outdated Facts**: Presenting historical facts as current status.
* **False Precision**: Providing exact numbers, timestamps, or dot counts without computational backing.
* **Broken Reasoning**: Drawing invalid logical deductions across intermediate steps.

---

### Part 8: Tools and Retrieval-Augmented Generation (RAG)

To overcome static knowledge cutoffs and eliminate math/reasoning errors, modern assistants incorporate **Tools** and **RAG**:

$$\mathbf{\text{The Golden Formula:}} \quad \text{Retrieval gives external evidence} \quad + \quad \text{Generation synthesizes the response}$$

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     RETRIEVAL-AUGMENTED GENERATION (RAG)                    │
│                                                                             │
│  1. User Query: "What is our company's refund policy for Enterprise?"       │
│                                │                                            │
│                                ▼                                            │
│  2. Retriever: Searches internal Vector Database / Knowledge Base           │
│     Extracts: Exact policy excerpt from internal handbook.                  │
│                                │                                            │
│                                ▼                                            │
│  3. Augmented Prompt sent to LLM:                                           │
│     "Context: [Policy excerpt...]                                           │
│      Question: Answer the user using ONLY the context above."               │
│                                │                                            │
│                                ▼                                            │
│  4. LLM Generation: Produces accurate, grounded, cited response!           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Part 9: Does the Model "Know" Itself? (The 4 Sources of Output)

When an LLM answers questions like *"Who created you?"*, *"Where are you hosted?"*, or *"What is your cutoff date?"*, beginners often mistake this for self-awareness.

In reality, every piece of text generated by an AI assistant originates from **four specific sources**:

```
                         THE 4 SOURCES OF MODEL OUTPUT
                                       │
      ┌──────────────────┬─────────────┴────────────┬──────────────────┐
      ▼                  ▼                          ▼                  ▼
┌──────────────┐   ┌──────────────┐           ┌──────────────┐   ┌──────────────┐
│  1. Training │   │  2. Context  │           │  3. System   │   │  4. External │
│     Data     │   │    Window    │           │    Prompt    │   │    Tools     │
│ Patterns     │   │ Prior user/  │           │ Hidden rule  │   │ Live web,    │
│ learned from │   │ assistant    │           │ injecting    │   │ calculators, │
│ pre-training │   │ conversation │           │ identity &   │   │ database     │
│ internet text│   │ history      │           │ constraints  │   │ retrievals   │
└──────────────┘   └──────────────┘           └──────────────┘   └──────────────┘
```

* **Multi-Turn Context Example**:
  * Message 1: *"What is the weather in Dehradun?"* $\rightarrow$ Assistant retrieves 22°C and rain.
  * Message 2: *"Should I take an umbrella?"* $\rightarrow$ The second prompt doesn't mention Dehradun, but the model connects the umbrella recommendation via conversation context.

---

## 📊 Summary Comparison: Search Engine vs. Base Model vs. AI Assistant

| Feature | Search Engine (Google) | Base LLM (GPT-4 Base) | Tool-Augmented Assistant (ChatGPT) |
| :--- | :--- | :--- | :--- |
| **Core Mechanism** | Keyword & Vector Retrieval | Next-Token Text Continuation | Layered System (LLM + Tools + Safety) |
| **Data Source** | Live Inverted Web Index | Static Frozen Weight Matrices | Pre-trained Weights $+$ Live Tools/RAG |
| **Handling Fictional Prompts** | Returns *"No results found"* | Hallucinates plausible prose | Validates via web/tools or warns user |
| **Arithmetic & Counting** | Computational widgets | Frequently incorrect (probabilistic) | Dispatches to Python / Calculator tool |
| **Source Traceability** | Direct URLs, authors, dates | None (Black-box parameter weights) | Citations provided when search tool runs |
| **Best Used For** | Discovering external web sources | Raw creative text completion | Complex synthesis, coding & workflows |

---

## 💡 Simple Example: Prompting Tactics to Mitigate Hallucinations

```text
❌ Vulnerable Prompt:
"Tell me about the latest electric vehicle launched in India yesterday."
-> Risk: Base model has a cutoff and will hallucinate a fictional car launch.

✅ Grounded, Defended Prompt:
"Search the live web for electric vehicles launched in India within the last 48 hours. 
Separate verified facts from rumors. 
Cite your sources with URLs. 
If no verified launch occurred, explicitly state: 'No launch found.'"
```

---

## ⚠️ Common Mistakes & Pitfalls

* **Mistake 1: Relying on LLMs for exact character or token counting**
  * *Correction*: LLMs process text in subword tokens, not raw characters. For exact string lengths, character counts, or complex math, always route the task to a **Code Interpreter tool**.
* **Mistake 2: Assuming a confident tone implies factual accuracy**
  * *Correction*: Softmax next-token selection produces identical grammatical fluency regardless of whether the fact is real or fabricated. Never use tone as a proxy for truth.
* **Mistake 3: Believing RAG completely eliminates hallucinations**
  * *Correction*: While RAG drastically reduces errors by grounding responses in provided documents, poor prompt design or ambiguous retrieved chunks can still lead to misinterpretation.

---

## 🔥 Important Points to Remember

* **Search engines retrieve** existing documents and expose their sources; **LLMs generate** original text token-by-token.
* **Probabilities drive generation**: Tokens are sampled based on statistical patterns formed across training data.
* **Base Models are engines; AI Assistants are complete cars** equipped with safety filters, system instructions, and tools.
* **Training mutates weights** across GPU clusters; **Inference executes frozen weights** at runtime.
* **Hallucination** is fluent, plausible, but fabricated output caused by cutoffs, false prompt assumptions, or probabilistic sampling.
* **Tools (Code Execution, Search, Calculators)** turn text generators into reliable computational systems.
* **Apparent self-awareness is an illusion** created by System Prompts, training data, conversation context, and tool outputs.

---

## 💻 Code / Commands / Configuration

### Complete JavaScript (Node.js) Simulation: Search Index vs. Probabilistic LLM Generator

```javascript
// =====================================================================
// 1. Search Engine Simulation (Inverted Index & Retrieval)
// =====================================================================
class SearchEngine {
  constructor() {
    this.index = new Map();
  }

  indexDocument(id, title, text, url) {
    const tokens = text.toLowerCase().split(/\W+/);
    tokens.forEach(token => {
      if (!this.index.has(token)) {
        this.index.set(token, []);
      }
      this.index.get(token).push({ id, title, url });
    });
  }

  search(query) {
    const term = query.toLowerCase().trim();
    const results = this.index.get(term) || [];
    return results.length > 0
      ? { found: true, results }
      : { found: false, message: "No indexed documents found." };
  }
}

console.log("=== 1. Search Engine Retrieval Demonstration ===");
const googleMock = new SearchEngine();
googleMock.indexDocument(1, "APJ Abdul Kalam Biography", "Dr APJ Abdul Kalam was the 11th President of India", "https://wiki.org/kalam");

console.log("Query 'Kalam':", googleMock.search("kalam"));
console.log("Query 'Namaste Wine':", googleMock.search("wine")); // Returns 'No indexed documents found'!


// =====================================================================
// 2. Probabilistic Next-Token Generator Simulation
// =====================================================================
function sampleNextToken(tokenProbabilities, temperature = 1.0) {
  // Apply Temperature scaling
  const scaledScores = Object.entries(tokenProbabilities).map(([token, prob]) => {
    return { token, score: Math.pow(prob, 1 / temperature) };
  });

  const totalScore = scaledScores.reduce((sum, item) => sum + item.score, 0);
  const normalized = scaledScores.map(item => ({ token: item.token, prob: item.score / totalScore }));

  // Probabilistic Selection
  const random = Math.random();
  let cumulative = 0;
  for (const item of normalized) {
    cumulative += item.prob;
    if (random <= cumulative) {
      return item.token;
    }
  }
  return normalized[0].token;
}

console.log("\n=== 2. Probabilistic Generation Demonstration ===");
const promptDistribution = { "Delhi": 0.90, "Punjab": 0.05, "Lucknow": 0.03, "Mumbai": 0.02 };
console.log("Generated Token (Greedy/Temp=0.1):", sampleNextToken(promptDistribution, 0.1));
console.log("Generated Token (Creative/Temp=1.2):", sampleNextToken(promptDistribution, 1.2));


// =====================================================================
// 3. Tool-Augmented Assistant Pattern (Safe Dot Counter)
// =====================================================================
function assistantRespond(prompt) {
  // Regex tool trigger for counting queries
  const dotMatch = prompt.match(/count dots:\s*([.]+)/i);
  
  if (dotMatch) {
    const dotsString = dotMatch[1];
    // Dispatch to programmatic tool execution instead of guessing!
    const exactCount = dotsString.length;
    return `[Tool: CodeInterpreter] The provided string contains exactly ${exactCount} dots.`;
  }

  return "Generating standard language response...";
}

console.log("\n=== 3. Tool-Augmented Assistant Demonstration ===");
const rawPrompt = "Count dots: ...................................."; // 36 dots
console.log(assistantRespond(rawPrompt));
```

---

## 🎤 Interview Perspective & Revision Questions

| Common Interview Question | What the Interviewer Is Really Testing | High-Scoring Answer Key Points |
| :--- | :--- | :--- |
| **"Explain the difference between a Search Engine and a Large Language Model."** | Core knowledge of Retrieval vs. Generation architectures. | A search engine parses an inverted index to **retrieve and rank** existing documents with verifiable source links. An LLM calculates **next-token probability distributions** to synthesize original text from patterns stored in frozen neural weights. |
| **"Why do LLMs hallucinate, and how do we prevent hallucinations in enterprise applications?"** | Practical production engineering and RAG design. | Hallucinations happen because LLMs sample tokens probabilistically without built-in fact verification. In production, mitigate hallucinations by using **RAG** (grounding in verified vector context), connecting **deterministic tools** (APIs/calculators), using **Temperature = 0**, and setting strict system prompt guardrails. |
| **"What is the difference between a Base Model and an AI Assistant?"** | Understanding the post-training alignment layers. | A Base Model is purely the raw next-token prediction engine. An AI Assistant wraps the base model with **System Instructions**, **SFT/RLHF alignment**, **Safety Moderation Filters**, **Context/Memory management**, and **Tool-calling dispatchers**. |
| **"What are the four sources of an AI model's output when answering about itself?"** | Awareness of the mechanics behind apparent self-knowledge. | 1. **Training Data** (web text absorbed before cutoff).<br>2. **Conversation Context** (prior chat turns in the session).<br>3. **System Prompt** (developer-defined instructions).<br>4. **External Tools** (live API/web search payloads). |

---

## 🧩 Connection With Previous Concepts

* **Connection to Season 01, Class 01**: In Class 01 ([The Evolution of AI](./01_The_Evolution_of_AI.md)), we traced how AI moved from rule-based systems to Deep Learning and Transformers. In Class 02, we demystified how these models generate text probabilistically versus search retrieval.
* **Bridge to Class 03**: In the next lesson ([03. The Secret Language of LLMs](./03_The_Secret_Language_of_LLMs.md)), we will examine the literal building blocks of this generation process: how words are sliced into **Tokens and Token IDs** and managed within strict **Context Windows**.

---

Previous : [01. The Evolution of AI](./01_The_Evolution_of_AI.md) | Index: [00_index.md](../00_index.md) | Next: [03. The Secret Language of LLMs](./03_The_Secret_Language_of_LLMs.md)
