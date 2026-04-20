# 📌 Sorting

## 🧠 Concept Explanation (Story Format)

Imagine you're a **teacher** with a stack of 100 exam papers, and you need to arrange them by marks — lowest to highest. How do you do it?

- **Bubble Sort:** Compare two adjacent papers, swap if out of order. Keep doing this until everything is sorted. Simple but slow.
- **Selection Sort:** Scan the entire pile, find the lowest score, place it first. Then find the next lowest, place it second. And so on.
- **Merge Sort:** Split the pile in half, sort each half separately, then merge the two sorted halves together.
- **Quick Sort:** Pick a random paper (pivot). Put all papers with lower scores on the left, higher on the right. Repeat for each side.

**Sorting** is the process of arranging data in a specific order. It's one of the most studied topics in computer science because sorted data makes searching, merging, and analysis much faster.

### Common Sorting Algorithms

| Algorithm | Time (Best) | Time (Average) | Time (Worst) | Space | Stable? |
|-----------|------------|---------------|-------------|-------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |

### What is "Stable" Sorting?

A stable sort preserves the relative order of equal elements. If two students have the same marks, their original order is maintained.

---

## 🐢 Brute Force Approach

### Bubble Sort — The Simplest Sort

**Idea:** Repeatedly compare adjacent elements and swap them if they're in the wrong order. Like bubbles rising to the surface.

```javascript
// Bubble Sort — O(n²)
function bubbleSort(arr) {
  const n = arr.length;

  for (let i = 0; i < n - 1; i++) {
    let swapped = false;

    for (let j = 0; j < n - 1 - i; j++) {
      // Compare adjacent elements
      if (arr[j] > arr[j + 1]) {
        // Swap them
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        swapped = true;
      }
    }

    // If no swaps happened, array is already sorted
    if (!swapped) break;
  }

  return arr;
}

console.log(bubbleSort([64, 34, 25, 12, 22, 11, 90]));
// [11, 12, 22, 25, 34, 64, 90]
```

### Line-by-Line Explanation

1. **Outer loop** — runs n-1 times (one pass per element).
2. **`n - 1 - i`** — after each pass, the largest unsorted element "bubbles up" to the end.
3. **`swapped` flag** — if no swaps happen in a pass, the array is sorted (optimization).
4. Each pass pushes the next largest element to its correct position.

### Selection Sort

```javascript
// Selection Sort — O(n²)
function selectionSort(arr) {
  const n = arr.length;

  for (let i = 0; i < n - 1; i++) {
    let minIdx = i; // Assume current position has minimum

    // Find the actual minimum in unsorted portion
    for (let j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }

    // Swap minimum with current position
    if (minIdx !== i) {
      [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
    }
  }

  return arr;
}

console.log(selectionSort([64, 25, 12, 22, 11]));
// [11, 12, 22, 25, 64]
```

### Insertion Sort

```javascript
// Insertion Sort — O(n²) worst, O(n) best (nearly sorted)
function insertionSort(arr) {
  for (let i = 1; i < arr.length; i++) {
    const key = arr[i]; // Element to insert
    let j = i - 1;

    // Shift elements that are greater than key
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }

    arr[j + 1] = key; // Place key in correct position
  }

  return arr;
}

console.log(insertionSort([12, 11, 13, 5, 6]));
// [5, 6, 11, 12, 13]
```

---

## ⚡ Optimized Approach

### Merge Sort — Divide and Conquer — O(n log n) guaranteed

```javascript
// Merge Sort — O(n log n) always
function mergeSort(arr) {
  // Base case: array of 0 or 1 element is already sorted
  if (arr.length <= 1) return arr;

  // Divide
  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));  // Sort left half
  const right = mergeSort(arr.slice(mid));     // Sort right half

  // Conquer (merge)
  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let i = 0, j = 0;

  // Compare and pick the smaller element
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.push(left[i]);
      i++;
    } else {
      result.push(right[j]);
      j++;
    }
  }

  // Add remaining elements
  while (i < left.length) result.push(left[i++]);
  while (j < right.length) result.push(right[j++]);

  return result;
}

console.log(mergeSort([38, 27, 43, 3, 9, 82, 10]));
// [3, 9, 10, 27, 38, 43, 82]
```

### Quick Sort — Average O(n log n), In-Place

```javascript
// Quick Sort — O(n log n) average
function quickSort(arr, low = 0, high = arr.length - 1) {
  if (low < high) {
    const pivotIdx = partition(arr, low, high);
    quickSort(arr, low, pivotIdx - 1);  // Sort left of pivot
    quickSort(arr, pivotIdx + 1, high);  // Sort right of pivot
  }
  return arr;
}

function partition(arr, low, high) {
  const pivot = arr[high]; // Choose last element as pivot
  let i = low - 1;        // Index of smaller element

  for (let j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]]; // Swap
    }
  }

  // Place pivot in correct position
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1;
}

console.log(quickSort([10, 7, 8, 9, 1, 5]));
// [1, 5, 7, 8, 9, 10]
```

