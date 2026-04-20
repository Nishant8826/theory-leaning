# 📌 Linked List

## 🧠 Concept Explanation (Story Format)

Imagine a **scavenger hunt** where each clue tells you two things: a piece of information AND the location of the next clue. You follow the chain from clue to clue until you reach the end.

That's a **Linked List** — a collection of **nodes**, where each node stores data and a pointer (reference) to the next node. Unlike arrays, nodes aren't stored next to each other in memory — they're scattered around, connected by pointers.

### Array vs Linked List

| Feature | Array | Linked List |
|---------|-------|-------------|
| Memory | Contiguous | Scattered |
| Access by index | O(1) | O(n) |
| Insert at beginning | O(n) — shift all | O(1) — just update pointers |
| Insert at end | O(1) amortized | O(n) without tail pointer |
| Dynamic size | Fixed (or resize) | Grows freely |

### Types of Linked Lists

1. **Singly Linked List:** Each node points to the next node only.
2. **Doubly Linked List:** Each node points to both next AND previous nodes.
3. **Circular Linked List:** The last node points back to the first.

### Node Structure

```javascript
class ListNode {
  constructor(val) {
    this.val = val;    // The data stored in this node
    this.next = null;  // Pointer to the next node
  }
}

// Creating a simple linked list: 1 → 2 → 3
const head = new ListNode(1);
head.next = new ListNode(2);
head.next.next = new ListNode(3);
```

### Real-Life Analogy

Think of a **train**: each car (node) carries passengers (data) and is connected to the next car (pointer). You can add or remove cars easily, but to reach car #5, you have to walk through cars 1, 2, 3, 4 first.

---

## 🐢 Brute Force Approach

### Problem: Traverse and Print a Linked List

```javascript
class ListNode {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
}

// Helper: Create linked list from array
function createList(arr) {
  if (arr.length === 0) return null;
  const head = new ListNode(arr[0]);
  let current = head;
  for (let i = 1; i < arr.length; i++) {
    current.next = new ListNode(arr[i]);
    current = current.next;
  }
  return head;
}

// Helper: Convert linked list to array (for easy printing)
function toArray(head) {
  const result = [];
  let current = head;
  while (current) {
    result.push(current.val);
    current = current.next;
  }
  return result;
}

// Traverse and print
function printList(head) {
  let current = head;
  const values = [];
  while (current !== null) {
    values.push(current.val);
    current = current.next; // Move to next node
  }
  console.log(values.join(' → '));
}

const list = createList([1, 2, 3, 4, 5]);
printList(list); // 1 → 2 → 3 → 4 → 5
```

---

## ⚡ Optimized Approach

### Reverse a Linked List (Most Classic Problem)

```javascript
// Iterative reversal — O(n) time, O(1) space
function reverseList(head) {
  let prev = null;
  let current = head;

  while (current !== null) {
    const nextTemp = current.next; // Save next node
    current.next = prev;           // Reverse the pointer
    prev = current;                // Move prev forward
    current = nextTemp;            // Move current forward
  }

  return prev; // prev is now the new head
}

const list = createList([1, 2, 3, 4, 5]);
const reversed = reverseList(list);
console.log(toArray(reversed)); // [5, 4, 3, 2, 1]
```

### Visual Step-by-Step

```
Original: 1 → 2 → 3 → null
Step 1:   null ← 1   2 → 3 → null  (prev=1, curr=2)
Step 2:   null ← 1 ← 2   3 → null  (prev=2, curr=3)
Step 3:   null ← 1 ← 2 ← 3         (prev=3, curr=null)
Result:   3 → 2 → 1 → null
```

---

## 🔍 Complexity Analysis

| Operation | Singly Linked List |
|-----------|-------------------|
| Access by index | O(n) |
| Insert at head | O(1) |
| Insert at tail | O(n) without tail pointer |
| Delete from head | O(1) |
| Search | O(n) |
| Reverse | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Detect a Cycle in a Linked List

**Problem Statement:** Determine if a linked list has a cycle.

