# 📌 10 — DSA in JavaScript (Interview Coding Round)

## 🌟 Introduction

Most companies include a **DSA coding round** in JavaScript interviews. This file covers the most frequently asked data structure and algorithm problems, solved in **idiomatic JavaScript** with time/space complexity analysis.

---

## 📂 Section 1: Strings

### 1. Reverse a String

```javascript
// Method 1: Built-in
const reverse = (str) => str.split('').reverse().join('');

// Method 2: Two pointers (in-place for array)
function reverseInPlace(arr) {
  let left = 0, right = arr.length - 1;
  while (left < right) {
    [arr[left], arr[right]] = [arr[right], arr[left]];
    left++;
    right--;
  }
  return arr;
}
```
**Time:** O(n) | **Space:** O(n) for Method 1, O(1) for Method 2

---

### 2. Check Palindrome

```javascript
function isPalindrome(str) {
  const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
  let left = 0, right = cleaned.length - 1;
  while (left < right) {
    if (cleaned[left] !== cleaned[right]) return false;
    left++;
    right--;
  }
  return true;
}

isPalindrome("A man, a plan, a canal: Panama"); // true
```
**Time:** O(n) | **Space:** O(n) for the cleaned string

---

### 3. First Non-Repeating Character

```javascript
function firstUnique(str) {
  const freq = new Map();
  for (const char of str) {
    freq.set(char, (freq.get(char) || 0) + 1);
  }
  for (const char of str) {
    if (freq.get(char) === 1) return char;
  }
  return null;
}

firstUnique("aabcbd"); // "c"
```
**Time:** O(n) | **Space:** O(k) where k = unique characters

---

### 4. Check if Two Strings are Anagrams

```javascript
function isAnagram(s1, s2) {
  if (s1.length !== s2.length) return false;
  const map = new Map();

  for (const c of s1) map.set(c, (map.get(c) || 0) + 1);
  for (const c of s2) {
    if (!map.has(c) || map.get(c) === 0) return false;
    map.set(c, map.get(c) - 1);
  }
  return true;
}

isAnagram("listen", "silent"); // true
```
**Time:** O(n) | **Space:** O(k)

---

### 5. Longest Substring Without Repeating Characters

```javascript
function lengthOfLongestSubstring(s) {
  const seen = new Map();
  let maxLen = 0;
  let start = 0;

  for (let end = 0; end < s.length; end++) {
    if (seen.has(s[end]) && seen.get(s[end]) >= start) {
      start = seen.get(s[end]) + 1;
    }
    seen.set(s[end], end);
    maxLen = Math.max(maxLen, end - start + 1);
  }
  return maxLen;
}

lengthOfLongestSubstring("abcabcbb"); // 3 ("abc")
```
**Time:** O(n) | **Space:** O(min(n, k)) — Sliding Window technique

---

## 📂 Section 2: Arrays

### 6. Two Sum

```javascript
function twoSum(nums, target) {
  const map = new Map();
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (map.has(complement)) {
      return [map.get(complement), i];
    }
    map.set(nums[i], i);
  }
  return [];
}

twoSum([2, 7, 11, 15], 9); // [0, 1]
```
**Time:** O(n) | **Space:** O(n)

---

### 7. Find Duplicates in Array

```javascript
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();

  for (const num of arr) {
    if (seen.has(num)) duplicates.add(num);
    seen.add(num);
  }
  return [...duplicates];
}

findDuplicates([1, 2, 3, 2, 4, 3, 5]); // [2, 3]
```

---

### 8. Maximum Subarray Sum (Kadane's Algorithm)

```javascript
function maxSubarraySum(arr) {
  let maxSoFar = arr[0];
  let maxEndingHere = arr[0];

  for (let i = 1; i < arr.length; i++) {
    maxEndingHere = Math.max(arr[i], maxEndingHere + arr[i]);
    maxSoFar = Math.max(maxSoFar, maxEndingHere);
  }
  return maxSoFar;
}

maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4]); // 6 ([4,-1,2,1])
```
**Time:** O(n) | **Space:** O(1)

---

### 9. Merge Two Sorted Arrays

```javascript
function mergeSorted(a, b) {
  const result = [];
  let i = 0, j = 0;

  while (i < a.length && j < b.length) {
    if (a[i] <= b[j]) result.push(a[i++]);
    else result.push(b[j++]);
  }

  return [...result, ...a.slice(i), ...b.slice(j)];
}

mergeSorted([1, 3, 5], [2, 4, 6]); // [1, 2, 3, 4, 5, 6]
```
**Time:** O(n + m) | **Space:** O(n + m)

---

### 10. Move Zeroes to End

```javascript
function moveZeroes(arr) {
  let insertPos = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] !== 0) {
      [arr[insertPos], arr[i]] = [arr[i], arr[insertPos]];
      insertPos++;
    }
  }
  return arr;
}

moveZeroes([0, 1, 0, 3, 12]); // [1, 3, 12, 0, 0]
```
**Time:** O(n) | **Space:** O(1) — in-place

---

## 📂 Section 3: Objects & Hash Maps

### 11. Group Anagrams

```javascript
function groupAnagrams(words) {
  const map = new Map();
  for (const word of words) {
    const key = word.split('').sort().join('');
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(word);
  }
  return [...map.values()];
}

groupAnagrams(["eat","tea","tan","ate","nat","bat"]);
// [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

---

### 12. Frequency Counter Pattern

```javascript
function topKFrequent(nums, k) {
  const freq = new Map();
  for (const n of nums) freq.set(n, (freq.get(n) || 0) + 1);

  return [...freq.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, k)
    .map(([num]) => num);
}

