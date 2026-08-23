# 🤖 AI – Complete Revision Guide

A complete revision guide for my journey from AI fundamentals to advanced concepts. This file provides a single place to navigate through every Season and class while reviewing the most important concepts, terminology, workflows, commands, configurations, best practices, and interview-relevant topics.

The goal is to use this file for a fast revision of the entire AI learning journey while opening individual class files whenever a deeper explanation is required.

---

## 🛠️ Daily Note Generator Prompt

Use the simple template below when sharing your class notes.

<details>
<summary>📋 <b>Click to expand and copy Daily Prompt Template</b></summary>

```text
Season: [e.g., Season 01]
Class: [e.g., Class 01]

--- RAW NOTES START ---
[Paste your raw notes, slides, transcripts, diagrams, or code snippets here]
--- RAW NOTES END ---
```

*(Note: The topic name, filename, and complete structured lesson will be identified and generated automatically based on your raw notes.)*

</details>

---

## 📌 Module Navigation

### Season 01

* [01. History and Evolution of AI](./Season_01/01_History_and_Evolution_of_AI.md)
* [02. Search Engines vs LLMs and LLM Fundamentals](./Season_01/02_Search_Engines_vs_LLMs_and_LLM_Fundamentals.md)
* [03. Tokenization and Context Windows](./Season_01/03_Tokenization_and_Context_Windows.md)

---

# Season 01

## 01. History and Evolution of AI

🔗 **Full Lesson:** [01_History_and_Evolution_of_AI.md](./Season_01/01_History_and_Evolution_of_AI.md)

* **What**: The chronological journey of Artificial Intelligence across 70+ years—spanning Symbolic/Rule-based systems, Statistical Machine Learning, Deep Learning, Transformers, Generative AI, and Agentic Systems.
* **Why It Exists**: Provides the historical context, algorithmic motivations, and technological paradigm shifts that explain why modern AI architectures (Transformers, RLHF, Autonomous Agents) exist and where the industry is heading.
* **Key Concepts**:
  * **1950 – Alan Turing**: Proposed the Turing Test ("Computing Machinery and Intelligence") defining observable machine intelligence.
  * **1956 – John McCarthy**: Coined the term "Artificial Intelligence" at the Dartmouth Conference.
  * **1950s–1980s – Symbolic / Rule-Based AI**: Expert systems (MYCIN, ELIZA) using handcrafted `IF-THEN` rules; collapsed into "AI Winters" due to combinatorial explosion and brittleness.
  * **1990s – Statistical Machine Learning**: Transition from hardcoded rules to learning patterns from structured data (SVMs, Decision Trees); required heavy manual feature engineering.
  * **1997 – Deep Blue vs. Kasparov**: IBM's supercomputer won via massive heuristic search (Alpha-Beta pruning, 200M positions/sec), not learning.
  * **2012 – AlexNet & Deep Learning**: ImageNet victory using CNNs, ReLU, and CUDA GPU acceleration; triggered the deep learning revolution by enabling end-to-end representation learning.
  * **2016 – AlphaGo vs. Lee Sedol**: Defeated Go master using Deep Reinforcement Learning (Policy & Value Networks) paired with Monte Carlo Tree Search (MCTS).
  * **2017 – Transformer Architecture**: "Attention Is All You Need" introduced Self-Attention, replacing sequential RNNs/LSTMs with massively parallelizable GPU training.
  * **2022 – ChatGPT & Generative AI**: Scaled LLMs aligned via Reinforcement Learning from Human Feedback (RLHF) for conversational, few-shot reasoning.
  * **2025+ – Agentic AI**: Autonomous multi-step execution loops (Plan $\rightarrow$ Tool Call $\rightarrow$ Observe $\rightarrow$ Reflect $\rightarrow$ Execute) solving complex end-to-end tasks.

### Evolution Timeline Quick Matrix

