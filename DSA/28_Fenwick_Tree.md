# 📌 Fenwick Tree (Binary Indexed Tree — BIT)

## 🧠 Concept Explanation (Story Format)

Remember the Segment Tree from the last chapter? It's powerful but uses a lot of memory (4n) and has more complex code. What if there was a **simpler, more space-efficient** alternative for prefix sum queries with updates?

Enter the **Fenwick Tree** (also called Binary Indexed Tree or BIT) — a clever data structure that uses binary representation of indices to efficiently compute prefix sums and handle point updates.

### What is a Fenwick Tree?

A Fenwick Tree stores **partial sums** in a flat array. Each position is responsible for a range of elements determined by the **lowest set bit** of its index.

```
Index (1-based):  1   2   3   4   5   6   7   8
Array:           [1] [3] [5] [7] [9] [11] [2] [4]

Fenwick Tree:    [1] [4] [5] [16] [9] [20] [2] [41]
                  │   │   │    │   │    │   │    │
                 1:1 1:2 3:3  1:4 5:5  5:6 7:7  1:8
              (range each position covers)
```

### Fenwick vs Segment Tree

| Feature | Fenwick Tree | Segment Tree |
|---------|-------------|-------------|
| Space | O(n) | O(4n) |
| Code complexity | Simple | Complex |
| Point update | O(log n) | O(log n) |
| Prefix query | O(log n) | O(log n) |
| Range update | With modification | With lazy propagation |
| Flexibility | Sum/XOR-like operations | Any merge operation |

### The Magic: lowbit(x)

The key insight is the function `lowbit(x) = x & (-x)` — it gives the lowest set bit of x.

```
x = 12 = 1100  →  lowbit = 100 = 4
x = 6  = 0110  →  lowbit = 010 = 2
x = 7  = 0111  →  lowbit = 001 = 1
```

- **Query:** Jump LEFT by removing the lowest bit: `i -= lowbit(i)`
- **Update:** Jump RIGHT by adding the lowest bit: `i += lowbit(i)`

### Real-Life Analogy

Think of a **hierarchical summary system**. In a company, team leads know their team's total, department heads know their department total, and the VP knows multiple departments. Instead of asking every employee, you ask the right level of the hierarchy. The lowbit determines which "level" handles which range.

---

## 🐢 Brute Force Approach

### Problem: Prefix Sum with Updates

```javascript
// Brute Force: Array with O(1) update, O(n) query
class PrefixSumBrute {
  constructor(nums) {
    this.nums = [...nums];
  }

  update(index, delta) {
    this.nums[index] += delta; // O(1)
  }

  prefixSum(index) {
    let sum = 0;
    for (let i = 0; i <= index; i++) {
      sum += this.nums[i]; // O(n)
    }
    return sum;
  }

  rangeSum(left, right) {
    return this.prefixSum(right) - (left > 0 ? this.prefixSum(left - 1) : 0);
  }
}

const psb = new PrefixSumBrute([1, 3, 5, 7, 9, 11]);
console.log(psb.rangeSum(1, 4)); // 24
psb.update(2, 5); // Add 5 to index 2
console.log(psb.rangeSum(1, 4)); // 29
```

---

## ⚡ Optimized Approach

### Fenwick Tree Implementation

```javascript
class FenwickTree {
  constructor(n) {
    this.n = n;
    this.tree = new Array(n + 1).fill(0); // 1-indexed
  }

  // Build from array
  static fromArray(nums) {
    const bit = new FenwickTree(nums.length);
    for (let i = 0; i < nums.length; i++) {
      bit.update(i + 1, nums[i]); // 1-indexed
    }
    return bit;
  }

  // Add delta to position index — O(log n)
  update(index, delta) {
    while (index <= this.n) {
      this.tree[index] += delta;
      index += index & (-index); // Add lowest set bit
    }
  }

  // Get prefix sum from 1 to index — O(log n)
  prefixSum(index) {
    let sum = 0;
    while (index > 0) {
      sum += this.tree[index];
      index -= index & (-index); // Remove lowest set bit
    }
    return sum;
  }

  // Get sum from left to right (1-indexed) — O(log n)
  rangeSum(left, right) {
    return this.prefixSum(right) - this.prefixSum(left - 1);
  }
}

// Usage
const bit = FenwickTree.fromArray([1, 3, 5, 7, 9, 11]);
console.log(bit.rangeSum(2, 5)); // 24 (3+5+7+9)
bit.update(3, 5);                 // Add 5 to index 3 (element 5 becomes 10)
console.log(bit.rangeSum(2, 5)); // 29 (3+10+7+9)
console.log(bit.prefixSum(6));   // 46 (1+3+10+7+9+11 = 41... +5 = 46)
```


