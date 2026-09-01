# 🤖 Neural Network Training and Optimization

## 📌 Overview

In the previous lessons, we explored how Transformers use **Self-Attention** to process tokens and generate probabilities. But where do the trillions of magical numbers inside a model come from? How does an uninitialized, random neural network transform into an intelligent assistant?

The answer is **Training (Optimization)**—often described as *"Sharpening the Computational Brain"*.

* **Parameters (Weights & Biases)**: The adjustable numerical values stored across all layers of a neural network that dictate how input vectors are transformed.
* **Learning**: The iterative mathematical process of adjusting a network's parameters to minimize its prediction error on training data.
* **The Core Training Loop**:
  $$\text{Input Data} \xrightarrow{\text{Forward Pass}} \text{Prediction} \xrightarrow{\text{Loss Function}} \text{Error Score} \xrightarrow{\text{Backpropagation}} \text{Gradients} \xrightarrow{\text{Optimizer}} \text{Updated Weights}$$

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         THE 5-STEP TRAINING CYCLE                           │
│                                                                             │
│   1. Forward Pass       : Input text flows through network to get logits.  │
│                                   │                                         │
│                                   ▼                                         │
│   2. Loss Calculation   : Measure how wrong the prediction was.             │
│                                   │                                         │
│                                   ▼                                         │
│   3. Backpropagation    : Use calculus (Chain Rule) to calculate gradients  │
│                           for every single parameter in the network.        │
│                                   │                                         │
│                                   ▼                                         │
│   4. Optimizer Step     : Adjust weights in the opposite direction of the   │
│                           gradient using a Learning Rate.                   │
│                                   │                                         │
│                                   ▼                                         │
│   5. Repeat Billions of Times across trillions of training tokens!          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Why This Matters

Understanding training mechanics demystifies how AI models work and reveals their real-world engineering constraints:
* **Explains Model Cost & Scale**: Training a 70B+ model requires millions of dollars in compute, thousands of interconnected GPUs, and weeks of continuous execution.
* **Explains Why Models Make Mistakes**: LLMs do not "know" facts; they learn statistical probability manifolds. Gaps or biases in training data directly dictate model errors.
* **Core Hyperparameters in Fine-Tuning**: When adapting models via SFT or LoRA, developers must configure **Learning Rates**, **Batch Sizes**, **Epochs**, and **Loss Functions**.
* **Diagnosing Failure Modes**: Understanding **Overfitting**, **Underfitting**, and **Gradient Explosion/Vanishing** is essential for any AI engineer.

---

## 🧠 Prerequisites

| Concept | Explanation |
| :--- | :--- |
| **Parameter / Weight** | An internal tunable floating-point number inside a neural network layer. |
| **Loss / Cost** | A single numerical score measuring the difference between the model's prediction and the actual ground-truth target. |
| **Gradient ($\nabla L$)** | The vector of partial derivatives indicating the direction and rate of fastest increase of the loss function. |
| **Learning Rate ($\alpha$)** | A hyperparameter controlling the step size taken during weight updates. |
| **Epoch** | One complete training pass through the entire training dataset. |

---

## 🔍 Deep Dive: Training the Computational Brain

---

### Part 1: What Does "Learning" Actually Mean for a Machine?

A neural network starts its life completely untrained—its parameters are initialized with **random numbers**. 

```text
Untrained Model Prompt: "The capital of France is _____"
Model Output: "elephant" (Probability: 0.0001%) | Random Gibberish!
```

During training, we repeatedly feed trillions of words into the model. **Learning** means continuously tweaking those billions of numbers until the output probability for `"Paris"` becomes $99.9\%$.

```
                           WHERE PARAMETERS LIVE IN AN LLM
                           
  Total Parameters = Embedding Weights + Attention Weights + FFN Weights + LayerNorm
  
  1. Embedding Table     : Matrix mapping TokenIDs to D-dimensional vectors.
  2. Self-Attention      : Projection matrices W_q, W_k, W_v, and W_o per head.
  3. Feed-Forward (MLP)  : Dense expansion and projection matrices W_1, W_2, W_3.
  4. Layer Normalization : Learnable scaling parameters (gamma, beta).
```