| Milestone | Year | Core Mechanism | Breakthrough Impact |
| :--- | :--- | :--- | :--- |
| **Turing Test** | 1950 | Behavioral imitation game | First formal philosophy of machine cognition |
| **Dartmouth Conference** | 1956 | Academic workshop | Coined the term "Artificial Intelligence" |
| **Symbolic AI** | 1950s–80s | Handcrafted `IF-THEN` rules | Expert systems, logic engines |
| **Deep Blue** | 1997 | Minimax + Alpha-Beta Search | Defeated World Chess Champion Garry Kasparov |
| **Statistical ML** | 1990s | Optimization on tabular data | SVMs, Random Forests, Spam filters |
| **AlexNet** | 2012 | CNNs + GPU CUDA + ReLU | Cut ImageNet error in half; ignited DL era |
| **AlphaGo** | 2016 | Policy/Value Nets + MCTS + RL | Conquered Go's $10^{170}$ state space |
| **Transformers** | 2017 | Self-Attention Mechanism | Parallelized sequence modeling for modern LLMs |
| **ChatGPT** | 2022 | Pre-training + SFT + RLHF | Consumer Generative AI breakthrough |
| **Agentic AI** | 2025+ | LLM + Tool Use + Autonomous Loops | Active task automation & multi-agent systems |

> [!IMPORTANT]
> The fundamental driver of AI progression is the convergence of **Algorithms** (Backpropagation, Attention), **Compute** (GPUs, TPUs), and **Data** (Internet-scale corpora, synthetic datasets). When studying subsequent lessons, always analyze how these three pillars interact.

---

## 02. Search Engines vs LLMs and LLM Fundamentals

🔗 **Full Lesson:** [02_Search_Engines_vs_LLMs_and_LLM_Fundamentals.md](./Season_01/02_Search_Engines_vs_LLMs_and_LLM_Fundamentals.md)

* **What**: A comprehensive structural breakdown comparing Search Engines (Information Retrieval via Crawling, Indexing, and Ranking) with Large Language Models (Probabilistic Next-Token Generation via static neural network weights).
* **Why It Exists**: Explains why LLMs are not search engines or databases, why they hallucinate, why knowledge cutoffs exist, and how tool integration (RAG, Web Search, Code Interpreters) bridges the gap between text synthesis and real-world truth.
* **Key Concepts**:
  * **Search Engine Architecture**: Crawling (Spiders fetching metadata), Indexing (Inverted Index mapping terms to documents), and Ranking (PageRank, relevance algorithms). Re-crawl frequencies vary based on volatility (news vs. static PDFs).
  * **Probabilistic Next-Token Prediction**: LLMs calculate mathematical probability distributions ($P(w_{t} \mid w_{1}, \dots, w_{t-1})$) to sample the next token. Scale leads to emergent capabilities in reasoning, grammar, and code.
  * **Weights / Parameters**: LLMs store compressed patterns in floating-point weight matrices, not in text files or database rows.
  * **Knowledge Cutoff & Frozen Weights**: Pre-training updates weights across GPU clusters; during inference, weights are frozen (read-only), creating a fixed knowledge cutoff date.
  * **Base Model vs AI Assistant (The Car Analogy)**: Base Models are raw completion engines (the engine). AI Assistants (ChatGPT, Claude) add SFT, RLHF, System Prompts, Guardrails, and Tool Access (the complete car).
  * **Training vs Inference**: Training is mutable weight learning ($1M+ compute, months); Inference is frozen weight forward pass (cents, milliseconds).
  * **Hallucinations & Fake Fluency**: Flawless grammar $\neq$ truthfulness. 4 Types: Invented facts, Outdated facts / Incorrect combinations, False precision, and Broken reasoning.
  * **Tool Calling & RAG**: Connecting LLMs to real-time APIs, calculators, and vector databases to retrieve ground-truth context and eliminate hallucinations.
  * **Self-Awareness Myth**: LLMs do not possess self-awareness; identity responses are driven by injected System Prompts.

### System Architectural Comparison Matrix

