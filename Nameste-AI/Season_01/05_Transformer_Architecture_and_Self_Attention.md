# 🤖 Transformer Architecture and Self-Attention

## 📌 Overview

The **Transformer** is the foundational neural network architecture behind almost every modern frontier AI model, including **ChatGPT (GPT-4o), Claude 3.5, Gemini, LLaMA 3, Mistral, and DeepSeek**.

Introduced by Google researchers in the seminal 2017 paper [*"Attention Is All You Need"*](https://arxiv.org/abs/1706.03762), the Transformer completely replaced previous sequential architectures (like RNNs and LSTMs) by relying entirely on a mathematical mechanism called **Self-Attention**.

* **ChatGPT Acronym**:
  * **G (Generative)**: Synthesizes original text, code, and content.
  * **P (Pre-trained)**: Pre-trained on trillions of tokens of web-scale text using self-supervised next-token prediction.
  * **T (Transformer)**: The underlying neural network architecture that processes sequences in parallel using attention mechanisms.

> **The Golden Rule of Modern AI:**  
> *"Without the Transformer, modern Large Language Models do not exist. Without Self-Attention, the Transformer is nothing."*

```
                           THE COMPLETE TRANSFORMER PIPELINE
                           
  Raw Input Text: "The pizza is _____"
         │
         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. Tokenizer (BPE) ──► TokenIDs: [464, 7421, 318]           │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 2. Embeddings (Token Vector + Positional Encoding)          │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 3. N Stacked Transformer Decoder Blocks (e.g., 32–96 layers)│
  │    ├── LayerNorm (Input Stabilization)                      │
  │    ├── Multi-Head Causal Self-Attention (Token Communication)│
  │    ├── Residual Add (+ Skip Connection)                     │
  │    ├── LayerNorm (Feature Normalization)                    │
  │    ├── Feed-Forward Network / MLP (Token Computation)       │
  │    └── Residual Add (+ Skip Connection)                     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 4. Output Linear Head ──► Unnormalized Logits               │
  │    ["ready": 4.2, "hot": 3.8, "cold": -1.2, "car": -8.5]    │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 5. Softmax Function ──► Probabilities (Sum to 100%)         │
  │    P("ready") = 82% | P("hot") = 15% | P("cold") = 3%       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  Selected Next Token: "ready" ──► Append to input and repeat!
```

---

## 🎯 Why This Matters

Before 2017, sequence models like **Recurrent Neural Networks (RNNs)** and **Long Short-Term Memory networks (LSTMs)** processed words one by one sequentially from left to right. This created two fatal roadblocks:
1. **The Sequential Compute Bottleneck**: Because Word 5 depended on Word 4, GPUs could not train on entire sentences in parallel ($O(N)$ sequential operations).
2. **Catastrophic Forgetting & Vanishing Gradients**: Over long sequences ($>100$ tokens), RNN hidden states lost information from earlier words.

The **Transformer** solved both problems:
* **Massive Parallelization**: All tokens in a sequence are processed simultaneously during training on GPU clusters.
* **Direct Token-to-Token Access**: Self-attention allows every token to directly look at any other token in the sequence ($O(1)$ path length), regardless of distance.

---

## 🧠 Prerequisites

| Concept | Explanation |
| :--- | :--- |
| **Autoregression** | A process where a model generates an output token, appends it to its input prompt, and feeds the combined text back into itself to generate the next token. |
| **Logits** | The raw, unnormalized numerical scores output by the final linear layer of a neural network before conversion to probabilities. |
| **Softmax** | A mathematical function that squashes an array of arbitrary numbers into valid probabilities between `0` and `1` that sum exactly to `1.0`. |
| **Matrix Multiplication ($Q \times K^T$)** | The fundamental linear algebra operation used by GPUs to calculate how strongly tokens attend to one another. |

---

## 🔍 Deep Dive: The Transformer Architecture Step-by-Step

---

### Part 1: The Autoregressive Generation Loop ("The pizza is ___")

How does an LLM actually write a complete paragraph? It does so token by token in an **autoregressive loop**:

```
Step 1: Input  = "The pizza is"
        Model  = Calculates probabilities over vocabulary:
                 - "ready"     ──► 82% (Selected)
                 - "hot"       ──► 12%
                 - "delicious" ──►  4%
                 - "expensive" ──►  2%

Step 2: Input  = "The pizza is ready"
        Model  = Predicts next token:
                 - "to"        ──► 91% (Selected)
                 - "and"       ──►  6%
                 - "now"       ──►  3%

Step 3: Input  = "The pizza is ready to"
        Model  = Predicts next token:
                 - "eat"       ──► 95% (Selected)

Final Generated Sentence: "The pizza is ready to eat."
```

Depending on the sampling strategy (e.g., Temperature, Top-P), the model can generate creative variations:
* *"The pizza is delicious and ready to eat."*
* *"The pizza is hot and fresh out of the oven."*
* *"The pizza is not ready yet."*

---

### Part 2: The Heart of the Transformer – Self-Attention Mechanism

#### The Core Question of Attention:
> *"Which other pieces of information in this sentence should I focus on right now, and how much weight should I give them?"*

Consider the sentence:
> **"The animal didn't cross the street because it was too tired."**

When the model processes the pronoun **"it"**, what does **"it"** refer to? The *animal* or the *street*?

```
      "The animal didn't cross the street because it was too tired."
           ▲                                       │
           │─────────── (High Attention: 88%) ─────┘
                                                   │
      "The animal didn't cross the street because it was too wide."
                                  ▲                │
                                  │── (High: 84%) ─┘
```

* If the sentence ends with **"too tired"**, the attention mechanism assigns high weight between **"it"** and **"animal"**.
* If the sentence ends with **"too wide"**, the attention mechanism shifts its focus, assigning high weight between **"it"** and **"street"**.

#### Resolving Ambiguity & Polysemy:
In Class 04, we learned about polysemy (words with multiple meanings). Self-attention allows words to absorb context from their neighbors:
* In *"I went to the **bank** to deposit **money**"*, the token `"bank"` attends strongly to `"deposit"` and `"money"`, shifting its vector toward *finance*.
* In *"I sat on the **bank** of the **river**"*, `"bank"` attends strongly to `"river"` and `"water"`, shifting its vector toward *geography*.

---

### Part 3: The Query, Key, and Value ($Q, K, V$) Analogy

Under the mathematical hood, Self-Attention is structured like a **database retrieval system** or a **library search**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          THE LIBRARY SEARCH ANALOGY                         │
│                                                                             │
│  1. Query (Q)  : What you are looking for.                                  │
│                  (e.g., "I need a book on Italian Cooking")                 │
│                                                                             │
│  2. Key (K)    : The title / label on every book on the library shelf.      │
│                  (e.g., "History", "Italian Cooking", "Quantum Physics")    │
│                                                                             │
│  3. Attention  : Match Query against all Keys (Dot Product) to calculate   │
│     Score        relevance weights (Softmax).                               │
│                                                                             │
│  4. Value (V)  : The actual contents/information inside the matching book.  │
│                  Extract the information scaled by the relevance score!     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### The Mathematical Formula for Scaled Dot-Product Attention:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

1. **$Q \times K^T$ (Dot Product)**: Compares every token's Query with every other token's Key to calculate raw affinity scores.
2. **$\frac{1}{\sqrt{d_k}}$ (Scaling Factor)**: Divides by the square root of the key dimension ($d_k$) to prevent dot products from growing excessively large, which would cause vanishing gradients in the Softmax function.
3. **$\text{softmax}(\dots)$**: Converts affinity scores into percentage weights ($0.0$ to $1.0$) across all tokens, summing to $100\%$.
4. **$\times V$ (Value Weighting)**: Multiplies the attention percentages by the Value vectors to produce the final context-enriched representation.

---

### Part 4: Multi-Head Causal Self-Attention

Modern LLMs (GPT, LLaMA, Claude) use a specialized variant: **Multi-Head Causal Self-Attention**.

```
                           MULTI-HEAD CAUSAL SELF-ATTENTION
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│   1. Self-Attention  │     │ 2. Causal (Masked)   │     │    3. Multi-Head     │
│ Tokens gather info   │     │ Tokens can only look │     │ Multiple attention   │
│ from other tokens in │     │ at PAST tokens, never│     │ heads run in         │
│ the same sequence.   │     │ future tokens.       │     │ parallel.            │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

#### 1. Why "Causal" (Masked)?
During text generation, the future does not exist yet. When predicting the word after `"The pizza is"`, the model must **never look ahead** at future tokens.
* **Causal Masking**: An upper-triangular matrix of $-\infty$ (negative infinity) is applied before Softmax, forcing attention scores for all future tokens to become $0\%$.
* **Information Flow**: Only flows in one direction: **Past $\rightarrow$ Present**.

```
                        Causal Attention Mask Matrix
                 "The"    "pizza"    "is"     "ready"
         "The"  [ 0.85,   -inf,     -inf,     -inf  ] ──► Can only see "The"
       "pizza"  [ 0.30,    0.70,    -inf,     -inf  ] ──► Can see "The", "pizza"
          "is"  [ 0.10,    0.40,     0.50,    -inf  ] ──► Can see "The", "pizza", "is"
       "ready"  [ 0.05,    0.35,     0.20,     0.40 ] ──► Can see all past tokens
```

#### 2. Why "Multi-Head"?
Instead of computing one single attention calculation, the model splits vectors into **multiple heads** (e.g., 32, 64, or 128 heads) running in parallel.
* **Head 1**: Specializes in tracking grammar and subject-verb agreements.
* **Head 2**: Specializes in pronoun resolution (*"it"* $\rightarrow$ *"animal"*).
* **Head 3**: Specializes in semantic relationships (*"pizza"* $\rightarrow$ *"eat"*).
* All heads are concatenated together at the end of the layer.

---

### Part 5: Residual / Skip Connections ($x + \text{SubLayer}(x)$)

Deep neural networks often suffer from the **Vanishing Gradient Problem**: as networks get deeper ($32-128+$ layers), signals weaken as they pass through multiple matrix multiplications.

Transformers solve this using **Residual (Skip) Connections**:

```
                       Input Vector: x = [1.0, 2.0, 3.0]
                                 │
                 ┌───────────────┴───────────────┐
                 │ (Skip Highway)                │
                 │                               ▼
                 │                    ┌─────────────────────┐
                 │                    │  Attention Sublayer │
                 │                    └──────────┬──────────┘
                 │                               │ Output: [0.2, -0.5, 0.7]
                 │                               ▼
                 └──────────────────────────► ( + Add )
                                                 │
                                                 ▼
                                     New Output: [1.2, 1.5, 3.7]
```

* **Core Idea**: Instead of forcing the layer to rebuild the entire representation from scratch, the layer only learns a **small delta update**, which is added directly to the original input.
* **Benefit**: Gradients flow backward uninterrupted through the skip highway during backpropagation, enabling stable training of massive 100+ layer networks.

---

### Part 6: Layer Normalization (LayerNorm & RMSNorm)

As vectors repeatedly pass through attention layers, FFNs, and residual additions, their numerical values can explode into extreme magnitudes ($[0.2, -0.3] \rightarrow [22.0, 154.0]$), destabilizing training.

* **LayerNorm**: Normalizes the numbers across each token's feature vector so they have a **mean of 0** and a **variance of 1**, followed by learnable scaling parameters.
* **RMSNorm (Modern LLMs)**: A faster variant used in LLaMA and Mistral that scales vectors by their Root Mean Square without calculating the mean, reducing GPU compute overhead.

---

### Part 7: Feed-Forward Network (FFN / MLP)

Every Transformer block contains a position-wise Feed-Forward Network following the attention layer:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ATTENTION vs. FEED-FORWARD NETWORK                       │
│                                                                             │
│  1. Self-Attention Layer:                                                   │
│     - Tokens COMMUNICATE and share information with each other.             │
│     - Contextualizes representations across sequence length.                │
│                                                                             │
│  2. Feed-Forward Network (FFN / MLP):                                       │
│     - Every token is processed INDEPENDENTLY in parallel.                   │
│     - Tokens DO NOT communicate with other tokens during FFN.               │
│     - Acts as the model's "factual memory bank" and reasoning compute.      │
│                                                                             │
│  "Attention lets tokens TALK; the Feed-Forward Network lets each token THINK."│
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Structure**: $\text{FFN}(x) = \text{Activation}(x W_1 + b_1) W_2 + b_2$
* **Modern Activations**: Older models used ReLU; modern LLMs use **GELU** or **SwiGLU** for smoother gradient transitions.

---

### Part 8: Output Head: Logits to Probabilities via Softmax

At the very top of the Transformer stack, the final token representation vector (e.g., 4,096 dimensions) is projected onto the entire vocabulary ($32,000-128,000$ tokens) using a **Linear Layer**:

```
Final Vector ──► [Linear Layer] ──► Logits (Raw Scores) ──► [Softmax] ──► Probabilities
                                    "ready"  :  4.2                       "ready"  : 62.0%
                                    "hot"    :  3.1                       "hot"    : 23.0%
                                    "cold"   :  1.2                       "cold"   : 11.0%
                                    "pizza"  : -0.5                       "pizza"  :  4.0%
                                                                          ─────────────────
                                                                          Total    : 100.0%
```

#### The Softmax Formula:
$$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{V} e^{z_j}}$$

* Converts negative, zero, or large positive numbers into positive values between $0.0$ and $1.0$.
* Guarantees that all vocabulary probabilities sum up to exactly $1.0$ ($100\%$).

---

## 🌐 Interactive 3D Visualization

To see animated data flowing through every attention head, residual connection, and FFN layer in real time, explore:
* **Interactive 3D LLM Visualizer**: [https://bbycroft.net/llm](https://bbycroft.net/llm)

---

## 📊 Summary Comparison: Transformer Components

| Component | Primary Function | Interaction Scope | Analogy |
| :--- | :--- | :--- | :--- |
| **Embeddings** | Convert TokenIDs + Position into vectors | Per Token | Translating words into coordinate points |
| **Self-Attention** | Exchange information between tokens | **Cross-Token** (All to All) | A group discussion in a meeting room |
| **Causal Mask** | Restrict attention to past/current tokens | Sequence Order | Reading a book without peeking at future pages |
| **Residual Connection** | Add input back to layer output ($x + f(x)$) | Per Layer | Incremental draft editing rather than rewrite |
| **LayerNorm / RMSNorm** | Stabilize vector scales to zero-mean/unit-var | Per Vector | Volume normalizer on an audio track |
| **Feed-Forward (FFN)** | Deep nonlinear processing & memory recall | **Per Token** (Independent) | An individual thinking quietly at their desk |
| **Softmax Head** | Convert logits into probability distribution | Vocabulary-wide | Voting ballot tallying final percentages |

---

## 💡 Simple Example: Step-by-Step Matrix Attention by Hand

Let's calculate Self-Attention for 2 simplified 2D tokens: `T1: "The"`, `T2: "Pizza"`:

```text
Query Matrix (Q):            Key Matrix (K):             Value Matrix (V):
T1 = [1.0, 0.0]              T1 = [1.0, 0.0]             T1 = [0.5, 0.2]
T2 = [0.0, 1.0]              T2 = [0.5, 0.5]             T2 = [0.8, 0.9]

Step 1: Compute Q * K^T (Dot Product Scores)
Score(T1, T1) = (1.0*1.0) + (0.0*0.0) = 1.0
Score(T1, T2) = (1.0*0.5) + (0.0*0.5) = 0.5

Step 2: Scale by sqrt(d_k) (where d_k = 2, sqrt(2) ≈ 1.414)
Scaled(T1, T1) = 1.0 / 1.414 ≈ 0.707
Scaled(T1, T2) = 0.5 / 1.414 ≈ 0.353

Step 3: Apply Softmax
e^(0.707) ≈ 2.028, e^(0.353) ≈ 1.423, Sum = 3.451
Weight(T1, T1) = 2.028 / 3.451 ≈ 0.588 (58.8%)
Weight(T1, T2) = 1.423 / 3.451 ≈ 0.412 (41.2%)

Step 4: Multiply Weights by Value Matrix (V)
Output(T1) = 0.588 * [0.5, 0.2] + 0.412 * [0.8, 0.9]
           = [0.294, 0.118] + [0.330, 0.371]
           = [0.624, 0.489] (Enriched Contextual Representation!)
```

---

## 🏗️ Real-World Example: Architecture of LLaMA 3 (8B / 70B)

Modern state-of-the-art open-weights models build directly upon this exact Transformer architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      LLaMA 3 (8B / 70B)                     │
│                                                             │
│  - Architecture: Decoder-Only Transformer                   │
│  - Vocabulary Size: 128,256 Tokens (tiktoken BPE)           │
│  - Context Length: 8,192 to 128,000 Tokens                  │
│  - Attention: Grouped-Query Attention (GQA) with RoPE       │
│  - Normalization: RMSNorm (Root Mean Square Normalization)  │
│  - Feed-Forward: SwiGLU Activation Function                 │
│  - Layers: 32 Layers (8B) / 80 Layers (70B)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Common Mistakes & Pitfalls

* **Mistake 1: Confusing Causal Attention (GPT) with Bidirectional Attention (BERT)**
  * *Correction*: GPT uses **Causal (Masked) Attention** to generate text one token at a time from left to right. BERT uses **Bidirectional Attention** (no masking) to understand entire sentences at once for classification/embeddings, but cannot generate autoregressive text.
* **Mistake 2: Believing tokens communicate during the Feed-Forward (FFN) step**
  * *Correction*: FFN layers operate strictly on each token in isolation ($1 \times D$). The **only** place tokens communicate across sequence positions is inside the **Self-Attention** layer.
* **Mistake 3: Assuming all tokens are generated simultaneously during inference**
  * *Correction*: Training runs across all tokens in parallel using causal masking. However, **inference is strictly sequential (autoregressive)**—each token must be generated before it can be fed back to generate the next.

---

## 🔥 Important Points to Remember

* **ChatGPT stands for Generative Pre-trained Transformer**.
* **Self-Attention** calculates relevance weights between all tokens in a sequence ($\text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$).
* **Causal Masking** ensures tokens only attend to past and current tokens, preventing future token leakage during generation.
* **Multi-Head Attention** allows the model to simultaneously attend to syntax, semantics, and reference relationships in parallel subspaces.
* **Residual Connections ($x + f(x)$)** prevent vanishing gradients and allow layers to learn additive updates.
* **LayerNorm / RMSNorm** stabilizes vector magnitudes across deep stacks of layers.
* **Attention lets tokens communicate; FFN lets each token think**.
* **Softmax** converts raw linear logits into a valid probability distribution summing to $1.0$.

---

## 💻 Code / Commands / Configuration

### Complete JavaScript (Node.js) Transformer Core Simulation

```javascript
// =====================================================================
// 1. Softmax Function Implementation
// =====================================================================
function softmax(logits) {
  const maxLogit = Math.max(...logits); // Numerical stability trick
  const expScores = logits.map(z => Math.exp(z - maxLogit));
  const sumExp = expScores.reduce((acc, val) => acc + val, 0);
  return expScores.map(score => score / sumExp);
}

console.log("=== 1. Softmax Demonstration ===");
const rawLogits = [4.2, 3.1, 1.2, -0.5]; // e.g., ["ready", "hot", "cold", "pizza"]
const probabilities = softmax(rawLogits);
console.log("Vocabulary Probabilities:", probabilities.map(p => (p * 100).toFixed(2) + "%"));


// =====================================================================
// 2. Scaled Dot-Product Attention Simulation
// =====================================================================
function scaledDotProductAttention(Q, K, V, isCausal = true) {
  const seqLen = Q.length;
  const d_k = Q[0].length;
  const scale = Math.sqrt(d_k);

  // Compute Q * K^T (Attention Scores Matrix)
  const scores = [];
  for (let i = 0; i < seqLen; i++) {
    scores[i] = [];
    for (let j = 0; j < seqLen; j++) {
      if (isCausal && j > i) {
        // Causal Mask: cannot look into future tokens
        scores[i][j] = -Infinity;
      } else {
        // Dot product between Q[i] and K[j]
        let dot = 0;
        for (let d = 0; d < d_k; d++) {
          dot += Q[i][d] * K[j][d];
        }
        scores[i][j] = dot / scale;
      }
    }
  }

  // Apply Softmax row-wise to get Attention Weights
  const attentionWeights = scores.map(row => softmax(row));

  // Multiply Attention Weights by Value Matrix (V)
  const output = [];
  for (let i = 0; i < seqLen; i++) {
    output[i] = new Array(V[0].length).fill(0);
    for (let j = 0; j < seqLen; j++) {
      const weight = attentionWeights[i][j];
      for (let d = 0; d < V[0].length; d++) {
        output[i][d] += weight * V[j][d];
      }
    }
  }

  return { attentionWeights, output };
}

console.log("\n=== 2. Scaled Dot-Product Attention with Causal Mask ===");
const sampleQ = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]; // 3 tokens: ["The", "pizza", "is"]
const sampleK = [[1.0, 0.0], [0.5, 0.5], [0.2, 0.8]];
const sampleV = [[0.5, 0.2], [0.8, 0.9], [0.1, 0.4]];