#### Frontier Model Parameter Scale:
* **GPT-3 (2020)**: $175\text{ Billion parameters}$
* **LLaMA 3 (2024)**: $8\text{ Billion} \rightarrow 70\text{ Billion} \rightarrow 405\text{ Billion parameters}$
* **GPT-4 (MoE)**: $\approx 1.8\text{ Trillion parameters}$ (Mixture of Experts across multiple sub-networks)

#### Do Parameters Store Knowledge like a Database?
**No.** Parameters do not store text strings, rows, or dictionary key-values.
* Parameters store **mathematical patterns and linguistic relationships**.
* When an LLM outputs `"Paris"`, it is not reading a text file; its parameters have adjusted so that the mathematical matrix multiplication of `"The capital of France is"` produces the highest logit score for token ID `Paris`.
* Knowledge emerges from the **collective interaction** of billions of weights.

---

### Part 2: Forward Pass & The Loss Function

#### 1. The Forward Pass
The forward pass is the standard execution of data moving from input to output:
$$\text{Tokens} \rightarrow \text{Embeddings} \rightarrow \text{Transformer Layers} \rightarrow \text{Logits} \rightarrow \text{Softmax Probabilities}$$

#### 2. The Loss Function (Measuring the Mistake)
A Loss Function converts the quality of a prediction into a single number:
* **Correct / Confident Prediction**: Loss is **small** ($\approx 0.01$).
* **Incorrect / Unsure Prediction**: Loss is **large** ($\ge 4.50$).

```
Example: Target Token is "blue" for input "The sky is _____"

Prediction A: P("blue") = 92%  ──►  Loss = -ln(0.92) = 0.083  (Low Loss! Good prediction)
Prediction B: P("blue") =  4%  ──►  Loss = -ln(0.04) = 3.218  (High Loss! Bad prediction)
```

For classification and next-token prediction, LLMs use **Cross-Entropy Loss**:

$$\mathcal{L} = -\sum_{i=1}^{V} y_i \ln(\hat{y}_i) = -\ln(P(\text{Target Token}))$$

---

### Part 3: Backpropagation & Gradients (Finding Who Made the Mistake)

When a model with 70 billion parameters makes an incorrect prediction, **which specific weights were responsible, and in which direction should each weight be adjusted?**

```
                                  BACKPROPAGATION
                                  
  Loss Score ──► Layer N ──► Layer N-1 ──► Layer N-2 ──► ... ──► Layer 1 (Embeddings)
  
  Calculates: "How much did Weight_ij in Layer_k contribute to the final error?"
              Mathematically: ∂Loss / ∂Weight
```

1. **The Chain Rule of Calculus**: Backpropagation starts at the final loss and moves **backward** through every layer, computing the partial derivative of the loss with respect to every single parameter ($\frac{\partial \mathcal{L}}{\partial w}$).
2. **Gradients**: A gradient is a number that tells us:
   * **Direction**: Should this weight increase ($+$) or decrease ($-$) to lower the loss?
   * **Sensitivity (Magnitude)**: How aggressively does changing this weight affect the loss?

> [!NOTE]
> **Backpropagation does NOT update weights.** Backpropagation only *calculates the gradients (sensitivities)*. The task of updating the weights belongs to the **Optimizer**.

---

### Part 4: Gradient Descent (The Foggy Mountain Analogy)

**Gradient Descent** is the optimization algorithm that takes the gradients computed by backpropagation and updates the parameters to minimize the loss.

```
                            THE FOGGY MOUNTAIN ANALOGY
                            
          High Loss (Peak)
              \
               \   Slope = Gradient (Tells you which way is downhill)
                \
                 \
                  \______ Lowest Loss Valley (Global Minimum!)
```

* **The Analogy**: Imagine being lost on a mountain in thick fog. You cannot see the bottom, but you can feel the slope of the ground under your feet. To reach the valley:
  1. Feel the slope (Compute Gradient).
  2. Take a step in the steepest downhill direction (Subtract Gradient $\times$ Learning Rate).
  3. Repeat until the ground becomes flat (Convergence).

#### The Weight Update Formula:
$$W_{\text{new}} = W_{\text{old}} - \alpha \cdot \nabla \mathcal{L}(W)$$

