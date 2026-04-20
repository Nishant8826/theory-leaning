# 📌 Segment Tree

## 🧠 Concept Explanation (Story Format)

Imagine you run a **chain of stores**, and you frequently need to answer questions like "What's the total sales from store 5 to store 20?" and sometimes update individual store sales. A simple array makes updates fast (O(1)) but range queries slow (O(n)), or you precompute prefix sums for fast queries but slow updates.

A **Segment Tree** gives you the best of both worlds — **O(log n)** for both range queries AND updates.

### What is a Segment Tree?

A segment tree is a binary tree where:
- Each **leaf** stores an element from the array
- Each **internal node** stores the result of merging its children (sum, min, max, etc.)
- The root stores the result for the entire array

```
Array: [1, 3, 5, 7, 9, 11]

Segment Tree (sum):
              [36]              → sum of [0..5]
            /      \
         [9]        [27]        → sum of [0..2], [3..5]
        /   \      /    \
      [4]   [5]  [16]   [11]   → sum of [0..1], [2..2], [3..4], [5..5]
     / \         / \
   [1] [3]     [7] [9]         → individual elements
```

### Key Operations

| Operation | Time |
|-----------|------|
| Build | O(n) |
| Query (range) | O(log n) |
| Update (point) | O(log n) |

### Where Segment Trees are Used

- **Range sum queries** — sum of elements from index i to j
- **Range min/max queries** — minimum/maximum in a range
- **Range updates** — update all elements in a range (with lazy propagation)
- **Competitive programming** — very common!

### Real-Life Analogy

Think of a **corporate hierarchy report**. Each manager knows the total of their direct reports. The VP knows the total of all managers. The CEO knows the company total. To find "total sales from departments 3-7," you combine a few manager reports instead of asking each employee individually.

---

## 🐢 Brute Force Approach

### Problem: Range Sum Query with Updates

```javascript
// Brute Force: Use array directly
class RangeSumBrute {
  constructor(nums) {
    this.nums = [...nums];
  }

  // Update: O(1)
  update(index, val) {
    this.nums[index] = val;
  }

  // Query: O(n) — sum from left to right
  query(left, right) {
    let sum = 0;
    for (let i = left; i <= right; i++) {
      sum += this.nums[i];
    }
    return sum;
  }
}

const rsb = new RangeSumBrute([1, 3, 5, 7, 9, 11]);
console.log(rsb.query(1, 4)); // 24 (3+5+7+9)
rsb.update(2, 10);
console.log(rsb.query(1, 4)); // 29 (3+10+7+9)
```

---

## ⚡ Optimized Approach

### Segment Tree Implementation

```javascript
class SegmentTree {
  constructor(nums) {
    this.n = nums.length;
    this.tree = new Array(4 * this.n).fill(0); // 4n is safe size
    if (this.n > 0) this._build(nums, 1, 0, this.n - 1);
  }

  // Build the tree — O(n)
  _build(nums, node, start, end) {
    if (start === end) {
      this.tree[node] = nums[start]; // Leaf node
      return;
    }

    const mid = Math.floor((start + end) / 2);
    this._build(nums, 2 * node, start, mid);      // Left child
    this._build(nums, 2 * node + 1, mid + 1, end); // Right child
    this.tree[node] = this.tree[2 * node] + this.tree[2 * node + 1]; // Merge
  }

  // Point update — O(log n)
  update(index, val, node = 1, start = 0, end = this.n - 1) {
    if (start === end) {
      this.tree[node] = val; // Update leaf
      return;
    }

    const mid = Math.floor((start + end) / 2);
    if (index <= mid) {
      this.update(index, val, 2 * node, start, mid);
    } else {
      this.update(index, val, 2 * node + 1, mid + 1, end);
    }

    this.tree[node] = this.tree[2 * node] + this.tree[2 * node + 1]; // Recalculate
  }

  // Range query — O(log n)
  query(left, right, node = 1, start = 0, end = this.n - 1) {
    if (right < start || end < left) return 0;      // No overlap
    if (left <= start && end <= right) return this.tree[node]; // Complete overlap

    // Partial overlap — check both children
    const mid = Math.floor((start + end) / 2);
    return this.query(left, right, 2 * node, start, mid) +
           this.query(left, right, 2 * node + 1, mid + 1, end);
  }
}

const st = new SegmentTree([1, 3, 5, 7, 9, 11]);
console.log(st.query(1, 4)); // 24 (3+5+7+9)
st.update(2, 10);
console.log(st.query(1, 4)); // 29 (3+10+7+9)
console.log(st.query(0, 5)); // 41 (1+3+10+7+9+11)
```

