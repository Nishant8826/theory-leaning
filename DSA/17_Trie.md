# 📌 Trie

## 🧠 Concept Explanation (Story Format)

Imagine you're building a **phone's autocomplete feature**. When someone types "app", you want to suggest "apple", "application", "approach". How do you quickly find all words starting with a prefix?

You could search through every word in the dictionary — but that's slow. Instead, you build a **Trie** (pronounced "try") — a tree where each path from root to leaf spells out a word, and shared prefixes share the same branches.

### What is a Trie?

A Trie is a tree-like data structure used to store strings, where:
- Each node represents a **single character**
- The path from root to a node spells a **prefix**
- Nodes marked as "end" represent complete words

```
Root
├── a
│   └── p
│       └── p
│           ├── l
│           │   └── e ✓ (apple)
│           └── s ✓ (apps)
├── c
│   ├── a
│   │   ├── r ✓ (car)
│   │   └── t ✓ (cat)
```

### When to Use Tries

| Use Case | Why Trie? |
|----------|-----------|
| Autocomplete | Find all words with given prefix |
| Spell checker | Check if a word exists quickly |
| IP routing | Longest prefix matching |
| Word games | Find valid words from letter combinations |
| Search engines | Suggest completions as you type |

### Trie vs Hash Map

| Feature | Trie | Hash Map |
|---------|------|----------|
| Prefix search | O(L) — excellent | O(n) — check every key |
| Exact search | O(L) | O(L) average |
| Space | Can share prefixes | Each key stored independently |
| Sorted iteration | Natural | Requires sorting |

L = length of the word/prefix

### Real-Life Analogy

Think of a **phone tree menu**: "Press 1 for sales, 2 for support..." At each step, you narrow down options. A Trie works the same way — each character narrows the search.

---

## 🐢 Brute Force Approach

### Problem: Implement Autocomplete

```javascript
// Brute Force: Store words in array, filter by prefix
function autocompleteBrute(words, prefix) {
  return words.filter(word => word.startsWith(prefix));
}

const dictionary = ["apple", "app", "application", "bat", "ball", "cat"];
console.log(autocompleteBrute(dictionary, "app"));
// ["apple", "app", "application"]
```

### Line-by-Line Explanation

1. Loop through every word in the dictionary.
2. Check if each word starts with the prefix.
3. For every search, we scan ALL words — O(n × L).

---

## ⚡ Optimized Approach

### Trie Implementation

```javascript
class TrieNode {
  constructor() {
    this.children = {};    // Character → TrieNode
    this.isEndOfWord = false; // Marks complete words
  }
}

class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  // Insert a word — O(L)
  insert(word) {
    let node = this.root;
    for (const char of word) {
      if (!node.children[char]) {
        node.children[char] = new TrieNode();
      }
      node = node.children[char];
    }
    node.isEndOfWord = true; // Mark end of word
  }

  // Search for exact word — O(L)
  search(word) {
    let node = this.root;
    for (const char of word) {
      if (!node.children[char]) return false;
      node = node.children[char];
    }
    return node.isEndOfWord;
  }

  // Check if any word starts with prefix — O(L)
  startsWith(prefix) {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children[char]) return false;
      node = node.children[char];
    }
    return true;
  }

  // Get all words with a given prefix
  autocomplete(prefix) {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children[char]) return [];
      node = node.children[char];
    }

    const results = [];
    this._collectWords(node, prefix, results);
    return results;
  }

  _collectWords(node, prefix, results) {
    if (node.isEndOfWord) results.push(prefix);
    for (const [char, childNode] of Object.entries(node.children)) {
      this._collectWords(childNode, prefix + char, results);
    }
  }
}

// Usage
const trie = new Trie();
["apple", "app", "application", "bat", "ball", "cat"].forEach(w => trie.insert(w));

console.log(trie.search("apple"));      // true
console.log(trie.search("app"));        // true
console.log(trie.search("ap"));         // false (not a complete word)
console.log(trie.startsWith("ap"));     // true
console.log(trie.autocomplete("app"));  // ["app", "apple", "application"]
```

