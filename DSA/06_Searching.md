# 📌 Searching

## 🧠 Concept Explanation (Story Format)

Imagine you've lost your keys somewhere in your house. You have two strategies:

1. **Linear Search:** Check every room, every drawer, every pocket — one by one. Guaranteed to find them, but slow.
2. **Binary Search:** If your rooms are organized (sorted), you can think: "Are my keys more likely upstairs or downstairs?" Then check only that half. Keep halving until you find them.

**Searching** is one of the most fundamental operations in computer science — finding a specific item in a collection of data.

### Types of Searching

| Algorithm | Requirement | Time Complexity | How It Works |
|-----------|------------|----------------|--------------|
| Linear Search | None | O(n) | Check every element |
| Binary Search | Sorted data | O(log n) | Halve the search space |

### Where Searching is Used

- Finding a contact in your phone
- Looking up a word in a dictionary
- Database queries
- Autocomplete suggestions
- Finding bugs in code (binary search on commits!)

### Real-Life Analogy

**Linear Search** = Reading every page of a book to find a word.
**Binary Search** = Using a dictionary — open to the middle, decide left or right, keep halving.

---

## 🐢 Brute Force Approach

### Problem: Find a Target in an Array

```javascript
// Linear Search — works on any array
function linearSearch(arr, target) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === target) {
      return i; // Found! Return the index
    }
  }
  return -1; // Not found
}

console.log(linearSearch([4, 2, 7, 1, 9, 3], 7)); // 2
console.log(linearSearch([4, 2, 7, 1, 9, 3], 5)); // -1
```

### Line-by-Line Explanation

1. **Loop through every element** — start at index 0, go to the end.
2. **Compare each element** with the target.
3. If found, return the index immediately.
4. If the loop ends without finding, return -1.

---

## ⚡ Optimized Approach

### Binary Search — Only works on sorted arrays

```javascript
// Binary Search — O(log n)
function binarySearch(arr, target) {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (arr[mid] === target) {
      return mid; // Found it!
    } else if (arr[mid] < target) {
      left = mid + 1; // Target is in the right half
    } else {
      right = mid - 1; // Target is in the left half
    }
  }

  return -1; // Not found
}

console.log(binarySearch([1, 2, 3, 4, 7, 9], 7)); // 4
console.log(binarySearch([1, 2, 3, 4, 7, 9], 5)); // -1
```

### How Binary Search Works — Step by Step

For array `[1, 3, 5, 7, 9, 11, 13]`, target = `7`:

```
Step 1: left=0, right=6, mid=3 → arr[3]=7 → FOUND!

For target = 11:
Step 1: left=0, right=6, mid=3 → arr[3]=7 < 11 → left=4
Step 2: left=4, right=6, mid=5 → arr[5]=11 → FOUND!
```

Each step eliminates **half** the remaining elements!

---

## 🔍 Complexity Analysis

| Algorithm | Time (Best) | Time (Worst) | Space |
|-----------|------------|-------------|-------|
| Linear Search | O(1) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(1) |

### Why O(log n)?

If you have 1,000,000 elements:
- Linear Search: up to **1,000,000** checks
- Binary Search: at most **20** checks (2²⁰ ≈ 1,000,000)

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Find First and Last Position of Element in Sorted Array

**Problem Statement:** Given a sorted array with possible duplicates, find the first and last position of a target value.

Example: `arr = [5, 7, 7, 8, 8, 10], target = 8` → `[3, 4]`

**Thought Process:** Use binary search twice — once to find the leftmost occurrence, once for the rightmost.

#### 🐢 Brute Force

```javascript
function searchRangeBrute(arr, target) {
  let first = -1, last = -1;

  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === target) {
      if (first === -1) first = i; // First occurrence
      last = i; // Keep updating last
    }
  }

  return [first, last];
}

console.log(searchRangeBrute([5, 7, 7, 8, 8, 10], 8)); // [3, 4]
console.log(searchRangeBrute([5, 7, 7, 8, 8, 10], 6)); // [-1, -1]
```

#### ⚡ Optimized — Two Binary Searches

```javascript
function searchRangeOptimized(arr, target) {
  return [findFirst(arr, target), findLast(arr, target)];
}

function findFirst(arr, target) {
  let left = 0, right = arr.length - 1;
  let result = -1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) {
      result = mid;      // Found, but keep searching left for earlier occurrence
      right = mid - 1;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return result;
}

function findLast(arr, target) {
  let left = 0, right = arr.length - 1;
  let result = -1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) {
      result = mid;     // Found, but keep searching right for later occurrence
      left = mid + 1;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return result;
}

console.log(searchRangeOptimized([5, 7, 7, 8, 8, 10], 8)); // [3, 4]
console.log(searchRangeOptimized([5, 7, 7, 8, 8, 10], 6)); // [-1, -1]
```