---

## 🔍 Complexity Analysis

| Operation | Brute Force | Segment Tree |
|-----------|------------|-------------|
| Build | O(n) | O(n) |
| Point Update | O(1) | O(log n) |
| Range Query | O(n) | O(log n) |
| Space | O(n) | O(4n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Range Sum Query — Mutable

**Problem Statement:** Handle multiple update and range sum queries efficiently.

#### 🐢 Brute Force — Prefix Sum (fast query, slow update)

```javascript
class NumArrayBrute {
  constructor(nums) {
    this.nums = [...nums];
  }

  update(index, val) {
    this.nums[index] = val;
  }

  sumRange(left, right) {
    let sum = 0;
    for (let i = left; i <= right; i++) sum += this.nums[i];
    return sum;
  }
}
```

#### ⚡ Optimized — Segment Tree

```javascript
class NumArray {
  constructor(nums) {
    this.st = new SegmentTree(nums);
  }

  update(index, val) {
    this.st.update(index, val);
  }

  sumRange(left, right) {
    return this.st.query(left, right);
  }
}

const na = new NumArray([1, 3, 5]);
console.log(na.sumRange(0, 2)); // 9
na.update(1, 2);
console.log(na.sumRange(0, 2)); // 8
```

**Simple Explanation:** Build a segment tree once. Each update takes O(log n) to propagate changes up. Each query takes O(log n) by combining relevant segment results.

**Complexity:** Build: O(n), Update: O(log n), Query: O(log n)

---

### Question 2: Range Minimum Query

**Problem Statement:** Find the minimum element in a range [l, r] with point updates.

#### ⚡ Optimized — Segment Tree (Min variant)

```javascript
class MinSegmentTree {
  constructor(nums) {
    this.n = nums.length;
    this.tree = new Array(4 * this.n).fill(Infinity);
    if (this.n > 0) this._build(nums, 1, 0, this.n - 1);
  }

  _build(nums, node, start, end) {
    if (start === end) { this.tree[node] = nums[start]; return; }
    const mid = Math.floor((start + end) / 2);
    this._build(nums, 2 * node, start, mid);
    this._build(nums, 2 * node + 1, mid + 1, end);
    this.tree[node] = Math.min(this.tree[2 * node], this.tree[2 * node + 1]);
  }

  update(index, val, node = 1, start = 0, end = this.n - 1) {
    if (start === end) { this.tree[node] = val; return; }
    const mid = Math.floor((start + end) / 2);
    if (index <= mid) this.update(index, val, 2 * node, start, mid);
    else this.update(index, val, 2 * node + 1, mid + 1, end);
    this.tree[node] = Math.min(this.tree[2 * node], this.tree[2 * node + 1]);
  }

  query(left, right, node = 1, start = 0, end = this.n - 1) {
    if (right < start || end < left) return Infinity;
    if (left <= start && end <= right) return this.tree[node];
    const mid = Math.floor((start + end) / 2);
    return Math.min(
      this.query(left, right, 2 * node, start, mid),
      this.query(left, right, 2 * node + 1, mid + 1, end)
    );
  }
}

const mst = new MinSegmentTree([2, 5, 1, 4, 9, 3]);
console.log(mst.query(1, 4)); // 1
console.log(mst.query(3, 5)); // 3
mst.update(2, 7);
console.log(mst.query(1, 4)); // 4
```

**Simple Explanation:** Same structure as sum tree, but instead of adding children, we take the minimum. Each node stores the minimum of its range.

**Complexity:** Build: O(n), Update: O(log n), Query: O(log n)

---

### Question 3: Count of Range Sum

**Problem Statement:** Count the number of range sums that lie in [lower, upper].

#### ⚡ Optimized — Merge Sort with Count

```javascript
function countRangeSum(nums, lower, upper) {
  const prefix = [0];
  for (const num of nums) {
    prefix.push(prefix[prefix.length - 1] + num);
  }

  let count = 0;

  function mergeSort(arr, left, right) {
    if (left >= right) return;
    const mid = Math.floor((left + right) / 2);
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);

    // Count valid pairs
    let lo = mid + 1, hi = mid + 1;
    for (let i = left; i <= mid; i++) {
      while (lo <= right && arr[lo] - arr[i] < lower) lo++;
      while (hi <= right && arr[hi] - arr[i] <= upper) hi++;
      count += hi - lo;
    }

    // Merge
    const temp = [];
    let p1 = left, p2 = mid + 1;
    while (p1 <= mid && p2 <= right) {
      if (arr[p1] <= arr[p2]) temp.push(arr[p1++]);
      else temp.push(arr[p2++]);
    }
    while (p1 <= mid) temp.push(arr[p1++]);
    while (p2 <= right) temp.push(arr[p2++]);
    for (let i = 0; i < temp.length; i++) arr[left + i] = temp[i];
  }

  mergeSort(prefix, 0, prefix.length - 1);
  return count;
}

console.log(countRangeSum([-2, 5, -1], -2, 2)); // 3
```

**Explanation:** Range sum from i to j = prefix[j+1] - prefix[i]. We need to count pairs where lower ≤ prefix[j] - prefix[i] ≤ upper. Merge sort maintains the sorted order needed for efficient counting.

**Complexity:** Time: O(n log n), Space: O(n)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Range XOR Query

```javascript
class XORSegmentTree {
  constructor(nums) {
    this.n = nums.length;
    this.tree = new Array(4 * this.n).fill(0);
    if (this.n > 0) this._build(nums, 1, 0, this.n - 1);
  }

  _build(nums, node, start, end) {
    if (start === end) { this.tree[node] = nums[start]; return; }
    const mid = Math.floor((start + end) / 2);
    this._build(nums, 2 * node, start, mid);
    this._build(nums, 2 * node + 1, mid + 1, end);
    this.tree[node] = this.tree[2 * node] ^ this.tree[2 * node + 1]; // XOR merge
  }

  query(left, right, node = 1, start = 0, end = this.n - 1) {
    if (right < start || end < left) return 0;
    if (left <= start && end <= right) return this.tree[node];
    const mid = Math.floor((start + end) / 2);
    return this.query(left, right, 2 * node, start, mid) ^
           this.query(left, right, 2 * node + 1, mid + 1, end);
  }
}

const xst = new XORSegmentTree([1, 3, 5, 7]);
console.log(xst.query(0, 3)); // 1^3^5^7 = 0
console.log(xst.query(1, 2)); // 3^5 = 6
```

**Explanation:** Same segment tree structure but merge using XOR instead of sum/min.

**Complexity:** Build: O(n), Query: O(log n)

---

### Problem 2: Count Inversions Using Segment Tree

```javascript
function countInversions(arr) {
  const sorted = [...new Set(arr)].sort((a, b) => a - b);
  const rank = new Map();
  sorted.forEach((val, idx) => rank.set(val, idx));

  const n = sorted.length;
  const tree = new Array(4 * n).fill(0);
  let inversions = 0;

  function update(idx, node = 1, start = 0, end = n - 1) {
    if (start === end) { tree[node]++; return; }
    const mid = Math.floor((start + end) / 2);
    if (idx <= mid) update(idx, 2 * node, start, mid);
    else update(idx, 2 * node + 1, mid + 1, end);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
  }

  function query(left, right, node = 1, start = 0, end = n - 1) {
    if (right < start || end < left || left > right) return 0;
    if (left <= start && end <= right) return tree[node];
    const mid = Math.floor((start + end) / 2);
    return query(left, right, 2 * node, start, mid) +
           query(left, right, 2 * node + 1, mid + 1, end);
  }

  // Process from right to left
  for (let i = arr.length - 1; i >= 0; i--) {
    const r = rank.get(arr[i]);
    inversions += query(0, r - 1); // Count elements smaller than arr[i] to its right
    update(r);
  }

  return inversions;
}

console.log(countInversions([2, 4, 1, 3, 5])); // 3
```

**Explanation:** Process elements from right to left. For each element, count how many previously processed elements (to its right) are smaller. Use segment tree for efficient counting.

**Complexity:** Time: O(n log n), Space: O(n)

---

### 🔗 Navigation
Prev: [26_Disjoint_Set.md](26_Disjoint_Set.md) | Index: [00_Index.md](00_Index.md) | Next: [28_Fenwick_Tree.md](28_Fenwick_Tree.md)
