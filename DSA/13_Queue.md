# 📌 Queue

## 🧠 Concept Explanation (Story Format)

Imagine standing in a **line at a movie theater**. The first person in line gets the ticket first. New people join at the back. No cutting!

That's a **Queue** — a **FIFO (First In, First Out)** data structure. The first element added is the first one removed.

### Key Operations

| Operation | Description | Time |
|-----------|-------------|------|
| `enqueue(x)` | Add element to back | O(1) |
| `dequeue()` | Remove from front | O(1) |
| `front()` / `peek()` | View front element | O(1) |
| `isEmpty()` | Check if empty | O(1) |

### Types of Queues

1. **Simple Queue:** FIFO — first in, first out
2. **Circular Queue:** The end connects back to the front (efficient use of space)
3. **Priority Queue:** Elements leave based on priority, not arrival order (see Heap chapter)
4. **Deque (Double-Ended Queue):** Insert/remove from both ends

### Where Queues are Used

- **Print queue** — documents print in order
- **CPU task scheduling** — processes are handled in order
- **BFS (Breadth-First Search)** — explore level by level
- **Message queues** — like RabbitMQ, Kafka in backend systems

### Real-Life Analogy

A queue is like a **drive-through**. Cars line up, the first car gets served first, new cars join at the end. If someone tries to skip, there's trouble! 😄

---

## 🐢 Brute Force Approach

### Queue Implementation Using Array

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/implement-queue-using-array/1)

```javascript
// Simple Queue using array (brute force — shift is O(n))
class QueueBrute {
  constructor() {
    this.items = [];
  }

  enqueue(val) {
    this.items.push(val); // Add to back — O(1)
  }

  dequeue() {
    if (this.isEmpty()) return null;
    return this.items.shift(); // Remove from front — O(n)!
  }

  front() {
    return this.isEmpty() ? null : this.items[0];
  }

  isEmpty() {
    return this.items.length === 0;
  }

  size() {
    return this.items.length;
  }
}

const q = new QueueBrute();
q.enqueue(1); q.enqueue(2); q.enqueue(3);
console.log(q.dequeue()); // 1
console.log(q.front());   // 2
```

### Why is `shift()` bad?

`Array.shift()` removes the first element and shifts ALL remaining elements left — O(n) operation!

---

## ⚡ Optimized Approach

### Queue Using Object (O(1) Dequeue)

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/implement-queue-using-array/1) (using object instead of array)

```javascript
class Queue {
  constructor() {
    this.items = {};
    this.head = 0;
    this.tail = 0;
  }

  enqueue(val) {
    this.items[this.tail] = val;
    this.tail++;
  }

  dequeue() {
    if (this.isEmpty()) return null;
    const val = this.items[this.head];
    delete this.items[this.head];
    this.head++;
    return val;
  }

  front() {
    return this.isEmpty() ? null : this.items[this.head];
  }

  isEmpty() {
    return this.head === this.tail;
  }

  size() {
    return this.tail - this.head;
  }
}

const q = new Queue();
q.enqueue(10); q.enqueue(20); q.enqueue(30);
console.log(q.dequeue()); // 10
console.log(q.dequeue()); // 20
console.log(q.front());   // 30
console.log(q.size());    // 1
```

---

## 🔍 Complexity Analysis

| Operation | Array (shift) | Object-based |
|-----------|--------------|-------------|
| Enqueue | O(1) | O(1) |
| Dequeue | O(n) | O(1) |
| Peek | O(1) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Implement Stack Using Queues

