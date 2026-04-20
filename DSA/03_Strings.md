# 📌 Strings

## 🧠 Concept Explanation (Story Format)

Imagine you're writing a **text message**. Each character — every letter, space, and punctuation — is stored one after another, like beads on a necklace. That necklace is a **string**.

A string is simply a **sequence of characters**. In JavaScript, strings are **immutable** — once created, you can't change individual characters. Any "modification" creates a brand-new string.

### Why Strings Matter

- **Everywhere in real apps:** User input, URLs, file names, database queries — all strings.
- **Interview favorite:** String problems test your ability to think about characters, patterns, and edge cases.
- **Foundation for:** Pattern matching, parsing, and text processing.

### Key String Properties in JavaScript

```javascript
const str = "Hello World";

str.length;          // 11 — number of characters
str[0];              // 'H' — access by index (0-based)
str.charAt(4);       // 'o' — same as str[4]
str.toUpperCase();   // 'HELLO WORLD'
str.toLowerCase();   // 'hello world'
str.split(' ');      // ['Hello', 'World']
str.includes('World'); // true
str.indexOf('o');    // 4 — first occurrence
```

### Real-Life Analogy

Think of a string like a **train of letters**. Each coach (character) has a seat number (index). You can read any coach, count all coaches, or compare two trains to see if they carry the same passengers. But you can't swap a coach in the middle — you'd need to build a whole new train.

---

## 🐢 Brute Force Approach

### Problem: Reverse a String

Given a string, reverse it.

```javascript
// Brute Force: Build a new string character by character
function reverseStringBrute(str) {
  let reversed = ""; // Start with empty string

  // Go from last character to first
  for (let i = str.length - 1; i >= 0; i--) {
    reversed += str[i]; // Append each character
  }

  return reversed;
}

console.log(reverseStringBrute("hello"));  // "olleh"
console.log(reverseStringBrute("world"));  // "dlrow"
```

### Line-by-Line Explanation

1. **`let reversed = ""`** — We build the result from scratch.
2. **`for (let i = str.length - 1; ...)`** — Start from the last character.
3. **`reversed += str[i]`** — Add each character to our result. (Note: string concatenation in a loop creates new strings each time — O(n) per concatenation)

---

## ⚡ Optimized Approach

Use an array for efficient character appending, then join.

```javascript
// Optimized: Use array and join
function reverseStringOptimized(str) {
  const chars = str.split(''); // Convert string to array of characters
  let left = 0;
  let right = chars.length - 1;

  // Swap characters from both ends
  while (left < right) {
    [chars[left], chars[right]] = [chars[right], chars[left]];
    left++;
    right--;
  }

  return chars.join(''); // Convert back to string
}

console.log(reverseStringOptimized("hello"));  // "olleh"
console.log(reverseStringOptimized("abcde"));  // "edcba"
```

### Why is this better?

- **Brute force:** String concatenation in a loop can be O(n²) because each `+=` creates a new string.
- **Optimized:** Array operations and a single `join()` at the end — O(n) total.

---

## 🔍 Complexity Analysis

| Approach | Time Complexity | Space Complexity |
|----------|----------------|-----------------|
| Brute Force (string concat) | O(n²) worst case | O(n) |
| Optimized (array swap) | O(n) | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Check if a String is a Palindrome

**Problem Statement:** A palindrome reads the same forward and backward. Check if a given string is a palindrome (ignore non-alphanumeric characters and case).

Example: `"A man, a plan, a canal: Panama"` → `true`

**Thought Process:** Clean the string (remove non-alphanumeric, lowercase), then compare from both ends.


#### Code Story
- This problem is about checking if a phrase reads the same way forward and backward.
- First, we clean up the text by removing spaces and punctuation and making everything lowercase.
- Then, we use two pointers—one at the start and one at the end—to compare each character.
- Finally, if all characters match, it's a palindrome; if even one pair differs, it isn't.
- This works because a palindrome is perfectly symmetrical, so the front and back must be identical mirror images.

#### 🐢 Brute Force

```javascript
function isPalindromeBrute(s) {
  // Clean the string: keep only letters and digits, make lowercase
  let cleaned = "";
  for (let i = 0; i < s.length; i++) {
    const ch = s[i].toLowerCase();
    if ((ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9')) {
      cleaned += ch;
    }
  }

  // Reverse the cleaned string
  let reversed = "";
  for (let i = cleaned.length - 1; i >= 0; i--) {
    reversed += cleaned[i];
  }

  // Compare
  return cleaned === reversed;
}

console.log(isPalindromeBrute("A man, a plan, a canal: Panama")); // true
console.log(isPalindromeBrute("race a car"));                      // false
```