const result = scaledDotProductAttention(sampleQ, sampleK, sampleV, true);
console.log("Causal Attention Weights (Past tokens only):");
console.table(result.attentionWeights.map(row => row.map(v => v.toFixed(3))));


// =====================================================================
// 3. Mini Transformer Block: Residual Connection + Feed-Forward
// =====================================================================
function miniTransformerLayer(inputVector) {
  // 1. Attention sublayer simulation
  const attentionDelta = inputVector.map(x => x * 0.1 - 0.05);

  // 2. Residual Connection 1: x + Attention(x)
  const postAttention = inputVector.map((x, i) => x + attentionDelta[i]);

  // 3. Layer Normalization (Simplified)
  const mean = postAttention.reduce((a, b) => a + b, 0) / postAttention.length;
  const normalized = postAttention.map(x => x - mean);

  // 4. Feed-Forward Network (FFN / MLP) simulation
  const ffnDelta = normalized.map(x => Math.max(0, x * 1.5)); // ReLU activation

  // 5. Residual Connection 2: x + FFN(x)
  const finalOutput = normalized.map((x, i) => x + ffnDelta[i]);

  return finalOutput;
}

console.log("\n=== 3. Mini Transformer Layer Execution ===");
const tokenVector = [1.0, 2.0, 3.0, 4.0];
console.log("Input Vector:        ", tokenVector);
console.log("Transformer Output:  ", miniTransformerLayer(tokenVector).map(v => v.toFixed(3)));
```

---

## 🎤 Interview Perspective

| Common Interview Question | What the Interviewer Is Really Testing | High-Scoring Answer Key Points |
| :--- | :--- | :--- |
| **"Why did Transformers replace RNNs and LSTMs in modern NLP?"** | Deep understanding of architectural bottlenecks and GPU parallelization. | RNNs process tokens sequentially ($O(N)$ time steps), preventing GPU parallelization during training and suffering from vanishing gradients over long contexts. Transformers use Self-Attention to process all tokens simultaneously ($O(1)$ sequential operations) and connect any two tokens directly regardless of distance. |
| **"What is the purpose of the Scaling Factor ($\frac{1}{\sqrt{d_k}}$) in Attention?"** | Mathematical grasp of dot products and Softmax gradient behavior. | As the vector dimension $d_k$ grows, dot products grow large in magnitude, pushing the Softmax function into regions with extremely small gradients (vanishing gradients). Dividing by $\sqrt{d_k}$ stabilizes the variance of dot products to $1.0$, ensuring stable gradient flow during backpropagation. |
| **"Explain the difference between Self-Attention and the Feed-Forward Network (FFN) inside a Transformer block."** | Knowledge of cross-token communication vs position-wise computation. | Self-Attention is the only layer where tokens **communicate across sequence positions** to exchange context. The FFN layer processes every token **independently in parallel** using dense linear layers and non-linear activations, acting as the model's factual memory storage. |
| **"Why are Residual (Skip) Connections essential in deep Transformers?"** | Understanding of gradient propagation in 100+ layer deep neural networks. | Residual connections ($x + \text{SubLayer}(x)$) create an uninterrupted highway for gradients to flow backward during backpropagation. Instead of forcing layers to rebuild representations from scratch, layers learn incremental additive updates, preventing gradient degradation in deep models. |

---

## 🧩 Connection With Previous Concepts

* **Connection to Season 01, Class 04**: In Class 04, we learned how **Vector Embeddings** represent words as static coordinates. In Class 05, we saw how the **Transformer's Self-Attention Mechanism** takes those static embeddings and dynamically contextualizes them through multi-layer attention stacks.
* **Bridge to Class 06**: In the next lesson, we will explore **Model Training, Fine-Tuning (SFT, LoRA), and Reinforcement Learning from Human Feedback (RLHF)** to understand how a raw Transformer becomes an aligned conversational assistant.

---

Previous : [04. Vector Embeddings and Semantic Search](./04_Vector_Embeddings_and_Semantic_Search.md) | Index: [00_index.md](../00_index.md) | Next: [06. Neural Network Training and Optimization](./06_Neural_Network_Training_and_Optimization.md)