**Practice Links:** [LeetCode #225](https://leetcode.com/problems/implement-stack-using-queues/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/stack-using-two-queues/1)

**Problem Statement:** Implement a stack using only queue operations.

**Thought Process:** After each push, rotate all previous elements behind the new one. This makes the most recent element always at the front.

#### 🐢 Brute Force

```javascript
class StackUsingQueuesBrute {
  constructor() {
    this.queue = [];
  }

  push(val) {
    this.queue.push(val);
    // Rotate: move all elements before val to behind it
    for (let i = 0; i < this.queue.length - 1; i++) {
      this.queue.push(this.queue.shift());
    }
  }

  pop() { return this.queue.shift(); }
  top() { return this.queue[0]; }
  isEmpty() { return this.queue.length === 0; }
}

const s = new StackUsingQueuesBrute();
s.push(1); s.push(2); s.push(3);
console.log(s.pop()); // 3 (LIFO!)
console.log(s.top()); // 2
```

#### ⚡ Optimized (Same logic — push O(n), pop O(1))

```javascript
class StackUsingQueues {
  constructor() {
    this.q = [];
  }

  push(val) {
    this.q.push(val);
    const size = this.q.length;
    for (let i = 0; i < size - 1; i++) {
      this.q.push(this.q.shift()); // Rotate previous elements to back
    }
  }

  pop() { return this.q.shift(); }
  top() { return this.q[0]; }
  isEmpty() { return this.q.length === 0; }
}
```

**Simple Explanation:** Every time we push, we rotate the queue so the newest element is at the front. It's like adding a book to a pile but then spinning the pile so the new book ends up on top.

**Complexity:** Push: O(n), Pop: O(1)

---

### Question 2: First Non-Repeating Character in a Stream

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/first-non-repeating-character-in-a-stream1216/1) | [InterviewBit](https://www.interviewbit.com/problems/first-non-repeating-character-in-a-stream/)

**Problem Statement:** Given a stream of characters, find the first non-repeating character at each step.

**Thought Process:** Use a queue to maintain order and a frequency map to track counts.

#### 🐢 Brute Force

```javascript
function firstNonRepeatingBrute(stream) {
  const result = [];
  const seen = [];

  for (const char of stream) {
    seen.push(char);
    const freq = {};
    for (const c of seen) freq[c] = (freq[c] || 0) + 1;

    let found = null;
    for (const c of seen) {
      if (freq[c] === 1) { found = c; break; }
    }
    result.push(found || '#');
  }

  return result;
}

console.log(firstNonRepeatingBrute("aabcbcd"));
```

#### ⚡ Optimized — Queue + Map

```javascript
function firstNonRepeatingOptimized(stream) {
  const queue = [];
  const freq = {};
  const result = [];

  for (const char of stream) {
    freq[char] = (freq[char] || 0) + 1;
    queue.push(char);

    // Remove characters from front that have repeated
    while (queue.length > 0 && freq[queue[0]] > 1) {
      queue.shift();
    }

    result.push(queue.length > 0 ? queue[0] : '#');
  }

  return result;
}

console.log(firstNonRepeatingOptimized("aabcbcd"));
// ['a', '#', 'b', 'b', 'c', 'c', 'd']
```

**Simple Explanation:** Keep a queue of characters in order. Track their frequency. The front of the queue should always be the first non-repeating character. If it has repeated, remove it from the front.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(n) |
| Optimized | O(n) | O(n) |

---

### Question 3: Rotting Oranges (BFS)

**Practice Links:** [LeetCode #994](https://leetcode.com/problems/rotting-oranges/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/rotten-oranges2536/1)

**Problem Statement:** In a grid, fresh oranges (1) rot if adjacent to rotten ones (2). Find the minimum time for all oranges to rot, or -1 if impossible.

**Thought Process:** Multi-source BFS. Start from all rotten oranges simultaneously.

#### 🐢 Brute Force

```javascript
function rottingOrangesBrute(grid) {
  const rows = grid.length, cols = grid[0].length;
  let minutes = 0;
  let changed = true;

  while (changed) {
    changed = false;
    const toRot = [];

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (grid[r][c] === 2) {
          const dirs = [[0,1],[0,-1],[1,0],[-1,0]];
          for (const [dr, dc] of dirs) {
            const nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] === 1) {
              toRot.push([nr, nc]);
            }
          }
        }
      }
    }

    for (const [r, c] of toRot) {
      grid[r][c] = 2;
      changed = true;
    }
    if (changed) minutes++;
  }

  // Check if any fresh orange remains
  for (const row of grid) {
    if (row.includes(1)) return -1;
  }
  return minutes;
}
```

#### ⚡ Optimized — BFS with Queue

```javascript
function rottingOrangesOptimized(grid) {
  const rows = grid.length, cols = grid[0].length;
  const queue = [];
  let fresh = 0;

  // Find all rotten oranges and count fresh ones
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === 2) queue.push([r, c]);
      if (grid[r][c] === 1) fresh++;
    }
  }

  if (fresh === 0) return 0;

  const dirs = [[0,1],[0,-1],[1,0],[-1,0]];
  let minutes = 0;

  while (queue.length > 0) {
    const size = queue.length;

    for (let i = 0; i < size; i++) {
      const [r, c] = queue.shift();

      for (const [dr, dc] of dirs) {
        const nr = r + dr, nc = c + dc;
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] === 1) {
          grid[nr][nc] = 2;
          fresh--;
          queue.push([nr, nc]);
        }
      }
    }

    if (queue.length > 0) minutes++;
  }

  return fresh === 0 ? minutes : -1;
}

console.log(rottingOrangesOptimized([[2,1,1],[1,1,0],[0,1,1]])); // 4
```

**Simple Explanation:** All rotten oranges spread rot simultaneously — like a wave. We use BFS (queue) to process each "wave" of rotting. Each wave takes 1 minute. Count the waves until all oranges rot (or we find it's impossible).

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Both | O(m × n) | O(m × n) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Circular Queue Implementation

**Practice Links:** [LeetCode #622](https://leetcode.com/problems/design-circular-queue/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/circular-queue-implementation/1)

```javascript
class CircularQueue {
  constructor(k) {
    this.queue = new Array(k);
    this.size = k;
    this.head = -1;
    this.tail = -1;
    this.count = 0;
  }

  enqueue(val) {
    if (this.isFull()) return false;
    if (this.isEmpty()) this.head = 0;
    this.tail = (this.tail + 1) % this.size;
    this.queue[this.tail] = val;
    this.count++;
    return true;
  }

  dequeue() {
    if (this.isEmpty()) return false;
    if (this.head === this.tail) { this.head = -1; this.tail = -1; }
    else this.head = (this.head + 1) % this.size;
    this.count--;
    return true;
  }

  front() { return this.isEmpty() ? -1 : this.queue[this.head]; }
  rear() { return this.isEmpty() ? -1 : this.queue[this.tail]; }
  isEmpty() { return this.count === 0; }
  isFull() { return this.count === this.size; }
}

const cq = new CircularQueue(3);
cq.enqueue(1); cq.enqueue(2); cq.enqueue(3);
console.log(cq.enqueue(4)); // false — full!
cq.dequeue();
console.log(cq.enqueue(4)); // true — space freed
console.log(cq.front());    // 2
```

**Explanation:** The tail wraps around using modulo. This avoids wasting space at the front after dequeues.

**Complexity:** All operations: O(1)

---

### Problem 2: Number of Recent Calls

**Practice Links:** [LeetCode #933](https://leetcode.com/problems/number-of-recent-calls/)

```javascript
class RecentCounter {
  constructor() {
    this.queue = [];
  }

  ping(t) {
    this.queue.push(t);
    // Remove calls outside the 3000ms window
    while (this.queue[0] < t - 3000) {
      this.queue.shift();
    }
    return this.queue.length;
  }
}

const rc = new RecentCounter();
console.log(rc.ping(1));    // 1
console.log(rc.ping(100));  // 2
console.log(rc.ping(3001)); // 3
console.log(rc.ping(3002)); // 3
```

**Explanation:** Keep a queue of timestamps. Remove old timestamps that fall outside the 3000ms window. The remaining count is our answer.

**Complexity:** Amortized O(1) per ping

---

### Problem 3: Generate Binary Numbers from 1 to N

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/generate-binary-numbers-1587115620/1)

```javascript
function generateBinary(n) {
  const result = [];
  const queue = ['1'];

  for (let i = 0; i < n; i++) {
    const current = queue.shift();
    result.push(current);
    queue.push(current + '0'); // Append 0
    queue.push(current + '1'); // Append 1
  }

  return result;
}

console.log(generateBinary(5));  // ['1', '10', '11', '100', '101']
console.log(generateBinary(10)); // ['1','10','11','100','101','110','111','1000','1001','1010']
```

**Explanation:** Start with "1". For each binary number, generate the next two by appending "0" and "1". This naturally produces binary numbers in order using BFS-like expansion.

**Complexity:** Time: O(n), Space: O(n)

---

### 🔗 Navigation
Prev: [12_Stack.md](12_Stack.md) | Index: [00_Index.md](00_Index.md) | Next: [14_Trees.md](14_Trees.md)
