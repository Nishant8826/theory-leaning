# 📌 Sliding Window

## 🧠 Concept Explanation (Story Format)

Imagine you're on a **train** looking out the window. As the train moves, you see different scenery — but the **size of your window stays the same**. The view changes because the window **slides** along the landscape.

That's exactly what the **Sliding Window** technique does! Instead of recalculating everything from scratch for each subarray or substring, we **slide** a window across the data, adding one element on the right and removing one on the left.

### Why Sliding Window?

Many problems ask about **contiguous subarrays or substrings** of a certain size or condition:
- "Find the maximum sum of k consecutive elements"
- "Find the smallest subarray with sum ≥ target"
- "Find the longest substring with at most k distinct characters"

Without sliding window, you'd recompute the sum/condition for every possible window — wasting time!

### Two Types of Sliding Windows

| Type | Window Size | When to Use |
|------|-------------|-------------|
| **Fixed Size** | Always `k` elements | "Find max/min of every k-sized subarray" |
| **Variable Size** | Grows and shrinks | "Find smallest subarray with sum ≥ target" |

### Real-Life Analogy

Think of calculating a **7-day moving average** of temperatures. Instead of adding all 7 days each time, when a new day comes in, you add the new day's temperature and subtract the oldest day's temperature. The "window" of 7 days slides forward by one day.

---

## 🐢 Brute Force Approach

### Problem: Maximum Sum of K Consecutive Elements

Given an array of integers and a number `k`, find the maximum sum of `k` consecutive elements.

```javascript
// Brute Force: Recalculate sum for every window
function maxSumBrute(arr, k) {
  if (arr.length < k) return null;

  let maxSum = -Infinity;

  // Try every window of size k
  for (let i = 0; i <= arr.length - k; i++) {
    let windowSum = 0;

    // Calculate sum of current window
    for (let j = i; j < i + k; j++) {
      windowSum += arr[j];
    }

    maxSum = Math.max(maxSum, windowSum);
  }

  return maxSum;
}

console.log(maxSumBrute([2, 1, 5, 1, 3, 2], 3)); // 9 (5+1+3)
console.log(maxSumBrute([2, 3, 4, 1, 5], 2));     // 7 (3+4)
```

### Line-by-Line Explanation

1. **Outer loop** — slides to each starting position of a window.
2. **Inner loop** — adds up all `k` elements in the current window.
3. For each window, we recalculate the sum from scratch — wasteful!

---

## ⚡ Optimized Approach

Slide the window: add the new element entering the right side, subtract the element leaving the left side.

```javascript
// Optimized: Sliding Window — O(n)
function maxSumOptimized(arr, k) {
  if (arr.length < k) return null;

  // Calculate sum of the first window
  let windowSum = 0;
  for (let i = 0; i < k; i++) {
    windowSum += arr[i];
  }

  let maxSum = windowSum;

  // Slide the window: add right element, remove left element
  for (let i = k; i < arr.length; i++) {
    windowSum += arr[i];       // Add new element entering window
    windowSum -= arr[i - k];   // Remove element leaving window
    maxSum = Math.max(maxSum, windowSum);
  }

  return maxSum;
}

console.log(maxSumOptimized([2, 1, 5, 1, 3, 2], 3)); // 9
console.log(maxSumOptimized([2, 3, 4, 1, 5], 2));     // 7
```

### Why is this better?

- **Brute force:** For each of `n-k+1` windows, we add `k` elements → O(n×k)
- **Sliding window:** We compute the first window sum, then each slide is just one add and one subtract → O(n)

---

## 🔍 Complexity Analysis

| Approach | Time Complexity | Space Complexity |
|----------|----------------|-----------------|
| Brute Force | O(n × k) | O(1) |
| Sliding Window | O(n) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Minimum Size Subarray Sum

**Problem Statement:** Find the smallest contiguous subarray whose sum is ≥ target. Return its length, or 0 if no such subarray.

Example: `target = 7, arr = [2, 3, 1, 2, 4, 3]` → `2` (subarray `[4, 3]`)

**Thought Process:** Use a variable-size sliding window. Expand right to increase sum. When sum ≥ target, try to shrink from left to find the minimum length.

#### 🐢 Brute Force