#### ⚡ Optimized — Two Pointers

```javascript
function isPalindromeOptimized(s) {
  let left = 0;
  let right = s.length - 1;

  while (left < right) {
    // Skip non-alphanumeric characters from left
    while (left < right && !isAlphaNumeric(s[left])) left++;
    // Skip non-alphanumeric characters from right
    while (left < right && !isAlphaNumeric(s[right])) right--;

    // Compare characters (case-insensitive)
    if (s[left].toLowerCase() !== s[right].toLowerCase()) {
      return false;
    }

    left++;
    right--;
  }

  return true;
}

function isAlphaNumeric(ch) {
  const c = ch.toLowerCase();
  return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9');
}

console.log(isPalindromeOptimized("A man, a plan, a canal: Panama")); // true
console.log(isPalindromeOptimized("race a car"));                      // false
```

**Simple Explanation:** You and a friend stand at opposite ends of the sentence. You both walk toward each other, skipping spaces and punctuation. At each step, you compare your characters. If they ever differ, it's not a palindrome.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Optimized | O(n) | O(1) |

---

### Question 2: First Non-Repeating Character

**Problem Statement:** Find the first character in a string that doesn't repeat.

Example: `"aabbcdd"` → `'c'`

**Thought Process:** Count the frequency of each character, then find the first one with count 1.

#### 🐢 Brute Force

```javascript
function firstUniqueBrute(s) {
  // For each character, check if it appears again
  for (let i = 0; i < s.length; i++) {
    let isUnique = true;

    for (let j = 0; j < s.length; j++) {
      if (i !== j && s[i] === s[j]) {
        isUnique = false;
        break;
      }
    }

    if (isUnique) return s[i];
  }

  return null; // No unique character
}

console.log(firstUniqueBrute("aabbcdd")); // 'c'
console.log(firstUniqueBrute("aabb"));     // null
```

#### ⚡ Optimized — Hash Map

```javascript
function firstUniqueOptimized(s) {
  const freq = new Map(); // Character → count

  // Count frequencies
  for (const ch of s) {
    freq.set(ch, (freq.get(ch) || 0) + 1);
  }

  // Find first character with count 1
  for (const ch of s) {
    if (freq.get(ch) === 1) {
      return ch;
    }
  }

  return null;
}

console.log(firstUniqueOptimized("aabbcdd"));       // 'c'
console.log(firstUniqueOptimized("leetcode"));       // 'l'
console.log(firstUniqueOptimized("aabb"));           // null
```

**Simple Explanation:** Imagine a roll call. First pass: count how many times each name is called. Second pass: go through the list and find the first name called exactly once. That's your unique character.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Optimized | O(n) | O(n) |

---

### Question 3: Check if Two Strings are Anagrams

**Problem Statement:** Two strings are anagrams if they contain the same characters with the same frequency, just rearranged.

Example: `"listen"` and `"silent"` → `true`

**Thought Process:** Count characters in both strings and compare.


#### Code Story
- This problem is about checking if two words contain exactly the same letters in a different order.
- First, we count how many times each letter appears in the first word.
- Then, we go through the second word and subtract the counts for each letter we find.
- Finally, if all our counts end up back at zero, the words are anagrams.
- This works because words with the same 'ingredient list' of letters will always cancel each other out in a tally.

#### 🐢 Brute Force — Sort and Compare

```javascript
function isAnagramBrute(s1, s2) {
  if (s1.length !== s2.length) return false;

  // Sort both strings and compare
  const sorted1 = s1.split('').sort().join('');
  const sorted2 = s2.split('').sort().join('');

  return sorted1 === sorted2;
}

console.log(isAnagramBrute("listen", "silent")); // true
console.log(isAnagramBrute("hello", "world"));   // false
```

#### ⚡ Optimized — Frequency Count

