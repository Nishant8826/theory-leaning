# 📌 Bit Manipulation

## 🧠 Concept Explanation (Story Format)

Imagine every number in your computer is stored as a row of **light switches** — each switch is either ON (1) or OFF (0). These are **bits**. When you manipulate numbers at the bit level, you're flipping individual switches — and it's **blazing fast** because CPUs are built to do this.

**Bit manipulation** is the technique of using bitwise operators to solve problems at the binary level. It's like having a secret shortcut that most people don't know about.

### Binary Representation

```
Decimal  →  Binary
  5      →  101
  10     →  1010
  15     →  1111
  8      →  1000
```

### Bitwise Operators

| Operator | Symbol | Example (5 & 3) | Result |
|----------|--------|-----------------|--------|
| AND | `&` | `101 & 011` | `001` (1) |
| OR | `\|` | `101 \| 011` | `111` (7) |
| XOR | `^` | `101 ^ 011` | `110` (6) |
| NOT | `~` | `~101` | `...010` (-6) |
| Left Shift | `<<` | `101 << 1` | `1010` (10) |
| Right Shift | `>>` | `101 >> 1` | `10` (2) |

### Key Bit Tricks

```javascript
// Check if number is even or odd
const isEven = (n & 1) === 0;  // Last bit is 0 → even

// Multiply by 2
const double = n << 1;  // Shift left = multiply by 2

// Divide by 2
const half = n >> 1;  // Shift right = divide by 2

// Check if power of 2
const isPowerOf2 = n > 0 && (n & (n - 1)) === 0;

// Toggle a bit at position k
const toggled = n ^ (1 << k);

// XOR properties
// a ^ a = 0  (any number XOR itself = 0)
// a ^ 0 = a  (any number XOR 0 = itself)
```

### Real-Life Analogy

Think of a row of **10 switches** controlling lights. Bitwise AND is like checking which lights are ON in BOTH rooms. XOR is finding which lights differ between rooms. Bit manipulation is electrician-level control of individual switches.

---

## 🐢 Brute Force Approach

### Problem: Find the Single Number (all others appear twice)

```javascript
// Brute Force: Use a hash map to count occurrences
function singleNumberBrute(nums) {
  const freq = {};

  for (const num of nums) {
    freq[num] = (freq[num] || 0) + 1;
  }

  for (const num in freq) {
    if (freq[num] === 1) return Number(num);
  }
}

console.log(singleNumberBrute([2, 2, 1]));       // 1
console.log(singleNumberBrute([4, 1, 2, 1, 2])); // 4
```

---

## ⚡ Optimized Approach

### XOR — Every number XOR'd with itself cancels out!

```javascript
// XOR: a ^ a = 0, a ^ 0 = a
function singleNumberXOR(nums) {
  let result = 0;

  for (const num of nums) {
    result ^= num; // XOR all numbers — pairs cancel out
  }

  return result; // Only the unique number remains
}

console.log(singleNumberXOR([2, 2, 1]));       // 1
console.log(singleNumberXOR([4, 1, 2, 1, 2])); // 4
```

### Why Does This Work?

```
2 ^ 2 ^ 1 = 0 ^ 1 = 1
4 ^ 1 ^ 2 ^ 1 ^ 2 = 4 ^ (1 ^ 1) ^ (2 ^ 2) = 4 ^ 0 ^ 0 = 4
```

---

## 🔍 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Hash Map | O(n) | O(n) |
| XOR | O(n) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Count Number of 1-Bits (Hamming Weight)

**Problem Statement:** Count the number of 1 bits in the binary representation of a number.

#### 🐢 Brute Force

```javascript
function hammingWeightBrute(n) {
  let count = 0;
  const binary = n.toString(2); // Convert to binary string

  for (const bit of binary) {
    if (bit === '1') count++;
  }

  return count;
}

console.log(hammingWeightBrute(11));  // 3 (1011)
console.log(hammingWeightBrute(128)); // 1 (10000000)
```

#### ⚡ Optimized — Brian Kernighan's Algorithm

```javascript
function hammingWeightOptimized(n) {
  let count = 0;

  while (n !== 0) {
    n &= (n - 1); // Remove the lowest set bit
    count++;
  }

  return count;
}

console.log(hammingWeightOptimized(11));  // 3
console.log(hammingWeightOptimized(128)); // 1
```

**Simple Explanation:** `n & (n - 1)` removes the rightmost 1-bit. Count how many times we can do this before n becomes 0. It's like turning off lights one at a time — count how many you turned off.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(log n) | O(log n) |
| Optimized | O(k) where k = number of 1-bits | O(1) |

---

### Question 2: Power of Two

**Problem Statement:** Check if a number is a power of 2.

#### 🐢 Brute Force

```javascript
function isPowerOfTwoBrute(n) {
  if (n <= 0) return false;
  while (n > 1) {
    if (n % 2 !== 0) return false;
    n = n / 2;
  }
  return true;
}
```

#### ⚡ Optimized — Bit Trick

