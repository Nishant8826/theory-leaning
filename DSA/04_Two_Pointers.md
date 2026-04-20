# 📌 Two Pointers

## 🧠 Concept Explanation (Story Format)

Imagine you're at a **party**, and you need to find two people whose heights add up to exactly 180 cm. Here are your options:

1. **Brute force:** Ask every person to stand next to every other person and measure. Exhausting!
2. **Smart way:** Line everyone up by height. Put one finger on the shortest person and another on the tallest. If their heights add up to too much, move the right finger left (shorter person). If too little, move the left finger right (taller person).

That's the **Two Pointer** technique! You use two pointers (usually one at the start and one at the end) and move them toward each other based on some condition.

### When to Use Two Pointers

| Scenario | Example |
|----------|---------|
| Sorted array pair problems | Find two numbers that sum to target |
| Removing duplicates in-place | Remove duplicates from sorted array |
| Comparing from both ends | Palindrome check |
| Merging two sorted arrays | Merge two lists |
| Partitioning | Separate even/odd numbers |

### Types of Two Pointer Approaches

1. **Opposite Direction:** Start from both ends, move inward (pair sum, palindrome).
2. **Same Direction (Fast & Slow):** Both start from the beginning, but move at different speeds (linked list cycle, remove duplicates).

### Real-Life Analogy

Think of **squeezing toothpaste from both ends** of the tube — your hands start at opposite ends and work toward the middle. Or think of two friends searching a bookshelf — one starts from the left, one from the right, and they meet in the middle.

---

## 🐢 Brute Force Approach

### Problem: Find Pair with Given Sum in Sorted Array

Given a **sorted** array and a target sum, find a pair of numbers that add up to the target.

```javascript
// Brute Force: Try all pairs
function findPairBrute(arr, target) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] + arr[j] === target) {
        return [arr[i], arr[j]]; // Found the pair!
      }
    }
  }
  return null; // No pair found
}

console.log(findPairBrute([1, 2, 3, 4, 6], 6));  // [2, 4]
console.log(findPairBrute([2, 5, 9, 11], 11));    // [2, 9]
```

### Line-by-Line Explanation

1. **Two nested loops** — try every possible combination of two elements.
2. **`arr[i] + arr[j] === target`** — check if the current pair sums to the target.
3. This works but checks n×(n-1)/2 pairs — very slow for large arrays.

---

## ⚡ Optimized Approach

Since the array is **sorted**, use two pointers — one at the start, one at the end.

```javascript
// Optimized: Two Pointers — O(n)
function findPairOptimized(arr, target) {
  let left = 0;                // Start pointer
  let right = arr.length - 1;  // End pointer

  while (left < right) {
    const sum = arr[left] + arr[right];

    if (sum === target) {
      return [arr[left], arr[right]]; // Perfect match!
    } else if (sum < target) {
      left++;   // Need a bigger sum → move left pointer right
    } else {
      right--;  // Need a smaller sum → move right pointer left
    }
  }

  return null; // No pair found
}

console.log(findPairOptimized([1, 2, 3, 4, 6], 6));  // [2, 4]
console.log(findPairOptimized([2, 5, 9, 11], 11));    // [2, 9]
```

### Why Does This Work?

- Array is sorted: small numbers on left, big on right.
- If sum is too small → we need a bigger number → move `left` right.
- If sum is too big → we need a smaller number → move `right` left.
- We never miss a valid pair because the sorted order guarantees we eliminate impossible pairs.

---

## 🔍 Complexity Analysis

| Approach | Time Complexity | Space Complexity |
|----------|----------------|-----------------|
| Brute Force | O(n²) | O(1) |
| Two Pointers | O(n) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Three Sum (Find Triplets that Sum to Zero)

**Problem Statement:** Given an array, find all unique triplets that sum to zero.

Example: `[-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]`

**Thought Process:** Sort the array. Fix one number, then use two pointers on the remaining to find pairs that complete the sum. Skip duplicates.


#### Code Story
- This problem is about finding all unique sets of three numbers that add up to zero.
- First, we sort the array and fix one number as our 'anchor'.
- Then, we use the 'Two Pointer' trick on the remaining numbers to find pairs that cancel out our anchor.
- Finally, we skip any duplicate numbers to ensure our results are all unique.
- This works because turning a 3-number problem into a 2-number problem (by fixing one) makes it much easier to solve.

#### 🐢 Brute Force

