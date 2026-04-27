# 📌 Backtracking

## 🧠 Concept Explanation (Story Format)

Imagine you're in a **maze**. You start walking, and at each junction, you pick a path. If you hit a dead end, you **go back** to the last junction and try a different path. You keep doing this until you find the exit.

That's **backtracking** — a systematic way to explore all possibilities by building a solution step by step, and **undoing** (backtracking) the last step when it leads to an invalid or dead-end solution.

### How Backtracking Works

1. **Choose:** Make a choice at the current step.
2. **Explore:** Recursively explore that choice.
3. **Un-choose (Backtrack):** Undo the choice and try the next option.

### When to Use Backtracking

| Problem Type | Example |
|-------------|---------|
| Combinations | Find all subsets, combinations of k numbers |
| Permutations | Arrange elements in all possible orders |
| Constraint satisfaction | Sudoku, N-Queens, crossword puzzles |
| Path finding | All paths in a grid/graph |

### Backtracking vs Brute Force

Brute force tries ALL possibilities blindly. Backtracking is smarter — it **prunes** branches that can't lead to valid solutions, saving time.

### Real-Life Analogy

Think of **trying on outfits**. You pick a shirt, then pants, then shoes. If the combination doesn't look good, you don't change everything — you backtrack: swap the shoes, check again. If still bad, swap the pants. You explore combinations systematically.

---

## 🐢 Brute Force Approach

### Problem: Generate All Subsets

