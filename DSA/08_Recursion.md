# 📌 Recursion

## 🧠 Concept Explanation (Story Format)

Imagine you're standing in a **line of people**, and someone asks: "How many people are behind you?" You can't see everyone, so you turn around and ask the person behind you: "How many people are behind YOU?" They do the same thing. The last person says "Zero!" and each person adds 1 to the answer they receive and passes it forward.

That's **recursion** — a function that calls itself to solve smaller versions of the same problem, until it reaches a simple "base case" that it can answer directly.

### The Two Key Parts of Recursion

1. **Base Case:** The simplest version of the problem that can be answered directly. Without this, recursion runs forever!
2. **Recursive Case:** Break the problem into a smaller version of itself and call the same function.

### How Recursion Works — The Call Stack

Every time a function calls itself, a new "frame" is added to the **call stack**. When the base case is reached, frames start "popping off" as answers flow back up.

```
factorial(4)
  → 4 × factorial(3)
    → 3 × factorial(2)
      → 2 × factorial(1)
        → 1  (base case!)
      → 2 × 1 = 2
    → 3 × 2 = 6
  → 4 × 6 = 24
```

### Real-Life Analogy

Think of **Russian nesting dolls (Matryoshka)**. To find the smallest doll, you open one doll, find another inside, open that, and repeat until you find the solid one (base case). Then you close them back up in reverse order.

### When to Use Recursion

- Problems that can be broken into **smaller identical subproblems**
- **Tree and graph traversals**
- **Divide and conquer** algorithms (merge sort, quick sort)
- **Backtracking** problems (combinations, permutations)
- **Dynamic programming** (recursion + memoization)

---

## 🐢 Brute Force Approach