```javascript
function threeSumBrute(nums) {
  const result = [];
  const n = nums.length;
  nums.sort((a, b) => a - b); // Sort to handle duplicates easily

  for (let i = 0; i < n; i++) {
    if (i > 0 && nums[i] === nums[i - 1]) continue; // Skip duplicate i

    for (let j = i + 1; j < n; j++) {
      if (j > i + 1 && nums[j] === nums[j - 1]) continue; // Skip duplicate j

      for (let k = j + 1; k < n; k++) {
        if (k > j + 1 && nums[k] === nums[k - 1]) continue; // Skip duplicate k

        if (nums[i] + nums[j] + nums[k] === 0) {
          result.push([nums[i], nums[j], nums[k]]);
        }
      }
    }
  }

  return result;
}

console.log(threeSumBrute([-1, 0, 1, 2, -1, -4])); // [[-1, -1, 2], [-1, 0, 1]]
```

#### ⚡ Optimized — Sort + Two Pointers

```javascript
function threeSumOptimized(nums) {
  const result = [];
  nums.sort((a, b) => a - b); // Sort the array

  for (let i = 0; i < nums.length - 2; i++) {
    // Skip duplicate values for i
    if (i > 0 && nums[i] === nums[i - 1]) continue;

    let left = i + 1;
    let right = nums.length - 1;

    while (left < right) {
      const sum = nums[i] + nums[left] + nums[right];

      if (sum === 0) {
        result.push([nums[i], nums[left], nums[right]]);

        // Skip duplicates for left and right
        while (left < right && nums[left] === nums[left + 1]) left++;
        while (left < right && nums[right] === nums[right - 1]) right--;

        left++;
        right--;
      } else if (sum < 0) {
        left++;   // Need bigger sum
      } else {
        right--;  // Need smaller sum
      }
    }
  }

  return result;
}

console.log(threeSumOptimized([-1, 0, 1, 2, -1, -4])); // [[-1, -1, 2], [-1, 0, 1]]
```

**Simple Explanation:** Sort the numbers. For each number, use two pointers on the remaining array to find two numbers that cancel it out (sum to its negative). Skip duplicates to avoid repeats.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n³) | O(1) |
| Optimized | O(n²) | O(1) |

---

### Question 2: Container With Most Water

**Problem Statement:** Given heights of lines at each position, find two lines that form the container holding the most water.

Example: `[1, 8, 6, 2, 5, 4, 8, 3, 7]` → `49`

**Thought Process:** Water area = min(height_left, height_right) × distance. Use two pointers from both ends and always move the shorter line inward.

#### 🐢 Brute Force

```javascript
function maxAreaBrute(heights) {
  let maxWater = 0;

  for (let i = 0; i < heights.length; i++) {
    for (let j = i + 1; j < heights.length; j++) {
      const width = j - i;
      const height = Math.min(heights[i], heights[j]);
      maxWater = Math.max(maxWater, width * height);
    }
  }

  return maxWater;
}

console.log(maxAreaBrute([1, 8, 6, 2, 5, 4, 8, 3, 7])); // 49
```

#### ⚡ Optimized — Two Pointers

```javascript
function maxAreaOptimized(heights) {
  let left = 0;
  let right = heights.length - 1;
  let maxWater = 0;

  while (left < right) {
    // Calculate water
    const width = right - left;
    const height = Math.min(heights[left], heights[right]);
    maxWater = Math.max(maxWater, width * height);

    // Move the pointer with the shorter line
    if (heights[left] < heights[right]) {
      left++;
    } else {
      right--;
    }
  }

  return maxWater;
}

console.log(maxAreaOptimized([1, 8, 6, 2, 5, 4, 8, 3, 7])); // 49
```

**Simple Explanation:** Imagine two walls with water between them. Start with the widest container (both ends). The water level is limited by the shorter wall. To find a potentially taller container, move the shorter wall inward — maybe the next wall is taller and holds more water.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(1) |

---

### Question 3: Sort Colors (Dutch National Flag)

**Problem Statement:** Given an array with only 0s, 1s, and 2s, sort it in-place in one pass.

Example: `[2, 0, 2, 1, 1, 0]` → `[0, 0, 1, 1, 2, 2]`

**Thought Process:** Use three pointers: `low` for placing 0s, `mid` for scanning, `high` for placing 2s.


#### Code Story
- This problem is about sorting a list with only three types of items (like 0s, 1s, and 2s).
- First, we use three pointers: 'low' for 0s, 'high' for 2s, and 'current' to scan.
- Then, if we see a 0, we swap it to the front; if a 2, we swap it to the back; if a 1, we just move on.
- Finally, the 0s are at the left, 2s at the right, and 1s are forced into the middle.
- This works because by pushing the 'outer' values to the ends, the middle value has nowhere to go but the center.

#### 🐢 Brute Force