**Practice Links:** [LeetCode #78](https://leetcode.com/problems/subsets/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/subsets-1613027340/1) | [InterviewBit](https://www.interviewbit.com/problems/subset/)

```javascript
// Brute Force: Iterative — build subsets by including/excluding each element
function subsetsBrute(nums) {
  let result = [[]];

  for (const num of nums) {
    const newSubsets = [];
    for (const subset of result) {
      newSubsets.push([...subset, num]); // Create new subset with num added
    }
    result = [...result, ...newSubsets];
  }

  return result;
}

console.log(subsetsBrute([1, 2, 3]));
// [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```


#### Code Story
- This problem is about finding every possible smaller group you can make from a larger set of items.
- First, for every item, we have a choice: 'include it' or 'leave it out'.
- Then, we branch out for each item, making two versions—one with and one without.
- Finally, at the end of the chain, we have every possible combination.
- This works because every subset is essentially a series of 'Yes' or 'No' decisions for every item in the set.

### Line-by-Line Explanation

1. Start with just the empty subset `[[]]`.
2. For each number, create new subsets by adding it to every existing subset.
3. This builds up all 2ⁿ subsets iteratively.

---

## ⚡ Optimized Approach

### Backtracking Template

```javascript
function backtrack(candidates, current, result, start) {
  // 1. Check if current solution is valid/complete
  result.push([...current]); // Add a copy of current

  // 2. Try each candidate from 'start'
  for (let i = start; i < candidates.length; i++) {
    current.push(candidates[i]);      // Choose
    backtrack(candidates, current, result, i + 1); // Explore
    current.pop();                     // Un-choose (backtrack)
  }
}

// Generate all subsets using backtracking
function subsetsBacktrack(nums) {
  const result = [];
  backtrack(nums, [], result, 0);
  return result;
}

console.log(subsetsBacktrack([1, 2, 3]));
// [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

The backtracking template follows the **choose → explore → un-choose** pattern consistently.

---

## 🔍 Complexity Analysis

| Aspect | Value |
|--------|-------|
| Time Complexity | O(2ⁿ × n) for subsets (2ⁿ subsets, each up to n elements) |
| Space Complexity | O(n) for recursion depth |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: N-Queens Problem

**Practice Links:** [LeetCode #51](https://leetcode.com/problems/n-queens/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/n-queen-problem0315/1) | [InterviewBit](https://www.interviewbit.com/problems/nqueens/)

**Problem Statement:** Place `n` queens on an `n×n` chessboard so that no two queens attack each other. Return all solutions.

**Thought Process:** Place queens row by row. For each row, try each column. Check if placement is valid (no conflicts). Backtrack if not.


#### Code Story
- This problem is about placing n queens on a chessboard so that none can attack each other.
- First, we try placing a queen in the first row.
- Then, we move to the next row and look for a safe spot; if we find one, we place a queen and keep going.
- Finally, if we get stuck, we 'backtrack' (remove the last queen) and try a different spot in the previous row.
- This works because it systematically explores only the paths that haven't been disqualified yet.

#### 🐢 Brute Force

```javascript
function solveNQueensBrute(n) {
  const result = [];

  function isValid(board, row, col) {
    // Check column
    for (let i = 0; i < row; i++) {
      if (board[i] === col) return false;
    }
    // Check upper-left diagonal
    for (let i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
      if (board[i] === j) return false;
    }
    // Check upper-right diagonal
    for (let i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
      if (board[i] === j) return false;
    }
    return true;
  }

  function solve(row, board) {
    if (row === n) {
      // Build the board visualization
      const solution = board.map(col => {
        return '.'.repeat(col) + 'Q' + '.'.repeat(n - col - 1);
      });
      result.push(solution);
      return;
    }

    for (let col = 0; col < n; col++) {
      if (isValid(board, row, col)) {
        board.push(col);
        solve(row + 1, board);
        board.pop(); // Backtrack
      }
    }
  }

  solve(0, []);
  return result;
}

console.log(solveNQueensBrute(4).length); // 2 solutions
```

#### ⚡ Optimized — Using Sets for O(1) Conflict Checking

```javascript
function solveNQueensOptimized(n) {
  const result = [];
  const cols = new Set();       // Columns with queens
  const diag1 = new Set();      // row - col diagonals
  const diag2 = new Set();      // row + col diagonals

  function solve(row, board) {
    if (row === n) {
      result.push(board.map(col =>
        '.'.repeat(col) + 'Q' + '.'.repeat(n - col - 1)
      ));
      return;
    }

    for (let col = 0; col < n; col++) {
      if (cols.has(col) || diag1.has(row - col) || diag2.has(row + col)) {
        continue; // This position is under attack
      }

      // Place queen
      cols.add(col);
      diag1.add(row - col);
      diag2.add(row + col);
      board.push(col);

      solve(row + 1, board);

      // Backtrack
      cols.delete(col);
      diag1.delete(row - col);
      diag2.delete(row + col);
      board.pop();
    }
  }

  solve(0, []);
  return result;
}

const solutions = solveNQueensOptimized(4);
solutions.forEach(sol => {
  console.log(sol.join('\n'));
  console.log('---');
});
```

**Simple Explanation:** Place queens one row at a time. For each row, try each column. A queen is safe if no other queen is in the same column or diagonal. We use sets to instantly check if a position is under attack an

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n! × n) | O(n) |
| Optimized | O(n!) | O(n) |

---

### Question 2: Combination Sum

**Practice Links:** [LeetCode #39](https://leetcode.com/problems/combination-sum/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/combination-sum-1587115620/1) | [InterviewBit](https://www.interviewbit.com/problems/combination-sum/)

**Problem Statement:** Find all unique combinations of candidates that sum to the target. Each number can be used unlimited times.

Example: `candidates = [2,3,6,7], target = 7` → `[[2,2,3], [7]]`

**Thought Process:** For each number, decide how many times to include it (0, 1, 2, ...). Backtrack when sum exceeds target.


#### Code Story
- This problem is about finding all groups of numbers that add up to a specific target.
- First, we try adding a number to our total.
- Then, if the total is still too small, we recursively try adding another number (even the same one!).
- Finally, if we hit the target, we save the group; if we exceed it, we step back and try a different number.
- This works by exploring every path of additions and quickly pruning paths that have already gone 'over budget'.

#### 🐢 Brute Force

```javascript
function combinationSumBrute(candidates, target) {
  const result = [];

  function find(start, current, remaining) {
    if (remaining === 0) {
      result.push([...current]);
      return;
    }
    if (remaining < 0) return;

    for (let i = start; i < candidates.length; i++) {
      current.push(candidates[i]);
      find(i, current, remaining - candidates[i]); // i, not i+1 (reuse allowed)
      current.pop(); // Backtrack
    }
  }

  find(0, [], target);
  return result;
}

console.log(combinationSumBrute([2, 3, 6, 7], 7));
// [[2,2,3], [7]]
```

#### ⚡ Optimized — Sort + Prune

```javascript
function combinationSumOptimized(candidates, target) {
  const result = [];
  candidates.sort((a, b) => a - b); // Sort for early termination

  function backtrack(start, current, remaining) {
    if (remaining === 0) {
      result.push([...current]);
      return;
    }

    for (let i = start; i < candidates.length; i++) {
      // Early termination: if current candidate > remaining, all after will also be
      if (candidates[i] > remaining) break;

      current.push(candidates[i]);
      backtrack(i, current, remaining - candidates[i]);
      current.pop();
    }
  }

  backtrack(0, [], target);
  return result;
}

console.log(combinationSumOptimized([2, 3, 6, 7], 7));
// [[2,2,3], [7]]
```

**Simple Explanation:** You're making change for $7 using coins of [2, 3, 6, 7]. Try adding each coin repeatedly. If you go over $7, backtrack and try the next coin. Sorting helps because once a coin is too large, all bigger coins are too.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Both | O(2^(t/m)) where t=target, m=min candidate | O(t/m) |

---

### Question 3: Word Search

**Practice Links:** [LeetCode #79](https://leetcode.com/problems/word-search/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/word-search/1) | [InterviewBit](https://www.interviewbit.com/problems/word-search/)

**Problem Statement:** Given a 2D grid of characters and a word, find if the word exists in the grid by moving up, down, left, or right (each cell used once).

**Thought Process:** For each cell, start DFS. If current character matches, explore all four neighbors for the next character. Backtrack by unmarking visited cells.

#### 🐢 Brute Force (Backtracking IS the approach)

```javascript
function wordSearch(board, word) {
  const rows = board.length;
  const cols = board[0].length;

  function dfs(r, c, index) {
    // Found all characters
    if (index === word.length) return true;

    // Out of bounds or character doesn't match
    if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== word[index]) {
      return false;
    }

    // Mark as visited
    const temp = board[r][c];
    board[r][c] = '#';

    // Explore all 4 directions
    const found =
      dfs(r + 1, c, index + 1) ||
      dfs(r - 1, c, index + 1) ||
      dfs(r, c + 1, index + 1) ||
      dfs(r, c - 1, index + 1);

    // Backtrack — restore the cell
    board[r][c] = temp;

    return found;
  }

  // Try starting from every cell
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (dfs(r, c, 0)) return true;
    }
  }

  return false;
}

