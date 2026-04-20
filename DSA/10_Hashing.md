# 📌 Hashing

## 🧠 Concept Explanation (Story Format)

Imagine you're at a **huge concert** with 50,000 people. Someone asks you to find "John Smith." Without any system, you'd have to check every single person — that's O(n). But what if there's a **smart seating system** where everyone sits based on the first letter of their last name? You'd go straight to the "S" section — much faster!

That's **hashing** — a technique that converts data into a fixed-size index using a **hash function**, allowing near-instant lookups, insertions, and deletions.

### What is a Hash Function?

A hash function takes input (a key) and returns a number (an index). The same key always produces the same index.

```
hash("apple") → 3
hash("banana") → 7
hash("cherry") → 1
```

### What is a Hash Table / Hash Map?

A hash table is an array where each position (bucket) stores key-value pairs. The hash function decides which bucket to use.

```
Index:  0        1         2       3         4
      [    ] [cherry] [      ] [apple]  [     ]
                                         
      5        6         7       8         9
      [    ] [      ] [banana] [     ]  [     ]
```

### Handling Collisions

Sometimes two keys produce the same index — this is called a **collision**. Two common solutions:

1. **Chaining:** Each bucket holds a linked list of entries
2. **Open Addressing:** Find the next empty slot


#### Code Story
- This problem is about what happens when two different pieces of data are assigned the same 'address' in memory.
- First, we realize that no system is perfect, and sometimes addresses overlap.
- Then, we use 'Chaining' (making a little list at that address) or 'Open Addressing' (looking for the next empty spot).
- Finally, the data is stored safely despite the overlap.
- This works because having a 'plan B' for overlapping addresses ensures that no data is ever lost or overwritten.

### Real-Life Analogy

Think of a **library catalog system**. Instead of searching every shelf, you look up a book's category code, which tells you exactly which shelf and section to go to. The catalog is the hash function, the shelves are the hash table.

### Time Complexities

| Operation | Average | Worst (many collisions) |
|-----------|---------|------------------------|
| Insert | O(1) | O(n) |
| Search | O(1) | O(n) |
| Delete | O(1) | O(n) |

---

## 🐢 Brute Force Approach

### Problem: Check if Two Arrays Have Common Elements

```javascript
// Brute Force: Compare every pair
function hasCommonBrute(arr1, arr2) {
  for (let i = 0; i < arr1.length; i++) {
    for (let j = 0; j < arr2.length; j++) {
      if (arr1[i] === arr2[j]) {
        return true; // Found a common element
      }
    }
  }
  return false;
}

console.log(hasCommonBrute([1, 2, 3], [4, 5, 3])); // true
console.log(hasCommonBrute([1, 2, 3], [4, 5, 6])); // false
```

### Line-by-Line Explanation

1. For each element in arr1, compare it with every element in arr2.
2. If any match, return true.
3. Two nested loops = O(n × m) time.

---

## ⚡ Optimized Approach

Store one array in a Set (hash-based), then check each element of the other array.

```javascript
// Optimized: Hash Set — O(n + m)
function hasCommonOptimized(arr1, arr2) {
  const set = new Set(arr1); // Store all elements from arr1

  for (const num of arr2) {
    if (set.has(num)) {
      return true; // O(1) lookup!
    }
  }

  return false;
}

console.log(hasCommonOptimized([1, 2, 3], [4, 5, 3])); // true
console.log(hasCommonOptimized([1, 2, 3], [4, 5, 6])); // false
```

### JavaScript Hash Data Structures

```javascript
// Map — stores key-value pairs
const map = new Map();
map.set("name", "Alice");
map.set("age", 25);
console.log(map.get("name")); // "Alice"
console.log(map.has("age"));  // true

// Set — stores unique values only
const set = new Set([1, 2, 3, 2, 1]);
console.log(set);       // Set { 1, 2, 3 }
console.log(set.has(2)); // true

// Object as hash map (simple cases)
const obj = {};
obj["key1"] = "value1";
console.log(obj["key1"]); // "value1"
```

