# 📌 Basics & Complexity Analysis

## 🧠 Concept Explanation (Story Format)

Imagine you're in a library with **1,000 books** on a shelf, and you need to find a specific one. You have two options:

1. **Option A:** Start from the first book and check each one until you find it. In the worst case, you check all 1,000 books.
2. **Option B:** The books are sorted alphabetically. You go to the middle, check if your book comes before or after, and keep halving. You find it in about 10 checks.

Both approaches **work**, but one is clearly **faster**. This is the heart of **complexity analysis** — measuring how efficient an algorithm is as the input grows.

### What is an Algorithm?

An algorithm is just a **step-by-step recipe** to solve a problem. Like a cooking recipe tells you what to do in order, an algorithm tells a computer what to do step by step.

### What is Time Complexity?

Time complexity measures **how many operations** an algorithm performs as the input size `n` grows. We don't measure actual seconds — we count operations.

### What is Space Complexity?

Space complexity measures **how much extra memory** an algorithm uses. If you need to create a new array of size `n`, that's O(n) space.

### Big O Notation — The Universal Language

Big O gives us a way to describe performance:

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Accessing array by index |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Looping through array |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Recursive fibonacci |
| O(n!) | Factorial | Permutations |

### Real-Life Analogy

Think of it like **searching for a friend's house**:
- **O(1):** You know the exact address — go directly.
- **O(n):** You walk down the street checking every house.
- **O(n²):** For every house, you ask every neighbor too.
- **O(log n):** You keep halving the street — "Is it left or right?"

---

## 🐢 Brute Force Approach

### Problem: Find if a number exists in an array

The simplest approach — check every single element.

```javascript
// Brute Force: Linear Search
function findNumber(arr, target) {
  // Loop through every element in the array
  for (let i = 0; i < arr.length; i++) {
    // If current element matches target, return the index
    if (arr[i] === target) {
      return i;
    }
  }
  // If we checked everything and didn't find it, return -1
  return -1;
}

// Example usage
const numbers = [5, 3, 8, 1, 9, 2, 7];
console.log(findNumber(numbers, 9)); // Output: 4
console.log(findNumber(numbers, 6)); // Output: -1
```

### Line-by-Line Explanation

1. **`for (let i = 0; i < arr.length; i++)`** — We start from the first element and go one by one.
2. **`if (arr[i] === target)`** — At each step, we ask: "Is this the number I'm looking for?"
3. **`return i`** — If yes, return where we found it.
4. **`return -1`** — If we went through everything and didn't find it, return -1 (meaning "not found").

---

## ⚡ Optimized Approach

If the array is **sorted**, we can use **Binary Search** — halving the search space each time.

```javascript
// Optimized: Binary Search (only works on sorted arrays)
function binarySearch(arr, target) {
  let left = 0;               // Start of search range
  let right = arr.length - 1;  // End of search range

  while (left <= right) {
    // Find the middle index
    const mid = Math.floor((left + right) / 2);

    if (arr[mid] === target) {
      // Found it! Return the index
      return mid;
    } else if (arr[mid] < target) {
      // Target is in the right half
      left = mid + 1;
    } else {
      // Target is in the left half
      right = mid - 1;
    }
  }

  // Target not found
  return -1;
}

// Example usage
const sortedNumbers = [1, 2, 3, 5, 7, 8, 9];
console.log(binarySearch(sortedNumbers, 7)); // Output: 4
console.log(binarySearch(sortedNumbers, 6)); // Output: -1
```

### Why is this better?

- **Linear Search:** checks up to `n` elements → O(n)
- **Binary Search:** halves the array each time → O(log n)

For 1,000,000 elements:
- Linear Search: up to **1,000,000** checks
- Binary Search: only about **20** checks!

---

## 🔍 Complexity Analysis

### Linear Search (Brute Force)
| Metric | Value |
|--------|-------|
| Time Complexity | O(n) — checks every element |
| Space Complexity | O(1) — no extra space used |

### Binary Search (Optimized)
| Metric | Value |
|--------|-------|
| Time Complexity | O(log n) — halves search space each time |
| Space Complexity | O(1) — no extra space used |