const board = [
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
];

console.log(wordSearch(board, "ABCCED")); // true
console.log(wordSearch(board, "SEE"));    // true
console.log(wordSearch(board, "ABCB"));   // false
```

#### ⚡ Optimized — Character Frequency Pruning

```javascript
function wordSearchOptimized(board, word) {
  const rows = board.length;
  const cols = board[0].length;

  // Optimization: Check if board has enough characters
  const boardFreq = {};
  const wordFreq = {};
  for (const row of board) for (const ch of row) boardFreq[ch] = (boardFreq[ch] || 0) + 1;
  for (const ch of word) wordFreq[ch] = (wordFreq[ch] || 0) + 1;
  for (const ch in wordFreq) {
    if ((boardFreq[ch] || 0) < wordFreq[ch]) return false;
  }

  function dfs(r, c, index) {
    if (index === word.length) return true;
    if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== word[index]) return false;

    const temp = board[r][c];
    board[r][c] = '#';

    const found =
      dfs(r + 1, c, index + 1) || dfs(r - 1, c, index + 1) ||
      dfs(r, c + 1, index + 1) || dfs(r, c - 1, index + 1);

    board[r][c] = temp;
    return found;
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (dfs(r, c, 0)) return true;
    }
  }
  return false;
}

console.log(wordSearchOptimized([['A','B'],['C','D']], "ABDC")); // true
```

**Simple Explanation:** Start at each cell. If the letter matches the first letter of the word, walk in all 4 directions looking for the next letter. Mark cells as visited so we don't reuse them. If we get stuck, unmark and try another direction.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Both | O(m × n × 4^L) where L = word length | O(L) — recursion depth |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Generate All Permutations

**Practice Links:** [LeetCode #46](https://leetcode.com/problems/permutations/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/permutations-of-a-given-string2041/1) | [InterviewBit](https://www.interviewbit.com/problems/permutations/)

**Problem Statement:** Given a list of distinct integers, return all possible permutations.

```javascript
function permute(nums) {
  const result = [];

  function backtrack(current, remaining) {
    if (remaining.length === 0) {
      result.push([...current]);
      return;
    }

    for (let i = 0; i < remaining.length; i++) {
      current.push(remaining[i]);
      backtrack(current, [...remaining.slice(0, i), ...remaining.slice(i + 1)]);
      current.pop(); // Backtrack
    }
  }

  backtrack([], nums);
  return result;
}