---

## 🔍 Complexity Analysis

| Approach | Time Complexity | Space Complexity |
|----------|----------------|-----------------|
| Brute Force | O(n × m) | O(1) |
| Hash Set | O(n + m) | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Two Sum

**Problem Statement:** Given an array and a target, find two numbers that add up to the target. Return their indices.

**Thought Process:** For each number, calculate its complement (target - number). Use a hash map to check if the complement has been seen before.


#### Code Story
- This problem is about finding two numbers that add up to a target in a single pass.
- First, for each number, we calculate exactly what 'complement' we need to finish the target.
- Then, we check our 'seen' map to see if that complement has already appeared.
- Finally, if it has, we've found our pair!
- This works because the map allows us to look into the past and see if the 'missing piece' of our puzzle has already been found.

#### 🐢 Brute Force

```javascript
function twoSumBrute(nums, target) {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] === target) {
        return [i, j];
      }
    }
  }
  return [];
}

console.log(twoSumBrute([2, 7, 11, 15], 9)); // [0, 1]
```

#### ⚡ Optimized — Hash Map

```javascript
function twoSumOptimized(nums, target) {
  const map = new Map(); // number → index

  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];

    if (map.has(complement)) {
      return [map.get(complement), i];
    }

    map.set(nums[i], i);
  }

  return [];
}

console.log(twoSumOptimized([2, 7, 11, 15], 9)); // [0, 1]
console.log(twoSumOptimized([3, 2, 4], 6));       // [1, 2]
```

**Simple Explanation:** As you walk through the array, you remember each number and where you saw it (using a map). For each new number, you ask: "Have I already seen the number that would complete the target sum?" If yes, you've found your pair!

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(n) |

---

### Question 2: Group Anagrams

**Problem Statement:** Given an array of strings, group anagrams together.

Example: `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`

**Thought Process:** Anagrams have the same characters. Sort each word — anagrams will produce the same sorted string. Use that as a hash map key.


#### Code Story
- This problem is about grouping words that use the same letters.
- First, we realize that anagrams have the same letter counts, which we can use as a 'fingerprint'.
- Then, we use this fingerprint as a key in a map and store all matching words in a list under that key.
- Finally, we return the map values as our groups.
- This works because identifying words by their 'ingredients' is a universal way to catch all scrambles.

#### 🐢 Brute Force

```javascript
function groupAnagramsBrute(strs) {
  const used = new Array(strs.length).fill(false);
  const result = [];

  for (let i = 0; i < strs.length; i++) {
    if (used[i]) continue;
    const group = [strs[i]];
    const sorted1 = strs[i].split('').sort().join('');

    for (let j = i + 1; j < strs.length; j++) {
      if (!used[j] && strs[j].split('').sort().join('') === sorted1) {
        group.push(strs[j]);
        used[j] = true;
      }
    }

    result.push(group);
  }

  return result;
}

console.log(groupAnagramsBrute(["eat","tea","tan","ate","nat","bat"]));
```

#### ⚡ Optimized — Hash Map with Sorted Key

