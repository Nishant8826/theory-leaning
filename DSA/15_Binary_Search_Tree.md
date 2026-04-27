# 📌 Binary Search Tree (BST)

## 🧠 Concept Explanation (Story Format)

Imagine a **library** where books are arranged with a rule: any book on the left shelf has a smaller ID, any book on the right shelf has a larger ID. To find a specific book, you start at the middle and keep going left or right. This is a **Binary Search Tree (BST)**.

A BST is a binary tree with a special property:
- **Left child** < Parent
- **Right child** > Parent
- This applies to every node in the tree!

```
        8
       / \
      3   10
     / \    \
    1   6   14
       / \  /
      4   7 13
```

### Why BSTs?

| Operation | Array (unsorted) | Sorted Array | BST (balanced) |
|-----------|-----------------|-------------|----------------|
| Search | O(n) | O(log n) | O(log n) |
| Insert | O(1) | O(n) | O(log n) |
| Delete | O(n) | O(n) | O(log n) |

BSTs give us the best of both worlds — fast search AND fast insert/delete.

### BST Property

**Inorder traversal of a BST always gives a sorted sequence.** This is the most important property to remember!

### Real-Life Analogy

Think of a **phone book** organized as a tree. Each page says: "names before me go left, names after me go right." To find "Kumar", start at the middle, go right for "K" (after the middle letter), and keep heading toward "Kumar".

---

## 🐢 Brute Force Approach

### Problem: Search in BST