Where $\alpha$ is the **Learning Rate**.

```
                        THE LEARNING RATE DILEMMA
                        
  1. Learning Rate Too Small (α = 0.000001):
     - Takes tiny microscopic steps.
     - Training is painfully slow and can get stuck in flat regions.
     
  2. Learning Rate Too Large (α = 1.5):
     - Takes massive wild steps.
     - Overshoots the valley and diverges to Infinity / NaN!
     
  3. Optimal Learning Rate with Schedule (e.g., α = 0.0003 with Warmup + Cosine Decay):
     - Fast initial progress, smoothly converging to the minimum error.
```

---

### Part 5: Gradient Descent Variants & Modern Optimizers

```
                      GRADIENT DESCENT OPTIMIZATION VARIANTS
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  1. Batch GD         │     │ 2. Stochastic GD(SGD)│     │ 3. Mini-Batch GD     │
│ Computes gradient    │     │ Computes gradient    │     │ Computes gradient    │
│ across ENTIRE dataset│     │ for ONE single sample│     │ for a small BATCH    │
│ per step.            │     │ at a time.           │     │ (e.g., 32–4096).     │
│ (Stable but very slow│     │ (Fast but extremely  │     │ (THE INDUSTRY        │
│ on big data).        │     │ noisy/erratic).      │     │  STANDARD).          │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

#### Modern Optimizer: AdamW (Adaptive Moment Estimation with Weight Decay)
Standard Stochastic Gradient Descent (SGD) uses a static step size for all parameters. Modern LLMs use **AdamW**:
* **Adaptive Learning Rates**: Maintains individual learning rates for every parameter based on past historical gradients (moving averages).
* **Momentum**: Accelerates gradient descent in consistent directions like a heavy ball rolling downhill.
* **Weight Decay**: Prevents parameters from growing excessively large, acting as a regularizer.

---

### Part 6: Self-Supervised Learning (No Human Labels Needed!)

How do we train models on 15 trillion tokens without paying humans to label billions of sentences?

```
Raw Text: "Artificial intelligence is transforming modern software engineering."

Training Sample 1: Input = "Artificial"                   Target = "intelligence"
Training Sample 2: Input = "Artificial intelligence"      Target = "is"
Training Sample 3: Input = "Artificial intelligence is"   Target = "transforming"
...
```

* **Self-Supervised Learning**: The training data itself provides both the input and the ground-truth target.
* The model hides the next word, tries to predict it, computes Cross-Entropy loss against the actual hidden word, and updates its weights.

---

### Part 7: Core Training Terminology

| Term | Definition | Concrete Example |
| :--- | :--- | :--- |
| **Dataset** | The complete corpus of training examples. | 15 Trillion tokens of web text, books, code. |
| **Batch Size** | The number of training sequences processed together before computing gradients and updating weights. | 2,048 sequences per step. |
| **Training Step** | Exactly one forward pass, loss calculation, backpropagation, and weight update on one batch. | Step #142,500 of 500,000. |
| **Epoch** | Exactly one complete pass through the entire training dataset. | Pre-training usually runs for 1 to 2 epochs; Fine-tuning runs for 3 to 5 epochs. |

---

### Part 8: Training vs Inference

| Metric | Training Phase | Inference Phase (Runtime) |
| :--- | :--- | :--- |
| **Primary Goal** | Teach the model patterns from raw data | Generate answers for user prompts |
| **Weight State** | **Mutable** (updated every step via gradients) | **Frozen** (read-only matrices) |
| **Operations** | Forward Pass $+$ Backward Pass $+$ Optimizer Step | Forward Pass **Only** |
| **Memory Required** | $\approx 4\times$ to $6\times$ Model Size (Weights + Gradients + Optimizer States + Activations) | $\approx 1\times$ Model Size (Weights + KV Cache) |
| **Compute / Hardware** | Thousands of high-end GPUs (H100 clusters) for weeks | Single GPU or shared inference server |
| **Cost** | Millions of dollars per run | Milliseconds, fractions of a cent per query |

---

### Part 9: Generalization vs Overfitting

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OVERFITTING vs. GENERALIZATION                           │
│                                                                             │
│  Training Data: "The sky is blue" (seen 10,000 times)                       │
│                                                                             │
│  1. Overfitted Model (Rote Memorization):                                   │
│     - Input: "The sky is" ──► Output: "blue" (100% confidence)              │
│     - Input: "On a clear afternoon, the heavens appeared" ──► GIBBERISH!    │
│       (Cannot handle slight variations because it only memorized exact rows)│
│                                                                             │
│  2. Generalizing Model (True Learning):                                     │
│     - Understands the underlying semantic concept of atmospheric color.     │
│     - Input: "On a clear afternoon, the heavens appeared" ──► Output: "blue"│
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Generalization**: The ability of a model to perform accurately on novel, unseen data that was never present in its training dataset.
* **Overfitting**: When a model memorizes the noise and exact phrasing of training data, failing on new inputs.
* **Mitigation**: Using massive diverse datasets, Dropout, Weight Decay, and Early Stopping.

---

### Part 10: How Embeddings are Learned from Scratch

In Class 04, we saw that `"King"` clusters near `"Queen"`. Nobody manually typed those coordinates.

```text
Step 1: Embedding table initialized with random numbers:
        "King"  = [ 0.001, -0.042,  0.119]
        "Queen" = [ 0.952,  0.714, -0.881] (Unrelated random vectors!)

