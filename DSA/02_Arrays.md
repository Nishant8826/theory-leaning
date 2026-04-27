# 📌 Arrays

## 🧠 Concept Explanation (Story Format)

Imagine you have a **row of lockers** in a school hallway. Each locker has a **number** (0, 1, 2, 3...) and can hold **one item**. You can instantly open any locker if you know its number — that's an **array**!

An array is the most fundamental data structure in programming. It stores elements in **contiguous memory** (side by side), and each element can be accessed using its **index**.

### Why Arrays Matter

- **Fast Access:** You can get any element instantly by its index — O(1).
- **Foundation:** Almost every other data structure is built on top of arrays.
- **Everywhere:** Arrays are used in databases, image processing, games, and more.

### How Arrays Work in Memory

```
Index:    0     1     2     3     4
        +-----+-----+-----+-----+-----+
Value:  | 10  | 20  | 30  | 40  | 50  |
        +-----+-----+-----+-----+-----+
Address: 100   104   108   112   116
```

Each element sits next to the other. Because the computer knows where the array starts and the size of each element, it can jump to any index instantly: `address = start + (index × size)`.

### Real-Life Analogy

Think of a **train with numbered coaches**. Want coach 5? Walk straight to it. You don't need to check coaches 1, 2, 3, 4 first. That's O(1) access!

### Common Array Operations

| Operation | Time Complexity | Why |
|-----------|----------------|-----|
| Access by index | O(1) | Direct jump |
| Search (unsorted) | O(n) | Check each element |
| Insert at end | O(1) | Just add |
| Insert at beginning | O(n) | Shift all elements |
| Delete at beginning | O(n) | Shift all elements |

---

## 🐢 Brute Force Approach

