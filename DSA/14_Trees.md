# 📌 Trees

## 🧠 Concept Explanation (Story Format)

Imagine your **family tree** — grandparents at the top, parents below, children below them. Each person connects to their children, branching out like an upside-down tree. That's exactly what a **Tree** data structure looks like!

A **tree** is a hierarchical data structure with a **root** node at the top, and each node can have zero or more **children**. Unlike a linked list (which is linear), a tree **branches out**.

### Key Terminology

| Term | Meaning |
|------|---------|
| **Root** | Top node (no parent) |
| **Node** | Each element in the tree |
| **Edge** | Connection between two nodes |
| **Parent** | Node above another |
| **Child** | Node below another |
| **Leaf** | Node with no children |
| **Height** | Longest path from root to leaf |
| **Depth** | Distance from root to a node |

### Binary Tree

A **binary tree** is a tree where each node has **at most 2 children** (left and right).

```
        1          ← Root
       / \
      2   3        ← Level 1
     / \   \
    4   5   6      ← Level 2 (4, 5, 6 are leaves)
```

### Tree Traversals

| Traversal | Order | Use Case |
|-----------|-------|----------|
| **Inorder** | Left → Root → Right | Sorted order (BST) |
| **Preorder** | Root → Left → Right | Copy/serialize tree |
| **Postorder** | Left → Right → Root | Delete tree |
| **Level Order (BFS)** | Level by level | Print by depth |

### Real-Life Analogy

- **File system**: folders contain subfolders and files — a tree!
- **Organization chart**: CEO → VPs → Managers → Employees
- **HTML DOM**: `<html>` → `<body>` → `<div>` → `<p>`

---

## 🐢 Brute Force Approach

### Tree Node and Traversals

```javascript
class TreeNode {
  constructor(val) {
    this.val = val;
    this.left = null;
    this.right = null;
  }
}

// Build a sample tree:     1
//                         / \
//                        2   3
//                       / \
//                      4   5

const root = new TreeNode(1);
root.left = new TreeNode(2);
root.right = new TreeNode(3);
root.left.left = new TreeNode(4);
root.left.right = new TreeNode(5);

// Inorder Traversal (Left → Root → Right)
function inorder(node) {
  if (node === null) return [];
  return [...inorder(node.left), node.val, ...inorder(node.right)];
}

// Preorder Traversal (Root → Left → Right)
function preorder(node) {
  if (node === null) return [];
  return [node.val, ...preorder(node.left), ...preorder(node.right)];
}

// Postorder Traversal (Left → Right → Root)
function postorder(node) {
  if (node === null) return [];
  return [...postorder(node.left), ...postorder(node.right), node.val];
}

console.log(inorder(root));   // [4, 2, 5, 1, 3]
console.log(preorder(root));  // [1, 2, 4, 5, 3]
console.log(postorder(root)); // [4, 5, 2, 3, 1]
```

---

## ⚡ Optimized Approach

### Level Order Traversal (BFS) — Using Queue

```javascript
function levelOrder(root) {
  if (!root) return [];

  const result = [];
  const queue = [root];

  while (queue.length > 0) {
    const levelSize = queue.length;
    const level = [];

    for (let i = 0; i < levelSize; i++) {
      const node = queue.shift();
      level.push(node.val);

      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }

    result.push(level);
  }

  return result;
}

console.log(levelOrder(root)); // [[1], [2, 3], [4, 5]]
```

### Iterative Inorder Traversal (Using Stack)

```javascript
function inorderIterative(root) {
  const result = [];
  const stack = [];
  let current = root;

  while (current !== null || stack.length > 0) {
    while (current !== null) {
      stack.push(current);
      current = current.left;
    }
    current = stack.pop();
    result.push(current.val);
    current = current.right;
  }

  return result;
}

console.log(inorderIterative(root)); // [4, 2, 5, 1, 3]
```

---

## 🔍 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Traversal (any) | O(n) | O(h) where h = height |
| Level Order | O(n) | O(w) where w = max width |
| Search | O(n) for general tree | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Maximum Depth of Binary Tree

**Problem Statement:** Find the maximum depth (height) of a binary tree.

#### 🐢 Brute Force — BFS Level Count

```javascript
function maxDepthBFS(root) {
  if (!root) return 0;
  const queue = [root];
  let depth = 0;

  while (queue.length > 0) {
    const size = queue.length;
    for (let i = 0; i < size; i++) {
      const node = queue.shift();
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    depth++;
  }

  return depth;
}

console.log(maxDepthBFS(root)); // 3
```

#### ⚡ Optimized — Recursive DFS

```javascript
function maxDepthDFS(root) {
  if (!root) return 0;
  return 1 + Math.max(maxDepthDFS(root.left), maxDepthDFS(root.right));
}

console.log(maxDepthDFS(root)); // 3
```

**Simple Explanation:** The height of a tree = 1 (current node) + the height of its taller subtree. The base case: an empty tree has height 0. Like asking: "How many floors does this building have?" = 1 + however many floors the taller wing has.

**Complexity:** Time: O(n), Space: O(h)

---

### Question 2: Invert Binary Tree

**Problem Statement:** Mirror a binary tree — swap every left and right child.

#### 🐢 Brute Force — BFS