Step 2: Model encounters: "The king and queen ruled together."
Step 3: Prediction error produces loss.
Step 4: Backpropagation sends gradients all the way back to the Embedding Table!
Step 5: Vectors for "King" and "Queen" are nudged slightly closer to satisfy the objective.
Step 6: After billions of sentences, semantic clusters naturally crystallize!
```

---

## 📊 Summary Comparison: Gradient Descent Methods

| Method | Data Processed per Step | Update Speed | Stability | Memory Requirement |
| :--- | :--- | :--- | :--- | :--- |
| **Batch GD** | Entire Dataset ($N$) | Very Slow | 100% Deterministic & Smooth | Huge (Cannot fit in GPU VRAM) |
| **Stochastic GD (SGD)** | 1 Sample | Extremely Fast | Highly Noisy / Fluctuates | Minimal |
| **Mini-Batch GD** | Small Batch ($B \approx 32–4096$) | Fast | Balanced & Stable | Fits perfectly in GPU VRAM |

---

## 💡 Simple Example: 1-Weight Manual Gradient Descent

Let's simulate how a single weight $w$ is updated over 2 steps using a simple loss function $\mathcal{L}(w) = (w - 3)^2$:

```text
Goal: Find the value of w that minimizes Loss L(w). (Minimum is at w = 3 where L = 0).
Derivative (Gradient): dL/dw = 2 * (w - 3)
Learning Rate: alpha = 0.1

Initial Weight: w_0 = 10.0

--- Step 1 ---
Loss = (10.0 - 3)^2 = 7^2 = 49.0
Gradient = 2 * (10.0 - 3) = 2 * 7 = +14.0 (Tells us: increasing w increases loss; move w down!)
Weight Update: w_1 = w_0 - (alpha * Gradient)
               w_1 = 10.0 - (0.1 * 14.0) = 10.0 - 1.4 = 8.6

--- Step 2 ---
Loss = (8.6 - 3)^2 = 5.6^2 = 31.36 (Loss decreased from 49.0 -> 31.36!)
Gradient = 2 * (8.6 - 3) = 2 * 5.6 = +11.2
Weight Update: w_2 = 8.6 - (0.1 * 11.2) = 8.6 - 1.12 = 7.48

