# 📌 Dynamic Programming

## 🧠 Concept Explanation (Story Format)

Imagine you're climbing **stairs** and you want to count how many ways you can reach the top (taking 1 or 2 steps at a time). You could count every possible path — but many paths share the same subproblems. For example, "ways to reach step 5" depends on "ways to reach step 3" and "ways to reach step 4" — which you've already calculated!

**Dynamic Programming (DP)** solves problems by breaking them into **overlapping subproblems**, solving each subproblem **once**, and storing the result to avoid redundant work.

### Two Key Properties

1. **Overlapping Subproblems:** The same subproblems are solved multiple times.
2. **Optimal Substructure:** The optimal solution can be built from optimal solutions of subproblems.

### Two Approaches

| Approach | Direction | Also Called |
|----------|-----------|-------------|
| **Top-Down** | Start from the big problem, recurse down | Memoization |
| **Bottom-Up** | Start from the smallest subproblems, build up | Tabulation |

### DP vs Greedy vs Recursion

| Feature | Recursion | Greedy | DP |
|---------|-----------|--------|-----|
| Explores | All options | Best local choice | All options (cached) |
| Repeats work? | Yes | No | No (memoized) |
| Optimal? | Yes (if complete) | Sometimes | Always |

### Real-Life Analogy

Think of **building a house**. You don't recalculate the cost of the foundation every time you add a new floor. You calculate it once and reuse it. That's memoization.

Or think of **learning multiplication tables**. Instead of counting 7×8 every time, you memorize it's 56. That's caching!

---

## 🐢 Brute Force Approach

### Problem: Climbing Stairs

