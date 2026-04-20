# 📌 Topological Sort

## 🧠 Concept Explanation (Story Format)

Imagine you're planning to **get dressed**. You need to put on underwear before pants, socks before shoes, and a shirt before a jacket. There's an **order of dependencies**. You can't wear shoes before socks!

**Topological Sort** takes a directed acyclic graph (DAG) and produces a linear ordering where for every directed edge (A → B), A comes before B.

### Key Rules

1. Only works on **Directed Acyclic Graphs (DAGs)** — no cycles allowed!
2. Multiple valid orderings may exist.
3. If a cycle exists, topological sort is impossible.

### Where Topological Sort is Used

- **Build systems:** Compile files in dependency order (Webpack, Make)
- **Course scheduling:** Prerequisites must come first
- **Task scheduling:** Some tasks depend on others
- **Package managers:** Install dependencies in the right order (npm)

### Real-Life Analogy

Think of a **recipe**. You must chop vegetables before cooking them, and cooking comes before serving. Topological sort gives you a valid order to complete all steps respecting all dependencies.

---

## 🐢 Brute Force Approach

### Kahn's Algorithm (BFS-Based)

```javascript
// Kahn's Algorithm — BFS using in-degree
function topologicalSortBFS(numNodes, edges) {
  // Build graph and in-degree count
  const graph = {};
  const inDegree = {};

  for (let i = 0; i < numNodes; i++) {
    graph[i] = [];
    inDegree[i] = 0;
  }

  for (const [from, to] of edges) {
    graph[from].push(to);
    inDegree[to]++;
  }

  // Find all nodes with in-degree 0 (no dependencies)
  const queue = [];
  for (let i = 0; i < numNodes; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  const result = [];

  while (queue.length > 0) {
    const node = queue.shift();
    result.push(node);

    // Reduce in-degree for neighbors
    for (const neighbor of graph[node]) {
      inDegree[neighbor]--;
      if (inDegree[neighbor] === 0) {
        queue.push(neighbor); // Ready to process
      }
    }
  }

  // If all nodes included, valid topological order exists
  return result.length === numNodes ? result : []; // Empty = cycle detected
}

console.log(topologicalSortBFS(6, [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]));
// Example output: [4, 5, 2, 0, 3, 1]
```


#### Code Story
- This problem is about finding a valid task order by repeatedly doing the tasks that have zero dependencies.
- First, we count how many prerequisites (in-degree) every task has.
- Then, we put all tasks with 0 prerequisites into a queue.
- Finally, as we do a task, we 'unblock' its neighbors; if a neighbor hits 0 prerequisites, it enters the queue.
- This works because it systematically drains the 'easiest' tasks first until the whole project is finished.

### Line-by-Line Explanation

1. **In-degree** — count how many edges point INTO each node (dependencies).
2. **Start with nodes that have 0 in-degree** — they have no dependencies.
3. **Process each node** — when removed, reduce in-degree of its neighbors.
4. **When a neighbor's in-degree hits 0** — it's ready (all dependencies met).

---

## ⚡ Optimized Approach

### DFS-Based Topological Sort

```javascript
// DFS-Based Topological Sort
function topologicalSortDFS(numNodes, edges) {
  const graph = {};
  for (let i = 0; i < numNodes; i++) graph[i] = [];
  for (const [from, to] of edges) graph[from].push(to);

  const visited = new Set();
  const inStack = new Set(); // For cycle detection
  const result = [];
  let hasCycle = false;

  function dfs(node) {
    if (hasCycle) return;
    if (inStack.has(node)) { hasCycle = true; return; } // Cycle!
    if (visited.has(node)) return;

    inStack.add(node);
    visited.add(node);

    for (const neighbor of graph[node]) {
      dfs(neighbor);
    }

    inStack.delete(node);
    result.push(node); // Add AFTER processing all descendants
  }

  for (let i = 0; i < numNodes; i++) {
    if (!visited.has(i)) dfs(i);
  }

  if (hasCycle) return [];
  return result.reverse(); // Reverse post-order = topological order
}

console.log(topologicalSortDFS(6, [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]));
// Example output: [5, 4, 2, 3, 1, 0]
```

---

## 🔍 Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS-based | O(V + E) | O(V + E) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Course Schedule II (Find Order)