### Problem: Calculate Factorial

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/factorial5739/1) | [CodeChef](https://www.codechef.com/problems/FCTRL2)

Factorial of n: `n! = n × (n-1) × (n-2) × ... × 1`

```javascript
// Iterative approach (non-recursive)
function factorialIterative(n) {
  let result = 1;

  for (let i = 2; i <= n; i++) {
    result *= i;
  }

  return result;
}

console.log(factorialIterative(5)); // 120
console.log(factorialIterative(0)); // 1
```


#### Code Story
- This problem is about multiplying a number by every positive number smaller than it (like 5! = 5x4x3x2x1).
- First, we realize that 5! is just 5 times 4!.
- Then, we keep asking the function for smaller factorials until we reach 1 (the 'stop signal').
- Finally, the answers multiply together on their way back up.
- This works because factorial has a perfect recursive structure where the big answer depends directly on a smaller version of itself.

### Line-by-Line Explanation

1. Start with `result = 1`.
2. Multiply by every number from 2 to n.
3. Simple loop — no recursion needed here, but recursion makes the logic elegant.

---

## ⚡ Optimized Approach

### Recursive Factorial

```javascript
// Recursive approach
function factorial(n) {
  // Base case: 0! = 1, 1! = 1
  if (n <= 1) return 1;

  // Recursive case: n! = n × (n-1)!
  return n * factorial(n - 1);
}

console.log(factorial(5)); // 120
console.log(factorial(0)); // 1
console.log(factorial(10)); // 3628800
```

### How It Works

```
factorial(5)
= 5 * factorial(4)
= 5 * 4 * factorial(3)
= 5 * 4 * 3 * factorial(2)
= 5 * 4 * 3 * 2 * factorial(1)
= 5 * 4 * 3 * 2 * 1
= 120
```

### Another Classic: Fibonacci

**Practice Links:** [LeetCode #509](https://leetcode.com/problems/fibonacci-number/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/nth-fibonacci-number1335/1) | [InterviewBit](https://www.interviewbit.com/problems/stairs/)

```javascript
// Recursive Fibonacci
function fibonacci(n) {
  // Base cases
  if (n === 0) return 0;
  if (n === 1) return 1;

  // Each number = sum of previous two
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(6)); // 8 (0, 1, 1, 2, 3, 5, 8)

// ⚡ Optimized with Memoization
function fibMemo(n, memo = {}) {
  if (n in memo) return memo[n]; // Return cached result
  if (n <= 1) return n;

  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  return memo[n];
}

console.log(fibMemo(50)); // 12586269025 (instant!)
```


#### Code Story
- This problem is about calculating a sequence where each number is the sum of the two before it.
- First, we ask 'what is the sum of the last two?'
- Then, each of those asks for the sum of *their* last two, creating a huge tree of questions.
- Finally, once we hit the base cases (0 and 1), the numbers start adding up.
- This works but can be slow because the computer ends up answering the same questions many, many times.

---

## 🔍 Complexity Analysis

| Function | Time | Space (Call Stack) |
|----------|------|-------------------|
| Factorial (iterative) | O(n) | O(1) |
| Factorial (recursive) | O(n) | O(n) |
| Fibonacci (recursive) | O(2ⁿ) | O(n) |
| Fibonacci (memoized) | O(n) | O(n) |

### Key Insight
Recursion uses **stack space** for each call. Deep recursion on large inputs can cause **stack overflow**. Memoization prevents redundant calculations.

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Power Function (x^n)

**Practice Links:** [LeetCode #50](https://leetcode.com/problems/powx-n/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/power-of-numbers-1587115620/1)

**Problem Statement:** Calculate x raised to the power n. Handle negative exponents.

**Thought Process:** Brute force multiplies x, n times. Optimized uses the property: x^n = (x^(n/2))² for even n.


#### Code Story
- This problem is about multiplying a number a, b times.
- First, we realize a^b is just a times a^(b-1).
- Then, we keep reducing the exponent until it reaches 0 (anything to the power of 0 is 1).
- Finally, the multiplication happens step-by-step.
- This works because exponents are naturally defined as repeated multiplication, which is exactly what recursion does.

#### 🐢 Brute Force

```javascript
function powerBrute(x, n) {
  if (n === 0) return 1;

  let result = 1;
  const absN = Math.abs(n);

  for (let i = 0; i < absN; i++) {
    result *= x;
  }

  return n < 0 ? 1 / result : result;
}

console.log(powerBrute(2, 10));  // 1024
console.log(powerBrute(2, -2));  // 0.25
```

#### ⚡ Optimized — Fast Exponentiation (Recursion)

```javascript
function powerOptimized(x, n) {
  // Base cases
  if (n === 0) return 1;
  if (n < 0) return 1 / powerOptimized(x, -n);

  // If n is even: x^n = (x^(n/2))²
  if (n % 2 === 0) {
    const half = powerOptimized(x, n / 2);
    return half * half;
  }

  // If n is odd: x^n = x × x^(n-1)
  return x * powerOptimized(x, n - 1);
}

console.log(powerOptimized(2, 10));  // 1024
console.log(powerOptimized(2, -2));  // 0.25
console.log(powerOptimized(3, 5));   // 243
```

**Simple Explanation:** To calculate 2^10, instead of multiplying 2 ten times, realize that 2^10 = (2^5)². And 2^5 = 2 × (2^4) = 2 × (2²)². We keep halving the exponent, doing far fewer multiplications.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(1) |
| Optimized | O(log n) | O(log n) |

---

### Question 2: Generate All Subsets (Power Set)

**Practice Links:** [LeetCode #78](https://leetcode.com/problems/subsets/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/subsets-1613027340/1) | [InterviewBit](https://www.interviewbit.com/problems/subset/)

**Problem Statement:** Given a set of unique integers, return all possible subsets.

Example: `[1, 2, 3]` → `[[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]`

**Thought Process:** At each element, make a choice: include it or exclude it. This creates a binary decision tree.

#### 🐢 Brute Force — Iterative

```javascript
function subsetsBrute(nums) {
  let result = [[]]; // Start with empty set

  for (const num of nums) {
    const newSubsets = [];
    // For each existing subset, create a new one with current number added
    for (const subset of result) {
      newSubsets.push([...subset, num]);
    }
    result = result.concat(newSubsets);
  }

  return result;
}

console.log(subsetsBrute([1, 2, 3]));
// [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

#### ⚡ Optimized — Recursive Backtracking

```javascript
function subsetsRecursive(nums) {
  const result = [];

  function backtrack(start, current) {
    // Add a copy of the current subset
    result.push([...current]);

    // Try adding each remaining number
    for (let i = start; i < nums.length; i++) {
      current.push(nums[i]);        // Include this number
      backtrack(i + 1, current);     // Explore further
      current.pop();                 // Backtrack — exclude and try next
    }
  }

  backtrack(0, []);
  return result;
}

console.log(subsetsRecursive([1, 2, 3]));
// [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

**Simple Explanation:** Imagine you're at a buffet with 3 dishes. For each dish, you decide: take it or skip it. That gives you 2³ = 8 possible meal combinations. The recursive approach makes this choice for each dish one by one.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Both | O(2ⁿ × n) | O(2ⁿ × n) |

---

### Question 3: Tower of Hanoi

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/tower-of-hanoi-1587115621/1) | [InterviewBit](https://www.interviewbit.com/problems/tower-of-hanoi/)

**Problem Statement:** Move `n` disks from source peg to destination peg using an auxiliary peg. Rules: move one disk at a time, never place a larger disk on a smaller one.

**Thought Process:** To move n disks from A to C: move top n-1 disks to B, move the largest disk to C, then move n-1 disks from B to C.

#### 🐢 Brute Force (No optimization possible — recursion IS the solution)

```javascript
function towerOfHanoi(n, source, destination, auxiliary) {
  if (n === 0) return; // Base case: no disks to move

  // Move n-1 disks from source to auxiliary
  towerOfHanoi(n - 1, source, auxiliary, destination);

  // Move the largest disk from source to destination
  console.log(`Move disk ${n} from ${source} to ${destination}`);

  // Move n-1 disks from auxiliary to destination
  towerOfHanoi(n - 1, auxiliary, destination, source);
}

towerOfHanoi(3, 'A', 'C', 'B');
// Move disk 1 from A to C
// Move disk 2 from A to B
// Move disk 1 from C to B
// Move disk 3 from A to C
// Move disk 1 from B to A
// Move disk 2 from B to C
// Move disk 1 from A to C
```

#### ⚡ Optimized — Count Moves

```javascript
function hanoiCount(n) {
  // The number of moves is always 2^n - 1
  return Math.pow(2, n) - 1;
}

console.log(hanoiCount(3));  // 7
console.log(hanoiCount(10)); // 1023
```

**Simple Explanation:** Moving a stack of plates: to move 3 plates, first move the top 2 to the spare peg, move the bottom plate to the destination, then move the 2 plates from the spare peg to the destination.

**Complexity:** Time: O(2ⁿ), Space: O(n) — call stack depth

---

### Question 4: Check if a String is a Palindrome (Recursive)

**Practice Links:** [LeetCode #125](https://leetcode.com/problems/valid-palindrome/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/palindrome-string0817/1)

**Problem Statement:** Use recursion to check if a string is a palindrome.

**Thought Process:** Compare the first and last characters. If they match, recursively check the substring between them.

#### 🐢 Brute Force — Iterative

```javascript
function isPalindromeBrute(s) {
  const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');
  return cleaned === cleaned.split('').reverse().join('');
}

console.log(isPalindromeBrute("racecar")); // true
console.log(isPalindromeBrute("hello"));   // false
```

#### ⚡ Optimized — Recursive

```javascript
function isPalindromeRecursive(s, left = 0, right = s.length - 1) {
  // Base case: pointers have met or crossed
  if (left >= right) return true;

  // Compare characters at both ends
  if (s[left] !== s[right]) return false;

  // Recurse on the inner substring
  return isPalindromeRecursive(s, left + 1, right - 1);
}

console.log(isPalindromeRecursive("racecar")); // true
console.log(isPalindromeRecursive("hello"));   // false
console.log(isPalindromeRecursive("abba"));    // true
```

**Simple Explanation:** Two friends start reading the word from opposite ends. They compare their letters as they walk toward the middle. If all letters match, it's a palindrome. Each step peels off the outer layer, checking a smaller subword.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Recursive | O(n) | O(n) call stack |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Sum of Digits

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/sum-of-digits1723/1) | [HackerRank](https://www.hackerrank.com/challenges/recursive-digit-sum/problem)

**Problem Statement:** Find the sum of digits of a number using recursion.

**Approach:** Extract the last digit, add it to the sum of remaining digits.

```javascript
function sumOfDigits(n) {
  n = Math.abs(n); // Handle negative numbers
  if (n < 10) return n; // Single digit — base case

  return (n % 10) + sumOfDigits(Math.floor(n / 10));
}

console.log(sumOfDigits(12345)); // 15 (1+2+3+4+5)
console.log(sumOfDigits(999));   // 27
console.log(sumOfDigits(0));     // 0
```


#### Code Story
- This problem is about taking a number like 123 and finding the sum 1+2+3.
- First, we take the last digit (3) and add it to the 'sum of the rest' (12).
- Then, we keep stripping off the last digit until the number is zero.
- Finally, all the stripped digits add together.
- This works because breaking a big number into 'last digit' + 'remaining digits' is a repeating pattern that eventually reaches zero.

**Explanation:** Peel off the last digit (n % 10), add it to the sum of the remaining number (n / 10). Like counting money by removing one coin at a time.

**Complexity:** Time: O(d) where d = number of digits, Space: O(d)

---

### Problem 2: Reverse a String Recursively

**Practice Links:** [LeetCode #344](https://leetcode.com/problems/reverse-string/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/reverse-a-string/1)

**Problem Statement:** Reverse a string using recursion.

**Approach:** Take the first character, put it at the end of the reversed rest.

```javascript
function reverseString(s) {
  // Base case: empty or single character
  if (s.length <= 1) return s;

  // Reverse the rest, then append the first character
  return reverseString(s.substring(1)) + s[0];
}

console.log(reverseString("hello"));    // "olleh"
console.log(reverseString("recursion")); // "noisrucer"
```

**Explanation:** To reverse "hello": reverse "ello" → "olle", then add "h" → "olleh". Each call handles one less character until we hit the base case.

**Complexity:** Time: O(n²) due to string concatenation, Space: O(n)

---

### Problem 3: Count Paths in a Grid

**Practice Links:** [LeetCode #62](https://leetcode.com/problems/unique-paths/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/number-of-paths0911/1) | [InterviewBit](https://www.interviewbit.com/problems/grid-unique-paths/)

**Problem Statement:** Count the number of ways to go from the top-left to the bottom-right of an m×n grid (can only move right or down).

**Approach:** At each cell, you can go right or down. Total paths = paths(right) + paths(down).

```javascript
// Recursive (with memoization)
function countPaths(m, n, memo = {}) {
  const key = `${m},${n}`;
  if (key in memo) return memo[key];

  if (m === 1 || n === 1) return 1; // Only one way if single row/column

  memo[key] = countPaths(m - 1, n, memo) + countPaths(m, n - 1, memo);
  return memo[key];
}

console.log(countPaths(3, 3)); // 6
console.log(countPaths(3, 7)); // 28
console.log(countPaths(7, 3)); // 28
```

**Explanation:** From any cell, you have two choices: go right (reducing columns) or go down (reducing rows). When you reach a single row or column, there's only one path. Total paths at any cell is the sum of paths from the cell below and the cell to the right.

**Complexity (with memo):** Time: O(m × n), Space: O(m × n)

---

### Problem 4: Flatten a Nested Array

**Practice Links:** [LeetCode #341](https://leetcode.com/problems/flatten-nested-list-iterator/)

**Problem Statement:** Given a deeply nested array, flatten it into a single-level array.

**Approach:** For each element: if it's an array, recursively flatten it; otherwise, add it to the result.

```javascript
function flattenArray(arr) {
  const result = [];

  for (const item of arr) {
    if (Array.isArray(item)) {
      // Recursively flatten and spread the results
      result.push(...flattenArray(item));
    } else {
      result.push(item);
    }
  }

  return result;
}

console.log(flattenArray([1, [2, [3, [4]], 5]]));  // [1, 2, 3, 4, 5]
console.log(flattenArray([[1, 2], [3, [4, [5]]]])); // [1, 2, 3, 4, 5]
```

**Explanation:** Like unpacking boxes within boxes. Open each box — if there's another box inside, open that too. Keep going until you find only items (not boxes). Collect all items into one list.

**Complexity:** Time: O(n) where n = total elements, Space: O(d) where d = max nesting depth

---

### Problem 5: Print All Permutations of a String

**Practice Links:** [LeetCode #46](https://leetcode.com/problems/permutations/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/permutations-of-a-given-string2041/1) | [InterviewBit](https://www.interviewbit.com/problems/permutations/)

**Problem Statement:** Generate all permutations of a string.

**Approach:** Fix each character at the first position, then recursively permute the rest.

```javascript
function permutations(str) {
  const result = [];

  function permute(chars, start) {
    if (start === chars.length - 1) {
      result.push(chars.join('')); // Found a complete permutation
      return;
    }

    for (let i = start; i < chars.length; i++) {
      // Swap current character with start
      [chars[start], chars[i]] = [chars[i], chars[start]];

      // Recurse on the rest
      permute(chars, start + 1);

      // Backtrack — undo the swap
      [chars[start], chars[i]] = [chars[i], chars[start]];
    }
  }

  permute(str.split(''), 0);
  return result;
}

console.log(permutations("abc"));
// ["abc", "acb", "bac", "bca", "cab", "cba"]
```


#### Code Story
- This problem is about finding every possible way to scramble a word.
- First, we pick a character to be at the front.
- Then, we recursively find all ways to scramble the remaining characters.
- Finally, we swap the front character and repeat the process for every other character.
- This works because it systematically tries every character in every position, ensuring no combination is missed.

**Explanation:** Put each character in the first position (by swapping), then find all arrangements of the remaining characters. Like arranging 3 friends in a photo: pick who stands first, then arrange the other two.

**Complexity:** Time: O(n! × n), Space: O(n) — call stack

---

### 🔗 Navigation
Prev: [07_Sorting.md](07_Sorting.md) | Index: [00_Index.md](00_Index.md) | Next: [09_Backtracking.md](09_Backtracking.md)
