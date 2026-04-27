# 📌 Heap

## 🧠 Concept Explanation (Story Format)

Imagine a **hospital emergency room**. Patients don't get treated in the order they arrive — the most critical patient gets treated first. That's a **Priority Queue**, and the data structure behind it is a **Heap**.

A **Heap** is a special binary tree where the parent node is always greater (Max Heap) or smaller (Min Heap) than its children.

### Types of Heaps

| Type | Property | Root Contains |
|------|----------|--------------|
| **Min Heap** | Parent ≤ Children | Smallest element |
| **Max Heap** | Parent ≥ Children | Largest element |


#### Code Story
- This problem is about building a structure that always keeps the 'best' item on top.
- First, we represent the tree as a simple array, where children can be found with math (2i+1, 2i+2).
- Then, we use 'bubble up' and 'bubble down' to keep the biggest (or smallest) at the top whenever we add or remove items.
- Finally, we have an extremely fast way to get the top priority item.
- This works because a heap only maintains partial order, just enough to find the winner without sorting everything.

### Heap as an Array

Heaps are typically stored in arrays. For node at index `i`:
- **Parent:** `Math.floor((i - 1) / 2)`
- **Left child:** `2 * i + 1`
- **Right child:** `2 * i + 2`

```
Min Heap:        1
               /   \
              3     5
             / \   /
            7   9 8

Array: [1, 3, 5, 7, 9, 8]
```

### Key Operations

| Operation | Time |
|-----------|------|
| Insert (push) | O(log n) |
| Remove top (pop) | O(log n) |
| Peek (get min/max) | O(1) |
| Build heap | O(n) |

### Real-Life Analogy

Think of a **company hierarchy**. The CEO (root) is always the most important person. If the CEO leaves, the next most important person takes over. New employees start at the bottom and "bubble up" if they're important enough.

---

## 🐢 Brute Force Approach

### Problem: Find Kth Largest Element

**Practice Links:** [LeetCode #215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/k-largest-elements3736/1)

```javascript
// Brute Force: Sort and pick
function kthLargestBrute(arr, k) {
  arr.sort((a, b) => b - a); // Sort descending
  return arr[k - 1];
}

console.log(kthLargestBrute([3, 2, 1, 5, 6, 4], 2)); // 5
```


#### Code Story
- This problem is about finding the 3rd or 4th or k-th biggest number in a huge pile.
- First, we create a 'Min-Heap' and put the first k numbers in it.
- Then, for every new number, if it's bigger than our heap's smallest, we swap them.
- Finally, after looking at all numbers, our heap of size k will contain the k largest items, and its top will be the one we need.
- This works because a small heap of size k acts like a filter that only keeps the absolute best numbers we've seen.

---

## ⚡ Optimized Approach

### Min Heap Implementation

```javascript
class MinHeap {
  constructor() {
    this.heap = [];
  }

  push(val) {
    this.heap.push(val);
    this._bubbleUp(this.heap.length - 1);
  }

  pop() {
    if (this.heap.length === 0) return null;
    const min = this.heap[0];
    const last = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this._sinkDown(0);
    }
    return min;
  }

  peek() { return this.heap[0]; }
  size() { return this.heap.length; }

  _bubbleUp(idx) {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.heap[parent] <= this.heap[idx]) break;
      [this.heap[parent], this.heap[idx]] = [this.heap[idx], this.heap[parent]];
      idx = parent;
    }
  }

  _sinkDown(idx) {
    const n = this.heap.length;
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;

      if (left < n && this.heap[left] < this.heap[smallest]) smallest = left;
      if (right < n && this.heap[right] < this.heap[smallest]) smallest = right;

      if (smallest === idx) break;
      [this.heap[smallest], this.heap[idx]] = [this.heap[idx], this.heap[smallest]];
      idx = smallest;
    }
  }
}

// Using Min Heap for Kth Largest
function kthLargestHeap(arr, k) {
  const minHeap = new MinHeap();

  for (const num of arr) {
    minHeap.push(num);
    if (minHeap.size() > k) {
      minHeap.pop(); // Remove smallest — keep only k largest
    }
  }

  return minHeap.peek(); // Top of min heap = kth largest
}

console.log(kthLargestHeap([3, 2, 1, 5, 6, 4], 2)); // 5
```

---

## 🔍 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Sort | O(n log n) | O(1) |
| Heap (size k) | O(n log k) | O(k) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Top K Frequent Elements

**Practice Links:** [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/top-k-frequent-elements-in-array--170637/1)

**Problem Statement:** Find the k most frequent elements in an array.

#### 🐢 Brute Force

```javascript
function topKFrequentBrute(nums, k) {
  const freq = {};
  for (const num of nums) freq[num] = (freq[num] || 0) + 1;

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, k)
    .map(e => Number(e[0]));
}

console.log(topKFrequentBrute([1,1,1,2,2,3], 2)); // [1, 2]
```

#### ⚡ Optimized — Bucket Sort

```javascript
function topKFrequentOptimized(nums, k) {
  const freq = {};
  for (const num of nums) freq[num] = (freq[num] || 0) + 1;

  // Create buckets: index = frequency, value = list of numbers
  const buckets = new Array(nums.length + 1).fill(null).map(() => []);
  for (const [num, count] of Object.entries(freq)) {
    buckets[count].push(Number(num));
  }

  // Collect from highest frequency
  const result = [];
  for (let i = buckets.length - 1; i >= 0 && result.length < k; i--) {
    result.push(...buckets[i]);
  }

  return result.slice(0, k);
}

console.log(topKFrequentOptimized([1,1,1,2,2,3], 2)); // [1, 2]
```

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n log n) | O(n) |
| Bucket Sort | O(n) | O(n) |