**Thought Process:** Use Floyd's Cycle Detection (tortoise and hare). One pointer moves 1 step, the other moves 2 steps. If they meet, there's a cycle.

#### 🐢 Brute Force — Using a Set

```javascript
function hasCycleBrute(head) {
  const visited = new Set();
  let current = head;

  while (current !== null) {
    if (visited.has(current)) return true; // Already visited!
    visited.add(current);
    current = current.next;
  }

  return false; // Reached the end — no cycle
}
```

#### ⚡ Optimized — Floyd's Cycle Detection

```javascript
function hasCycleOptimized(head) {
  let slow = head; // Moves 1 step
  let fast = head; // Moves 2 steps

  while (fast !== null && fast.next !== null) {
    slow = slow.next;
    fast = fast.next.next;

    if (slow === fast) return true; // They met — cycle exists!
  }

  return false; // Fast reached the end — no cycle
}
```

**Simple Explanation:** Two runners on a circular track. The fast runner will eventually lap the slow runner — they'll meet again! On a straight track (no cycle), the fast runner reaches the end first.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Optimized | O(n) | O(1) |

---

### Question 2: Find the Middle of a Linked List

**Problem Statement:** Find the middle node of a linked list.

**Thought Process:** Use slow/fast pointers. When fast reaches the end, slow is at the middle.

#### 🐢 Brute Force

```javascript
function middleBrute(head) {
  // First pass: count nodes
  let count = 0;
  let current = head;
  while (current) {
    count++;
    current = current.next;
  }

  // Second pass: go to middle
  current = head;
  for (let i = 0; i < Math.floor(count / 2); i++) {
    current = current.next;
  }

  return current;
}
```

#### ⚡ Optimized — Slow & Fast Pointers

```javascript
function middleOptimized(head) {
  let slow = head;
  let fast = head;

  while (fast !== null && fast.next !== null) {
    slow = slow.next;       // 1 step
    fast = fast.next.next;  // 2 steps
  }

  return slow; // Slow is at the middle
}

const list = createList([1, 2, 3, 4, 5]);
console.log(middleOptimized(list).val); // 3
```

**Simple Explanation:** Two people walk. One takes 1 step at a time, the other takes 2. When the fast walker reaches the end, the slow walker is exactly at the middle (since they started together).

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) — two passes | O(1) |
| Optimized | O(n) — one pass | O(1) |

---

### Question 3: Merge Two Sorted Linked Lists

**Problem Statement:** Merge two sorted linked lists into one sorted list.

#### 🐢 Brute Force

```javascript
function mergeBrute(l1, l2) {
  // Collect all values into an array
  const values = [];
  while (l1) { values.push(l1.val); l1 = l1.next; }
  while (l2) { values.push(l2.val); l2 = l2.next; }

  // Sort and create a new list
  values.sort((a, b) => a - b);
  return createList(values);
}
```

#### ⚡ Optimized — Merge In-Place

```javascript
function mergeOptimized(l1, l2) {
  const dummy = new ListNode(0); // Dummy head
  let current = dummy;

  while (l1 !== null && l2 !== null) {
    if (l1.val <= l2.val) {
      current.next = l1;
      l1 = l1.next;
    } else {
      current.next = l2;
      l2 = l2.next;
    }
    current = current.next;
  }

  // Attach remaining nodes
  current.next = l1 || l2;

  return dummy.next; // Skip dummy head
}

const l1 = createList([1, 2, 4]);
const l2 = createList([1, 3, 4]);
console.log(toArray(mergeOptimized(l1, l2))); // [1, 1, 2, 3, 4, 4]
```

**Simple Explanation:** Use a dummy node as the starting point. Compare nodes from both lists and always attach the smaller one. When one list runs out, attach the rest of the other.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O((n+m) log(n+m)) | O(n+m) |
| Optimized | O(n+m) | O(1) |

---

### Question 4: Remove Nth Node from End

**Problem Statement:** Remove the nth node from the end of a linked list.

**Thought Process:** Use two pointers with n nodes gap between them. When the leading pointer reaches the end, the trailing pointer is at the node before the one to remove.

