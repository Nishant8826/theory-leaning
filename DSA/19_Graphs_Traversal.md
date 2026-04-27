# 📌 Graphs — Traversal (BFS & DFS)

## 🧠 Concept Explanation (Story Format)

Imagine you're exploring a **dungeon** with multiple rooms connected by hallways. You need to visit every room. You have two strategies:

1. **DFS (Depth-First Search):** Pick a hallway and keep going deeper and deeper until you hit a dead end. Then backtrack and try the next unexplored hallway. Like exploring one branch completely before moving to the next.

2. **BFS (Breadth-First Search):** Explore ALL rooms directly connected to your current room first, then move to rooms that are 2 steps away, then 3, and so on. Like a ripple spreading outward.

### DFS vs BFS Comparison

| Feature | DFS | BFS |
|---------|-----|-----|
| Data Structure | Stack (or recursion) | Queue |
| Explores | Depth first (go deep) | Width first (go wide) |
| Memory | O(h) — height | O(w) — width |
| Finds shortest path? | No | Yes (unweighted) |
| Use cases | Cycle detection, topological sort, connected components | Shortest path, level-order, nearest neighbor |

### Visual Example

```
Graph:    A --- B --- E
          |         |
          C --- D ---

DFS (from A): A → B → E → D → C
BFS (from A): A → B, C → E, D
```

### Real-Life Analogy

- **DFS** = Solving a maze by always taking the first available turn, going as deep as possible, then backtracking.
- **BFS** = A fire spreading in a building — it spreads to ALL adjacent rooms at each time step.

---

## 🐢 Brute Force Approach

### DFS — Recursive

```javascript
function dfsRecursive(graph, start) {
  const visited = new Set();
  const result = [];

  function dfs(node) {
    if (visited.has(node)) return;
    visited.add(node);
    result.push(node);

    // Visit all neighbors
    for (const neighbor of (graph[node] || [])) {
      dfs(neighbor);
    }
  }

  dfs(start);
  return result;
}

const graph = {
  'A': ['B', 'C'],
  'B': ['A', 'D', 'E'],
  'C': ['A', 'D'],
  'D': ['B', 'C', 'E'],
  'E': ['B', 'D']
};

console.log(dfsRecursive(graph, 'A')); // ['A', 'B', 'D', 'C', 'E']
```

### Line-by-Line Explanation

1. **`visited`** — tracks which nodes we've already seen (avoid revisiting).
2. **Mark current node** as visited and add to result.
3. **Recurse** into each unvisited neighbor.
4. The recursion stack naturally provides the "backtracking" behavior.

---

## ⚡ Optimized Approach

### DFS — Iterative (Using Stack)

```javascript
function dfsIterative(graph, start) {
  const visited = new Set();
  const stack = [start];
  const result = [];

  while (stack.length > 0) {
    const node = stack.pop();

    if (visited.has(node)) continue;
    visited.add(node);
    result.push(node);

    // Push neighbors onto stack (reverse order for consistent traversal)
    const neighbors = graph[node] || [];
    for (let i = neighbors.length - 1; i >= 0; i--) {
      if (!visited.has(neighbors[i])) {
        stack.push(neighbors[i]);
      }
    }
  }

  return result;
}

console.log(dfsIterative(graph, 'A')); // ['A', 'B', 'D', 'C', 'E']
```

### BFS — Using Queue

```javascript
function bfs(graph, start) {
  const visited = new Set([start]);
  const queue = [start];
  const result = [];

  while (queue.length > 0) {
    const node = queue.shift();
    result.push(node);

    for (const neighbor of (graph[node] || [])) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }
  }

  return result;
}

console.log(bfs(graph, 'A')); // ['A', 'B', 'C', 'D', 'E']
```

---

## 🔍 Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| DFS | O(V + E) | O(V) |
| BFS | O(V + E) | O(V) |

Both visit every vertex and edge exactly once.

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Number of Islands

**Practice Links:** [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/find-the-number-of-islands/1)

**Problem Statement:** Given a 2D grid of `'1'` (land) and `'0'` (water), count the number of islands.

**Thought Process:** Each island is a connected component of `'1'`s. Use DFS/BFS from each unvisited `'1'` to mark the entire island.

#### 🐢 Brute Force — DFS

```javascript
function numIslandsDFS(grid) {
  if (!grid || grid.length === 0) return 0;

  const rows = grid.length;
  const cols = grid[0].length;
  let count = 0;

  function dfs(r, c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] === '0') return;

    grid[r][c] = '0'; // Mark as visited (sink the land)

    dfs(r + 1, c); // Down
    dfs(r - 1, c); // Up
    dfs(r, c + 1); // Right
    dfs(r, c - 1); // Left
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === '1') {
        count++;      // Found a new island
        dfs(r, c);    // Sink the entire island
      }
    }
  }

  return count;
}

console.log(numIslandsDFS([
  ['1','1','0','0','0'],
  ['1','1','0','0','0'],
  ['0','0','1','0','0'],
  ['0','0','0','1','1']
])); // 3
```