```javascript
function isPowerOfTwo(n) {
  return n > 0 && (n & (n - 1)) === 0;
}

console.log(isPowerOfTwo(1));   // true  (2⁰)
console.log(isPowerOfTwo(16));  // true  (2⁴)
console.log(isPowerOfTwo(6));   // false
console.log(isPowerOfTwo(0));   // false
```

**Simple Explanation:** Powers of 2 have exactly one 1-bit: `1→1, 2→10, 4→100, 8→1000`. Subtracting 1 flips all bits after the 1-bit: `8-1=7→0111`. AND of these is 0 only for powers of 2.

**Complexity:** O(1) time, O(1) space

---

### Question 3: Missing Number (XOR Approach)

**Problem Statement:** Given array of n numbers from 0 to n, find the missing one.

#### 🐢 Brute Force — Sum Formula

```javascript
function missingNumberSum(nums) {
  const n = nums.length;
  const expected = (n * (n + 1)) / 2;
  const actual = nums.reduce((sum, num) => sum + num, 0);
  return expected - actual;
}
```

#### ⚡ Optimized — XOR

```javascript
function missingNumberXOR(nums) {
  let xor = nums.length; // Start with n

  for (let i = 0; i < nums.length; i++) {
    xor ^= i ^ nums[i]; // XOR index with value
  }

  return xor;
}

console.log(missingNumberXOR([3, 0, 1]));           // 2
console.log(missingNumberXOR([9,6,4,2,3,5,7,0,1])); // 8
```

**Simple Explanation:** XOR all indices (0 to n) with all values. Every number that appears in both cancels out (a ^ a = 0). The only number left is the missing one.

**Complexity:** Time: O(n), Space: O(1)

---

### Question 4: Reverse Bits

**Problem Statement:** Reverse all 32 bits of a given unsigned integer.

#### ⚡ Optimized

```javascript
function reverseBits(n) {
  let result = 0;

  for (let i = 0; i < 32; i++) {
    result = (result << 1) | (n & 1); // Shift result left, add last bit of n
    n >>= 1;                           // Shift n right
  }

  return result >>> 0; // Convert to unsigned
}

console.log(reverseBits(43261596)); // 964176192
// Binary: 00000010100101000001111010011100
// Reversed: 00111001011110000010100101000000
```

**Simple Explanation:** Extract the last bit of n (using `n & 1`), append it to the result (using `result << 1 | bit`), then shift n right. Repeat 32 times. Like reading a word backward letter by letter.

**Complexity:** Time: O(32) = O(1), Space: O(1)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Counting Bits

**Problem Statement:** For every number from 0 to n, count the number of 1-bits.

```javascript
function countBits(n) {
  const result = new Array(n + 1).fill(0);

  for (let i = 1; i <= n; i++) {
    result[i] = result[i >> 1] + (i & 1);
    // Number of 1s in i = number of 1s in i/2 + last bit of i
  }

  return result;
}

console.log(countBits(5)); // [0, 1, 1, 2, 1, 2]
console.log(countBits(2)); // [0, 1, 1]
```

**Explanation:** The number of 1-bits in `i` = bits in `i/2` (shift right) + whether the last bit is 1. Use previously computed values — classic DP!

**Complexity:** Time: O(n), Space: O(n)

---

### Problem 2: Sum of Two Integers Without + Operator

```javascript
function getSum(a, b) {
  while (b !== 0) {
    const carry = (a & b) << 1; // Carry = AND shifted left
    a = a ^ b;                   // Sum without carry = XOR
    b = carry;                   // Add carry in next iteration
  }
  return a;
}

console.log(getSum(1, 2));  // 3
console.log(getSum(-2, 3)); // 1
```

**Explanation:** XOR gives sum without carry. AND gives carry positions. Shift carry left and add again. Repeat until no carry remains. Like manual binary addition.

**Complexity:** Time: O(32) = O(1), Space: O(1)

---

### Problem 3: Single Number III (Two Unique Numbers)

```javascript
function singleNumberIII(nums) {
  // XOR all → gives xor of the two unique numbers
  let xor = 0;
  for (const num of nums) xor ^= num;

  // Find a bit where the two numbers differ
  const diffBit = xor & (-xor); // Lowest set bit

  let a = 0, b = 0;
  for (const num of nums) {
    if (num & diffBit) a ^= num; // Group with this bit set
    else b ^= num;                // Group without this bit
  }

  return [a, b];
}

console.log(singleNumberIII([1, 2, 1, 3, 2, 5])); // [3, 5]
```

**Explanation:** XOR all numbers to get `a ^ b`. Find any bit where they differ (lowest set bit). Use that bit to split all numbers into two groups — each group has exactly one unique number. XOR within each group to find them.

**Complexity:** Time: O(n), Space: O(1)

---

### 🔗 Navigation
Prev: [24_Dynamic_Programming.md](24_Dynamic_Programming.md) | Index: [00_Index.md](00_Index.md) | Next: [26_Disjoint_Set.md](26_Disjoint_Set.md)