topKFrequent([1,1,1,2,2,3], 2); // [1, 2]
```

---

## 📂 Section 4: Linked Lists (Implement in JS)

### 13. Implement a Singly Linked List

```javascript
class ListNode {
  constructor(val, next = null) {
    this.val = val;
    this.next = next;
  }
}

class LinkedList {
  constructor() {
    this.head = null;
    this.size = 0;
  }

  prepend(val) {
    this.head = new ListNode(val, this.head);
    this.size++;
  }

  append(val) {
    const node = new ListNode(val);
    if (!this.head) { this.head = node; }
    else {
      let curr = this.head;
      while (curr.next) curr = curr.next;
      curr.next = node;
    }
    this.size++;
  }

  reverse() {
    let prev = null, curr = this.head;
    while (curr) {
      const next = curr.next;
      curr.next = prev;
      prev = curr;
      curr = next;
    }
    this.head = prev;
  }

  hasCycle() {
    let slow = this.head, fast = this.head;
    while (fast && fast.next) {
      slow = slow.next;
      fast = fast.next.next;
      if (slow === fast) return true;
    }
    return false;
  }

  toArray() {
    const result = [];
    let curr = this.head;
    while (curr) {
      result.push(curr.val);
      curr = curr.next;
    }
    return result;
  }
}
```

---

## 📂 Section 5: Stacks & Queues

### 14. Valid Parentheses

```javascript
function isValid(s) {
  const stack = [];
  const pairs = { ')': '(', ']': '[', '}': '{' };

  for (const char of s) {
    if ('([{'.includes(char)) {
      stack.push(char);
    } else {
      if (stack.pop() !== pairs[char]) return false;
    }
  }
  return stack.length === 0;
}

isValid("([{}])"); // true
isValid("([)]");   // false
```

---

### 15. Implement Queue using Two Stacks

```javascript
class Queue {
  constructor() {
    this.inbox = [];
    this.outbox = [];
  }

  enqueue(val) {
    this.inbox.push(val);
  }

  dequeue() {
    if (this.outbox.length === 0) {
      while (this.inbox.length) {
        this.outbox.push(this.inbox.pop());
      }
    }
    return this.outbox.pop();
  }

  peek() {
    if (this.outbox.length === 0) {
      while (this.inbox.length) {
        this.outbox.push(this.inbox.pop());
      }
    }
    return this.outbox[this.outbox.length - 1];
  }
}
```
**Amortized Time:** O(1) per operation

---

## 📂 Section 6: Trees

### 16. Binary Tree Traversals (BFS + DFS)

```javascript
class TreeNode {
  constructor(val, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// DFS: Inorder (Left → Root → Right)
function inorder(node, result = []) {
  if (!node) return result;
  inorder(node.left, result);
  result.push(node.val);
  inorder(node.right, result);
  return result;
}

// DFS: Preorder (Root → Left → Right)
function preorder(node, result = []) {
  if (!node) return result;
  result.push(node.val);
  preorder(node.left, result);
  preorder(node.right, result);
  return result;
}

// BFS: Level Order
function levelOrder(root) {
  if (!root) return [];
  const result = [];
  const queue = [root];

  while (queue.length) {
    const levelSize = queue.length;
    const level = [];
    for (let i = 0; i < levelSize; i++) {
      const node = queue.shift();
      level.push(node.val);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    result.push(level);
  }
  return result;
}

// Max depth
function maxDepth(node) {
  if (!node) return 0;
  return 1 + Math.max(maxDepth(node.left), maxDepth(node.right));
}
```

---

## 📂 Section 7: Sorting & Searching

### 17. Binary Search

```javascript
function binarySearch(arr, target) {
  let left = 0, right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
```
**Time:** O(log n)

---

### 18. Merge Sort (Most asked sorting algorithm)

```javascript
function mergeSort(arr) {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let i = 0, j = 0;
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) result.push(left[i++]);
    else result.push(right[j++]);
  }
  return [...result, ...left.slice(i), ...right.slice(j)];
}
```
**Time:** O(n log n) | **Space:** O(n)

---

## 📂 Section 8: Common Patterns

### 19. Sliding Window — Max Sum of K elements

```javascript
function maxSumSubarray(arr, k) {
  let windowSum = arr.slice(0, k).reduce((a, b) => a + b, 0);
  let maxSum = windowSum;

  for (let i = k; i < arr.length; i++) {
    windowSum += arr[i] - arr[i - k]; // Slide the window
    maxSum = Math.max(maxSum, windowSum);
  }
  return maxSum;
}

maxSumSubarray([2, 1, 5, 1, 3, 2], 3); // 9 (5+1+3)
```

---

### 20. Implement `memoize()`

```javascript
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const factorial = memoize(function(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
});

factorial(10); // Calculates
factorial(10); // Returns from cache instantly
```

---

## 📐 Complexity Cheat Sheet

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space |
| :--- | :--- | :--- | :--- | :--- |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Hash Map lookup | O(1) | O(1) | O(n) | O(n) |
| BFS/DFS | O(V+E) | O(V+E) | O(V+E) | O(V) |

| JS Operation | Time Complexity |
| :--- | :--- |
| `Array.push/pop` | O(1) |
| `Array.shift/unshift` | O(n) |
| `Array.splice` | O(n) |
| `Map.get/set/has` | O(1) |
| `Set.add/has/delete` | O(1) |
| `Object.keys` | O(n) |

---

## 🔗 Navigation

**Prev:** [09_ES6_Plus_Interview.md](09_ES6_Plus_Interview.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** —