---

## 🔍 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(L) — L = word length | O(L) per word |
| Search | O(L) | O(1) |
| StartsWith | O(L) | O(1) |
| Autocomplete | O(L + k) — k = results | O(k) |
| Space (total) | — | O(N × L) worst case |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Implement Trie (LeetCode 208)

**Problem Statement:** Implement a trie with insert, search, and startsWith methods.

#### 🐢 Brute Force — Using Array of Words

```javascript
class TrieBrute {
  constructor() { this.words = []; }
  insert(word) { this.words.push(word); }
  search(word) { return this.words.includes(word); }
  startsWith(prefix) { return this.words.some(w => w.startsWith(prefix)); }
}
```

#### ⚡ Optimized — Full Trie (shown above in the optimized section)

**Complexity:**
| Approach | Insert | Search | StartsWith |
|----------|--------|--------|------------|
| Brute Force | O(1) | O(n × L) | O(n × L) |
| Trie | O(L) | O(L) | O(L) |

---

### Question 2: Word Search II

**Problem Statement:** Given a 2D board and a list of words, find all words that exist in the board.

**Thought Process:** Build a Trie from the word list, then DFS on the board using the Trie to prune paths.

#### 🐢 Brute Force

```javascript
function findWordsBrute(board, words) {
  const result = new Set();
  const rows = board.length, cols = board[0].length;

  function dfs(r, c, idx, word, visited) {
    if (idx === word.length) { result.add(word); return; }
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;
    if (visited[r][c] || board[r][c] !== word[idx]) return;

    visited[r][c] = true;
    const dirs = [[0,1],[0,-1],[1,0],[-1,0]];
    for (const [dr, dc] of dirs) {
      dfs(r + dr, c + dc, idx + 1, word, visited);
    }
    visited[r][c] = false;
  }

  for (const word of words) {
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const visited = Array.from({length: rows}, () => Array(cols).fill(false));
        dfs(r, c, 0, word, visited);
      }
    }
  }

  return [...result];
}
```

#### ⚡ Optimized — Trie + DFS

```javascript
function findWordsOptimized(board, words) {
  const root = {};

  // Build trie from words
  for (const word of words) {
    let node = root;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node.word = word; // Store complete word at end
  }

  const rows = board.length, cols = board[0].length;
  const result = [];

  function dfs(r, c, node) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;
    const ch = board[r][c];
    if (ch === '#' || !node[ch]) return;

    node = node[ch];
    if (node.word) {
      result.push(node.word);
      node.word = null; // Avoid duplicates
    }

    board[r][c] = '#'; // Mark visited
    dfs(r + 1, c, node);
    dfs(r - 1, c, node);
    dfs(r, c + 1, node);
    dfs(r, c - 1, node);
    board[r][c] = ch; // Restore
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      dfs(r, c, root);
    }
  }

  return result;
}

const board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]];
console.log(findWordsOptimized(board, ["oath","pea","eat","rain"]));
// ["oath", "eat"]
```

**Simple Explanation:** Instead of searching the board for each word separately, build a Trie from all words. Then DFS the board once, following Trie paths. If a path doesn't exist in the Trie, stop early (pruning). Much faster when there are many words.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(W × M × N × 4^L) | O(L) |
| Trie + DFS | O(M × N × 4^L) | O(W × L) |

---

### Question 3: Design Add and Search Words (with wildcards)

**Problem Statement:** Design a data structure supporting addWord and search (where `.` matches any character).

#### ⚡ Optimized — Trie with DFS for Wildcards