```javascript
function sortColorsBrute(arr) {
  // Count occurrences of 0, 1, 2
  let count0 = 0, count1 = 0, count2 = 0;

  for (const num of arr) {
    if (num === 0) count0++;
    else if (num === 1) count1++;
    else count2++;
  }

  // Fill the array
  let idx = 0;
  while (count0-- > 0) arr[idx++] = 0;
  while (count1-- > 0) arr[idx++] = 1;
  while (count2-- > 0) arr[idx++] = 2;

  return arr;
}

console.log(sortColorsBrute([2, 0, 2, 1, 1, 0])); // [0, 0, 1, 1, 2, 2]
```

#### ⚡ Optimized — Dutch National Flag (Three Pointers)

```javascript
function sortColorsOptimized(arr) {
  let low = 0;              // Next position for 0
  let mid = 0;              // Current element being examined
  let high = arr.length - 1; // Next position for 2

  while (mid <= high) {
    if (arr[mid] === 0) {
      // Swap with low, move both forward
      [arr[low], arr[mid]] = [arr[mid], arr[low]];
      low++;
      mid++;
    } else if (arr[mid] === 1) {
      // 1 is in the right place, just move forward
      mid++;
    } else {
      // Swap with high, move high backward
      [arr[mid], arr[high]] = [arr[high], arr[mid]];
      high--;
      // Don't increment mid — need to check the swapped element
    }
  }

  return arr;
}

console.log(sortColorsOptimized([2, 0, 2, 1, 1, 0])); // [0, 0, 1, 1, 2, 2]
```

**Simple Explanation:** Imagine sorting balls into three buckets (red=0, white=1, blue=2). You have three markers: `low` marks where the next red ball goes, `high` marks where the next blue ball goes, and `mid` scans through. Red balls go left, blue balls go right, white stays put.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) (two passes) | O(1) |
| Optimized | O(n) (one pass) | O(1) |

---

### Question 4: Trapping Rain Water

**Problem Statement:** Given elevation map heights, find how much rain water can be trapped.

Example: `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` → `6`

**Thought Process:** Water at any position = min(maxLeft, maxRight) - height. Use two pointers with leftMax and rightMax.

#### 🐢 Brute Force

```javascript
function trapBrute(heights) {
  let water = 0;

  for (let i = 0; i < heights.length; i++) {
    // Find max height to the left
    let leftMax = 0;
    for (let j = 0; j <= i; j++) {
      leftMax = Math.max(leftMax, heights[j]);
    }

    // Find max height to the right
    let rightMax = 0;
    for (let j = i; j < heights.length; j++) {
      rightMax = Math.max(rightMax, heights[j]);
    }

    // Water at this position
    water += Math.min(leftMax, rightMax) - heights[i];
  }

  return water;
}

console.log(trapBrute([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])); // 6
```

#### ⚡ Optimized — Two Pointers

```javascript
function trapOptimized(heights) {
  let left = 0;
  let right = heights.length - 1;
  let leftMax = 0;
  let rightMax = 0;
  let water = 0;

  while (left < right) {
    if (heights[left] < heights[right]) {
      // Process left side
      if (heights[left] >= leftMax) {
        leftMax = heights[left]; // Update left max
      } else {
        water += leftMax - heights[left]; // Water trapped here
      }
      left++;
    } else {
      // Process right side
      if (heights[right] >= rightMax) {
        rightMax = heights[right]; // Update right max
      } else {
        water += rightMax - heights[right]; // Water trapped here
      }
      right--;
    }
  }

  return water;
}

console.log(trapOptimized([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])); // 6
```

**Simple Explanation:** Imagine buildings in a city after rain. Water collects between tall buildings. At each spot, the water level is limited by the shorter of the tallest buildings on each side. Two pointers let us calculate this in one pass by tracking the maximum heights seen from each direction.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(1) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Remove Duplicates from Sorted Array

**Problem Statement:** Remove duplicates in-place from a sorted array and return the new length.

**Approach:** Use slow/fast pointers. Slow tracks unique position, fast scans ahead.

```javascript
function removeDuplicates(arr) {
  if (arr.length === 0) return 0;

  let slow = 0; // Position of last unique element

  for (let fast = 1; fast < arr.length; fast++) {
    if (arr[fast] !== arr[slow]) {
      slow++;
      arr[slow] = arr[fast]; // Place unique element
    }
  }

  return slow + 1; // Length of unique portion
}

const arr = [1, 1, 2, 2, 3, 4, 4, 5];
console.log(removeDuplicates(arr)); // 5
console.log(arr.slice(0, 5));       // [1, 2, 3, 4, 5]
```