**Practice Links:** [LeetCode #70](https://leetcode.com/problems/climbing-stairs/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/count-ways-to-reach-the-nth-stair-1587115620/1) | [InterviewBit](https://www.interviewbit.com/problems/stairs/)

How many distinct ways to climb n stairs (1 or 2 steps at a time)?

```javascript
// Brute Force: Pure recursion — O(2ⁿ)
function climbStairsBrute(n) {
  if (n <= 2) return n;
  return climbStairsBrute(n - 1) + climbStairsBrute(n - 2);
}

console.log(climbStairsBrute(5));  // 8
console.log(climbStairsBrute(10)); // 89
// climbStairsBrute(45) would take forever!
```


#### Code Story
- This problem is about finding how many ways you can reach the top of a staircase if you can take 1 or 2 steps at a time.
- First, we realize that to reach step 10, you must have come from either step 9 or step 8.
- Then, the number of ways to reach step 10 is just the sum of the ways to reach those two steps.
- Finally, we build this up from step 1, 2, 3... until we reach our goal.
- This works because a big complicated problem can be unraveled into a simple sequence of small, repeating steps.

### Why is This Slow?

The same values are computed repeatedly. `climbStairs(3)` is calculated multiple times!

```
climbStairs(5)
├── climbStairs(4)
│   ├── climbStairs(3)  ← computed again!
│   └── climbStairs(2)
└── climbStairs(3)      ← same as above!
    ├── climbStairs(2)
    └── climbStairs(1)
```

---

## ⚡ Optimized Approach

### Top-Down (Memoization)

```javascript
function climbStairsMemo(n, memo = {}) {
  if (n <= 2) return n;
  if (n in memo) return memo[n]; // Return cached result

  memo[n] = climbStairsMemo(n - 1, memo) + climbStairsMemo(n - 2, memo);
  return memo[n];
}

console.log(climbStairsMemo(45)); // 1836311903 (instant!)
```

### Bottom-Up (Tabulation)

```javascript
function climbStairsTab(n) {
  if (n <= 2) return n;

  const dp = new Array(n + 1);
  dp[1] = 1;
  dp[2] = 2;

  for (let i = 3; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2]; // Build from smaller subproblems
  }

  return dp[n];
}

console.log(climbStairsTab(45)); // 1836311903
```

### Space-Optimized

```javascript
function climbStairsOptimal(n) {
  if (n <= 2) return n;

  let prev2 = 1, prev1 = 2;

  for (let i = 3; i <= n; i++) {
    const current = prev1 + prev2;
    prev2 = prev1;
    prev1 = current;
  }

  return prev1;
}

console.log(climbStairsOptimal(45)); // 1836311903
```

---

## 🔍 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Brute Force (recursion) | O(2ⁿ) | O(n) |
| Memoization (top-down) | O(n) | O(n) |
| Tabulation (bottom-up) | O(n) | O(n) |
| Space-optimized | O(n) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: 0/1 Knapsack

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/0-1-knapsack-problem0945/1) | [InterviewBit](https://www.interviewbit.com/problems/0-1-knapsack/)

**Problem Statement:** Given items with weights and values, maximize value in a knapsack of capacity W. Each item can be taken at most once.

#### 🐢 Brute Force

```javascript
function knapsackBrute(weights, values, capacity) {
  function solve(idx, remaining) {
    if (idx < 0 || remaining <= 0) return 0;

    // Skip this item
    let skip = solve(idx - 1, remaining);

    // Take this item (if it fits)
    let take = 0;
    if (weights[idx] <= remaining) {
      take = values[idx] + solve(idx - 1, remaining - weights[idx]);
    }

    return Math.max(skip, take);
  }

  return solve(weights.length - 1, capacity);
}

console.log(knapsackBrute([1, 3, 4, 5], [1, 4, 5, 7], 7)); // 9
```

#### ⚡ Optimized — Bottom-Up DP

```javascript
function knapsackDP(weights, values, capacity) {
  const n = weights.length;
  const dp = Array.from({length: n + 1}, () => new Array(capacity + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    for (let w = 0; w <= capacity; w++) {
      dp[i][w] = dp[i - 1][w]; // Don't take item i

      if (weights[i - 1] <= w) {
        dp[i][w] = Math.max(dp[i][w], values[i - 1] + dp[i - 1][w - weights[i - 1]]);
      }
    }
  }

  return dp[n][capacity];
}

console.log(knapsackDP([1, 3, 4, 5], [1, 4, 5, 7], 7)); // 9
```

**Simple Explanation:** For each item, we decide: take it or leave it. If we take it, we add its value but reduce available capacity. DP stores the best value for each (item count, remaining capacity) combination.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(2ⁿ) | O(n) |
| DP | O(n × W) | O(n × W) |

---

### Question 2: Longest Common Subsequence (LCS)

**Practice Links:** [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/longest-common-subsequence-1587115620/1) | [InterviewBit](https://www.interviewbit.com/problems/longest-common-subsequence/)

**Problem Statement:** Find the length of the longest subsequence common to two strings.

Example: `"abcde"` and `"ace"` → `3` ("ace")


#### Code Story
- This problem is about finding the longest string of characters that appears in the same order in two different words (like 'ace' in 'abcde').
- First, we make a grid where we compare every character of word A with word B.
- Then, if letters match, we add 1 to the best result from the 'inner' part of the words; if they don't, we take the better of the two neighbors.
- Finally, the bottom-right corner of the grid holds the answer.
- This works because the grid allows the computer to remember and combine small matches into the largest possible overall match.

#### 🐢 Brute Force

```javascript
function lcsBrute(text1, text2) {
  function solve(i, j) {
    if (i < 0 || j < 0) return 0;

    if (text1[i] === text2[j]) {
      return 1 + solve(i - 1, j - 1); // Characters match
    }

    return Math.max(solve(i - 1, j), solve(i, j - 1)); // Skip one character
  }

  return solve(text1.length - 1, text2.length - 1);
}
```

#### ⚡ Optimized — DP Table

```javascript
function lcsDP(text1, text2) {
  const m = text1.length, n = text2.length;
  const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (text1[i - 1] === text2[j - 1]) {
        dp[i][j] = 1 + dp[i - 1][j - 1]; // Match — extend LCS
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]); // Take best without one char
      }
    }
  }

  return dp[m][n];
}

console.log(lcsDP("abcde", "ace"));   // 3
console.log(lcsDP("abc", "abc"));     // 3
console.log(lcsDP("abc", "def"));     // 0
```

**Simple Explanation:** Compare characters one by one. If they match, they're part of the LCS — add 1 and move diagonally. If not, try skipping one character from each string and take the better result.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(2^(m+n)) | O(m+n) |
| DP | O(m × n) | O(m × n) |

---

### Question 3: Coin Change (Minimum Coins)

**Practice Links:** [LeetCode #322](https://leetcode.com/problems/coin-change/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/number-of-coins1824/1)

**Problem Statement:** Given coin denominations, find the minimum coins to make the target amount.


#### Code Story
- This problem is about finding the fewest coins needed to reach a specific total.
- First, we create a table that stores the 'cheapest way' to reach every amount from 0 to our target.
- Then, for every coin and every amount, we check: 'Is it cheaper to reach this amount using this coin, or using what I found before?'
- Finally, we return the value stored for our target amount.
- This works because by solving for small amounts first, we can build the 'perfect' answer for the big amount one coin at a time.

#### 🐢 Brute Force

```javascript
function coinChangeBrute(coins, amount) {
  if (amount === 0) return 0;
  if (amount < 0) return -1;

  let minCoins = Infinity;

  for (const coin of coins) {
    const result = coinChangeBrute(coins, amount - coin);
    if (result >= 0) {
      minCoins = Math.min(minCoins, result + 1);
    }
  }

  return minCoins === Infinity ? -1 : minCoins;
}
```

#### ⚡ Optimized — Bottom-Up DP

```javascript
function coinChangeDP(coins, amount) {
  const dp = new Array(amount + 1).fill(Infinity);
  dp[0] = 0; // 0 coins needed for amount 0

  for (let i = 1; i <= amount; i++) {
    for (const coin of coins) {
      if (coin <= i && dp[i - coin] !== Infinity) {
        dp[i] = Math.min(dp[i], dp[i - coin] + 1);
      }
    }
  }

  return dp[amount] === Infinity ? -1 : dp[amount];
}

console.log(coinChangeDP([1, 5, 10, 25], 63)); // 6
console.log(coinChangeDP([2], 3));               // -1
console.log(coinChangeDP([1, 2, 5], 11));        // 3
```

**Simple Explanation:** For each amount from 1 to target, try each coin. `dp[amount]` = minimum coins to make that amount. For each coin, check: "If I use this coin, how many coins do I need for the rest?" Take the minimum.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(S^n) | O(n) |
| DP | O(n × S) | O(S) |

---

### Question 4: Longest Increasing Subsequence (LIS)

**Practice Links:** [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/longest-increasing-subsequence-1587115620/1) | [InterviewBit](https://www.interviewbit.com/problems/longest-increasing-subsequence/)

**Problem Statement:** Find the length of the longest strictly increasing subsequence.

Example: `[10, 9, 2, 5, 3, 7, 101, 18]` → `4` ([2, 3, 7, 101])


#### Code Story
- This problem is about finding the longest string of numbers in a list that keeps going UP.
- First, we create a 'memo' where we store the longest streak ending at every specific number.
- Then, for a new number, we look back at all previous numbers that are smaller than it and add 1 to their best streaks.
- Finally, we return the highest streak we found anywhere in our memo.
- This works because it builds a memory of 'winning streaks' that future numbers can latch onto and continue.

#### 🐢 Brute Force — DP O(n²)

```javascript
function lisBrute(nums) {
  const n = nums.length;
  const dp = new Array(n).fill(1); // Each element is a subsequence of length 1

  for (let i = 1; i < n; i++) {
    for (let j = 0; j < i; j++) {
      if (nums[j] < nums[i]) {
        dp[i] = Math.max(dp[i], dp[j] + 1);
      }
    }
  }

  return Math.max(...dp);
}

console.log(lisBrute([10, 9, 2, 5, 3, 7, 101, 18])); // 4
```

#### ⚡ Optimized — Binary Search O(n log n)

```javascript
function lisOptimized(nums) {
  const tails = []; // tails[i] = smallest tail element for LIS of length i+1

  for (const num of nums) {
    let left = 0, right = tails.length;

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (tails[mid] < num) left = mid + 1;
      else right = mid;
    }

    tails[left] = num; // Replace or extend
  }

  return tails.length;
}

console.log(lisOptimized([10, 9, 2, 5, 3, 7, 101, 18])); // 4
```

**Simple Explanation:** Maintain an array `tails` where `tails[i]` is the smallest possible tail for an increasing subsequence of length `i+1`. For each number, use binary search to find where it fits. This gives us the length of LIS efficiently.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| DP | O(n²) | O(n) |
| Binary Search | O(n log n) | O(n) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: House Robber

**Practice Links:** [LeetCode #198](https://leetcode.com/problems/house-robber/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/stickler-theif-1587115620/1)

**Problem Statement:** Rob houses along a street. Can't rob adjacent houses. Maximize total loot.

```javascript
function rob(nums) {
  if (nums.length === 0) return 0;
  if (nums.length === 1) return nums[0];

  let prev2 = 0;          // dp[i-2]
  let prev1 = nums[0];    // dp[i-1]

  for (let i = 1; i < nums.length; i++) {
    const current = Math.max(prev1, prev2 + nums[i]);
    prev2 = prev1;
    prev1 = current;
  }

  return prev1;
}

console.log(rob([1, 2, 3, 1]));     // 4 (rob house 1 and 3)
console.log(rob([2, 7, 9, 3, 1]));  // 12 (rob house 1, 3, 5)
```

**Explanation:** At each house, choose: rob it (add its value + best from two houses back) or skip it (keep best from previous house). Track only the last two values.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 2: Unique Paths

**Practice Links:** [LeetCode #62](https://leetcode.com/problems/unique-paths/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/number-of-paths0911/1)

```javascript
function uniquePaths(m, n) {
  const dp = Array.from({length: m}, () => new Array(n).fill(1));

  for (let i = 1; i < m; i++) {
    for (let j = 1; j < n; j++) {
      dp[i][j] = dp[i - 1][j] + dp[i][j - 1]; // From top + from left
    }
  }

  return dp[m - 1][n - 1];
}

console.log(uniquePaths(3, 7)); // 28
console.log(uniquePaths(3, 3)); // 6
```

**Explanation:** First row and first column have only 1 way to reach them. Every other cell = ways from top + ways from left.

**Complexity:** Time: O(m × n), Space: O(m × n)

---

### Problem 3: Edit Distance

**Practice Links:** [LeetCode #72](https://leetcode.com/problems/edit-distance/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/edit-distance3702/1) | [InterviewBit](https://www.interviewbit.com/problems/edit-distance/)

```javascript
function minDistance(word1, word2) {
  const m = word1.length, n = word2.length;
  const dp = Array.from({length: m + 1}, (_, i) =>
    Array.from({length: n + 1}, (_, j) => (i === 0 ? j : j === 0 ? i : 0))
  );

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (word1[i - 1] === word2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1]; // Characters match — no operation
      } else {
        dp[i][j] = 1 + Math.min(
          dp[i - 1][j],     // Delete
          dp[i][j - 1],     // Insert
          dp[i - 1][j - 1]  // Replace
        );
      }
    }
  }

  return dp[m][n];
}

console.log(minDistance("horse", "ros"));       // 3
console.log(minDistance("intention", "execution")); // 5
```

**Explanation:** Transform word1 into word2 using insert, delete, or replace. If characters match, no cost. Otherwise, try all three operations and take the cheapest.

**Complexity:** Time: O(m × n), Space: O(m × n)

---

### Problem 4: Longest Palindromic Substring

**Practice Links:** [LeetCode #5](https://leetcode.com/problems/longest-palindromic-substring/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/longest-palindromic-substring0806/1) | [InterviewBit](https://www.interviewbit.com/problems/longest-palindromic-substring/)

```javascript
function longestPalindrome(s) {
  const n = s.length;
  let start = 0, maxLen = 1;

  // Expand from center approach
  function expandFromCenter(left, right) {
    while (left >= 0 && right < n && s[left] === s[right]) {
      if (right - left + 1 > maxLen) {
        start = left;
        maxLen = right - left + 1;
      }
      left--;
      right++;
    }
  }

  for (let i = 0; i < n; i++) {
    expandFromCenter(i, i);     // Odd length palindromes
    expandFromCenter(i, i + 1); // Even length palindromes
  }

  return s.substring(start, start + maxLen);
}

console.log(longestPalindrome("babad")); // "bab" or "aba"
console.log(longestPalindrome("cbbd"));  // "bb"
```

**Explanation:** Every palindrome has a center. Try each position as center (both odd and even lengths). Expand outward while characters match. Track the longest found.

**Complexity:** Time: O(n²), Space: O(1)

---

### 🔗 Navigation
Prev: [23_Greedy.md](23_Greedy.md) | Index: [00_Index.md](00_Index.md) | Next: [25_Bit_Manipulation.md](25_Bit_Manipulation.md)