```javascript
function minSubArrayLenBrute(target, arr) {
  let minLen = Infinity;

  for (let i = 0; i < arr.length; i++) {
    let sum = 0;
    for (let j = i; j < arr.length; j++) {
      sum += arr[j];
      if (sum >= target) {
        minLen = Math.min(minLen, j - i + 1);
        break; // Found shortest starting at i
      }
    }
  }

  return minLen === Infinity ? 0 : minLen;
}

console.log(minSubArrayLenBrute(7, [2, 3, 1, 2, 4, 3])); // 2
```

#### ⚡ Optimized — Variable Sliding Window

```javascript
function minSubArrayLenOptimized(target, arr) {
  let minLen = Infinity;
  let sum = 0;
  let start = 0;

  for (let end = 0; end < arr.length; end++) {
    sum += arr[end]; // Expand window

    // Shrink window while condition is met
    while (sum >= target) {
      minLen = Math.min(minLen, end - start + 1);
      sum -= arr[start]; // Remove from left
      start++;           // Shrink window
    }
  }

  return minLen === Infinity ? 0 : minLen;
}

console.log(minSubArrayLenOptimized(7, [2, 3, 1, 2, 4, 3])); // 2
console.log(minSubArrayLenOptimized(15, [1, 2, 3, 4, 5]));    // 5
```

**Simple Explanation:** Imagine you're eating candy from a conveyor belt. You keep adding candy until you have enough (≥ target). Then you try eating from the left to see the minimum candies needed. Keep sliding to check all possibilities.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(1) |

---

### Question 2: Longest Substring with At Most K Distinct Characters

**Problem Statement:** Find the length of the longest substring with at most `k` distinct characters.

Example: `s = "eceba", k = 2` → `3` ("ece")

**Thought Process:** Use a sliding window with a hash map to track character frequencies. Shrink from left when distinct characters exceed `k`.


#### Code Story
- This problem is about finding the longest stretch of text that uses only k different types of letters.
- First, we expand our window and count how many different letters are inside using a map.
- Then, if we exceed k types, we shrink the window from the left until we are back down to k.
- Finally, we keep track of the largest window size that stayed within the rules.
- This works because the window acts like an accordion—expanding as long as it's allowed and contracting only when it breaks the rule.

#### 🐢 Brute Force

```javascript
function longestWithKDistinctBrute(s, k) {
  let maxLen = 0;

  for (let i = 0; i < s.length; i++) {
    const seen = new Set();
    for (let j = i; j < s.length; j++) {
      seen.add(s[j]);
      if (seen.size > k) break; // Too many distinct chars
      maxLen = Math.max(maxLen, j - i + 1);
    }
  }

  return maxLen;
}

console.log(longestWithKDistinctBrute("eceba", 2)); // 3
```

#### ⚡ Optimized — Sliding Window + Hash Map

```javascript
function longestWithKDistinctOptimized(s, k) {
  const charCount = new Map(); // Character → frequency
  let maxLen = 0;
  let start = 0;

  for (let end = 0; end < s.length; end++) {
    // Add right character
    charCount.set(s[end], (charCount.get(s[end]) || 0) + 1);

    // Shrink window if too many distinct characters
    while (charCount.size > k) {
      const leftChar = s[start];
      charCount.set(leftChar, charCount.get(leftChar) - 1);
      if (charCount.get(leftChar) === 0) {
        charCount.delete(leftChar); // Remove character completely
      }
      start++;
    }

    maxLen = Math.max(maxLen, end - start + 1);
  }

  return maxLen;
}

console.log(longestWithKDistinctOptimized("eceba", 2));   // 3
console.log(longestWithKDistinctOptimized("aabacbebebe", 3)); // 7
```

**Simple Explanation:** You're reading a book and highlighting with colored markers. You can only use `k` colors. As you read forward, you add new characters. When you use too many colors, erase highlights from the beginning until you're back to `k` colors.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(n) |
| Optimized | O(n) | O(k) |

---

### Question 3: Maximum of All Subarrays of Size K

**Problem Statement:** Given an array and integer `k`, find the maximum element in every contiguous subarray of size `k`.

Example: `arr = [1, 3, -1, -3, 5, 3, 6, 7], k = 3` → `[3, 3, 5, 5, 6, 7]`

**Thought Process:** Use a deque (double-ended queue) to maintain indices of potential maximums in the current window.

#### 🐢 Brute Force

```javascript
function maxOfSubarraysBrute(arr, k) {
  const result = [];

  for (let i = 0; i <= arr.length - k; i++) {
    let max = arr[i];
    for (let j = i; j < i + k; j++) {
      max = Math.max(max, arr[j]);
    }
    result.push(max);
  }

  return result;
}

console.log(maxOfSubarraysBrute([1, 3, -1, -3, 5, 3, 6, 7], 3));
// [3, 3, 5, 5, 6, 7]
```