| Characteristic | Search Engine | Base LLM | Tool-Augmented LLM (RAG) |
| :--- | :--- | :--- | :--- |
| **Primary Function** | Document Retrieval | Next-Token Text Generation | Grounded Synthesis & Execution |
| **Data Source** | Live Web Index | Frozen Neural Network Weights | Real-Time Retrieval + Weights |
| **Knowledge Cutoff** | None (Real-time) | Fixed (Pre-training End Date) | None (Live context injection) |
| **Factual Traceability** | High (Direct URLs) | Low (Black-box parameters) | High (Grounded citation links) |
| **Reasoning & Synthesis** | None | High | High |

> [!NOTE]
> Never treat an LLM as a static database. To build accurate enterprise applications, use **RAG** (Retrieval-Augmented Generation) to supply verified data in the prompt context while leveraging the LLM exclusively for reasoning and synthesis.

---

## 03. Tokenization and Context Windows

🔗 **Full Lesson:** [03_Tokenization_and_Context_Windows.md](./Season_01/03_Tokenization_and_Context_Windows.md)

* **What**: The fundamental preprocessing layer that translates human text into numerical TokenIDs (Encoding) and back (Decoding), alongside the mathematical memory constraints (Context Length & Active Context Window) governing LLMs.
* **Why It Exists**: Explains how LLMs process text without understanding words natively, why API pricing is billed per token, how subword algorithms (BPE, WordPiece, Unigram) eliminate Out-of-Vocabulary errors, and why long prompts experience accuracy degradation.
* **Key Concepts**:
  * **Words vs Characters vs Subwords**: Word tokenization creates massive vocabularies; character tokenization creates long sequences ($O(N^2)$ attention compute); subword tokenization provides an optimal trade-off (e.g., `"Un"` + `"trust"` + `"able"`).
  * **Subword Algorithms**: BPE (Byte Pair Encoding - greedy merge of frequent character pairs, used by OpenAI & LLaMA), WordPiece (BERT likelihood merge), and Unigram (SentencePiece top-down pruning).
  * **Multilingual Fertility Bias**: Ratio of tokens to words ($\frac{\text{Tokens}}{\text{Words}}$). Non-English languages (Hindi, Arabic) generate 2x to 4x more tokens per word due to English-centric training corpora, spiking API costs and shrinking effective memory.
  * **Tokenization Edge Cases**: Capitalization (`"Apple"` vs `"apple"`), Whitespace, Emojis (multi-byte Unicode splitting), and Code syntax.
  * **Special Tokens**: Control tokens like `<|im_start|>`, `<|im_end|>`, and `<|tool_call|>` defining conversational structure and safety boundaries.
  * **Context Length vs Context Window**: Context Length is the hard ceiling imposed by model architecture/hardware (e.g., 128k); Context Window is the active payload shared between System Prompt + History + RAG Context + Generated Output.
  * **Context Overflow Strategies**: Request rejection, truncation, sliding window FIFO pruning, context summarization, selective RAG retrieval, and task chunking.
  * **The "Lost in the Middle" Effect**: Recall accuracy is high at the beginning (Primacy) and end (Recency) of prompts, but drops significantly for information in central positions.

### Tokenization Algorithm Comparison Matrix

| Feature | Byte Pair Encoding (BPE) | WordPiece | Unigram |
| :--- | :--- | :--- | :--- |
| **Direction** | Bottom-up (Merge) | Bottom-up (Merge) | Top-down (Prune) |
| **Merge Criterion** | Pair Frequency | Maximum Likelihood | Loss Minimization |
| **Popular Models** | GPT-3.5, GPT-4, LLaMA, Mistral | BERT, RoBERTa | SentencePiece, T5 |
| **OOV Handling** | 100% Coverage (Falls back to bytes/chars) | 100% Coverage (`[UNK]` or subwords) | 100% Coverage |

> [!WARNING]
> Do not assume longer prompts lead to better LLM responses. Irrelevant text increases API costs, spikes inference latency, and triggers the "Lost in the Middle" effect, causing the model to miss critical instructions.

---