#### ⚡ Optimized — BFS

```javascript
function numIslandsBFS(grid) {
  if (!grid || grid.length === 0) return 0;

  const rows = grid.length, cols = grid[0].length;
  let count = 0;
  const dirs = [[0,1],[0,-1],[1,0],[-1,0]];

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === '1') {
        count++;
        const queue = [[r, c]];
        grid[r][c] = '0';

        while (queue.length > 0) {
          const [cr, cc] = queue.shift();
          for (const [dr, dc] of dirs) {
            const nr = cr + dr, nc = cc + dc;
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] === '1') {
              grid[nr][nc] = '0';
              queue.push([nr, nc]);
            }
          }
        }
      }
    }
  }

  return count;
}
```

**Simple Explanation:** Walk through the grid. When you find land ('1'), you've discovered an island — increment the count. Then explore the entire island using DFS or BFS, marking all visited land as water ('0') so you don't count it again.

**Complexity:** Time: O(m × n), Space: O(m × n) worst case

---

### Question 2: Shortest Path in Unweighted Graph (BFS)

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1)

**Problem Statement:** Find the shortest path from source to destination in an unweighted graph.

#### 🐢 Brute Force — DFS (finds a path, not necessarily shortest)

```javascript
function findPathDFS(graph, source, dest) {
  const visited = new Set();

  function dfs(node, path) {
    if (node === dest) return [...path, node];
    if (visited.has(node)) return null;

    visited.add(node);
    for (const neighbor of (graph[node] || [])) {
      const result = dfs(neighbor, [...path, node]);
      if (result) return result;
    }
    return null;
  }

  return dfs(source, []);
}
```

#### ⚡ Optimized — BFS (guarantees shortest path)

```javascript
function shortestPathBFS(graph, source, dest) {
  const visited = new Set([source]);
  const queue = [[source, [source]]]; // [node, path]

  while (queue.length > 0) {
    const [node, path] = queue.shift();

    if (node === dest) return path;

    for (const neighbor of (graph[node] || [])) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push([neighbor, [...path, neighbor]]);
      }
    }
  }

  return null; // No path exists
}

const g = {
  'A': ['B', 'C'],
  'B': ['A', 'D'],
  'C': ['A', 'D', 'E'],
  'D': ['B', 'C', 'E'],
  'E': ['C', 'D']
};

console.log(shortestPathBFS(g, 'A', 'E')); // ['A', 'C', 'E']
```

**Simple Explanation:** BFS explores level by level. Since each "level" adds one more edge, the first time BFS reaches the destination, it's guaranteed to be the shortest path. DFS might take a longer detour.

**Complexity:** Time: O(V + E), Space: O(V)

---

### Question 3: Detect Cycle in an Undirected Graph

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/detect-cycle-in-an-undirected-graph/1)

**Problem Statement:** Check if an undirected graph contains a cycle.

#### 🐢 Brute Force — DFS

```javascript
function hasCycleDFS(n, edges) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];
  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
  }

  const visited = new Set();

  function dfs(node, parent) {
    visited.add(node);

    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) {
        if (dfs(neighbor, node)) return true;
      } else if (neighbor !== parent) {
        return true; // Visited neighbor that isn't our parent → cycle!
      }
    }

    return false;
  }

  for (let i = 0; i < n; i++) {
    if (!visited.has(i)) {
      if (dfs(i, -1)) return true;
    }
  }

  return false;
}

console.log(hasCycleDFS(4, [[0,1],[1,2],[2,3]]));       // false
console.log(hasCycleDFS(4, [[0,1],[1,2],[2,3],[3,0]])); // true
```

#### ⚡ Optimized — BFS

```javascript
function hasCycleBFS(n, edges) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];
  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
  }

  const visited = new Set();

  for (let i = 0; i < n; i++) {
    if (visited.has(i)) continue;

    const queue = [[i, -1]]; // [node, parent]
    visited.add(i);

    while (queue.length > 0) {
      const [node, parent] = queue.shift();

      for (const neighbor of graph[node]) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push([neighbor, node]);
        } else if (neighbor !== parent) {
          return true; // Cycle detected!
        }
      }
    }
  }

  return false;
}
```

**Simple Explanation:** In DFS/BFS, if we encounter a visited node that isn't our immediate parent, we've found a different path to the same node — meaning there's a cycle. Like walking through a maze and finding your own footprints from a different direction.

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### Question 4: Detect Cycle in a Directed Graph