```javascript
function invertBFS(root) {
  if (!root) return null;
  const queue = [root];

  while (queue.length > 0) {
    const node = queue.shift();
    [node.left, node.right] = [node.right, node.left]; // Swap

    if (node.left) queue.push(node.left);
    if (node.right) queue.push(node.right);
  }

  return root;
}
```

#### ⚡ Optimized — Recursive

```javascript
function invertDFS(root) {
  if (!root) return null;

  // Swap children
  [root.left, root.right] = [root.right, root.left];

  // Recursively invert subtrees
  invertDFS(root.left);
  invertDFS(root.right);

  return root;
}
```

**Simple Explanation:** At every node, swap the left and right children, then do the same for all subtrees. Like holding a tree up to a mirror.

**Complexity:** Time: O(n), Space: O(h)

---

### Question 3: Check if Two Trees are Identical

**Problem Statement:** Check if two binary trees are structurally identical with the same values.

#### 🐢 Brute Force — Convert to Arrays and Compare

```javascript
function isSameBrute(p, q) {
  const serialize = (node) => {
    if (!node) return 'null';
    return `${node.val},${serialize(node.left)},${serialize(node.right)}`;
  };
  return serialize(p) === serialize(q);
}
```

#### ⚡ Optimized — Recursive Comparison

```javascript
function isSameTree(p, q) {
  if (!p && !q) return true;                    // Both null — same
  if (!p || !q) return false;                   // One null — different
  if (p.val !== q.val) return false;            // Values differ

  return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
}
```

**Simple Explanation:** Two trees are the same if their roots are equal AND their left subtrees are the same AND their right subtrees are the same. Like comparing two family trees person by person.

**Complexity:** Time: O(n), Space: O(h)

---

### Question 4: Diameter of Binary Tree

**Problem Statement:** Find the diameter — the longest path between any two nodes (not necessarily through the root).

#### 🐢 Brute Force

```javascript
function diameterBrute(root) {
  let maxDiameter = 0;

  function height(node) {
    if (!node) return 0;
    return 1 + Math.max(height(node.left), height(node.right));
  }

  function traverse(node) {
    if (!node) return;
    const d = height(node.left) + height(node.right);
    maxDiameter = Math.max(maxDiameter, d);
    traverse(node.left);
    traverse(node.right);
  }

  traverse(root);
  return maxDiameter;
}
```

#### ⚡ Optimized — Single Traversal

```javascript
function diameterOptimized(root) {
  let maxDiameter = 0;

  function height(node) {
    if (!node) return 0;

    const leftH = height(node.left);
    const rightH = height(node.right);

    // Update diameter at this node
    maxDiameter = Math.max(maxDiameter, leftH + rightH);

    return 1 + Math.max(leftH, rightH);
  }

  height(root);
  return maxDiameter;
}

console.log(diameterOptimized(root)); // 3
```

**Simple Explanation:** At each node, the longest path through that node = left height + right height. We calculate heights once and track the maximum path seen.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(h) |
| Optimized | O(n) | O(h) |

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Check if Tree is Symmetric

```javascript
function isSymmetric(root) {
  if (!root) return true;

  function isMirror(left, right) {
    if (!left && !right) return true;
    if (!left || !right) return false;
    return left.val === right.val &&
           isMirror(left.left, right.right) &&
           isMirror(left.right, right.left);
  }

  return isMirror(root.left, root.right);
}
```

**Explanation:** A tree is symmetric if the left subtree is a mirror of the right subtree. For each pair, left's left should match right's right, and vice versa.

**Complexity:** Time: O(n), Space: O(h)

---

### Problem 2: Path Sum

**Problem Statement:** Check if any root-to-leaf path sums to a target.

```javascript
function hasPathSum(root, target) {
  if (!root) return false;

  // Leaf node — check if remaining sum matches
  if (!root.left && !root.right) {
    return root.val === target;
  }

  // Check left and right subtrees with reduced target
  return hasPathSum(root.left, target - root.val) ||
         hasPathSum(root.right, target - root.val);
}
```

**Explanation:** Walk from root toward leaves, subtracting each node's value from the target. At a leaf, if the remaining target equals the leaf's value, we found a path.

**Complexity:** Time: O(n), Space: O(h)

---

### Problem 3: Count Good Nodes

**Problem Statement:** A node is "good" if no node on the path from root to it has a greater value.

```javascript
function goodNodes(root) {
  let count = 0;

  function dfs(node, maxSoFar) {
    if (!node) return;

    if (node.val >= maxSoFar) {
      count++;
    }

    const newMax = Math.max(maxSoFar, node.val);
    dfs(node.left, newMax);
    dfs(node.right, newMax);
  }

  dfs(root, root.val);
  return count;
}
```

**Explanation:** Track the maximum value seen on the path from root to current node. If the current node's value is ≥ that maximum, it's a good node. Like walking downhill — a good node is any point that's at least as high as the highest point you've been.

**Complexity:** Time: O(n), Space: O(h)

---

### 🔗 Navigation
Prev: [13_Queue.md](13_Queue.md) | Index: [00_Index.md](00_Index.md) | Next: [15_Binary_Search_Tree.md](15_Binary_Search_Tree.md)