**Practice Links:** [LeetCode #700](https://leetcode.com/problems/search-in-a-binary-search-tree/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/search-a-node-in-bst/1)

```javascript
class TreeNode {
  constructor(val) {
    this.val = val;
    this.left = null;
    this.right = null;
  }
}

// Brute Force: Traverse entire tree (ignoring BST property)
function searchBrute(root, target) {
  if (!root) return null;
  if (root.val === target) return root;

  // Check both sides (doesn't use BST property)
  const left = searchBrute(root.left, target);
  if (left) return left;
  return searchBrute(root.right, target);
}
```


#### Code Story
- This problem is about finding a specific value in a sorted Binary Search Tree.
- First, if the value is bigger than the Root, we go right; if smaller, we go left.
- Then, we repeat this at every node we land on.
- Finally, we either find the node or hit a dead end (null).
- This works because the BST's sorted nature allows us to skip half the tree at every single step, making searches incredibly fast.

---

## ⚡ Optimized Approach

### BST Search — Use the BST Property

**Practice Links:** [LeetCode #700](https://leetcode.com/problems/search-in-a-binary-search-tree/)

```javascript
// Optimized: Use BST property — O(log n) for balanced tree
function searchBST(root, target) {
  let current = root;

  while (current !== null) {
    if (target === current.val) return current;
    if (target < current.val) current = current.left;
    else current = current.right;
  }

  return null; // Not found
}
```

### BST Insert

**Practice Links:** [LeetCode #701](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/insert-a-node-in-bst/1)

```javascript
function insertBST(root, val) {
  if (!root) return new TreeNode(val);

  if (val < root.val) {
    root.left = insertBST(root.left, val);
  } else {
    root.right = insertBST(root.right, val);
  }

  return root;
}

// Build a BST
let root = null;
[8, 3, 10, 1, 6, 14, 4, 7, 13].forEach(val => {
  root = insertBST(root, val);
});
```

### BST Delete

**Practice Links:** [LeetCode #450](https://leetcode.com/problems/delete-node-in-a-bst/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/delete-a-node-from-bst/1)

```javascript
function deleteBST(root, key) {
  if (!root) return null;

  if (key < root.val) {
    root.left = deleteBST(root.left, key);
  } else if (key > root.val) {
    root.right = deleteBST(root.right, key);
  } else {
    // Found the node to delete
    if (!root.left) return root.right;   // No left child
    if (!root.right) return root.left;   // No right child

    // Two children: replace with inorder successor (smallest in right subtree)
    let successor = root.right;
    while (successor.left) successor = successor.left;

    root.val = successor.val;
    root.right = deleteBST(root.right, successor.val);
  }

  return root;
}
```

---

## 🔍 Complexity Analysis

| Operation | Balanced BST | Skewed BST (worst) |
|-----------|-------------|-------------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Space | O(n) | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Validate Binary Search Tree

**Practice Links:** [LeetCode #98](https://leetcode.com/problems/validate-binary-search-tree/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/check-for-bst/1) | [InterviewBit](https://www.interviewbit.com/problems/valid-binary-search-tree/)

**Problem Statement:** Check if a binary tree is a valid BST.

#### 🐢 Brute Force — Inorder and Check Sorted

```javascript
function isValidBSTBrute(root) {
  const values = [];
  function inorder(node) {
    if (!node) return;
    inorder(node.left);
    values.push(node.val);
    inorder(node.right);
  }
  inorder(root);

  for (let i = 1; i < values.length; i++) {
    if (values[i] <= values[i - 1]) return false;
  }
  return true;
}
```

#### ⚡ Optimized — Recursive with Bounds

```javascript
function isValidBST(root, min = -Infinity, max = Infinity) {
  if (!root) return true;
  if (root.val <= min || root.val >= max) return false;

  return isValidBST(root.left, min, root.val) &&
         isValidBST(root.right, root.val, max);
}
```

**Simple Explanation:** Each node must be within valid bounds. The root can be anything. Its left child must be less than the root. Its left child's right child must be between the left child and the root. We pass these bounds down recursively.

**Complexity:** Time: O(n), Space: O(h)

---

### Question 2: Lowest Common Ancestor in BST

**Practice Links:** [LeetCode #235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/lowest-common-ancestor-in-a-bst/1) | [InterviewBit](https://www.interviewbit.com/problems/least-common-ancestor/)

**Problem Statement:** Find the lowest common ancestor (LCA) of two nodes in a BST.

#### 🐢 Brute Force — Find Paths

```javascript
function lcaBrute(root, p, q) {
  function findPath(node, target, path) {
    if (!node) return false;
    path.push(node);
    if (node.val === target) return true;
    if (findPath(node.left, target, path) || findPath(node.right, target, path)) return true;
    path.pop();
    return false;
  }

  const pathP = [], pathQ = [];
  findPath(root, p, pathP);
  findPath(root, q, pathQ);

  let lca = null;
  for (let i = 0; i < Math.min(pathP.length, pathQ.length); i++) {
    if (pathP[i] === pathQ[i]) lca = pathP[i];
    else break;
  }
  return lca;
}
```

#### ⚡ Optimized — Use BST Property

```javascript
function lcaOptimized(root, p, q) {
  let current = root;

  while (current) {
    if (p < current.val && q < current.val) {
      current = current.left;  // Both on the left
    } else if (p > current.val && q > current.val) {
      current = current.right; // Both on the right
    } else {
      return current; // Split point — this is the LCA!
    }
  }

  return null;
}
```

**Simple Explanation:** In a BST, if both values are smaller, go left. If both are larger, go right. The moment they "split" — one goes left and one goes right — you've found the LCA. Like two people at a fork in the road; the fork is their common ancestor.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Optimized | O(h) | O(1) |

---

### Question 3: Kth Smallest Element in BST

**Practice Links:** [LeetCode #230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/find-k-th-smallest-element-in-bst/1) | [InterviewBit](https://www.interviewbit.com/problems/kth-smallest-element-in-tree/)

**Problem Statement:** Find the kth smallest element in a BST.


#### Code Story
- This problem is about finding the k-th item if you were to list all numbers in order.
- First, we remember that an 'Inorder' traversal (Left, Me, Right) visits nodes in perfectly sorted order.
- Then, we perform that traversal and count how many items we've seen.
- Finally, when our count hits k, we stop and return the current node.
- This works because it leverages the natural sorted structure of the tree to find the answer without actually having to sort anything.

#### 🐢 Brute Force — Inorder to Array

```javascript
function kthSmallestBrute(root, k) {
  const values = [];
  function inorder(node) {
    if (!node) return;
    inorder(node.left);
    values.push(node.val);
    inorder(node.right);
  }
  inorder(root);
  return values[k - 1];
}
```

#### ⚡ Optimized — Stop Early

```javascript
function kthSmallestOptimized(root, k) {
  let count = 0;
  let result = null;

  function inorder(node) {
    if (!node || result !== null) return;

    inorder(node.left);

    count++;
    if (count === k) {
      result = node.val;
      return;
    }

    inorder(node.right);
  }

  inorder(root);
  return result;
}
```

**Simple Explanation:** Inorder traversal of a BST gives sorted order. Count as you traverse; stop at the kth element. No need to traverse the entire tree.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n) | O(n) |
| Optimized | O(h + k) | O(h) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Convert Sorted Array to Balanced BST

**Practice Links:** [LeetCode #108](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/array-to-bst4443/1) | [InterviewBit](https://www.interviewbit.com/problems/sorted-array-to-balanced-bst/)

```javascript
function sortedArrayToBST(nums) {
  if (nums.length === 0) return null;

  const mid = Math.floor(nums.length / 2);
  const root = new TreeNode(nums[mid]);

  root.left = sortedArrayToBST(nums.slice(0, mid));
  root.right = sortedArrayToBST(nums.slice(mid + 1));

  return root;
}

const bst = sortedArrayToBST([1, 2, 3, 4, 5, 6, 7]);
// Creates a balanced BST with 4 as root
```

**Explanation:** Pick the middle element as root (balances the tree). Left half becomes left subtree, right half becomes right subtree. Recurse.

**Complexity:** Time: O(n), Space: O(log n) stack

---

### Problem 2: BST Iterator

**Practice Links:** [LeetCode #173](https://leetcode.com/problems/binary-search-tree-iterator/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/bst-iterator/1) | [InterviewBit](https://www.interviewbit.com/problems/bst-iterator/)

```javascript
class BSTIterator {
  constructor(root) {
    this.stack = [];
    this._pushLeft(root);
  }

  _pushLeft(node) {
    while (node) {
      this.stack.push(node);
      node = node.left;
    }
  }

  next() {
    const node = this.stack.pop();
    if (node.right) this._pushLeft(node.right);
    return node.val;
  }

  hasNext() {
    return this.stack.length > 0;
  }
}
```

**Explanation:** Simulates inorder traversal lazily. Push all left nodes initially. On each `next()`, pop, return value, and push left nodes of the right subtree. Gives sorted elements one at a time.

**Complexity:** Next: O(1) amortized, Space: O(h)

---

### Problem 3: Two Sum in BST

**Practice Links:** [LeetCode #653](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/find-a-pair-with-given-target-in-bst/1) | [InterviewBit](https://www.interviewbit.com/problems/2sum-binary-tree/)

```javascript
function findTarget(root, k) {
  const set = new Set();

  function dfs(node) {
    if (!node) return false;
    if (set.has(k - node.val)) return true;
    set.add(node.val);
    return dfs(node.left) || dfs(node.right);
  }

  return dfs(root);
}
```

**Explanation:** Traverse the BST. For each value, check if `k - value` has been seen before using a set. Same as Two Sum but on a tree.

**Complexity:** Time: O(n), Space: O(n)

---

### 🔗 Navigation
Prev: [14_Trees.md](14_Trees.md) | Index: [00_Index.md](00_Index.md) | Next: [16_Heap.md](16_Heap.md)