### How to Calculate Complexity — Simple Rules

1. **Single loop** over `n` items → O(n)
2. **Nested loops** (loop inside loop) → O(n²)
3. **Halving the input** each step → O(log n)
4. **Constant operations** (no loops) → O(1)
5. **Drop constants:** O(2n) becomes O(n)
6. **Keep the dominant term:** O(n² + n) becomes O(n²)

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: What is the difference between O(n) and O(n²)?

**Problem Statement:** Explain with code the difference between O(n) and O(n²) complexity.

**Thought Process:** O(n) means one loop through the data. O(n²) means for every element, we loop through all elements again — a loop inside a loop.

#### 🐢 Brute Force — O(n²) Example

```javascript
// O(n²) — Check if array has any duplicates using nested loops
function hasDuplicatesBrute(arr) {
  // For each element...
  for (let i = 0; i < arr.length; i++) {
    // ...compare with every other element
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) {
        return true; // Found a duplicate!
      }
    }
  }
  return false; // No duplicates found
}

console.log(hasDuplicatesBrute([1, 2, 3, 4, 5])); // false
console.log(hasDuplicatesBrute([1, 2, 3, 2, 5])); // true
```

#### ⚡ Optimized — O(n) Example

```javascript
// O(n) — Use a Set to track seen numbers
function hasDuplicatesOptimized(arr) {
  const seen = new Set(); // A Set stores unique values

  for (let i = 0; i < arr.length; i++) {
    // If we've already seen this number, it's a duplicate
    if (seen.has(arr[i])) {
      return true;
    }
    // Otherwise, remember this number
    seen.add(arr[i]);
  }

  return false; // No duplicates found
}

console.log(hasDuplicatesOptimized([1, 2, 3, 4, 5])); // false
console.log(hasDuplicatesOptimized([1, 2, 3, 2, 5])); // true
```

**Simple Explanation:** Imagine you're checking if any student in a class has the same birthday. The brute force way is to ask every student to compare with every other student (n² comparisons). The smart way is to write each birthday on a board and check if it's already there before writing (n checks).

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(n) |

---

### Question 2: Analyze the Time Complexity of the Following Code

**Problem Statement:** What is the time complexity of this code?

```javascript
function mystery(n) {
  let count = 0;
  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= n; j = j * 2) {
      count++;
    }
  }
  return count;
}
```

**Thought Process:**
- The outer loop runs `n` times.
- The inner loop doubles `j` each time (1, 2, 4, 8, ...), so it runs `log n` times.
- Total: **O(n log n)**

#### 🐢 Brute Force — Count Operations Manually

```javascript
// Let's count operations for small n values
function countOps(n) {
  let count = 0;
  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= n; j = j * 2) {
      count++;
    }
  }
  console.log(`n = ${n}, operations = ${count}`);
  return count;
}

countOps(4);   // n = 4, operations = 12  (4 * 3)
countOps(8);   // n = 8, operations = 32  (8 * 4)
countOps(16);  // n = 16, operations = 80 (16 * 5)
// Pattern: n * log2(n) → O(n log n)
```

#### ⚡ Optimized — Mathematical Analysis

```javascript
// We can calculate the count directly without looping
function calculateOps(n) {
  // Inner loop runs log2(n) + 1 times (since j doubles: 1, 2, 4, ..., n)
  const innerLoopCount = Math.floor(Math.log2(n)) + 1;
  // Outer loop runs n times
  // Total = n * (log2(n) + 1)
  const total = n * innerLoopCount;
  console.log(`n = ${n}, calculated ops = ${total}`);
  return total;
}

calculateOps(4);   // 12
calculateOps(8);   // 32
calculateOps(16);  // 80
```

**Simple Explanation:** Think of the outer loop as walking through `n` houses. At each house, you climb stairs — but the staircase only has `log n` steps (because you skip more steps each time by doubling). So total work = n houses × log n stairs = O(n log n).

**Complexity:** O(n log n) time, O(1) space.

---

### Question 3: Best, Average, and Worst Case

**Problem Statement:** Explain best, average, and worst case complexity with an example.