```javascript
function isAnagramOptimized(s1, s2) {
  if (s1.length !== s2.length) return false;

  const freq = new Map();

  // Count characters in first string
  for (const ch of s1) {
    freq.set(ch, (freq.get(ch) || 0) + 1);
  }

  // Subtract counts using second string
  for (const ch of s2) {
    if (!freq.has(ch) || freq.get(ch) === 0) {
      return false; // Character not found or count exhausted
    }
    freq.set(ch, freq.get(ch) - 1);
  }

  return true;
}

console.log(isAnagramOptimized("listen", "silent")); // true
console.log(isAnagramOptimized("rat", "car"));       // false
```

**Simple Explanation:** Imagine you have two bags of Scrabble tiles. Are they identical sets? Brute force: sort both bags and compare. Smart way: count tiles in bag 1, then for each tile in bag 2, reduce the count. If any count goes below zero, they're different.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n log n) | O(n) |
| Optimized | O(n) | O(n) |

---

### Question 4: Longest Substring Without Repeating Characters

**Problem Statement:** Find the length of the longest substring without repeating characters.

Example: `"abcabcbb"` → `3` (substring `"abc"`)

**Thought Process:** Use a sliding window with a set to track characters in the current window.

#### 🐢 Brute Force

```javascript
function longestSubstringBrute(s) {
  let maxLen = 0;

  // Try every possible substring
  for (let i = 0; i < s.length; i++) {
    const seen = new Set();
    let len = 0;

    for (let j = i; j < s.length; j++) {
      if (seen.has(s[j])) break; // Duplicate found, stop
      seen.add(s[j]);
      len++;
    }

    maxLen = Math.max(maxLen, len);
  }

  return maxLen;
}

console.log(longestSubstringBrute("abcabcbb")); // 3
console.log(longestSubstringBrute("bbbbb"));     // 1
```

#### ⚡ Optimized — Sliding Window

```javascript
function longestSubstringOptimized(s) {
  const charIndex = new Map(); // Character → last seen index
  let maxLen = 0;
  let start = 0; // Start of current window

  for (let end = 0; end < s.length; end++) {
    // If character was seen and is within current window
    if (charIndex.has(s[end]) && charIndex.get(s[end]) >= start) {
      // Move start past the duplicate
      start = charIndex.get(s[end]) + 1;
    }

    charIndex.set(s[end], end); // Update last seen position
    maxLen = Math.max(maxLen, end - start + 1); // Update max length
  }

  return maxLen;
}

console.log(longestSubstringOptimized("abcabcbb")); // 3
console.log(longestSubstringOptimized("bbbbb"));     // 1
console.log(longestSubstringOptimized("pwwkew"));    // 3
```

**Simple Explanation:** Imagine looking through a window at passing train coaches. You want the longest stretch where all coaches have different colors. When you see a repeated color, you slide the left edge of your window past the older duplicate.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(n) |
| Optimized | O(n) | O(n) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Count Vowels and Consonants

**Problem Statement:** Count the number of vowels and consonants in a string.

**Approach:** Loop through each character and check if it's a vowel.

```javascript
function countVowelsConsonants(str) {
  let vowels = 0;
  let consonants = 0;
  const vowelSet = new Set(['a', 'e', 'i', 'o', 'u']);

  for (const ch of str.toLowerCase()) {
    if (ch >= 'a' && ch <= 'z') {
      if (vowelSet.has(ch)) {
        vowels++;
      } else {
        consonants++;
      }
    }
  }

  return { vowels, consonants };
}

console.log(countVowelsConsonants("Hello World"));
// { vowels: 3, consonants: 7 }
```

**Explanation:** Walk through each letter. If it's a, e, i, o, or u — it's a vowel. Any other letter? Consonant. Skip spaces and special characters.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 2: String Compression

**Problem Statement:** Compress a string by counting consecutive repeated characters. `"aabcccccaaa"` → `"a2b1c5a3"`

**Approach:** Walk through the string, count consecutive same characters.

```javascript
function compressString(s) {
  if (s.length === 0) return s;

  let compressed = "";
  let count = 1;

  for (let i = 1; i <= s.length; i++) {
    if (i < s.length && s[i] === s[i - 1]) {
      count++; // Same character, increment count
    } else {
      compressed += s[i - 1] + count; // Add character and its count
      count = 1; // Reset count
    }
  }

  // Return shorter version
  return compressed.length < s.length ? compressed : s;
}

console.log(compressString("aabcccccaaa")); // "a2b1c5a3"
console.log(compressString("abc"));          // "abc" (compressed is longer)
```