#### ⚡ Optimized — Deque (Monotonic Queue)

```javascript
function maxOfSubarraysOptimized(arr, k) {
  const result = [];
  const deque = []; // Store indices, front is always the max

  for (let i = 0; i < arr.length; i++) {
    // Remove indices outside the current window
    if (deque.length > 0 && deque[0] <= i - k) {
      deque.shift();
    }

    // Remove smaller elements from the back (they'll never be max)
    while (deque.length > 0 && arr[deque[deque.length - 1]] <= arr[i]) {
      deque.pop();
    }

    deque.push(i); // Add current index

    // Window is fully formed, record the max
    if (i >= k - 1) {
      result.push(arr[deque[0]]); // Front of deque is the max
    }
  }

  return result;
}

console.log(maxOfSubarraysOptimized([1, 3, -1, -3, 5, 3, 6, 7], 3));
// [3, 3, 5, 5, 6, 7]
```

**Simple Explanation:** Imagine a leaderboard that always shows the tallest person in a group of `k` people sliding through a queue. As new people enter, anyone shorter who entered before them will never be the tallest — remove them. The front of the deque always has the current window's champion.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n × k) | O(1) |
| Optimized | O(n) | O(k) |

---

### Question 4: Count Number of Nice Subarrays

**Problem Statement:** Given an array and integer `k`, find the count of subarrays with exactly `k` odd numbers.

Example: `arr = [1, 1, 2, 1, 1], k = 3` → `2`

**Thought Process:** Use the "at most K" trick: exactly(k) = atMost(k) - atMost(k-1).

#### 🐢 Brute Force

```javascript
function countNiceSubarraysBrute(arr, k) {
  let count = 0;

  for (let i = 0; i < arr.length; i++) {
    let oddCount = 0;
    for (let j = i; j < arr.length; j++) {
      if (arr[j] % 2 !== 0) oddCount++;
      if (oddCount === k) count++;
      if (oddCount > k) break;
    }
  }

  return count;
}

console.log(countNiceSubarraysBrute([1, 1, 2, 1, 1], 3)); // 2
```

#### ⚡ Optimized — Sliding Window with "At Most K" Trick

```javascript
function countNiceSubarraysOptimized(arr, k) {
  // Subarrays with exactly k odds = atMost(k) - atMost(k-1)
  return atMostK(arr, k) - atMostK(arr, k - 1);
}

function atMostK(arr, k) {
  let count = 0;
  let oddCount = 0;
  let start = 0;

  for (let end = 0; end < arr.length; end++) {
    if (arr[end] % 2 !== 0) oddCount++;

    while (oddCount > k) {
      if (arr[start] % 2 !== 0) oddCount--;
      start++;
    }

    // All subarrays ending at 'end' with start from current 'start' to 'end'
    count += end - start + 1;
  }

  return count;
}

console.log(countNiceSubarraysOptimized([1, 1, 2, 1, 1], 3)); // 2
console.log(countNiceSubarraysOptimized([2, 4, 6], 1));         // 0
```

**Simple Explanation:** Counting "exactly k" is tricky. But counting "at most k" is easier with a sliding window. So we use the formula: exactly(k) = atMost(k) - atMost(k-1). Like asking "how many groups have at most 3 people?" minus "how many have at most 2 people?" to get "exactly 3 people groups."

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(1) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Average of All Subarrays of Size K

**Problem Statement:** Find the average of all contiguous subarrays of size `k`.

**Approach:** Fixed-size sliding window. Maintain a running sum.

```javascript
function averageOfSubarrays(arr, k) {
  const result = [];
  let windowSum = 0;

  for (let i = 0; i < arr.length; i++) {
    windowSum += arr[i]; // Add to window

    if (i >= k - 1) {
      result.push(windowSum / k); // Record average
      windowSum -= arr[i - k + 1]; // Remove leftmost
    }
  }

  return result;
}

console.log(averageOfSubarrays([1, 3, 2, 6, -1, 4, 1, 8, 2], 5));
// [2.2, 2.8, 2.4, 3.6, 2.8]
```

**Explanation:** Keep a running sum. Once the window has `k` elements, record the average and remove the oldest element before adding the next.

**Complexity:** Time: O(n), Space: O(n - k + 1) for result

---

### Problem 2: Maximum Consecutive Ones After Flipping K Zeros

