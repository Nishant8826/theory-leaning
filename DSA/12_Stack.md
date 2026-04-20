# 📌 Stack

## 🧠 Concept Explanation (Story Format)

Imagine a **stack of plates** in a cafeteria. You can only add a plate on **top** and take a plate from the **top**. You can't pull a plate from the middle or bottom without removing everything above it.

That's a **Stack** — a **LIFO (Last In, First Out)** data structure. The last element added is the first one removed.

### Key Operations

| Operation | Description | Time |
|-----------|-------------|------|
| `push(x)` | Add element to top | O(1) |
| `pop()` | Remove and return top element | O(1) |
| `peek()` / `top()` | View top element without removing | O(1) |
| `isEmpty()` | Check if stack is empty | O(1) |

### Where Stacks are Used

- **Undo/Redo** in text editors
- **Browser Back button** (history of visited pages)
- **Function call stack** in programming languages
- **Expression evaluation** (parentheses matching, postfix)
- **DFS (Depth-First Search)** in graphs

### Stack Implementation in JavaScript

```javascript
// Using an array as a stack
const stack = [];
stack.push(1);    // [1]
stack.push(2);    // [1, 2]
stack.push(3);    // [1, 2, 3]
stack.pop();      // Returns 3, stack = [1, 2]
stack[stack.length - 1]; // Peek: 2
```

### Real-Life Analogy

Besides the plate analogy, think of **Pringles chips** — you can only take the top chip. Or think of **clothes in a suitcase** — the last item you packed is the first one you unpack.

---

## 🐢 Brute Force Approach

### Problem: Valid Parentheses

Given a string containing `(){}[]`, determine if it's valid. Every opening bracket must have a matching closing bracket in the correct order.

```javascript
// Brute Force: Keep replacing matched pairs until none left
function isValidBrute(s) {
  let prev = '';

  while (s !== prev) {
    prev = s;
    s = s.replace('()', '').replace('[]', '').replace('{}', '');
  }

  return s.length === 0;
}

console.log(isValidBrute("()[]{}")); // true
console.log(isValidBrute("(]"));     // false
console.log(isValidBrute("([)]"));   // false
console.log(isValidBrute("{[]}"));   // true
```

### Line-by-Line Explanation

1. Repeatedly find and remove matching pairs `()`, `[]`, `{}`.
2. If the string becomes empty, all brackets matched.
3. This works but is very slow — O(n²) due to repeated string scanning.

---

## ⚡ Optimized Approach

Use a **stack** — push opening brackets, pop when closing brackets arrive.

```javascript
// Optimized: Stack — O(n)
function isValidOptimized(s) {
  const stack = [];
  const map = { ')': '(', ']': '[', '}': '{' };

  for (const char of s) {
    if (char === '(' || char === '[' || char === '{') {
      stack.push(char); // Opening bracket → push
    } else {
      // Closing bracket → check if it matches the top
      if (stack.length === 0 || stack[stack.length - 1] !== map[char]) {
        return false; // No matching opening bracket
      }
      stack.pop(); // Match found — remove the opening bracket
    }
  }

  return stack.length === 0; // Stack should be empty if all matched
}

console.log(isValidOptimized("()[]{}")); // true
console.log(isValidOptimized("(]"));     // false
console.log(isValidOptimized("{[]}"));   // true
```

---

## 🔍 Complexity Analysis

| Approach | Time Complexity | Space Complexity |
|----------|----------------|-----------------|
| Brute Force | O(n²) | O(n) |
| Stack | O(n) | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Min Stack

**Problem Statement:** Design a stack that supports push, pop, top, and retrieving the minimum element in O(1).

**Thought Process:** Maintain a second stack that tracks the minimum at each level.

#### 🐢 Brute Force

```javascript
class MinStackBrute {
  constructor() {
    this.stack = [];
  }

  push(val) { this.stack.push(val); }
  pop() { this.stack.pop(); }
  top() { return this.stack[this.stack.length - 1]; }

  getMin() {
    return Math.min(...this.stack); // O(n) each time!
  }
}
```

#### ⚡ Optimized — Two Stacks