**Simple Explanation:** Standard binary search stops when it finds the target. But with duplicates, we need the FIRST and LAST positions. For the first position, when we find the target, we don't stop — we continue searching LEFT. For the last, we continue searching RIGHT.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(1) |
| Optimized | O(log n) | O(1) |

---

### Question 2: Search in Rotated Sorted Array

**Problem Statement:** A sorted array has been rotated at some pivot. Find the target in O(log n).

Example: `arr = [4, 5, 6, 7, 0, 1, 2], target = 0` → `4`

**Thought Process:** In a rotated sorted array, at least one half is always sorted. Determine which half is sorted and check if the target lies in that half.

#### 🐢 Brute Force

```javascript
function searchRotatedBrute(arr, target) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === target) return i;
  }
  return -1;
}

console.log(searchRotatedBrute([4, 5, 6, 7, 0, 1, 2], 0)); // 4
```

#### ⚡ Optimized — Modified Binary Search

```javascript
function searchRotatedOptimized(arr, target) {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (arr[mid] === target) return mid;

    // Check which half is sorted
    if (arr[left] <= arr[mid]) {
      // Left half is sorted
      if (target >= arr[left] && target < arr[mid]) {
        right = mid - 1; // Target is in sorted left half
      } else {
        left = mid + 1;  // Target is in right half
      }
    } else {
      // Right half is sorted
      if (target > arr[mid] && target <= arr[right]) {
        left = mid + 1;  // Target is in sorted right half
      } else {
        right = mid - 1; // Target is in left half
      }
    }
  }

  return -1;
}

console.log(searchRotatedOptimized([4, 5, 6, 7, 0, 1, 2], 0)); // 4
console.log(searchRotatedOptimized([4, 5, 6, 7, 0, 1, 2], 3)); // -1
```

**Simple Explanation:** Imagine a clock with sorted numbers, but someone rotated the ring. At any point, at least one side (left or right of middle) is still in order. Check if your target is in the ordered side — if yes, search there. If not, search the other side.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(1) |
| Optimized | O(log n) | O(1) |

---

### Question 3: Find Peak Element

**Problem Statement:** Find any peak element (greater than its neighbors). The array may have multiple peaks.

Example: `[1, 2, 3, 1]` → index `2` (element 3)

**Thought Process:** Use binary search. If the middle element is less than its right neighbor, a peak must exist on the right. Otherwise, a peak exists on the left (or mid itself).

#### 🐢 Brute Force

```javascript
function findPeakBrute(arr) {
  for (let i = 0; i < arr.length; i++) {
    const leftOk = i === 0 || arr[i] > arr[i - 1];
    const rightOk = i === arr.length - 1 || arr[i] > arr[i + 1];
    if (leftOk && rightOk) return i;
  }
  return -1;
}

console.log(findPeakBrute([1, 2, 3, 1]));    // 2
console.log(findPeakBrute([1, 2, 1, 3, 5])); // 1 (or 4)
```

#### ⚡ Optimized — Binary Search

```javascript
function findPeakOptimized(arr) {
  let left = 0;
  let right = arr.length - 1;

  while (left < right) {
    const mid = Math.floor((left + right) / 2);

    if (arr[mid] < arr[mid + 1]) {
      // Rising → peak must be on the right
      left = mid + 1;
    } else {
      // Falling or peak → peak is at mid or left
      right = mid;
    }
  }

  return left; // left === right === peak index
}

console.log(findPeakOptimized([1, 2, 3, 1]));       // 2
console.log(findPeakOptimized([1, 2, 1, 3, 5, 6])); // 5
```