**Practice Links:** [GeeksforGeeks](https://www.geeksforgeeks.org/problems/detect-cycle-in-a-directed-graph/1)

```javascript
function hasCycleDirected(n, edges) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];
  for (const [u, v] of edges) graph[u].push(v);

  const WHITE = 0, GRAY = 1, BLACK = 2;
  const color = new Array(n).fill(WHITE);

  function dfs(node) {
    color[node] = GRAY; // Being processed

    for (const neighbor of graph[node]) {
      if (color[neighbor] === GRAY) return true;  // Back edge → cycle!
      if (color[neighbor] === WHITE && dfs(neighbor)) return true;
    }

    color[node] = BLACK; // Fully processed
    return false;
  }

  for (let i = 0; i < n; i++) {
    if (color[i] === WHITE && dfs(i)) return true;
  }

  return false;
}

console.log(hasCycleDirected(4, [[0,1],[1,2],[2,3]]));       // false
console.log(hasCycleDirected(4, [[0,1],[1,2],[2,0]]));       // true
```

**Simple Explanation:** Use three colors: WHITE (unvisited), GRAY (in current path), BLACK (done). If we visit a GRAY node, we've circled back to a node in our current exploration path — that's a cycle!

**Complexity:** Time: O(V + E), Space: O(V)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Flood Fill

**Practice Links:** [LeetCode #733](https://leetcode.com/problems/flood-fill/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/flood-fill-algorithm1856/1)

```javascript
function floodFill(image, sr, sc, color) {
  const original = image[sr][sc];
  if (original === color) return image; // Already the right color

  function dfs(r, c) {
    if (r < 0 || r >= image.length || c < 0 || c >= image[0].length) return;
    if (image[r][c] !== original) return;

    image[r][c] = color;
    dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1);
  }

  dfs(sr, sc);
  return image;
}

console.log(floodFill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2));
// [[2,2,2],[2,2,0],[2,0,1]]
```

**Explanation:** From the starting pixel, change its color and spread to all matching neighbors. Like the paint bucket tool in image editors.

**Complexity:** Time: O(m × n), Space: O(m × n)

---

### Problem 2: Course Schedule (Can Finish?)

**Practice Links:** [LeetCode #207](https://leetcode.com/problems/course-schedule/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/course-schedule/1) | [InterviewBit](https://www.interviewbit.com/problems/possibility-of-finishing-all-courses-given-prerequisites/)

```javascript
function canFinish(numCourses, prerequisites) {
  const graph = {};
  for (let i = 0; i < numCourses; i++) graph[i] = [];
  for (const [course, prereq] of prerequisites) {
    graph[prereq].push(course);
  }

  const WHITE = 0, GRAY = 1, BLACK = 2;
  const color = new Array(numCourses).fill(WHITE);

  function dfs(node) {
    color[node] = GRAY;
    for (const neighbor of graph[node]) {
      if (color[neighbor] === GRAY) return false;
      if (color[neighbor] === WHITE && !dfs(neighbor)) return false;
    }
    color[node] = BLACK;
    return true;
  }

  for (let i = 0; i < numCourses; i++) {
    if (color[i] === WHITE && !dfs(i)) return false;
  }
  return true;
}

console.log(canFinish(2, [[1,0]]));      // true
console.log(canFinish(2, [[1,0],[0,1]])); // false (cycle!)
```

**Explanation:** If there's a cycle in the prerequisite graph, you can never finish all courses (circular dependency). Use cycle detection for directed graphs.

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### Problem 3: Surrounded Regions

**Practice Links:** [LeetCode #130](https://leetcode.com/problems/surrounded-regions/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/surrounded-regions-1616126287/1)

```javascript
function solve(board) {
  const rows = board.length, cols = board[0].length;

  // DFS from border 'O's — mark them as safe
  function dfs(r, c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== 'O') return;
    board[r][c] = 'S'; // Safe — connected to border
    dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1);
  }

  // Mark border-connected O's as safe
  for (let r = 0; r < rows; r++) { dfs(r, 0); dfs(r, cols - 1); }
  for (let c = 0; c < cols; c++) { dfs(0, c); dfs(rows - 1, c); }

  // Flip: O → X (surrounded), S → O (safe)
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (board[r][c] === 'O') board[r][c] = 'X';
      else if (board[r][c] === 'S') board[r][c] = 'O';
    }
  }
}
```

**Explanation:** O's on the border can't be captured. Start DFS from border O's and mark them as safe. Everything else that's still 'O' is surrounded and gets flipped to 'X'.

**Complexity:** Time: O(m × n), Space: O(m × n)

---

### 🔗 Navigation
Prev: [18_Graphs_Basics.md](18_Graphs_Basics.md) | Index: [00_Index.md](00_Index.md) | Next: [20_Topological_Sort.md](20_Topological_Sort.md)