```javascript
class MinStack {
  constructor() {
    this.stack = [];
    this.minStack = []; // Tracks minimum at each level
  }

  push(val) {
    this.stack.push(val);
    // Push to minStack if it's empty or val ≤ current min
    const currentMin = this.minStack.length === 0
      ? val
      : Math.min(val, this.minStack[this.minStack.length - 1]);
    this.minStack.push(currentMin);
  }

  pop() {
    this.stack.pop();
    this.minStack.pop();
  }

  top() {
    return this.stack[this.stack.length - 1];
  }

  getMin() {
    return this.minStack[this.minStack.length - 1]; // O(1)!
  }
}

const ms = new MinStack();
ms.push(5); ms.push(2); ms.push(7); ms.push(1);
console.log(ms.getMin()); // 1
ms.pop();
console.log(ms.getMin()); // 2
```

**Simple Explanation:** Every time we push, we also record what the minimum is at that point. When we pop, both stacks pop together— so the minimum is always up to date. Like writing the "current leader" on each plate as you stack them.

**Complexity:** All operations: O(1) time, O(n) space

---

### Question 2: Next Greater Element

**Problem Statement:** For each element, find the next element that is greater than it (-1 if no such element).

Example: `[4, 5, 2, 25]` → `[5, 25, 25, -1]`

**Thought Process:** Use a stack to track elements waiting for their "next greater." When we find a greater element, pop and assign.

#### 🐢 Brute Force

```javascript
function nextGreaterBrute(arr) {
  const result = [];

  for (let i = 0; i < arr.length; i++) {
    let found = -1;
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[j] > arr[i]) {
        found = arr[j];
        break;
      }
    }
    result.push(found);
  }

  return result;
}

console.log(nextGreaterBrute([4, 5, 2, 25])); // [5, 25, 25, -1]
```

#### ⚡ Optimized — Monotonic Stack

```javascript
function nextGreaterOptimized(arr) {
  const result = new Array(arr.length).fill(-1);
  const stack = []; // Stack of indices

  for (let i = 0; i < arr.length; i++) {
    // While current element is greater than elements waiting in stack
    while (stack.length > 0 && arr[i] > arr[stack[stack.length - 1]]) {
      const idx = stack.pop();
      result[idx] = arr[i]; // Found the next greater for this index
    }
    stack.push(i); // Push current index
  }

  return result;
}

console.log(nextGreaterOptimized([4, 5, 2, 25]));    // [5, 25, 25, -1]
console.log(nextGreaterOptimized([13, 7, 6, 12]));   // [-1, 12, 12, -1]
```

**Simple Explanation:** Walk through the array. The stack holds indices of elements that haven't found their "next greater" yet. When we see a bigger element, we pop smaller ones from the stack and assign this bigger element as their answer.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(n) |
| Optimized | O(n) | O(n) |

---

### Question 3: Evaluate Reverse Polish Notation (Postfix)

**Problem Statement:** Evaluate a postfix expression like `["2", "1", "+", "3", "*"]` → `9`.

**Thought Process:** Use a stack. Push numbers. When you see an operator, pop two numbers, apply the operator, push the result.

#### 🐢 Brute Force (Stack IS the optimal approach here)

```javascript
function evalRPN(tokens) {
  const stack = [];

  for (const token of tokens) {
    if (['+', '-', '*', '/'].includes(token)) {
      const b = stack.pop(); // Second operand
      const a = stack.pop(); // First operand

      switch (token) {
        case '+': stack.push(a + b); break;
        case '-': stack.push(a - b); break;
        case '*': stack.push(a * b); break;
        case '/': stack.push(Math.trunc(a / b)); break; // Truncate toward zero
      }
    } else {
      stack.push(Number(token)); // Push number
    }
  }

  return stack[0]; // Final result
}

console.log(evalRPN(["2", "1", "+", "3", "*"])); // 9 → (2+1)*3
console.log(evalRPN(["4", "13", "5", "/", "+"])); // 6 → 4 + (13/5)
```

#### ⚡ Optimized (Same approach — already optimal)

**Simple Explanation:** In postfix, operators come AFTER their operands. We stack numbers until we see an operator, then pop two, compute, and push the result back. Like a calculator that collects numbers first.

**Complexity:** Time: O(n), Space: O(n)

---

### Question 4: Daily Temperatures

**Problem Statement:** Given daily temperatures, for each day find how many days you'd wait for a warmer day.

Example: `[73, 74, 75, 71, 69, 72, 76, 73]` → `[1, 1, 4, 2, 1, 1, 0, 0]`

#### 🐢 Brute Force