**Simple Explanation:** Imagine climbing a mountain with your eyes closed. At any point, feel the slope. If the ground goes up to the right, keep going right — a peak is ahead. If it goes down, a peak is behind (or you're on it). You'll always find a peak!

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(1) |
| Optimized | O(log n) | O(1) |

---

### Question 4: Find Square Root (Integer)

**Problem Statement:** Given a non-negative integer `x`, return the integer square root (floor of actual square root).

Example: `sqrt(8)` → `2` (since 2² = 4 ≤ 8, 3² = 9 > 8)

**Thought Process:** Binary search between 0 and x. Check if mid² ≤ x.

#### 🐢 Brute Force

```javascript
function mySqrtBrute(x) {
  if (x < 2) return x;

  let result = 0;
  for (let i = 1; i <= x; i++) {
    if (i * i <= x) {
      result = i;
    } else {
      break;
    }
  }

  return result;
}

console.log(mySqrtBrute(8));  // 2
console.log(mySqrtBrute(16)); // 4
```

#### ⚡ Optimized — Binary Search

```javascript
function mySqrtOptimized(x) {
  if (x < 2) return x;

  let left = 1;
  let right = Math.floor(x / 2);
  let result = 0;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    const square = mid * mid;

    if (square === x) {
      return mid; // Perfect square
    } else if (square < x) {
      result = mid;    // Could be the answer
      left = mid + 1;  // Try a bigger number
    } else {
      right = mid - 1; // Too big
    }
  }

  return result;
}

console.log(mySqrtOptimized(8));   // 2
console.log(mySqrtOptimized(16));  // 4
console.log(mySqrtOptimized(100)); // 10
```

**Simple Explanation:** Guess the square root by trying the middle number. If its square is too small, guess higher. If too big, guess lower. This is like a guessing game: "Is the number bigger or smaller than my guess?"

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(√x) | O(1) |
| Optimized | O(log x) | O(1) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Search Insert Position

**Problem Statement:** Given a sorted array and target, find the index where it would be inserted to keep the array sorted.

**Approach:** Binary search. If not found, `left` will be at the correct insert position.

```javascript
function searchInsert(arr, target) {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }

  return left; // Insert position
}

console.log(searchInsert([1, 3, 5, 6], 5)); // 2
console.log(searchInsert([1, 3, 5, 6], 2)); // 1
console.log(searchInsert([1, 3, 5, 6], 7)); // 4
console.log(searchInsert([1, 3, 5, 6], 0)); // 0
```

**Explanation:** Like finding where to insert a book on a sorted shelf. Binary search narrows it down. If the exact book isn't there, `left` points to where it should go.

**Complexity:** Time: O(log n), Space: O(1)

---

### Problem 2: Count Occurrences in Sorted Array

**Problem Statement:** Count how many times a target appears in a sorted array.

**Approach:** Find first and last position using binary search, then count = last - first + 1.

```javascript
function countOccurrences(arr, target) {
  const first = findBound(arr, target, true);
  if (first === -1) return 0;
  const last = findBound(arr, target, false);
  return last - first + 1;
}

function findBound(arr, target, isFirst) {
  let left = 0, right = arr.length - 1;
  let result = -1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) {
      result = mid;
      if (isFirst) right = mid - 1; // Keep searching left
      else left = mid + 1;          // Keep searching right
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return result;
}

console.log(countOccurrences([1, 2, 2, 2, 3, 4], 2)); // 3
console.log(countOccurrences([1, 2, 3, 4, 5], 6));     // 0
```

**Explanation:** Find where the target starts and where it ends in the sorted array. The count is just the distance between those positions plus one.

**Complexity:** Time: O(log n), Space: O(1)

---

### Problem 3: Find Minimum in Rotated Sorted Array

**Problem Statement:** A sorted array was rotated. Find the minimum element.

**Approach:** Binary search. The minimum is where the rotation "breaks" the sorted order.

```javascript
function findMin(arr) {
  let left = 0;
  let right = arr.length - 1;

  while (left < right) {
    const mid = Math.floor((left + right) / 2);

    if (arr[mid] > arr[right]) {
      // Rotation point is in the right half
      left = mid + 1;
    } else {
      // Minimum is in the left half (including mid)
      right = mid;
    }
  }

  return arr[left];
}

console.log(findMin([3, 4, 5, 1, 2]));    // 1
console.log(findMin([4, 5, 6, 7, 0, 1])); // 0
console.log(findMin([1, 2, 3, 4, 5]));    // 1 (not rotated)
```

**Explanation:** In a rotated sorted array, the minimum is at the "break point." If the middle is bigger than the rightmost, the break is on the right. Otherwise, it's on the left (or at mid).

**Complexity:** Time: O(log n), Space: O(1)

---

### Problem 4: Search a 2D Matrix

**Problem Statement:** Search for a target in a matrix where each row is sorted and the first element of each row is greater than the last element of the previous row.

**Approach:** Treat the entire matrix as a 1D sorted array and apply binary search.

```javascript
function searchMatrix(matrix, target) {
  const rows = matrix.length;
  const cols = matrix[0].length;
  let left = 0;
  let right = rows * cols - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    // Convert 1D index to 2D coordinates
    const row = Math.floor(mid / cols);
    const col = mid % cols;
    const value = matrix[row][col];

    if (value === target) return true;
    if (value < target) left = mid + 1;
    else right = mid - 1;
  }

  return false;
}

const matrix = [
  [1,  3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 60]
];

console.log(searchMatrix(matrix, 3));  // true
console.log(searchMatrix(matrix, 13)); // false
```

**Explanation:** The matrix is essentially a sorted array broken into rows. Map any 1D index to 2D using: row = index ÷ cols, col = index % cols. Then binary search as usual.

**Complexity:** Time: O(log(m × n)), Space: O(1)

---

### 🔗 Navigation
Prev: [05_Sliding_Window.md](05_Sliding_Window.md) | Index: [00_Index.md](00_Index.md) | Next: [07_Sorting.md](07_Sorting.md)