console.log(permute([1, 2, 3]));
// [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Explanation:** Fix each number at the current position, then permute the rest. Like arranging people in a line — pick who goes first, then arrange the others.

**Complexity:** Time: O(n! × n), Space: O(n)

---

### Problem 2: Palindrome Partitioning

**Practice Links:** [LeetCode #131](https://leetcode.com/problems/palindrome-partitioning/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/find-all-possible-palindromic-partitions-of-a-string/1) | [InterviewBit](https://www.interviewbit.com/problems/palindrome-partitioning/)

**Problem Statement:** Partition a string such that every substring is a palindrome. Return all possible partitions.

```javascript
function palindromePartition(s) {
  const result = [];

  function isPalindrome(str, left, right) {
    while (left < right) {
      if (str[left] !== str[right]) return false;
      left++;
      right--;
    }
    return true;
  }

  function backtrack(start, current) {
    if (start === s.length) {
      result.push([...current]);
      return;
    }

    for (let end = start; end < s.length; end++) {
      if (isPalindrome(s, start, end)) {
        current.push(s.substring(start, end + 1)); // Choose
        backtrack(end + 1, current);                 // Explore
        current.pop();                               // Backtrack
      }
    }
  }

  backtrack(0, []);
  return result;
}

console.log(palindromePartition("aab"));
// [["a","a","b"], ["aa","b"]]
```

**Explanation:** At each position, try every possible substring starting there. If it's a palindrome, include it and partition the rest. Like cutting a string into pieces where each piece reads the same forward and backward.

**Complexity:** Time: O(n × 2ⁿ), Space: O(n)

---

### Problem 3: Sudoku Solver

**Practice Links:** [LeetCode #37](https://leetcode.com/problems/sudoku-solver/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/solve-the-sudoku-1587115621/1) | [InterviewBit](https://www.interviewbit.com/problems/sudoku/)

**Problem Statement:** Fill a 9×9 Sudoku board so each row, column, and 3×3 box contains digits 1-9.

```javascript
function solveSudoku(board) {
  function isValid(board, row, col, num) {
    const char = String(num);

    // Check row
    for (let c = 0; c < 9; c++) {
      if (board[row][c] === char) return false;
    }

    // Check column
    for (let r = 0; r < 9; r++) {
      if (board[r][col] === char) return false;
    }

    // Check 3x3 box
    const boxRow = Math.floor(row / 3) * 3;
    const boxCol = Math.floor(col / 3) * 3;
    for (let r = boxRow; r < boxRow + 3; r++) {
      for (let c = boxCol; c < boxCol + 3; c++) {
        if (board[r][c] === char) return false;
      }
    }

    return true;
  }

  function solve() {
    for (let row = 0; row < 9; row++) {
      for (let col = 0; col < 9; col++) {
        if (board[row][col] === '.') {
          // Try each number 1-9
          for (let num = 1; num <= 9; num++) {
            if (isValid(board, row, col, num)) {
              board[row][col] = String(num); // Choose
              if (solve()) return true;       // Explore
              board[row][col] = '.';          // Backtrack
            }
          }
          return false; // No valid number found — backtrack
        }
      }
    }
    return true; // All cells filled
  }

  solve();
  return board;
}
```


#### Code Story
- This problem is about filling a 9x9 grid with numbers following specific rules.
- First, we find an empty cell and try a number from 1 to 9.
- Then, if that number is valid, we move to the next cell and try again.
- Finally, if we hit an impossible situation, we undo our choice and try the next number.
- This works because it uses 'trial and error' with smart rules to find the one correct configuration for the grid.

**Explanation:** For each empty cell, try numbers 1-9. If a number doesn't conflict with existing numbers in the same row, column, or box, place it and move on. If no number works, backtrack and change the previous cell.

**Complexity:** Time: O(9^(empty cells)), Space: O(81) for the board

---

### 🔗 Navigation
Prev: [08_Recursion.md](08_Recursion.md) | Index: [00_Index.md](00_Index.md) | Next: [10_Hashing.md](10_Hashing.md)