```javascript
function groupAnagramsOptimized(strs) {
  const map = new Map(); // sorted string → group of anagrams

  for (const str of strs) {
    const key = str.split('').sort().join(''); // Sort characters

    if (!map.has(key)) {
      map.set(key, []);
    }
    map.get(key).push(str);
  }

  return [...map.values()];
}

console.log(groupAnagramsOptimized(["eat","tea","tan","ate","nat","bat"]));
// [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

**Simple Explanation:** Sort the letters of each word — all anagrams become the same sorted string. Use this sorted string as a locker number. All words that belong to the same locker are anagrams of each other.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n² × k log k) | O(n) |
| Optimized | O(n × k log k) | O(n) |

---

### Question 3: Longest Consecutive Sequence

**Problem Statement:** Find the length of the longest consecutive sequence in an unsorted array.

Example: `[100, 4, 200, 1, 3, 2]` → `4` (sequence: 1, 2, 3, 4)

**Thought Process:** Put everything in a Set. For each number that could be the START of a sequence (no n-1 exists), count how long the sequence goes.

#### 🐢 Brute Force

```javascript
function longestConsecutiveBrute(nums) {
  if (nums.length === 0) return 0;

  nums.sort((a, b) => a - b);
  let maxLen = 1;
  let currentLen = 1;

  for (let i = 1; i < nums.length; i++) {
    if (nums[i] === nums[i - 1]) continue; // Skip duplicates
    if (nums[i] === nums[i - 1] + 1) {
      currentLen++;
    } else {
      maxLen = Math.max(maxLen, currentLen);
      currentLen = 1;
    }
  }

  return Math.max(maxLen, currentLen);
}

console.log(longestConsecutiveBrute([100, 4, 200, 1, 3, 2])); // 4
```

#### ⚡ Optimized — Hash Set

```javascript
function longestConsecutiveOptimized(nums) {
  const set = new Set(nums);
  let maxLen = 0;

  for (const num of set) {
    // Only start counting from the beginning of a sequence
    if (!set.has(num - 1)) {
      let current = num;
      let length = 1;

      // Count consecutive numbers
      while (set.has(current + 1)) {
        current++;
        length++;
      }

      maxLen = Math.max(maxLen, length);
    }
  }

  return maxLen;
}

console.log(longestConsecutiveOptimized([100, 4, 200, 1, 3, 2])); // 4
console.log(longestConsecutiveOptimized([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])); // 9
```

**Simple Explanation:** Put all numbers in a set. For each number, check if it's the START of a sequence (meaning num-1 doesn't exist). If yes, count forward (num+1, num+2, ...) as long as consecutive numbers exist.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n log n) | O(1) |
| Optimized | O(n) | O(n) |

---

### Question 4: Subarray Sum Equals K

**Problem Statement:** Find the total number of contiguous subarrays whose sum equals `k`.

Example: `arr = [1, 1, 1], k = 2` → `2`

**Thought Process:** Use prefix sums with a hash map. If prefixSum[j] - prefixSum[i] = k, then the subarray from i+1 to j sums to k.


#### Code Story
- This problem is about finding how many sections of a list add up exactly to k.
- First, we keep a 'running total' (prefix sum) as we walk through the list.
- Then, we check if (Current Total - k) has appeared in our map before.
- Finally, if it has, it means the section between that old total and our current total must add up to k.
- This works because it uses simple subtraction and a memory of past totals to find hidden patterns in the data.

#### 🐢 Brute Force

```javascript
function subarraySumBrute(nums, k) {
  let count = 0;

  for (let i = 0; i < nums.length; i++) {
    let sum = 0;
    for (let j = i; j < nums.length; j++) {
      sum += nums[j];
      if (sum === k) count++;
    }
  }

  return count;
}

console.log(subarraySumBrute([1, 1, 1], 2)); // 2
```

#### ⚡ Optimized — Prefix Sum + Hash Map

```javascript
function subarraySumOptimized(nums, k) {
  const prefixMap = new Map(); // prefixSum → count of occurrences
  prefixMap.set(0, 1); // Empty prefix sum

  let sum = 0;
  let count = 0;

  for (const num of nums) {
    sum += num; // Running prefix sum

    // If (sum - k) was a previous prefix sum, we found subarrays
    if (prefixMap.has(sum - k)) {
      count += prefixMap.get(sum - k);
    }

    // Record this prefix sum
    prefixMap.set(sum, (prefixMap.get(sum) || 0) + 1);
  }

  return count;
}