---

## 🔍 Complexity Analysis

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Sort an Array of 0s, 1s, and 2s (Dutch National Flag)

**Problem Statement:** Sort an array containing only 0, 1, and 2 in one pass without using a sorting algorithm.

**Thought Process:** Use three pointers (low, mid, high) to partition the array into three sections.

#### 🐢 Brute Force

```javascript
function sortColorsBrute(arr) {
  return arr.sort((a, b) => a - b);
}

console.log(sortColorsBrute([2, 0, 1, 2, 1, 0])); // [0, 0, 1, 1, 2, 2]
```

#### ⚡ Optimized — Dutch National Flag

```javascript
function sortColorsOptimized(arr) {
  let low = 0, mid = 0, high = arr.length - 1;

  while (mid <= high) {
    if (arr[mid] === 0) {
      [arr[low], arr[mid]] = [arr[mid], arr[low]];
      low++;
      mid++;
    } else if (arr[mid] === 1) {
      mid++;
    } else {
      [arr[mid], arr[high]] = [arr[high], arr[mid]];
      high--;
    }
  }

  return arr;
}

console.log(sortColorsOptimized([2, 0, 1, 2, 1, 0])); // [0, 0, 1, 1, 2, 2]
```

**Simple Explanation:** Three zones: 0s go to the left (before `low`), 2s go to the right (after `high`), 1s stay in the middle. The `mid` pointer scans through, placing elements in their zone.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n log n) | O(1) |
| Optimized | O(n) | O(1) |

---

### Question 2: Merge Intervals

**Problem Statement:** Given a collection of intervals, merge all overlapping intervals.

Example: `[[1,3], [2,6], [8,10], [15,18]]` → `[[1,6], [8,10], [15,18]]`

**Thought Process:** Sort by start time, then merge overlapping intervals.

#### 🐢 Brute Force

```javascript
function mergeIntervalsBrute(intervals) {
  if (intervals.length <= 1) return intervals;

  intervals.sort((a, b) => a[0] - b[0]);
  const result = [intervals[0]];

  for (let i = 1; i < intervals.length; i++) {
    const last = result[result.length - 1];
    const current = intervals[i];

    if (current[0] <= last[1]) {
      // Overlapping — merge
      last[1] = Math.max(last[1], current[1]);
    } else {
      // Non-overlapping — add as new interval
      result.push(current);
    }
  }

  return result;
}

console.log(mergeIntervalsBrute([[1,3],[2,6],[8,10],[15,18]]));
// [[1,6],[8,10],[15,18]]
```

#### ⚡ Optimized (Same approach — sorting is the key insight)

```javascript
function mergeIntervalsOptimized(intervals) {
  if (intervals.length <= 1) return intervals;

  // Sort by start time
  intervals.sort((a, b) => a[0] - b[0]);

  const merged = [intervals[0]];

  for (let i = 1; i < intervals.length; i++) {
    const prev = merged[merged.length - 1];

    if (intervals[i][0] <= prev[1]) {
      // Overlapping — extend the end
      prev[1] = Math.max(prev[1], intervals[i][1]);
    } else {
      // No overlap — add new interval
      merged.push(intervals[i]);
    }
  }

  return merged;
}

console.log(mergeIntervalsOptimized([[1,3],[2,6],[8,10],[15,18]]));
// [[1,6],[8,10],[15,18]]
```

**Simple Explanation:** Sort meetings by start time. Walk through them. If the next meeting overlaps with the current one, extend the current meeting. If not, start a new one.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Both | O(n log n) | O(n) |

---

### Question 3: Kth Largest Element

**Problem Statement:** Find the kth largest element in an unsorted array.

Example: `[3, 2, 1, 5, 6, 4], k = 2` → `5`

**Thought Process:** Sort and pick, or use QuickSelect (partition-based approach).

#### 🐢 Brute Force — Sort

```javascript
function findKthLargestBrute(arr, k) {
  arr.sort((a, b) => b - a); // Sort descending
  return arr[k - 1];          // Pick kth element
}

console.log(findKthLargestBrute([3, 2, 1, 5, 6, 4], 2)); // 5
```

#### ⚡ Optimized — QuickSelect

```javascript
function findKthLargestOptimized(arr, k) {
  const targetIdx = arr.length - k; // kth largest = (n-k)th smallest
  return quickSelect(arr, 0, arr.length - 1, targetIdx);
}

function quickSelect(arr, low, high, target) {
  const pivotIdx = partition(arr, low, high);

  if (pivotIdx === target) return arr[pivotIdx];
  if (pivotIdx < target) return quickSelect(arr, pivotIdx + 1, high, target);
  return quickSelect(arr, low, pivotIdx - 1, target);
}

function partition(arr, low, high) {
  const pivot = arr[high];
  let i = low;

  for (let j = low; j < high; j++) {
    if (arr[j] <= pivot) {
      [arr[i], arr[j]] = [arr[j], arr[i]];
      i++;
    }
  }

  [arr[i], arr[high]] = [arr[high], arr[i]];
  return i;
}

console.log(findKthLargestOptimized([3, 2, 1, 5, 6, 4], 2)); // 5
```