**Problem Statement:** Given a binary array and `k`, find the longest stretch of 1s if you can flip at most `k` zeros to 1s.

**Approach:** Sliding window. Count zeros in window. If zeros > k, shrink from left.

```javascript
function longestOnes(arr, k) {
  let maxLen = 0;
  let zeroCount = 0;
  let start = 0;

  for (let end = 0; end < arr.length; end++) {
    if (arr[end] === 0) zeroCount++;

    // Shrink window if too many zeros
    while (zeroCount > k) {
      if (arr[start] === 0) zeroCount--;
      start++;
    }

    maxLen = Math.max(maxLen, end - start + 1);
  }

  return maxLen;
}

console.log(longestOnes([1, 1, 0, 0, 1, 1, 1, 0, 1, 1], 2)); // 8
console.log(longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0], 3)); // 9
```

**Explanation:** Expand the window to include more elements. When the window has more than `k` zeros, shrink from the left. The longest valid window is our answer.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 3: Fruit Into Baskets

**Problem Statement:** You have a row of fruit trees. Each tree has a type. You carry 2 baskets, each can hold one type. Find the maximum number of fruits you can collect in a contiguous section using only 2 baskets.

**Approach:** This is "longest substring with at most 2 distinct characters."

```javascript
function totalFruit(fruits) {
  const basket = new Map(); // type → count
  let maxFruits = 0;
  let start = 0;

  for (let end = 0; end < fruits.length; end++) {
    basket.set(fruits[end], (basket.get(fruits[end]) || 0) + 1);

    // More than 2 types? Shrink window
    while (basket.size > 2) {
      const leftFruit = fruits[start];
      basket.set(leftFruit, basket.get(leftFruit) - 1);
      if (basket.get(leftFruit) === 0) basket.delete(leftFruit);
      start++;
    }

    maxFruits = Math.max(maxFruits, end - start + 1);
  }

  return maxFruits;
}

console.log(totalFruit([1, 2, 1]));       // 3
console.log(totalFruit([0, 1, 2, 2]));    // 3
console.log(totalFruit([1, 2, 3, 2, 2])); // 4
```

**Explanation:** Walk through the orchard. Pick fruits and track types in your baskets. When you have more than 2 types, drop the oldest type from the left. Track the longest valid stretch.

**Complexity:** Time: O(n), Space: O(1) — at most 3 entries in map

---

### Problem 4: Find All Anagrams in a String

**Problem Statement:** Find all start indices in string `s` where an anagram of string `p` begins.

Example: `s = "cbaebabacd", p = "abc"` → `[0, 6]`

**Approach:** Fixed-size sliding window of length `p.length`. Compare character frequencies.

```javascript
function findAnagrams(s, p) {
  const result = [];
  if (s.length < p.length) return result;

  const pFreq = new Map();
  const windowFreq = new Map();

  // Count frequency of characters in p
  for (const ch of p) {
    pFreq.set(ch, (pFreq.get(ch) || 0) + 1);
  }

  for (let i = 0; i < s.length; i++) {
    // Add character to window
    windowFreq.set(s[i], (windowFreq.get(s[i]) || 0) + 1);

    // Remove character leaving the window
    if (i >= p.length) {
      const leftChar = s[i - p.length];
      windowFreq.set(leftChar, windowFreq.get(leftChar) - 1);
      if (windowFreq.get(leftChar) === 0) windowFreq.delete(leftChar);
    }

    // Compare frequency maps
    if (i >= p.length - 1 && mapsEqual(windowFreq, pFreq)) {
      result.push(i - p.length + 1);
    }
  }

  return result;
}

function mapsEqual(map1, map2) {
  if (map1.size !== map2.size) return false;
  for (const [key, val] of map1) {
    if (map2.get(key) !== val) return false;
  }
  return true;
}

console.log(findAnagrams("cbaebabacd", "abc")); // [0, 6]
console.log(findAnagrams("abab", "ab"));         // [0, 1, 2]
```

**Explanation:** Slide a window of size `p.length` over `s`. At each position, check if the characters in the window match the frequency of characters in `p`. If yes, it's an anagram!

**Complexity:** Time: O(n × 26) ≈ O(n), Space: O(1) — at most 26 characters

---

### 🔗 Navigation
Prev: [04_Two_Pointers.md](04_Two_Pointers.md) | Index: [00_Index.md](00_Index.md) | Next: [06_Searching.md](06_Searching.md)