console.log(subarraySumOptimized([1, 1, 1], 2));       // 2
console.log(subarraySumOptimized([1, 2, 3, -3, 1, 1, 1, 4, 2, -3], 3)); // 8
```

**Simple Explanation:** Keep a running sum as you walk through the array. At any point, if (runningSum - k) was seen as a previous running sum, then the subarray between those two points sums to k. The hash map tracks how many times each running sum has occurred.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(n) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Valid Sudoku

**Problem Statement:** Determine if a 9×9 Sudoku board is valid (partially filled). Check each row, column, and 3×3 box for duplicates.

```javascript
function isValidSudoku(board) {
  const rows = Array.from({ length: 9 }, () => new Set());
  const cols = Array.from({ length: 9 }, () => new Set());
  const boxes = Array.from({ length: 9 }, () => new Set());

  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const num = board[r][c];
      if (num === '.') continue;

      const boxIdx = Math.floor(r / 3) * 3 + Math.floor(c / 3);

      if (rows[r].has(num) || cols[c].has(num) || boxes[boxIdx].has(num)) {
        return false; // Duplicate found!
      }

      rows[r].add(num);
      cols[c].add(num);
      boxes[boxIdx].add(num);
    }
  }

  return true;
}
```

**Explanation:** Use three arrays of sets — one for rows, columns, and boxes. As you scan each cell, check if the number already exists in its row, column, or box. If it does, the board is invalid.

**Complexity:** Time: O(81) = O(1), Space: O(81) = O(1)

---

### Problem 2: Intersection of Two Arrays

**Problem Statement:** Find the common elements between two arrays (each element appears only once in result).

```javascript
function intersection(nums1, nums2) {
  const set1 = new Set(nums1);
  const result = new Set();

  for (const num of nums2) {
    if (set1.has(num)) {
      result.add(num);
    }
  }

  return [...result];
}

console.log(intersection([1, 2, 2, 1], [2, 2]));       // [2]
console.log(intersection([4, 9, 5], [9, 4, 9, 8, 4])); // [9, 4]
```

**Explanation:** Store one array in a set. Walk through the other array — if an element is in the set, it's common. Use a result set to avoid duplicates.

**Complexity:** Time: O(n + m), Space: O(n)

---

### Problem 3: First Unique Character in a String

**Problem Statement:** Find the index of the first non-repeating character.

```javascript
function firstUniqChar(s) {
  const freq = new Map();

  // Count frequencies
  for (const ch of s) {
    freq.set(ch, (freq.get(ch) || 0) + 1);
  }

  // Find first character with count 1
  for (let i = 0; i < s.length; i++) {
    if (freq.get(s[i]) === 1) return i;
  }

  return -1;
}

console.log(firstUniqChar("leetcode"));     // 0 ('l')
console.log(firstUniqChar("loveleetcode")); // 2 ('v')
console.log(firstUniqChar("aabb"));         // -1
```

**Explanation:** First pass: count how many times each character appears. Second pass: find the first character that appeared exactly once.

**Complexity:** Time: O(n), Space: O(1) — at most 26 characters

---

### Problem 4: Contains Duplicate Within K Distance

**Problem Statement:** Check if the array has two equal elements within distance `k` of each other.

```javascript
function containsNearbyDuplicate(nums, k) {
  const map = new Map(); // number → last seen index

  for (let i = 0; i < nums.length; i++) {
    if (map.has(nums[i]) && i - map.get(nums[i]) <= k) {
      return true;
    }
    map.set(nums[i], i); // Update last seen index
  }

  return false;
}

console.log(containsNearbyDuplicate([1, 2, 3, 1], 3));    // true
console.log(containsNearbyDuplicate([1, 0, 1, 1], 1));    // true
console.log(containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2)); // false
```

**Explanation:** Track the last index where each number was seen. When you encounter a number again, check if the distance is ≤ k.

**Complexity:** Time: O(n), Space: O(n)

---

### 🔗 Navigation
Prev: [09_Backtracking.md](09_Backtracking.md) | Index: [00_Index.md](00_Index.md) | Next: [11_Linked_List.md](11_Linked_List.md)