Repeating this brings w smoothly toward 3.0 (Loss = 0.0)!
```

---

## 🏗️ Real-World Example: Distributed GPU Training (3D Parallelism)

Frontier models cannot fit onto a single GPU. A 70B parameter model in 16-bit precision requires **140 GB of VRAM just to hold its weights**, plus another **500+ GB for gradients and optimizer states during training!**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       3D PARALLELISM ARCHITECTURE                           │
│                                                                             │
│  1. Tensor Parallelism (TP)   : Splits individual weight matrices across     │
│                                 multiple GPUs inside the same node (NVLink).│
│                                                                             │
│  2. Pipeline Parallelism (PP) : Splits layers sequentially across nodes      │
│                                 (e.g., Layers 1–20 on Node 1, 21–40 on Node 2)│
│                                                                             │
│  3. Data Parallelism (DDP/ZeRO): Distributes different data batches across   │
│                                 GPU replicas and averages gradients.        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Common Mistakes & Pitfalls

* **Mistake 1: Confusing Backpropagation with Gradient Descent**
  * *Correction*: **Backpropagation** calculates the gradient vectors via the Chain Rule. **Gradient Descent** is the optimizer that actually applies the updates to change the weights.
* **Mistake 2: Setting the Learning Rate too high**
  * *Correction*: If the learning rate is too large, the optimizer overshoots the minimum loss valley, causing the loss to explode into `NaN` (Not a Number). Always use learning rate warmups and decay schedules.
* **Mistake 3: Believing more training epochs always produce a better model**
  * *Correction*: Training for too many epochs on the same dataset causes **Overfitting**—the model memorizes the exact training text and loses its ability to generalize to new prompts.

---

## 🔥 Important Points to Remember

* **Learning means optimizing parameters** to minimize prediction error on training data.
* **Parameters live across all layers**: Embeddings, Attention matrices ($W_q, W_k, W_v, W_o$), LayerNorm, and FFNs.
* **Forward Pass** pushes data forward to generate predictions; **Loss Function** measures the mistake.
* **Backpropagation** uses the Chain Rule to calculate gradients ($\frac{\partial \mathcal{L}}{\partial w}$) backward through all layers.
* **Gradient Descent** updates weights: $W_{\text{new}} = W_{\text{old}} - \alpha \cdot \nabla \mathcal{L}$.
* **Self-Supervised Learning** eliminates manual human labeling by using the next token as the target.
* **Training mutates weights** (resource-intensive); **Inference reads frozen weights** (fast, cheap).
* **Generalization** is the ultimate goal of machine learning—performing accurately on unseen prompts.

---

## 💻 Code / Commands / Configuration

### Complete JavaScript (Node.js) Training Loop & Gradient Descent Simulation

```javascript
// =====================================================================
// 1. Cross-Entropy Loss Calculation in JavaScript
// =====================================================================
function crossEntropyLoss(predictedProbability) {
  // Prevent log(0) calculation error
  const epsilon = 1e-15;
  const safeProb = Math.max(predictedProbability, epsilon);
  return -Math.log(safeProb);
}

console.log("=== 1. Cross-Entropy Loss Demonstration ===");
console.log("Loss for 95% Confident Correct Prediction:", crossEntropyLoss(0.95).toFixed(4));
console.log("Loss for 10% Unsure Prediction:            ", crossEntropyLoss(0.10).toFixed(4));
console.log("Loss for 0.1% Completely Wrong Prediction:", crossEntropyLoss(0.001).toFixed(4));


// =====================================================================
// 2. Complete Mini Neural Network Training Loop (Linear Neuron)
// =====================================================================
// Model: y_pred = w * x + b
// Objective: Learn w and b to fit target dataset: y = 2x + 1
function trainToyModel() {
  let w = Math.random(); // Initial random weight
  let b = Math.random(); // Initial random bias
  const learningRate = 0.05;
  const epochs = 100;

  // Training Dataset (x -> y)
  const data = [
    { x: 1, y: 3 }, // 2(1) + 1 = 3
    { x: 2, y: 5 }, // 2(2) + 1 = 5
    { x: 3, y: 7 }, // 2(3) + 1 = 7
    { x: 4, y: 9 }  // 2(4) + 1 = 9
  ];

  console.log("\n=== 2. Training Loop Execution ===");
  console.log(`Initial Random Parameters: Weight = ${w.toFixed(4)}, Bias = ${b.toFixed(4)}`);

  for (let epoch = 1; epoch <= epochs; epoch++) {
    let totalLoss = 0;
    let gradW = 0;
    let gradB = 0;

    // Mini-Batch Forward & Backward Pass
    for (const sample of data) {
      // 1. Forward Pass
      const yPred = w * sample.x + b;
      const error = yPred - sample.y;
      totalLoss += Math.pow(error, 2); // Mean Squared Error

      // 2. Backpropagation (Calculate Gradients)
      gradW += 2 * error * sample.x;
      gradB += 2 * error;
    }

    // Average gradients over batch
    gradW /= data.length;
    gradB /= data.length;
    totalLoss /= data.length;

    // 3. Optimizer Step (Gradient Descent Update)
    w = w - learningRate * gradW;
    b = b - learningRate * gradB;

    if (epoch % 20 === 0 || epoch === 1) {
      console.log(`Epoch ${epoch.toString().padStart(3, ' ')} | Loss: ${totalLoss.toFixed(5)} | w: ${w.toFixed(4)} | b: ${b.toFixed(4)}`);
    }
  }

  console.log(`\nFinal Learned Model: y = ${w.toFixed(2)}x + ${b.toFixed(2)} (Target: y = 2x + 1)`);
}