#### Code Story
- This problem is about cleaning up a list so every number only appears once, without using extra space.
- First, we use one pointer to walk through the list and another to keep track of where the unique items go.
- Then, every time we see a number that is different from the last one we kept, we move it to the 'unique' spot.
- Finally, we return the new length of the unique list.
- This works because it effectively 'slides' all unique items to the front, overwriting the duplicates as it goes.

**Explanation:** `slow` is like a stamp saying "last unique element placed here." `fast` runs ahead looking for new unique elements. When `fast` finds something different from `slow`, we advance `slow` and place it there.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 2: Squares of a Sorted Array

**Problem Statement:** Given a sorted array (may contain negatives), return an array of squares sorted in non-decreasing order.

Example: `[-4, -1, 0, 3, 10]` → `[0, 1, 9, 16, 100]`

**Approach:** Since negatives become positive after squaring, the largest squares are at the edges. Use two pointers from both ends.

```javascript
function sortedSquares(arr) {
  const n = arr.length;
  const result = new Array(n);
  let left = 0;
  let right = n - 1;
  let pos = n - 1; // Fill result from the end

  while (left <= right) {
    const leftSq = arr[left] * arr[left];
    const rightSq = arr[right] * arr[right];

    if (leftSq > rightSq) {
      result[pos] = leftSq;
      left++;
    } else {
      result[pos] = rightSq;
      right--;
    }
    pos--;
  }

  return result;
}

console.log(sortedSquares([-4, -1, 0, 3, 10])); // [0, 1, 9, 16, 100]
console.log(sortedSquares([-7, -3, 2, 3, 11]));  // [4, 9, 9, 49, 121]
```

**Explanation:** The biggest squares hide at the edges (large positives or large negatives). Compare squares from both ends, place the larger one at the back of the result, and move that pointer inward.

**Complexity:** Time: O(n), Space: O(n)

---

### Problem 3: Is Subsequence

**Problem Statement:** Check if string `s` is a subsequence of string `t` (characters appear in order but not necessarily consecutively).

Example: `s = "ace"`, `t = "abcde"` → `true`

**Approach:** Two pointers — one on each string. Advance `s` pointer only when characters match.

```javascript
function isSubsequence(s, t) {
  let sPtr = 0; // Pointer for s
  let tPtr = 0; // Pointer for t

  while (sPtr < s.length && tPtr < t.length) {
    if (s[sPtr] === t[tPtr]) {
      sPtr++; // Match! Move s pointer
    }
    tPtr++; // Always move t pointer
  }

  return sPtr === s.length; // Did we match all characters of s?
}

console.log(isSubsequence("ace", "abcde"));  // true
console.log(isSubsequence("aec", "abcde"));  // false
console.log(isSubsequence("", "anything"));  // true
```

**Explanation:** Imagine watching a movie (string `t`) and checking off scenes from a checklist (string `s`). You watch each scene in order. When a scene matches the next item on your checklist, check it off. If you finish the checklist before the movie ends, it's a subsequence.

**Complexity:** Time: O(n + m), Space: O(1)

---

### Problem 4: Merge Sorted Array In-Place

**Problem Statement:** Merge `nums2` into `nums1` where `nums1` has enough space. Both are sorted.

Example: `nums1 = [1, 2, 3, 0, 0, 0]`, `nums2 = [2, 5, 6]` → `[1, 2, 2, 3, 5, 6]`

**Approach:** Start from the end to avoid overwriting elements.

```javascript
function merge(nums1, m, nums2, n) {
  let p1 = m - 1;      // Last real element in nums1
  let p2 = n - 1;      // Last element in nums2
  let pos = m + n - 1;  // Last position in nums1

  // Fill from the back
  while (p1 >= 0 && p2 >= 0) {
    if (nums1[p1] > nums2[p2]) {
      nums1[pos] = nums1[p1];
      p1--;
    } else {
      nums1[pos] = nums2[p2];
      p2--;
    }
    pos--;
  }

  // Copy remaining elements from nums2 (if any)
  while (p2 >= 0) {
    nums1[pos] = nums2[p2];
    p2--;
    pos--;
  }

  return nums1;
}

const nums1 = [1, 2, 3, 0, 0, 0];
console.log(merge(nums1, 3, [2, 5, 6], 3)); // [1, 2, 2, 3, 5, 6]
```

**Explanation:** Instead of shifting elements right (expensive!), fill from the back. Compare the largest remaining elements from both arrays and place the bigger one at the end. Work backwards until done.

**Complexity:** Time: O(m + n), Space: O(1)

---

### 🔗 Navigation
Prev: [03_Strings.md](03_Strings.md) | Index: [00_Index.md](00_Index.md) | Next: [05_Sliding_Window.md](05_Sliding_Window.md)