**Problem Statement:** Given n courses and prerequisites, return an order to take all courses (or empty if impossible).


#### Code Story
- This problem is about finding the actual list of steps to finish all tasks.
- First, we use Topological Sort (either Kahn's or DFS with a stack).
- Then, we build our list as we process the tasks.
- Finally, if our list contains all tasks, we return it; if not (due to a cycle), we return an empty list.
- This works because topological sorting is specifically designed to linearize hierarchical dependencies.

#### 🐢 Brute Force — Kahn's Algorithm

```javascript
function findOrder(numCourses, prerequisites) {
  const graph = {};
  const inDegree = new Array(numCourses).fill(0);

  for (let i = 0; i < numCourses; i++) graph[i] = [];
  for (const [course, prereq] of prerequisites) {
    graph[prereq].push(course);
    inDegree[course]++;
  }

  const queue = [];
  for (let i = 0; i < numCourses; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  const order = [];
  while (queue.length > 0) {
    const node = queue.shift();
    order.push(node);
    for (const neighbor of graph[node]) {
      inDegree[neighbor]--;
      if (inDegree[neighbor] === 0) queue.push(neighbor);
    }
  }

  return order.length === numCourses ? order : [];
}

console.log(findOrder(4, [[1,0],[2,0],[3,1],[3,2]])); // [0, 1, 2, 3] or [0, 2, 1, 3]
console.log(findOrder(2, [[1,0],[0,1]]));               // [] (cycle!)
```

#### ⚡ Optimized — DFS

```javascript
function findOrderDFS(numCourses, prerequisites) {
  const graph = {};
  for (let i = 0; i < numCourses; i++) graph[i] = [];
  for (const [course, prereq] of prerequisites) graph[prereq].push(course);

  const WHITE = 0, GRAY = 1, BLACK = 2;
  const color = new Array(numCourses).fill(WHITE);
  const result = [];

  function dfs(node) {
    color[node] = GRAY;
    for (const next of graph[node]) {
      if (color[next] === GRAY) return false;
      if (color[next] === WHITE && !dfs(next)) return false;
    }
    color[node] = BLACK;
    result.push(node);
    return true;
  }

  for (let i = 0; i < numCourses; i++) {
    if (color[i] === WHITE && !dfs(i)) return [];
  }

  return result.reverse();
}
```

**Simple Explanation:** Start with courses that have no prerequisites (in-degree 0). Complete them, then their dependents become available. Continue until all courses are done. If some courses are never reachable (cycle), return empty.

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### Question 2: Alien Dictionary

**Problem Statement:** Given a sorted list of words from an alien language, determine the character order.


#### Code Story
- This problem is about deriving the alphabet order of a new language by looking at sorted words.
- First, we compare adjacent words to see which letter comes before another (like 'apple' and 'apply' tells us 'e' < 'y').
- Then, we build a directed graph where an arrow means 'comes before'.
- Finally, we perform a Topological Sort on the letters to get the final alphabet string.
- This works because the rules from the word list form clear 'prerequisites' for the letters, which is exactly what topological sorting solves.

#### ⚡ Optimized — Build Graph + Topological Sort

```javascript
function alienOrder(words) {
  const graph = {};
  const inDegree = {};

  // Initialize all characters
  for (const word of words) {
    for (const ch of word) {
      if (!graph[ch]) graph[ch] = [];
      if (!(ch in inDegree)) inDegree[ch] = 0;
    }
  }

  // Compare adjacent words to build edges
  for (let i = 0; i < words.length - 1; i++) {
    const w1 = words[i], w2 = words[i + 1];
    const minLen = Math.min(w1.length, w2.length);

    // Edge case: "abc" before "ab" is invalid
    if (w1.length > w2.length && w1.startsWith(w2)) return "";

    for (let j = 0; j < minLen; j++) {
      if (w1[j] !== w2[j]) {
        graph[w1[j]].push(w2[j]);
        inDegree[w2[j]]++;
        break; // Only first difference matters
      }
    }
  }

  // Kahn's algorithm
  const queue = [];
  for (const ch in inDegree) {
    if (inDegree[ch] === 0) queue.push(ch);
  }

  let result = "";
  while (queue.length > 0) {
    const ch = queue.shift();
    result += ch;
    for (const next of graph[ch]) {
      inDegree[next]--;
      if (inDegree[next] === 0) queue.push(next);
    }
  }

  return result.length === Object.keys(inDegree).length ? result : "";
}

console.log(alienOrder(["wrt","wrf","er","ett","rftt"])); // "wertf"
```

**Simple Explanation:** Compare adjacent words to find which character comes before which. Build a graph of these relationships. Topological sort gives the character order. Like reverse-engineering an alphabetical sorting.

**Complexity:** Time: O(total characters), Space: O(unique characters)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Minimum Height Trees

```javascript
function findMinHeightTrees(n, edges) {
  if (n === 1) return [0];

  const graph = {};
  const degree = new Array(n).fill(0);

  for (let i = 0; i < n; i++) graph[i] = [];
  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
    degree[u]++;
    degree[v]++;
  }

  // Start with leaves (degree 1)
  let leaves = [];
  for (let i = 0; i < n; i++) {
    if (degree[i] === 1) leaves.push(i);
  }

  let remaining = n;
  while (remaining > 2) {
    remaining -= leaves.length;
    const newLeaves = [];

    for (const leaf of leaves) {
      for (const neighbor of graph[leaf]) {
        degree[neighbor]--;
        if (degree[neighbor] === 1) newLeaves.push(neighbor);
      }
    }

    leaves = newLeaves;
  }

  return leaves;
}

console.log(findMinHeightTrees(6, [[3,0],[3,1],[3,2],[3,4],[5,4]])); // [3, 4]
```

**Explanation:** Peel leaves layer by layer (like peeling an onion). The last 1-2 nodes remaining are the roots that minimize tree height. Think of finding the "center" of the tree.

**Complexity:** Time: O(V), Space: O(V)

---

### Problem 2: Parallel Courses

```javascript
function minimumSemesters(n, relations) {
  const graph = {};
  const inDegree = new Array(n + 1).fill(0);

  for (let i = 1; i <= n; i++) graph[i] = [];
  for (const [prev, next] of relations) {
    graph[prev].push(next);
    inDegree[next]++;
  }

  let queue = [];
  for (let i = 1; i <= n; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  let semesters = 0;
  let completed = 0;

  while (queue.length > 0) {
    const nextQueue = [];
    semesters++;

    for (const course of queue) {
      completed++;
      for (const next of graph[course]) {
        inDegree[next]--;
        if (inDegree[next] === 0) nextQueue.push(next);
      }
    }

    queue = nextQueue;
  }

  return completed === n ? semesters : -1;
}

console.log(minimumSemesters(3, [[1,3],[2,3]])); // 2
```

**Explanation:** Process all courses with no prerequisites each semester (BFS levels). Each level = one semester. The number of levels is the minimum semesters needed.

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### Problem 3: Sequence Reconstruction

```javascript
function sequenceReconstruction(original, sequences) {
  const graph = {};
  const inDegree = {};

  // Build graph from sequences
  for (const seq of sequences) {
    for (const num of seq) {
      if (!graph[num]) graph[num] = [];
      if (!(num in inDegree)) inDegree[num] = 0;
    }
    for (let i = 0; i < seq.length - 1; i++) {
      graph[seq[i]].push(seq[i + 1]);
      inDegree[seq[i + 1]]++;
    }
  }

  // Kahn's algorithm — check uniqueness
  const queue = [];
  for (const key in inDegree) {
    if (inDegree[key] === 0) queue.push(Number(key));
  }

  const result = [];
  while (queue.length === 1) { // Must be EXACTLY one choice at each step
    const node = queue.shift();
    result.push(node);
    for (const next of graph[node]) {
      inDegree[next]--;
      if (inDegree[next] === 0) queue.push(next);
    }
  }

  return result.length === original.length &&
         result.every((val, idx) => val === original[idx]);
}
```

**Explanation:** The original sequence can be uniquely reconstructed only if at every step in topological sort, there's exactly one choice (queue never has more than one element).

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### 🔗 Navigation
Prev: [19_Graphs_Traversal.md](19_Graphs_Traversal.md) | Index: [00_Index.md](00_Index.md) | Next: [21_Shortest_Path.md](21_Shortest_Path.md)