#### Code Story
- This problem is about shortening a string like 'aaabb' into 'a3b2'.
- First, we look at the first character and start counting its 'streak'.
- Then, as soon as the character changes, we write the old character and its count into our result.
- Finally, if the 'compressed' version is actually shorter than the original, we keep it.
- This works because it replaces repeated patterns with a simple tally, saving space whenever many same letters are in a row.

**Explanation:** Like describing a crowd: "2 red shirts, 1 blue, 5 green, 3 red" instead of listing each person. You walk through the string counting same-character streaks.

**Complexity:** Time: O(n), Space: O(n)

---

### Problem 3: Check if String is a Rotation of Another

**Problem Statement:** Check if string `s2` is a rotation of `s1`.

Example: `"waterbottle"` is a rotation of `"erbottlewat"`.

**Approach:** If `s2` is a rotation of `s1`, then `s2` must be a substring of `s1 + s1`.

```javascript
function isRotation(s1, s2) {
  // Lengths must match
  if (s1.length !== s2.length || s1.length === 0) return false;

  // Concatenate s1 with itself
  const doubled = s1 + s1;

  // Check if s2 exists in doubled string
  return doubled.includes(s2);
}

console.log(isRotation("waterbottle", "erbottlewat")); // true
console.log(isRotation("hello", "llohe"));              // true
console.log(isRotation("hello", "world"));              // false
```

**Explanation:** Imagine a circular bracelet with letters. Any rotation is just starting to read from a different bead. By doubling the string ("abcabc"), every possible rotation is a substring of this doubled version.

**Complexity:** Time: O(n), Space: O(n)

---

### Problem 4: Reverse Words in a Sentence

**Problem Statement:** Reverse the order of words in a sentence.

Example: `"the sky is blue"` → `"blue is sky the"`

**Approach:** Split into words, reverse the array, join back.

```javascript
function reverseWords(s) {
  // Split by spaces, filter empty strings, reverse, join
  return s
    .trim()                          // Remove leading/trailing spaces
    .split(/\s+/)                    // Split by one or more spaces
    .reverse()                       // Reverse the word array
    .join(' ');                       // Join with single space
}

console.log(reverseWords("the sky is blue"));    // "blue is sky the"
console.log(reverseWords("  hello world  "));    // "world hello"
console.log(reverseWords("a good   example"));   // "example good a"
```

**Explanation:** Think of words as train coaches. You detach all the coaches, turn the train around, and reattach them. The last coach is now first.

**Complexity:** Time: O(n), Space: O(n)

---

### Problem 5: Longest Common Prefix

**Problem Statement:** Find the longest common prefix among an array of strings.

Example: `["flower", "flow", "flight"]` → `"fl"`

**Approach:** Compare characters column by column across all strings.

```javascript
function longestCommonPrefix(strs) {
  if (strs.length === 0) return "";

  // Use the first string as reference
  const first = strs[0];

  for (let i = 0; i < first.length; i++) {
    const char = first[i];

    // Check this character against all other strings
    for (let j = 1; j < strs.length; j++) {
      // If we've exceeded a word's length or characters don't match
      if (i >= strs[j].length || strs[j][i] !== char) {
        return first.substring(0, i);
      }
    }
  }

  return first; // First string is the prefix
}

console.log(longestCommonPrefix(["flower", "flow", "flight"])); // "fl"
console.log(longestCommonPrefix(["dog", "racecar", "car"]));     // ""
console.log(longestCommonPrefix(["interstellar", "internet", "internal"])); // "inter"
```


#### Code Story
- This problem is about finding the longest starting string shared by a group of words.
- First, we take the first word and assume it's the whole prefix.
- Then, we compare it to the next word and 'shrink' it until it matches the start of that word.
- Finally, we repeat this for every word until our prefix is either correct for everyone or empty.
- This works because a shared prefix can only get smaller as you add more words to the rule.

**Explanation:** Line up all the words vertically. Read column by column (first letter of each, then second, etc.). The moment any word doesn't match, stop. Everything you've read so far is the common prefix.

**Complexity:** Time: O(S) where S = sum of all characters, Space: O(1)

---

### 🔗 Navigation
Prev: [02_Arrays.md](02_Arrays.md) | Index: [00_Index.md](00_Index.md) | Next: [04_Two_Pointers.md](04_Two_Pointers.md)