### Problem: Find the Second Largest Element

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/second-largest3735/1) | [InterviewBit](https://www.interviewbit.com/problems/second-largest-element/)

Given an array, find the second largest element.

**Brute Force Idea:** Sort the array, then pick the second element from the end.

```javascript
// Brute Force: Sort and pick second last unique element
function secondLargestBrute(arr) {
  if (arr.length < 2) return -1;

  // Sort in ascending order
  const sorted = [...arr].sort((a, b) => a - b);

  // Find the second distinct largest
  const largest = sorted[sorted.length - 1];

  // Walk backward to find a number different from largest
  for (let i = sorted.length - 2; i >= 0; i--) {
    if (sorted[i] !== largest) {
      return sorted[i];
    }
  }

  return -1; // All elements are the same
}

console.log(secondLargestBrute([12, 35, 1, 10, 34, 1])); // 34
console.log(secondLargestBrute([10, 10, 10]));             // -1
console.log(secondLargestBrute([5, 8]));                   // 5
```


### Line-by-Line Explanation

1. **`[...arr].sort((a, b) => a - b)`** — Create a copy and sort it smallest to largest.
2. **`sorted[sorted.length - 1]`** — The last element after sorting is the largest.
3. **Walk backward** — We go from the end to find the first number that's different from the largest.
4. If all numbers are the same, return -1.

---

## ⚡ Optimized Approach

**Idea:** Single pass — track both the largest and second largest as we go.

```javascript
// Optimized: Single pass — O(n)
function secondLargestOptimized(arr) {
  if (arr.length < 2) return -1;

  let first = -Infinity;   // Largest so far
  let second = -Infinity;  // Second largest so far

  for (let i = 0; i < arr.length; i++) {
    if (arr[i] > first) {
      // Current element is the new largest
      second = first;    // Old largest becomes second
      first = arr[i];    // Update largest
    } else if (arr[i] > second && arr[i] !== first) {
      // Current element is between first and second
      second = arr[i];
    }
  }

  return second === -Infinity ? -1 : second;
}

console.log(secondLargestOptimized([12, 35, 1, 10, 34, 1])); // 34
console.log(secondLargestOptimized([10, 10, 10]));             // -1
console.log(secondLargestOptimized([5, 8]));                   // 5
```

#### Code Story
- This problem is about finding the 'runner-up' in a group of numbers.
- First, we keep two markers: one for the leader and one for the second place.
- Then, as we look at each number, if it's bigger than our leader, the current leader moves to second place and the new number takes the lead.
- Finally, we return the value held in second place.
- This works because by tracking the top two contenders at all times, we only need to pass through the list once.

### Why is this better?

- **Brute Force:** Sorting takes O(n log n) time.
- **Optimized:** One loop through the array — O(n) time.

We keep two variables (`first` and `second`) and update them as we scan. Like having two podium spots — if someone taller comes along, the current champion moves to second place.

---

## 🔍 Complexity Analysis

| Approach | Time Complexity | Space Complexity |
|----------|----------------|-----------------|
| Brute Force (Sort) | O(n log n) | O(n) — sorted copy |
| Optimized (Single Pass) | O(n) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Rotate Array by K Positions

**Practice Links:** [LeetCode #189](https://leetcode.com/problems/rotate-array/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/rotate-array-by-n-elements-1587115621/1) | [CodeChef](https://www.codechef.com/problems/ROTATE) | [HackerRank](https://www.hackerrank.com/challenges/array-left-rotation/problem)

**Problem Statement:** Given an array and a number `k`, rotate the array to the right by `k` positions.

Example: `[1, 2, 3, 4, 5]` rotated by 2 → `[4, 5, 1, 2, 3]`

**Thought Process:** The last `k` elements should come to the front. The brute force way is to shift one by one, `k` times. The optimized way uses the **reversal trick**.

#### 🐢 Brute Force

```javascript
function rotateBrute(arr, k) {
  const n = arr.length;
  k = k % n; // Handle k > n

  // Rotate one position at a time, k times
  for (let step = 0; step < k; step++) {
    const last = arr[n - 1]; // Save the last element

    // Shift everything right by one
    for (let i = n - 1; i > 0; i--) {
      arr[i] = arr[i - 1];
    }

    arr[0] = last; // Put last element at front
  }

  return arr;
}

console.log(rotateBrute([1, 2, 3, 4, 5], 2)); // [4, 5, 1, 2, 3]
```

#### ⚡ Optimized Solution — Reversal Algorithm

```javascript
function rotateOptimized(nums, k) {
  k = k % nums.length // Handle k > n

  // Helper function to reverse a portion of the array
  function revser(arr, i, j) {
      while (i < j) {
          let temp = arr[i];
          arr[i] = arr[j];
          arr[j] = temp;
          i++;
          j--;
      }
  }

  // Step 1: Reverse the entire array
  revser(nums, 0, nums.length - 1);      // [5, 4, 3, 2, 1]

  // Step 2: Reverse the first k elements
  revser(nums, 0, k - 1);       // [4, 5, 3, 2, 1]

  // Step 3: Reverse the remaining elements
  revser(nums, k, nums.length - 1);      // [4, 5, 1, 2, 3]

  return nums;
}

console.log(rotateOptimized([1, 2, 3, 4, 5], 2)); // [4, 5, 1, 2, 3]
```

**Simple Explanation:** Imagine a playlist of 5 songs. You want the last 2 songs first. The reversal trick: flip the whole playlist backward, then flip the first 2 and last 3 separately. Magic — they end up in the right order!

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n × k) | O(1) |
| Optimized | O(n) | O(1) |


#### Code Story
- This problem is about shifting everything to the right by k steps.
- First, we could shift one by one (slow!), but the smart way is to reverse parts of the array.
- Then, we flip the whole list, then flip the first k items, then flip the rest.
- Finally, the array ends up perfectly rotated.
- This works because the mathematical property of reversing sections allows us to move blocks of data efficiently with zero extra space.

---

### Question 2: Move All Zeros to End

**Practice Links:** [LeetCode #283](https://leetcode.com/problems/move-zeroes/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/move-all-zeroes-to-end-of-array0751/1) | [InterviewBit](https://www.interviewbit.com/problems/move-zeroes/)

**Problem Statement:** Given an array, move all zeros to the end while keeping the order of non-zero elements.

Example: `[0, 1, 0, 3, 12]` → `[1, 3, 12, 0, 0]`

**Thought Process:** We need to keep non-zero elements in order and push zeros to the end.

#### 🐢 Brute Force

```javascript
function moveZerosBrute(arr) {
  const nonZeros = []; // Collect all non-zero elements

  // Step 1: Collect non-zeros
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] !== 0) {
      nonZeros.push(arr[i]);
    }
  }

  // Step 2: Fill back non-zeros, then fill remaining with zeros
  for (let i = 0; i < arr.length; i++) {
    if (i < nonZeros.length) {
      arr[i] = nonZeros[i];
    } else {
      arr[i] = 0;
    }
  }

  return arr;
}

console.log(moveZerosBrute([0, 1, 0, 3, 12])); // [1, 3, 12, 0, 0]
```

#### ⚡ Optimized — Two Pointer (In-Place)

```javascript
function moveZerosOptimized(arr) {
    function swap(arr, i, j) {
        let temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    let j = 0;
    for (let i = 0; i < arr.length; i++) {
       if (arr[i] !== 0) {
            swap(arr, i, j);
            j++;
        }
    }
    return arr;
}

console.log(moveZerosOptimized([0, 1, 0, 3, 12])); // [1, 3, 12, 0, 0]
console.log(moveZerosOptimized([0, 0, 1]));          // [1, 0, 0]
```

**Simple Explanation:** Imagine sorting books on a shelf. `insertPos` is like a bookmark for "next empty good spot." When you find a real book (non-zero), you place it at the bookmark and move the bookmark forward. Empty slots (zeros) naturally end up at the end.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Optimized | O(n) | O(1) |


#### Code Story
- This problem is about pushing all zeros to the back while keeping the other numbers in their original order.
- First, we use a marker to point to the 'next good spot' for a non-zero number.
- Then, as we find a non-zero number, we place it at the marker and move the marker forward.
- Finally, any remaining spots at the end are filled with zeros.
- This works because it slides the 'real' data to the front, naturally leaving empty space at the back.

---

### Question 3: Find Missing Number

**Practice Links:** [LeetCode #268](https://leetcode.com/problems/missing-number/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/missing-number-in-array1416/1) | [InterviewBit](https://www.interviewbit.com/problems/missing-number/)

**Problem Statement:** Given an array containing `n` distinct numbers from 0 to n, find the one missing. 

Example: `[3, 0, 1]` → Missing: `2`

**Thought Process:** The sum of 0 to n is `n*(n+1)/2`. Subtract the actual sum to find the missing number.

#### 🐢 Brute Force

```javascript
function missingNumberBrute(arr) {
  const n = arr.length;

  // Check each number from 0 to n
  for (let i = 0; i <= n; i++) {
    let found = false;

    // Search for i in the array
    for (let j = 0; j < n; j++) {
      if (arr[j] === i) {
        found = true;
        break;
      }
    }

    if (!found) return i; // This number is missing!
  }

  return -1;
}

console.log(missingNumberBrute([3, 0, 1])); // 2
```

#### ⚡ Optimized — Math Formula

```javascript
function missingNumberOptimized(arr) {
  const n = arr.length;
  const expectedSum = (n * (n + 1)) / 2; // Sum of 0 to n

  let actualSum = 0;
  for (let i = 0; i < n; i++) {
    actualSum += arr[i]; // Sum of array elements
  }

  return expectedSum - actualSum; // The difference is the missing number!
}

console.log(missingNumberOptimized([3, 0, 1]));       // 2
console.log(missingNumberOptimized([9,6,4,2,3,5,7,0,1])); // 8
```

**Simple Explanation:** If you know 10 friends were invited to a party and the total of their jersey numbers should be 55, but the actual total is 47, then jersey number 8 is missing. Simple subtraction!

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(1) |


#### Code Story
- This problem is about finding which number is missing from a sequence of 0 to n.
- First, we calculate what the total sum *should* be using a math formula.
- Then, we add up all the numbers we actually have.
- Finally, we subtract our actual sum from the expected sum—the difference is the missing number!
- This works because every number has a specific value, so any missing value will create a predictable 'gap' in the total.

---

### Question 4: Best Time to Buy and Sell Stock

**Practice Links:** [LeetCode #121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/buy-maximum-stocks-if-i-stocks-can-be-bought-on-i-th-day/1) | [InterviewBit](https://www.interviewbit.com/problems/best-time-to-buy-and-sell-stocks-i/)

**Problem Statement:** Given an array where `prices[i]` is the price of a stock on day `i`, find the maximum profit from one buy and one sell. You must buy before you sell.

Example: `[7, 1, 5, 3, 6, 4]` → Buy at 1, sell at 6 → Profit = 5

**Thought Process:** Track the minimum price seen so far. At each day, calculate the potential profit.

#### 🐢 Brute Force

```javascript
function maxProfitBrute(prices) {
  let maxProfit = 0;

  // Try every pair of buy day and sell day
  for (let buy = 0; buy < prices.length; buy++) {
    for (let sell = buy + 1; sell < prices.length; sell++) {
      const profit = prices[sell] - prices[buy];
      maxProfit = Math.max(maxProfit, profit);
    }
  }

  return maxProfit;
}

console.log(maxProfitBrute([7, 1, 5, 3, 6, 4])); // 5
```

#### ⚡ Optimized — Single Pass

```javascript
function maxProfitOptimized(prices) {
  let minPrice = Infinity; // Track the lowest price so far
  let maxProfit = 0;       // Track the best profit so far

  for (let i = 0; i < prices.length; i++) {
    if (prices[i] < minPrice) {
      minPrice = prices[i]; // Found a new lowest price
    } else {
      const profit = prices[i] - minPrice;
      maxProfit = Math.max(maxProfit, profit); // Is this the best profit?
    }
  }

  return maxProfit;
}

console.log(maxProfitOptimized([7, 1, 5, 3, 6, 4])); // 5
console.log(maxProfitOptimized([7, 6, 4, 3, 1]));     // 0 (prices only go down)
```

**Simple Explanation:** You're time-traveling through a week of stock prices. You always remember the cheapest price you've seen. Each day, you check: "If I bought at the cheapest and sold today, how much would I make?" You keep track of the best deal.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(1) |


#### Code Story
- This problem is about finding the biggest possible profit from buying low and selling high.
- First, we travel through time (the array) and always remember the cheapest price we've seen so far.
- Then, for every new day, we check: 'If I sold today, how much profit would I make?'
- Finally, we keep track of the best profit we ever found.
- This works because you can't sell before you buy, so tracking the 'minimum so far' is the best way to evaluate future deals.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Find Two Numbers That Add Up to Target (Two Sum)

**Practice Links:** [LeetCode #1](https://leetcode.com/problems/two-sum/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/key-pair5616/1) | [InterviewBit](https://www.interviewbit.com/problems/2-sum/)

**Problem Statement:** Given an array and a target, find two numbers that add up to the target. Return their indices.

**Approach:** Use a hash map to store numbers we've seen and check if the complement exists.

```javascript
function twoSum(arr, target) {
  const map = new Map(); // Store number → index

  for (let i = 0; i < arr.length; i++) {
    const complement = target - arr[i]; // What number do we need?

    if (map.has(complement)) {
      return [map.get(complement), i]; // Found the pair!
    }

    map.set(arr[i], i); // Remember this number and its index
  }

  return []; // No pair found
}

console.log(twoSum([2, 7, 11, 15], 9));  // [0, 1] → 2 + 7 = 9
console.log(twoSum([3, 2, 4], 6));        // [1, 2] → 2 + 4 = 6
```

**Explanation:** For each number, ask: "What number do I need to reach the target?" Check if that number is in our map. If not, store the current number for later.

**Complexity:** Time: O(n), Space: O(n)


#### Code Story
- This problem is about finding two numbers that add up to a specific target.
- First, for every number, we calculate its 'complement' (the number we need to reach the target).
- Then, we use a map to check if we've already seen that complement earlier.
- Finally, if we find it, we return the two indices.
- This works because a map remembers everything we've passed, allowing us to find 'matching pairs' instantly.

---

### Problem 2: Remove Duplicates from Sorted Array (In-Place)

**Practice Links:** [LeetCode #26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/remove-duplicate-elements-from-sorted-array/1) | [InterviewBit](https://www.interviewbit.com/problems/remove-duplicates-from-sorted-array/)

**Problem Statement:** Given a sorted array, remove duplicates in-place and return the new length.

**Approach:** Use a pointer to track the position of unique elements.

```javascript
function removeDuplicates(arr) {
  if (arr.length === 0) return 0;

  let uniquePos = 0; // Position of last unique element

  for (let i = 1; i < arr.length; i++) {
    if (arr[i] !== arr[uniquePos]) {
      uniquePos++;            // Move to next position
      arr[uniquePos] = arr[i]; // Place the unique element
    }
  }

  return uniquePos + 1; // Length of unique portion
}

const arr = [1, 1, 2, 2, 3, 4, 4, 5];
const len = removeDuplicates(arr);
console.log(len);                    // 5
console.log(arr.slice(0, len));      // [1, 2, 3, 4, 5]
```

**Explanation:** Like organizing a bookshelf where duplicate titles appear next to each other. You keep one copy and skip the rest, sliding unique books to the front.

**Complexity:** Time: O(n), Space: O(1)


#### Code Story
- This problem is about cleaning up a list so every number only appears once.
- First, since the list is sorted, duplicates are always next to each other.
- Then, we use a marker to keep track of where the unique numbers should go.
- Finally, we only move a number to the marker if it's different from the last unique one we found.
- This works because skipping identical neighbors is a very fast way to filter out duplicates in-place.

---

### Problem 3: Maximum Subarray Sum (Kadane's Algorithm)

**Practice Links:** [LeetCode #53](https://leetcode.com/problems/maximum-subarray/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/kadanes-algorithm-1587115620/1) | [InterviewBit](https://www.interviewbit.com/problems/max-sum-contiguous-subarray/)

**Problem Statement:** Find the contiguous subarray with the largest sum.

**Approach:** Track current sum; if it goes negative, reset it to 0 (start fresh).

```javascript
function maxSubarraySum(arr) {
  let maxSum = arr[0];      // Best sum seen so far
  let currentSum = arr[0];  // Current running sum

  for (let i = 1; i < arr.length; i++) {
    // Either extend the current subarray or start fresh
    currentSum = Math.max(arr[i], currentSum + arr[i]);

    // Update best if current is better
    maxSum = Math.max(maxSum, currentSum);
  }

  return maxSum;
}

console.log(maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4])); // 6 → [4, -1, 2, 1]
console.log(maxSubarraySum([1, 2, 3, 4]));                       // 10 → entire array
console.log(maxSubarraySum([-1, -2, -3]));                       // -1 → least negative
```

**Explanation:** You're walking through a tunnel collecting coins (positive) and paying tolls (negative). If your total goes below zero, it's better to start fresh from the next position. Keep track of the best total you've ever had.

**Complexity:** Time: O(n), Space: O(1)


#### Code Story
- This problem is about finding the 'hot streak'—the section of numbers with the highest total sum.
- First, we walk through the list and keep a running total.
- Then, if our total ever drops below zero, we realize it's better to 'start fresh' from the next number.
- Finally, we remember the highest total we ever reached during the walk.
- This works because a negative sum only drags down future numbers, so resetting to zero ensures we are always looking for the best possible start.

---

### Problem 4: Merge Two Sorted Arrays

**Practice Links:** [LeetCode #88](https://leetcode.com/problems/merge-sorted-array/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/merge-two-sorted-arrays-1587115620/1) | [InterviewBit](https://www.interviewbit.com/problems/merge-two-sorted-lists/) | [HackerRank](https://www.hackerrank.com/challenges/merge-two-sorted-linked-lists/problem)

**Problem Statement:** Given two sorted arrays, merge them into one sorted array.

**Approach:** Use two pointers, one for each array. Compare and pick the smaller element.

```javascript
function mergeSortedArrays(arr1, arr2) {
  const merged = [];
  let i = 0; // Pointer for arr1
  let j = 0; // Pointer for arr2

  // Compare elements from both arrays
  while (i < arr1.length && j < arr2.length) {
    if (arr1[i] <= arr2[j]) {
      merged.push(arr1[i]);
      i++;
    } else {
      merged.push(arr2[j]);
      j++;
    }
  }

  // Add remaining elements from arr1
  while (i < arr1.length) {
    merged.push(arr1[i]);
    i++;
  }

  // Add remaining elements from arr2
  while (j < arr2.length) {
    merged.push(arr2[j]);
    j++;
  }

  return merged;
}

console.log(mergeSortedArrays([1, 3, 5], [2, 4, 6])); // [1, 2, 3, 4, 5, 6]
console.log(mergeSortedArrays([1, 2], [3, 4, 5, 6])); // [1, 2, 3, 4, 5, 6]
```

**Explanation:** Imagine merging two sorted stacks of papers. You compare the top papers of each stack, take the smaller one, and place it in a new pile. Repeat until both stacks are empty.

**Complexity:** Time: O(n + m), Space: O(n + m)


#### Code Story
- This problem is about combining two already-sorted piles into one big sorted pile.
- First, we compare the top items of both piles.
- Then, we pick the smaller one, add it to our new pile, and move to the next item in that pile.
- Finally, we repeat this until all items are moved.
- This works because since both piles are already ordered, the overall smallest item *must* be at the top of one of the two piles.

---

### Problem 5: Product of Array Except Self

**Practice Links:** [LeetCode #238](https://leetcode.com/problems/product-of-array-except-self/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/product-array-puzzle4525/1) | [CodeChef](https://www.codechef.com/problems/PRODARRAY)

**Problem Statement:** Given an array, return an array where each element is the product of all others except itself. Do NOT use division.

**Approach:** Use prefix and suffix products.

```javascript
function productExceptSelf(arr) {
  const n = arr.length;
  const result = new Array(n).fill(1);

  // Step 1: Calculate prefix products (left to right)
  let prefix = 1;
  for (let i = 0; i < n; i++) {
    result[i] = prefix;     // Product of everything to the left
    prefix *= arr[i];       // Include current in prefix for next iteration
  }

  // Step 2: Multiply by suffix products (right to left)
  let suffix = 1;
  for (let i = n - 1; i >= 0; i--) {
    result[i] *= suffix;    // Multiply by product of everything to the right
    suffix *= arr[i];       // Include current in suffix for next iteration
  }

  return result;
}

console.log(productExceptSelf([1, 2, 3, 4]));   // [24, 12, 8, 6]
console.log(productExceptSelf([2, 3, 4, 5]));    // [60, 40, 30, 24]
```

**Explanation:** For each position, you need the product of ALL elements except the one at that position. Instead of multiplying everything and dividing (can't divide by zero!), we build the answer in two passes: first collect the product of everything to the LEFT, then multiply by the product of everything to the RIGHT.

**Complexity:** Time: O(n), Space: O(1) — result array doesn't count as extra space


#### Code Story
- This problem is about calculating the product of all numbers except the current one, without using division.
- First, we calculate the product of everything to the LEFT of each number.
- Then, we calculate the product of everything to the RIGHT and multiply it in.
- Finally, each spot has exactly what it needs: (everything before) x (everything after).
- This works because by splitting the work into 'left' and 'right' passes, we avoid the need for division and keep the math simple.

---

### 🔗 Navigation
Prev: [01_Basics_Complexity.md](01_Basics_Complexity.md) | Index: [00_Index.md](00_Index.md) | Next: [03_Strings.md](03_Strings.md)