#### 🐢 Brute Force

```javascript
function removeNthFromEndBrute(head, n) {
  // Count total nodes
  let count = 0;
  let current = head;
  while (current) { count++; current = current.next; }

  // Edge case: removing the head
  if (n === count) return head.next;

  // Navigate to the node BEFORE the one to remove
  current = head;
  for (let i = 0; i < count - n - 1; i++) {
    current = current.next;
  }

  current.next = current.next.next; // Skip the target node
  return head;
}
```

#### ⚡ Optimized — Two Pointers with Gap

```javascript
function removeNthFromEndOptimized(head, n) {
  const dummy = new ListNode(0);
  dummy.next = head;

  let fast = dummy;
  let slow = dummy;

  // Move fast n+1 steps ahead
  for (let i = 0; i <= n; i++) {
    fast = fast.next;
  }

  // Move both until fast reaches the end
  while (fast !== null) {
    slow = slow.next;
    fast = fast.next;
  }

  // slow.next is the node to remove
  slow.next = slow.next.next;

  return dummy.next;
}

const list = createList([1, 2, 3, 4, 5]);
console.log(toArray(removeNthFromEndOptimized(list, 2))); // [1, 2, 3, 5]
```

**Simple Explanation:** Create a gap of `n` nodes between two pointers. When the leading pointer reaches the end, the trailing pointer is right before the node to delete. It's like two people walking with a rope of length `n` between them.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) — two passes | O(1) |
| Optimized | O(n) — one pass | O(1) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Check if Linked List is a Palindrome

```javascript
function isPalindrome(head) {
  // Find middle
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }

  // Reverse second half
  let prev = null;
  while (slow) {
    const next = slow.next;
    slow.next = prev;
    prev = slow;
    slow = next;
  }

  // Compare halves
  let left = head, right = prev;
  while (right) {
    if (left.val !== right.val) return false;
    left = left.next;
    right = right.next;
  }

  return true;
}

console.log(isPalindrome(createList([1, 2, 2, 1]))); // true
console.log(isPalindrome(createList([1, 2, 3]))); // false
```

**Explanation:** Find the middle, reverse the second half, then compare both halves node by node.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 2: Intersection of Two Linked Lists

```javascript
function getIntersection(headA, headB) {
  let pA = headA;
  let pB = headB;

  // When one reaches the end, redirect to the other list's head
  while (pA !== pB) {
    pA = pA === null ? headB : pA.next;
    pB = pB === null ? headA : pB.next;
  }

  return pA; // Either the intersection node or null
}
```

**Explanation:** Both pointers traverse both lists. After traversing one list, they switch to the other. This equalizes the path lengths, so they'll meet at the intersection point (or both reach null).

**Complexity:** Time: O(n + m), Space: O(1)

---

### Problem 3: Add Two Numbers (Linked List)

**Problem Statement:** Two linked lists represent numbers in reverse. Add them and return the sum as a linked list.

```javascript
function addTwoNumbers(l1, l2) {
  const dummy = new ListNode(0);
  let current = dummy;
  let carry = 0;

  while (l1 || l2 || carry) {
    const sum = (l1 ? l1.val : 0) + (l2 ? l2.val : 0) + carry;
    carry = Math.floor(sum / 10);
    current.next = new ListNode(sum % 10);
    current = current.next;

    if (l1) l1 = l1.next;
    if (l2) l2 = l2.next;
  }

  return dummy.next;
}

// 342 + 465 = 807
// 2→4→3 + 5→6→4 = 7→0→8
const result = addTwoNumbers(createList([2, 4, 3]), createList([5, 6, 4]));
console.log(toArray(result)); // [7, 0, 8]
```

**Explanation:** Like adding numbers by hand. Process digit by digit, carry over when the sum exceeds 9.

**Complexity:** Time: O(max(n, m)), Space: O(max(n, m))

---

### 🔗 Navigation
Prev: [10_Hashing.md](10_Hashing.md) | Index: [00_Index.md](00_Index.md) | Next: [12_Stack.md](12_Stack.md)