---

### Question 2: Merge K Sorted Lists

**Practice Links:** [LeetCode #23](https://leetcode.com/problems/merge-k-sorted-lists/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/merge-k-sorted-linked-lists/1)

**Problem Statement:** Merge k sorted linked lists into one sorted list.


#### Code Story
- This problem is about merging many sorted chains into one big sorted chain.
- First, we put the 'Head' of every list into a Min-Heap.
- Then, we always take the smallest node from the heap, add it to our new chain, and put the next node from that same list into the heap.
- Finally, we repeat until all nodes have been merged.
- This works because the heap always keeps the next potential winner right at our fingertips, no matter how many lists there are.

#### 🐢 Brute Force

```javascript
function mergeKListsBrute(lists) {
  const values = [];
  for (const list of lists) {
    let node = list;
    while (node) { values.push(node.val); node = node.next; }
  }
  values.sort((a, b) => a - b);

  const dummy = { next: null };
  let current = dummy;
  for (const val of values) {
    current.next = { val, next: null };
    current = current.next;
  }
  return dummy.next;
}
```

#### ⚡ Optimized — Min Heap

```javascript
function mergeKListsOptimized(lists) {
  const heap = new MinHeap();

  // Add first node from each list
  for (const list of lists) {
    if (list) heap.push(list);
  }

  const dummy = { next: null };
  let current = dummy;

  while (heap.size() > 0) {
    const node = heap.pop();
    current.next = node;
    current = current.next;

    if (node.next) {
      heap.push(node.next);
    }
  }

  return dummy.next;
}
```

**Simple Explanation:** Use a min heap to always pick the smallest among the heads of all lists. After picking, push the next node of that list into the heap. Like merging sorted piles of cards — always take the smallest visible card.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(N log N) | O(N) |
| Heap | O(N log k) | O(k) |

---

### Question 3: Find Median from Data Stream

**Practice Links:** [LeetCode #295](https://leetcode.com/problems/find-median-from-data-stream/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/median-in-a-stream-1587115620/1)

**Problem Statement:** Design a class that can find the median from a stream of numbers.


#### Code Story
- This problem is about finding the middle number in a list that keeps growing.
- First, we use two heaps: one for the smaller half of numbers (Max-Heap) and one for the larger half (Min-Heap).
- Then, we keep the heaps balanced so they stay equal in size.
- Finally, the median is either the top of one heap or the average of both tops.
- This works because the middle of the data is always where the two halves of our heap structure meet.

#### 🐢 Brute Force

```javascript
class MedianFinderBrute {
  constructor() { this.nums = []; }

  addNum(num) {
    this.nums.push(num);
    this.nums.sort((a, b) => a - b);
  }

  findMedian() {
    const n = this.nums.length;
    const mid = Math.floor(n / 2);
    return n % 2 === 0 ? (this.nums[mid - 1] + this.nums[mid]) / 2 : this.nums[mid];
  }
}
```

#### ⚡ Optimized — Two Heaps

```javascript
class MedianFinderOptimized {
  constructor() {
    this.maxHeap = []; // Lower half (stores negatives for max behavior)
    this.minHeap = new MinHeap(); // Upper half
  }

  addNum(num) {
    // Add to max heap (lower half)
    this.maxHeap.push(-num);
    this.maxHeap.sort((a, b) => a - b);

    // Move max of lower half to min heap (upper half)
    this.minHeap.push(-this.maxHeap.shift());

    // Balance: max heap should have equal or one more element
    if (this.minHeap.size() > this.maxHeap.length) {
      this.maxHeap.push(-this.minHeap.pop());
      this.maxHeap.sort((a, b) => a - b);
    }
  }

  findMedian() {
    if (this.maxHeap.length > this.minHeap.size()) {
      return -this.maxHeap[0];
    }
    return (-this.maxHeap[0] + this.minHeap.peek()) / 2;
  }
}
```

**Simple Explanation:** Keep two heaps — a max heap for the smaller half and a min heap for the larger half. The median is either the top of the max heap or the average of both tops. Like splitting a sorted list into two halves.

**Complexity:** addNum: O(log n), findMedian: O(1)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Sort a Nearly Sorted Array

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/nearly-sorted-1587115620/1)

```javascript
function sortNearlySorted(arr, k) {
  const heap = new MinHeap();
  const result = [];

  for (let i = 0; i < arr.length; i++) {
    heap.push(arr[i]);
    if (heap.size() > k + 1) {
      result.push(heap.pop());
    }
  }

  while (heap.size() > 0) result.push(heap.pop());
  return result;
}

console.log(sortNearlySorted([6, 5, 3, 2, 8, 10, 9], 3)); // [2, 3, 5, 6, 8, 9, 10]
```

**Explanation:** Each element is at most k positions from its sorted position. Use a min heap of size k+1 to always extract the correct next element.

**Complexity:** Time: O(n log k), Space: O(k)

---

### Problem 2: Last Stone Weight

**Practice Links:** [LeetCode #1046](https://leetcode.com/problems/last-stone-weight/)

```javascript
function lastStoneWeight(stones) {
  // Simulate max heap using sorted array
  stones.sort((a, b) => b - a);

  while (stones.length > 1) {
    const s1 = stones.shift(); // Largest
    const s2 = stones.shift(); // Second largest

    if (s1 !== s2) {
      const diff = s1 - s2;
      // Insert diff in sorted position
      let i = 0;
      while (i < stones.length && stones[i] > diff) i++;
      stones.splice(i, 0, diff);
    }
  }

  return stones.length === 0 ? 0 : stones[0];
}

console.log(lastStoneWeight([2, 7, 4, 1, 8, 1])); // 1
```

**Explanation:** Always smash the two heaviest stones. If they differ, put the remainder back. Like a rock-paper-scissors tournament where the winner loses some weight.

**Complexity:** Time: O(n² log n), Space: O(1)

---

### Problem 3: K Closest Points to Origin

**Practice Links:** [LeetCode #973](https://leetcode.com/problems/k-closest-points-to-origin/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/k-closest-points-to-origin--170637/1)

**Problem Statement:** Find the k points closest to the origin (0, 0).

```javascript
function kClosest(points, k) {
  // Calculate distance and sort
  return points
    .map(p => ({ point: p, dist: p[0] * p[0] + p[1] * p[1] }))
    .sort((a, b) => a.dist - b.dist)
    .slice(0, k)
    .map(p => p.point);
}

console.log(kClosest([[1,3],[-2,2],[5,8],[0,1]], 2));
// [[0,1], [-2,2]]
```

**Explanation:** Calculate squared distance from origin (no need for sqrt). Sort by distance and take the first k points.

**Complexity:** Time: O(n log n), Space: O(n)

---

### 🔗 Navigation
Prev: [15_Binary_Search_Tree.md](15_Binary_Search_Tree.md) | Index: [00_Index.md](00_Index.md) | Next: [17_Trie.md](17_Trie.md)