**Thought Process:** Different inputs can make the same algorithm run faster or slower. We analyze three scenarios.

#### 🐢 Brute Force — Linear Search Analysis

```javascript
function linearSearch(arr, target) {
  let comparisons = 0;

  for (let i = 0; i < arr.length; i++) {
    comparisons++;
    if (arr[i] === target) {
      console.log(`Found at index ${i} after ${comparisons} comparisons`);
      return i;
    }
  }

  console.log(`Not found after ${comparisons} comparisons`);
  return -1;
}

const arr = [10, 20, 30, 40, 50];

// Best Case: Target is the first element → O(1)
linearSearch(arr, 10);  // Found at index 0 after 1 comparison

// Average Case: Target is in the middle → O(n/2) → O(n)
linearSearch(arr, 30);  // Found at index 2 after 3 comparisons

// Worst Case: Target is last or not present → O(n)
linearSearch(arr, 50);  // Found at index 4 after 5 comparisons
linearSearch(arr, 99);  // Not found after 5 comparisons
```

#### ⚡ Optimized — Summary

```javascript
// Function to demonstrate all three cases
function analyzeComplexity(arr, target) {
  const n = arr.length;
  const index = arr.indexOf(target);

  if (index === 0) {
    console.log("Best Case: O(1) — found at first position");
  } else if (index === -1 || index === n - 1) {
    console.log("Worst Case: O(n) — at end or not found");
  } else {
    console.log(`Average Case: O(n) — found after checking ~n/2 elements`);
  }
}

analyzeComplexity([10, 20, 30, 40, 50], 10); // Best Case: O(1)
analyzeComplexity([10, 20, 30, 40, 50], 30); // Average Case: O(n)
analyzeComplexity([10, 20, 30, 40, 50], 99); // Worst Case: O(n)
```

**Simple Explanation:** Imagine searching for your friend in a queue. Best case: they're first in line (1 check). Average case: they're somewhere in the middle. Worst case: they're at the very end or not even in the queue.

**Complexity:**
| Case | Time |
|------|------|
| Best | O(1) |
| Average | O(n) |
| Worst | O(n) |

---

### Question 4: Space Complexity — In-Place vs Extra Space

**Problem Statement:** Reverse an array. Show an in-place solution (O(1) space) and one using extra space (O(n) space).

**Thought Process:** In-place means we modify the original array without creating a new one. Extra space means we create a new array.

#### 🐢 Brute Force — O(n) Extra Space

```javascript
// Create a new reversed array
function reverseBrute(arr) {
  const reversed = []; // Extra array — O(n) space

  // Go from end to start, push each element
  for (let i = arr.length - 1; i >= 0; i--) {
    reversed.push(arr[i]);
  }

  return reversed;
}

console.log(reverseBrute([1, 2, 3, 4, 5])); // [5, 4, 3, 2, 1]
```

#### ⚡ Optimized — O(1) In-Place

```javascript
// Swap elements from both ends moving inward
function reverseInPlace(arr) {
  let left = 0;
  let right = arr.length - 1;

  while (left < right) {
    // Swap elements at left and right positions
    [arr[left], arr[right]] = [arr[right], arr[left]];
    left++;   // Move left pointer right
    right--;  // Move right pointer left
  }

  return arr;
}

const myArr = [1, 2, 3, 4, 5];
console.log(reverseInPlace(myArr)); // [5, 4, 3, 2, 1]
```

**Simple Explanation:** Imagine you have 5 cards in a row. The brute force way is to get 5 new cards and write the numbers in reverse. The smart way is to just swap the first card with the last, then the second with the second-to-last, and so on. No extra cards needed!

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Optimized | O(n) | O(1) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Sum of All Elements in an Array

**Problem Statement:** Given an array of numbers, find the sum of all elements.

**Approach:** Loop through the array and add each element to a running total.

```javascript
function sumArray(arr) {
  let sum = 0; // Start with sum = 0

  for (let i = 0; i < arr.length; i++) {
    sum += arr[i]; // Add each element to sum
  }

  return sum;
}

console.log(sumArray([1, 2, 3, 4, 5]));  // 15
console.log(sumArray([10, 20, 30]));      // 60
console.log(sumArray([-1, 0, 1]));        // 0
```