#### Code Story
- This problem is about calculating totals for parts of a list in a way that is very fast and uses almost zero extra memory.
- First, we use a special array where each index stores a sum of a carefully chosen block of items.
- Then, we use 'Binary' math tricks (like stripping the last set bit) to instantly jump between the blocks we need.
- Finally, we can update a number or find a prefix sum in just a few binary jumps.
- This works because the blocks are designed so that any range can be formed by adding up at most O(log n) pre-calculated sums.

### How Update Works (Visual)

```
Update index 3 (binary: 011):
  011 (+001) → update tree[3]
  100 (+100) → update tree[4]
  1000       → update tree[8]
              → stop (8 > n)

Jump pattern: 3 → 4 → 8 (add lowest set bit each time)
```

### How Query Works (Visual)

```
PrefixSum of index 7 (binary: 111):
  111 (-001) → add tree[7] (covers 7:7)
  110 (-010) → add tree[6] (covers 5:6)
  100 (-100) → add tree[4] (covers 1:4)
  000        → stop

Jump pattern: 7 → 6 → 4 → 0 (remove lowest set bit each time)
```

---

## 🔍 Complexity Analysis

| Operation | Brute Force | Fenwick Tree |
|-----------|------------|-------------|
| Build | O(n) | O(n log n) |
| Point Update | O(1) | O(log n) |
| Prefix Query | O(n) | O(log n) |
| Range Query | O(n) | O(log n) |
| Space | O(n) | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Range Sum Query — Mutable (Fenwick Approach)

**Problem Statement:** Support update(index, val) and sumRange(left, right) operations efficiently.

#### ⚡ Optimized — Fenwick Tree

```javascript
class NumArrayFenwick {
  constructor(nums) {
    this.nums = new Array(nums.length).fill(0);
    this.bit = new FenwickTree(nums.length);

    for (let i = 0; i < nums.length; i++) {
      this._update(i, nums[i]);
    }
  }

  _update(index, delta) {
    this.nums[index] += delta;
    this.bit.update(index + 1, delta); // Convert to 1-indexed
  }

  update(index, val) {
    const delta = val - this.nums[index];
    this._update(index, delta);
  }

  sumRange(left, right) {
    return this.bit.rangeSum(left + 1, right + 1); // Convert to 1-indexed
  }
}

const na = new NumArrayFenwick([1, 3, 5]);
console.log(na.sumRange(0, 2)); // 9
na.update(1, 2);
console.log(na.sumRange(0, 2)); // 8
```

**Complexity:** Update: O(log n), Query: O(log n), Space: O(n)

---

### Question 2: Count of Smaller Numbers After Self

**Problem Statement:** For each element, count how many elements after it are smaller.


#### Code Story
- This problem is about taking a list and for every number, counting how many smaller numbers appear later on.
- First, we process the numbers from right to left.
- Then, for each number, we query our Fenwick Tree to see how many numbers smaller than it we've already seen.
- Finally, we 'add' the current number into the Fenwick Tree and repeat.
- This works because it uses the Fenwick Tree as a running 'frequency counter' that can answer range questions in record time.

#### 🐢 Brute Force

```javascript
function countSmallerBrute(nums) {
  const result = [];

  for (let i = 0; i < nums.length; i++) {
    let count = 0;
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[j] < nums[i]) count++;
    }
    result.push(count);
  }

  return result;
}

console.log(countSmallerBrute([5, 2, 6, 1])); // [2, 1, 1, 0]
```

#### ⚡ Optimized — Fenwick Tree

```javascript
function countSmaller(nums) {
  // Coordinate compression
  const sorted = [...new Set(nums)].sort((a, b) => a - b);
  const rank = new Map();
  sorted.forEach((val, idx) => rank.set(val, idx + 1)); // 1-indexed

  const bit = new FenwickTree(sorted.length);
  const result = new Array(nums.length);

  // Process from right to left
  for (let i = nums.length - 1; i >= 0; i--) {
    const r = rank.get(nums[i]);
    result[i] = bit.prefixSum(r - 1); // Count elements smaller than current
    bit.update(r, 1);                  // Add current element
  }

  return result;
}

console.log(countSmaller([5, 2, 6, 1])); // [2, 1, 1, 0]
```

**Simple Explanation:** Process arrays from right to left. For each number, query the Fenwick Tree: "How many numbers smaller than me have I seen so far?" Then add this number to the tree. Coordinate compression maps values to ranks for indexing.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(n) |
| Fenwick | O(n log n) | O(n) |

---

### Question 3: Reverse Pairs

**Problem Statement:** Count pairs (i, j) where i < j and nums[i] > 2 × nums[j].

#### ⚡ Optimized — Modified Merge Sort