```javascript
class WordDictionary {
  constructor() {
    this.root = {};
  }

  addWord(word) {
    let node = this.root;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node.isEnd = true;
  }

  search(word) {
    return this._dfs(word, 0, this.root);
  }

  _dfs(word, idx, node) {
    if (idx === word.length) return !!node.isEnd;

    const ch = word[idx];

    if (ch === '.') {
      // Wildcard — try all children
      for (const key of Object.keys(node)) {
        if (key !== 'isEnd' && this._dfs(word, idx + 1, node[key])) {
          return true;
        }
      }
      return false;
    }

    if (!node[ch]) return false;
    return this._dfs(word, idx + 1, node[ch]);
  }
}

const dict = new WordDictionary();
dict.addWord("bad");
dict.addWord("dad");
dict.addWord("mad");
console.log(dict.search("pad"));  // false
console.log(dict.search("bad"));  // true
console.log(dict.search(".ad"));  // true
console.log(dict.search("b.."));  // true
```

**Simple Explanation:** Normal characters follow the trie path. When we see a `.` (wildcard), we try ALL children at that level. It's like a maze where `.` means "try every door at this junction."

**Complexity:** addWord: O(L), search: O(26^L) worst case with all wildcards

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Longest Common Prefix Using Trie

```javascript
function longestCommonPrefix(words) {
  if (words.length === 0) return "";

  const root = {};

  // Insert all words into trie
  for (const word of words) {
    let node = root;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node.isEnd = true;
  }

  // Walk the trie until branching or end of word
  let prefix = "";
  let node = root;
  while (Object.keys(node).length === 1 && !node.isEnd) {
    const ch = Object.keys(node)[0];
    if (ch === 'isEnd') break;
    prefix += ch;
    node = node[ch];
  }

  return prefix;
}

console.log(longestCommonPrefix(["flower","flow","flight"])); // "fl"
console.log(longestCommonPrefix(["dog","car","race"]));       // ""
```

**Explanation:** Insert all words. Walk from root as long as each node has exactly one child and isn't an end-of-word. The path traversed is the longest common prefix.

**Complexity:** Time: O(S) where S = sum of all characters, Space: O(S)

---

### Problem 2: Replace Words with Root

```javascript
function replaceWords(dictionary, sentence) {
  const root = {};

  // Build trie from dictionary
  for (const word of dictionary) {
    let node = root;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node.isEnd = true;
  }

  // Replace each word with its shortest root
  return sentence.split(' ').map(word => {
    let node = root;
    let prefix = '';
    for (const ch of word) {
      if (!node[ch] || node.isEnd) break;
      prefix += ch;
      node = node[ch];
    }
    return node.isEnd ? prefix : word;
  }).join(' ');
}

console.log(replaceWords(["cat","bat","rat"], "the cattle was rattled by the battery"));
// "the cat was rat by the bat"
```

**Explanation:** Build a Trie from root words. For each word in the sentence, walk the trie until we find an end-of-word marker (root found) or run out of trie path (no root, keep original).

**Complexity:** Time: O(N × L), Space: O(D) where D = dictionary size

---

### Problem 3: Count Distinct Substrings

```javascript
function countDistinctSubstrings(s) {
  const root = {};
  let count = 0;

  for (let i = 0; i < s.length; i++) {
    let node = root;
    for (let j = i; j < s.length; j++) {
      const ch = s[j];
      if (!node[ch]) {
        node[ch] = {};
        count++; // New substring found
      }
      node = node[ch];
    }
  }

  return count + 1; // +1 for empty string
}

console.log(countDistinctSubstrings("abc")); // 7 ("", "a", "ab", "abc", "b", "bc", "c")
console.log(countDistinctSubstrings("aba")); // 6
```

**Explanation:** Insert all suffixes of the string into a trie. Each new node created represents a new distinct substring.

**Complexity:** Time: O(n²), Space: O(n²)

---

### 🔗 Navigation
Prev: [16_Heap.md](16_Heap.md) | Index: [00_Index.md](00_Index.md) | Next: [18_Graphs_Basics.md](18_Graphs_Basics.md)