**Explanation:** We walk through every number, adding it to our total. Like counting money in a piggy bank — pick each coin, add it to your count.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 2: Find the Maximum Element

**Problem Statement:** Given an array, find the largest number.

**Approach:** Assume the first element is the largest. Compare with each subsequent element.

```javascript
function findMax(arr) {
  if (arr.length === 0) return null; // Handle empty array

  let max = arr[0]; // Assume first element is largest

  for (let i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
      max = arr[i]; // Found a bigger number, update max
    }
  }

  return max;
}

console.log(findMax([3, 7, 2, 9, 1]));   // 9
console.log(findMax([-5, -2, -8, -1]));   // -1
console.log(findMax([42]));                // 42
```

**Explanation:** Imagine you're in a room full of people looking for the tallest person. You start by pointing at the first person. Then you look at each person — if they're taller than who you're pointing at, you point at them instead.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 3: Count Occurrences of a Target

**Problem Statement:** Given an array and a target value, count how many times the target appears.

**Approach:** Loop through the array, increment a counter each time we find the target.

```javascript
function countOccurrences(arr, target) {
  let count = 0;

  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === target) {
      count++; // Found one more occurrence
    }
  }

  return count;
}

console.log(countOccurrences([1, 2, 3, 2, 4, 2], 2));  // 3
console.log(countOccurrences([5, 5, 5, 5], 5));          // 4
console.log(countOccurrences([1, 2, 3], 7));              // 0
```

**Explanation:** Like counting how many red cars you see on a road trip. Every time you spot one, you add 1 to your count.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 4: Check if Array is Sorted

**Problem Statement:** Given an array, check if it is sorted in non-decreasing order.

**Approach:** Compare each element with the next one. If any element is greater than the next, it's not sorted.

```javascript
function isSorted(arr) {
  for (let i = 0; i < arr.length - 1; i++) {
    if (arr[i] > arr[i + 1]) {
      return false; // Found an element larger than the next
    }
  }
  return true; // All elements are in order
}

console.log(isSorted([1, 2, 3, 4, 5]));   // true
console.log(isSorted([1, 3, 2, 4, 5]));   // false
console.log(isSorted([5, 5, 5]));          // true
console.log(isSorted([1]));                // true
```

**Explanation:** Imagine a line of students sorted by height. You walk along the line checking: "Is the next person at least as tall as the current one?" If you find someone shorter, the line isn't sorted.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 5: Fibonacci — Understand Exponential vs Linear Complexity

**Problem Statement:** Calculate the nth Fibonacci number using both recursive (exponential) and iterative (linear) approaches.

**Approach:**
- Recursive: Simple but very slow — O(2ⁿ)
- Iterative: Loop from bottom up — O(n)

```javascript
// 🐢 Brute Force: Recursive — O(2ⁿ) time!
function fibRecursive(n) {
  if (n <= 1) return n;
  return fibRecursive(n - 1) + fibRecursive(n - 2);
}

// ⚡ Optimized: Iterative — O(n) time
function fibIterative(n) {
  if (n <= 1) return n;

  let prev2 = 0; // fib(0)
  let prev1 = 1; // fib(1)

  for (let i = 2; i <= n; i++) {
    const current = prev1 + prev2; // Next fibonacci = sum of previous two
    prev2 = prev1;                 // Shift window forward
    prev1 = current;
  }

  return prev1;
}

console.log(fibRecursive(10)); // 55
console.log(fibIterative(10)); // 55
console.log(fibIterative(50)); // 12586269025 (recursive would take forever!)
```

**Explanation:** The recursive approach is like asking two friends to each ask two more friends, and so on — the number of people explodes! The iterative approach is like two friends walking together, always keeping track of the last two answers. Much simpler and faster.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Recursive | O(2ⁿ) | O(n) — call stack |
| Iterative | O(n) | O(1) |

---

### 🔗 Navigation
Prev: None | Index: [00_Index.md](00_Index.md) | Next: [02_Arrays.md](02_Arrays.md)