**Simple Explanation:** Instead of fully sorting, use QuickSort's partitioning. After one partition, the pivot is in its final position. If that position is where the kth largest should be, we're done. Otherwise, only recurse into the relevant half.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n log n) | O(1) |
| QuickSelect | O(n) avg, O(n²) worst | O(1) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Sort Characters by Frequency

**Problem Statement:** Sort characters in a string by how frequently they appear.

**Approach:** Count frequencies, sort by count, build result.

```javascript
function frequencySort(s) {
  const freq = new Map();

  // Count frequencies
  for (const ch of s) {
    freq.set(ch, (freq.get(ch) || 0) + 1);
  }

  // Sort by frequency (descending)
  const sorted = [...freq.entries()].sort((a, b) => b[1] - a[1]);

  // Build result
  let result = "";
  for (const [char, count] of sorted) {
    result += char.repeat(count);
  }

  return result;
}

console.log(frequencySort("tree"));    // "eert" or "eetr"
console.log(frequencySort("cccaaa")); // "cccaaa" or "aaaccc"
```

**Explanation:** Count how often each character appears, sort by count, then repeat each character by its count.

**Complexity:** Time: O(n log n), Space: O(n)

---

### Problem 2: Largest Number

**Problem Statement:** Given a list of non-negative integers, arrange them to form the largest number.

**Approach:** Custom sort — compare by string concatenation.

```javascript
function largestNumber(nums) {
  // Convert to strings and sort with custom comparator
  const sorted = nums.map(String).sort((a, b) => {
    // Compare "ab" vs "ba" — which gives a bigger number?
    return (b + a) - (a + b);
  });

  // Edge case: if all zeros
  if (sorted[0] === '0') return '0';

  return sorted.join('');
}

console.log(largestNumber([10, 2]));      // "210"
console.log(largestNumber([3, 30, 34]));  // "34330"
console.log(largestNumber([0, 0]));       // "0"
```

**Explanation:** Should "30" come before "3"? Compare "303" vs "330". Since 330 > 303, "3" should come first. This custom comparison gives us the optimal arrangement.

**Complexity:** Time: O(n log n), Space: O(n)

---

### Problem 3: Relative Sort Array

**Problem Statement:** Sort `arr1` so that elements in `arr2` come first (in `arr2`'s order), followed by remaining elements in ascending order.

**Approach:** Use a map for ordering, then custom sort.

```javascript
function relativeSortArray(arr1, arr2) {
  // Create order map from arr2
  const order = new Map();
  arr2.forEach((val, idx) => order.set(val, idx));

  return arr1.sort((a, b) => {
    const hasA = order.has(a);
    const hasB = order.has(b);

    if (hasA && hasB) return order.get(a) - order.get(b); // Both in arr2
    if (hasA) return -1; // Only a in arr2, a comes first
    if (hasB) return 1;  // Only b in arr2, b comes first
    return a - b;         // Neither in arr2, sort naturally
  });
}

console.log(relativeSortArray([2,3,1,3,2,4,6,7,9,2,19], [2,1,4,3,9,6]));
// [2,2,2,1,4,3,3,9,6,7,19]
```

**Explanation:** Elements in `arr2` get priority based on their position. Elements not in `arr2` go at the end in ascending order.

**Complexity:** Time: O(n log n), Space: O(n)

---

### Problem 4: Intersection of Two Arrays

**Problem Statement:** Find the intersection of two arrays (each element appears as many times as it shows in both).

**Approach:** Sort both arrays and use two pointers.

```javascript
function intersect(nums1, nums2) {
  nums1.sort((a, b) => a - b);
  nums2.sort((a, b) => a - b);

  const result = [];
  let i = 0, j = 0;

  while (i < nums1.length && j < nums2.length) {
    if (nums1[i] === nums2[j]) {
      result.push(nums1[i]);
      i++;
      j++;
    } else if (nums1[i] < nums2[j]) {
      i++;
    } else {
      j++;
    }
  }

  return result;
}

console.log(intersect([1, 2, 2, 1], [2, 2]));       // [2, 2]
console.log(intersect([4, 9, 5], [9, 4, 9, 8, 4])); // [4, 9]
```

**Explanation:** Sort both arrays. Use two pointers — if elements match, add to result and advance both. If one is smaller, advance that pointer to catch up.

**Complexity:** Time: O(n log n + m log m), Space: O(1) excluding output

---

### 🔗 Navigation
Prev: [06_Searching.md](06_Searching.md) | Index: [00_Index.md](00_Index.md) | Next: [08_Recursion.md](08_Recursion.md)