```javascript
function dailyTempsBrute(temps) {
  const result = new Array(temps.length).fill(0);

  for (let i = 0; i < temps.length; i++) {
    for (let j = i + 1; j < temps.length; j++) {
      if (temps[j] > temps[i]) {
        result[i] = j - i;
        break;
      }
    }
  }

  return result;
}

console.log(dailyTempsBrute([73, 74, 75, 71, 69, 72, 76, 73]));
// [1, 1, 4, 2, 1, 1, 0, 0]
```

#### ⚡ Optimized — Monotonic Stack

```javascript
function dailyTempsOptimized(temps) {
  const result = new Array(temps.length).fill(0);
  const stack = []; // Stack of indices

  for (let i = 0; i < temps.length; i++) {
    while (stack.length > 0 && temps[i] > temps[stack[stack.length - 1]]) {
      const prevDay = stack.pop();
      result[prevDay] = i - prevDay; // Days waited
    }
    stack.push(i);
  }

  return result;
}

console.log(dailyTempsOptimized([73, 74, 75, 71, 69, 72, 76, 73]));
// [1, 1, 4, 2, 1, 1, 0, 0]
```

**Simple Explanation:** Stack holds days still waiting for a warmer day. When a warmer day arrives, pop all colder days and record the wait time. Like people standing in a cold weather, when warm weather comes, everyone leaves.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(n) |
| Optimized | O(n) | O(n) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Implement a Queue using Two Stacks

```javascript
class QueueUsingStacks {
  constructor() {
    this.pushStack = [];
    this.popStack = [];
  }

  enqueue(val) {
    this.pushStack.push(val);
  }

  dequeue() {
    if (this.popStack.length === 0) {
      while (this.pushStack.length > 0) {
        this.popStack.push(this.pushStack.pop());
      }
    }
    return this.popStack.pop();
  }
}

const q = new QueueUsingStacks();
q.enqueue(1); q.enqueue(2); q.enqueue(3);
console.log(q.dequeue()); // 1 (FIFO!)
console.log(q.dequeue()); // 2
```

**Explanation:** Push stack collects items. When we need to dequeue, we reverse items into the pop stack, making the oldest item accessible.

**Complexity:** Amortized O(1) per operation

---

### Problem 2: Largest Rectangle in Histogram

```javascript
function largestRectangle(heights) {
  const stack = [];
  let maxArea = 0;
  const n = heights.length;

  for (let i = 0; i <= n; i++) {
    const currentHeight = i === n ? 0 : heights[i];

    while (stack.length > 0 && currentHeight < heights[stack[stack.length - 1]]) {
      const height = heights[stack.pop()];
      const width = stack.length === 0 ? i : i - stack[stack.length - 1] - 1;
      maxArea = Math.max(maxArea, height * width);
    }

    stack.push(i);
  }

  return maxArea;
}

console.log(largestRectangle([2, 1, 5, 6, 2, 3])); // 10
```

**Explanation:** Use a stack to track bars. When a shorter bar appears, calculate rectangles using taller bars from the stack. Each bar is pushed and popped once.

**Complexity:** Time: O(n), Space: O(n)

---

### Problem 3: Decode String

**Problem Statement:** Decode strings like `"3[a2[c]]"` → `"accaccacc"`.

```javascript
function decodeString(s) {
  const countStack = [];
  const stringStack = [];
  let currentString = '';
  let currentNum = 0;

  for (const char of s) {
    if (char >= '0' && char <= '9') {
      currentNum = currentNum * 10 + Number(char);
    } else if (char === '[') {
      countStack.push(currentNum);
      stringStack.push(currentString);
      currentNum = 0;
      currentString = '';
    } else if (char === ']') {
      const count = countStack.pop();
      const prevString = stringStack.pop();
      currentString = prevString + currentString.repeat(count);
    } else {
      currentString += char;
    }
  }

  return currentString;
}

console.log(decodeString("3[a]2[bc]"));   // "aaabcbc"
console.log(decodeString("3[a2[c]]"));    // "accaccacc"
console.log(decodeString("2[abc]3[cd]")); // "abcabccdcdcd"
```

**Explanation:** Use two stacks — one for counts, one for strings. When we see `[`, save current state. When we see `]`, pop and build. Like unwinding nested Russian dolls.

**Complexity:** Time: O(n), Space: O(n)

---

### 🔗 Navigation
Prev: [11_Linked_List.md](11_Linked_List.md) | Index: [00_Index.md](00_Index.md) | Next: [13_Queue.md](13_Queue.md)