trainToyModel();


// =====================================================================
// 3. Learning Rate Simulation (Small vs Large vs Optimal)
// =====================================================================
function simulateLearningRates() {
  console.log("\n=== 3. Learning Rate Convergence Simulation ===");
  const targetMin = 3.0; // Function: L(w) = (w - 3)^2
  
  const testRates = [0.001, 0.1, 1.1]; // Too small, Optimal, Too large

  testRates.forEach(alpha => {
    let w = 10.0;
    for (let step = 0; step < 5; step++) {
      const grad = 2 * (w - targetMin);
      w = w - alpha * grad;
    }
    console.log(`Learning Rate: ${alpha.toString().padEnd(5, ' ')} -> Weight after 5 steps: ${w.toFixed(4)}`);
  });
}

simulateLearningRates();
```

---

## 🎤 Interview Perspective

| Common Interview Question | What the Interviewer Is Really Testing | High-Scoring Answer Key Points |
| :--- | :--- | :--- |
| **"What is the difference between Backpropagation and Gradient Descent?"** | Fundamental understanding of optimization algorithms. | **Backpropagation** is the backward pass algorithm that uses the Chain Rule of Calculus to compute the partial derivatives (gradients) of the loss with respect to each parameter. **Gradient Descent** is the optimizer that takes those calculated gradients and updates the parameter values ($W \leftarrow W - \alpha \nabla W$). |
| **"Why do we use Mini-Batch Gradient Descent instead of Full Batch or Single-Sample SGD?"** | Knowledge of compute efficiency and GPU vectorization. | Full Batch GD computes gradients over the entire dataset, which is stable but too slow and cannot fit into GPU memory. Stochastic GD (1 sample) is noisy and fails to utilize GPU parallelism. Mini-Batch GD strikes the optimal balance: it fits into GPU VRAM, enables matrix parallelization, and provides smooth, stable gradient convergence. |
| **"What happens if the Learning Rate is set too high or too low?"** | Practical troubleshooting experience in deep learning training. | If the learning rate is too low, training is excessively slow and gets trapped in saddle points or poor local minima. If it is too high, the optimizer overshoots the loss valley, destabilizing training and causing gradients to explode into `NaN` / infinity. |
| **"What is the difference between Generalization and Overfitting in LLMs?"** | Understanding model evaluation and evaluation benchmarks. | **Generalization** is the model's ability to apply learned linguistic patterns and reasoning to novel, unseen prompts. **Overfitting** occurs when a model memorizes the exact training text verbatim; it achieves near-zero training loss but fails to generate coherent answers for slightly modified user prompts. |

---

## 🧩 Connection With Previous Concepts

* **Connection to Season 01, Class 05**: In Class 05, we studied the **Transformer Architecture** (Multi-Head Attention, Residuals, FFNs, Softmax). In Class 06, we learned how all the parameters across those Transformer layers are trained via **Backpropagation and Gradient Descent**.
* **Bridge to Class 07**: In the next lesson, we will explore **Post-Training Alignment**: how a pre-trained base model is transformed into a helpful conversational assistant via **Supervised Fine-Tuning (SFT)**, **LoRA (Parameter-Efficient Fine-Tuning)**, and **RLHF**.

---

Previous : [05. Transformer Architecture and Self-Attention](./05_Transformer_Architecture_and_Self_Attention.md) | Index: [00_index.md](../00_index.md) | Next: —