```javascript
function reversePairs(nums) {
  let count = 0;

  function mergeSort(arr, left, right) {
    if (left >= right) return;
    const mid = Math.floor((left + right) / 2);
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);

    // Count reverse pairs
    let j = mid + 1;
    for (let i = left; i <= mid; i++) {
      while (j <= right && arr[i] > 2 * arr[j]) j++;
      count += j - (mid + 1);
    }

    // Standard merge
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

  mergeSort(nums, 0, nums.length - 1);
  return count;
}

console.log(reversePairs([1, 3, 2, 3, 1])); // 2
console.log(reversePairs([2, 4, 3, 5, 1])); // 3
```

**Simple Explanation:** After sorting left and right halves, count pairs where left[i] > 2 × right[j]. Since both halves are sorted, this counting is efficient. Then merge as usual.

**Complexity:** Time: O(n log n), Space: O(n)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: 2D Fenwick Tree (Matrix Range Sum)

```javascript
class FenwickTree2D {
  constructor(rows, cols) {
    this.rows = rows;
    this.cols = cols;
    this.tree = Array.from({length: rows + 1}, () => new Array(cols + 1).fill(0));
  }

  update(row, col, delta) {
    for (let i = row; i <= this.rows; i += i & (-i)) {
      for (let j = col; j <= this.cols; j += j & (-j)) {
        this.tree[i][j] += delta;
      }
    }
  }

  prefixSum(row, col) {
    let sum = 0;
    for (let i = row; i > 0; i -= i & (-i)) {
      for (let j = col; j > 0; j -= j & (-j)) {
        sum += this.tree[i][j];
      }
    }
    return sum;
  }

  rangeSum(r1, c1, r2, c2) {
    return this.prefixSum(r2, c2)
         - this.prefixSum(r1 - 1, c2)
         - this.prefixSum(r2, c1 - 1)
         + this.prefixSum(r1 - 1, c1 - 1);
  }
}

const bit2d = new FenwickTree2D(3, 3);
bit2d.update(1, 1, 1); bit2d.update(1, 2, 2);
bit2d.update(2, 1, 3); bit2d.update(2, 2, 4);
console.log(bit2d.rangeSum(1, 1, 2, 2)); // 10
```

**Explanation:** Extend the 1D Fenwick Tree to 2D by nesting the index jumps. Each update/query traverses O(log m × log n) cells.

**Complexity:** Update: O(log m × log n), Query: O(log m × log n)

---

### Problem 2: Range Frequency Query

```javascript
class RangeFreqQuery {
  constructor(arr) {
    this.indices = {}; // value → sorted list of indices

    for (let i = 0; i < arr.length; i++) {
      if (!this.indices[arr[i]]) this.indices[arr[i]] = [];
      this.indices[arr[i]].push(i);
    }
  }

  query(left, right, value) {
    const idx = this.indices[value];
    if (!idx) return 0;

    // Binary search for left bound and right bound
    const lo = this._lowerBound(idx, left);
    const hi = this._upperBound(idx, right);
    return hi - lo;
  }

  _lowerBound(arr, target) {
    let lo = 0, hi = arr.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (arr[mid] < target) lo = mid + 1;
      else hi = mid;
    }
    return lo;
  }

  _upperBound(arr, target) {
    let lo = 0, hi = arr.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (arr[mid] <= target) lo = mid + 1;
      else hi = mid;
    }
    return lo;
  }
}

const rfq = new RangeFreqQuery([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]);
console.log(rfq.query(1, 8, 33)); // 2
console.log(rfq.query(0, 11, 12)); // 2
```

**Explanation:** Store indices for each value. Use binary search to count how many indices fall within [left, right].

**Complexity:** Build: O(n), Query: O(log n)

---

### Problem 3: Fenwick Tree for Prefix XOR

```javascript
class FenwickXOR {
  constructor(n) {
    this.n = n;
    this.tree = new Array(n + 1).fill(0);
  }

  update(index, val) {
    while (index <= this.n) {
      this.tree[index] ^= val;
      index += index & (-index);
    }
  }

  prefixXOR(index) {
    let result = 0;
    while (index > 0) {
      result ^= this.tree[index];
      index -= index & (-index);
    }
    return result;
  }

  rangeXOR(left, right) {
    return this.prefixXOR(right) ^ this.prefixXOR(left - 1);
  }
}

const fxor = new FenwickXOR(5);
[3, 1, 4, 1, 5].forEach((val, i) => fxor.update(i + 1, val));
console.log(fxor.rangeXOR(1, 3)); // 3^1^4 = 6
console.log(fxor.rangeXOR(2, 5)); // 1^4^1^5 = 1
```

**Explanation:** Same Fenwick structure but with XOR instead of addition. Works because XOR is associative, commutative, and has an inverse (itself).

**Complexity:** Update: O(log n), Query: O(log n)

---

### 🔗 Navigation
Prev: [27_Segment_Tree.md](27_Segment_Tree.md) | Index: [00_Index.md](00_Index.md) | Next: End of Course 🎓
