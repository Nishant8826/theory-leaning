# 📌 Graphs — Basics

## 🧠 Concept Explanation (Story Format)

Imagine a **social network** like Facebook. Each person is a dot (node), and each friendship is a line (edge) connecting two dots. Some friendships are one-way (like Twitter follows) and some are two-way (like Facebook friends). This network of connections is a **Graph**.

A **graph** is a collection of **nodes (vertices)** connected by **edges**. Unlike trees, graphs can have cycles, multiple paths between nodes, and nodes with any number of connections.

### Key Terms

| Term | Meaning |
|------|---------|
| **Vertex/Node** | A point in the graph |
| **Edge** | A connection between two nodes |
| **Directed** | Edges have a direction (A → B) |
| **Undirected** | Edges go both ways (A — B) |
| **Weighted** | Edges have values (distances, costs) |
| **Degree** | Number of edges connected to a node |
| **Path** | A sequence of edges from one node to another |
| **Cycle** | A path that starts and ends at the same node |
| **Connected** | Every node can reach every other node |

### Types of Graphs

```
Undirected:          Directed:           Weighted:
A --- B              A → B               A --5-- B
|     |              ↑   ↓               |       |
C --- D              C ← D               3       2
                                         |       |
                                         C --4-- D
```

### Graph Representations

#### 1. Adjacency List (Most Common)

```javascript
// Using Map of arrays
const graph = {
  'A': ['B', 'C'],
  'B': ['A', 'D'],
  'C': ['A', 'D'],
  'D': ['B', 'C']
};
```

#### 2. Adjacency Matrix

```javascript
// 0 = no edge, 1 = edge exists
//     A  B  C  D
// A [ 0, 1, 1, 0 ]
// B [ 1, 0, 0, 1 ]
// C [ 1, 0, 0, 1 ]
// D [ 0, 1, 1, 0 ]
const matrix = [
  [0, 1, 1, 0],
  [1, 0, 0, 1],
  [1, 0, 0, 1],
  [0, 1, 1, 0]
];
```

### Adjacency List vs Matrix

| Feature | Adjacency List | Adjacency Matrix |
|---------|---------------|-----------------|
| Space | O(V + E) | O(V²) |
| Check if edge exists | O(degree) | O(1) |
| Get all neighbors | O(degree) | O(V) |
| Best for | Sparse graphs | Dense graphs |

### Real-Life Examples

- **Google Maps:** Cities = nodes, roads = edges, distances = weights
- **Social Networks:** People = nodes, connections = edges
- **Internet:** Web pages = nodes, hyperlinks = edges
- **Dependencies:** Tasks = nodes, dependencies = edges

---

## 🐢 Brute Force Approach

### Building a Graph from Edges

```javascript
// Build adjacency list from edge list
function buildGraph(edges, directed = false) {
  const graph = {};

  for (const [src, dest] of edges) {
    if (!graph[src]) graph[src] = [];
    if (!graph[dest]) graph[dest] = [];

    graph[src].push(dest);
    if (!directed) {
      graph[dest].push(src); // Add reverse edge for undirected
    }
  }

  return graph;
}

const edges = [['A','B'], ['A','C'], ['B','D'], ['C','D']];
const graph = buildGraph(edges);
console.log(graph);
// { A: ['B','C'], B: ['A','D'], C: ['A','D'], D: ['B','C'] }
```

---

## ⚡ Optimized Approach

### Graph Class with Weighted Edges

```javascript
class Graph {
  constructor(directed = false) {
    this.adjacencyList = new Map();
    this.directed = directed;
  }

  addVertex(vertex) {
    if (!this.adjacencyList.has(vertex)) {
      this.adjacencyList.set(vertex, []);
    }
  }

  addEdge(src, dest, weight = 1) {
    this.addVertex(src);
    this.addVertex(dest);

    this.adjacencyList.get(src).push({ node: dest, weight });
    if (!this.directed) {
      this.adjacencyList.get(dest).push({ node: src, weight });
    }
  }

  getNeighbors(vertex) {
    return this.adjacencyList.get(vertex) || [];
  }

  getAllVertices() {
    return [...this.adjacencyList.keys()];
  }

  print() {
    for (const [vertex, neighbors] of this.adjacencyList) {
      const edges = neighbors.map(n => `${n.node}(${n.weight})`).join(', ');
      console.log(`${vertex} → ${edges}`);
    }
  }
}

const g = new Graph();
g.addEdge('A', 'B', 5);
g.addEdge('A', 'C', 3);
g.addEdge('B', 'D', 2);
g.addEdge('C', 'D', 4);
g.print();
// A → B(5), C(3)
// B → A(5), D(2)
// C → A(3), D(4)
// D → B(2), C(4)
```

---

## 🔍 Complexity Analysis

| Operation | Adjacency List | Adjacency Matrix |
|-----------|---------------|-----------------|
| Add vertex | O(1) | O(V²) — resize |
| Add edge | O(1) | O(1) |
| Check edge | O(V) | O(1) |
| Get neighbors | O(1) | O(V) |
| Space | O(V + E) | O(V²) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Find if Path Exists (Graph Connectivity)

**Practice Links:** [LeetCode #1971](https://leetcode.com/problems/find-if-path-exists-in-graph/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/find-if-path-exists-in-graph/1)

**Problem Statement:** Given n nodes and edges, check if there's a path between source and destination.


#### Code Story
- This problem is about finding if there is any way to travel from node A to node B.
- First, we pick a traversal strategy like BFS (layer by layer) or DFS (as far as possible).
- Then, we explore outward from A, marking nodes as 'visited' so we don't wander in circles.
- Finally, if our exploration ever hits node B, a path exists.
- This works because systematically checking reachable nodes will eventually reveal if the destination is part of the same network.

#### 🐢 Brute Force — DFS

```javascript
function hasPathDFS(n, edges, source, destination) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];

  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
  }

  const visited = new Set();

  function dfs(node) {
    if (node === destination) return true;
    if (visited.has(node)) return false;

    visited.add(node);
    for (const neighbor of graph[node]) {
      if (dfs(neighbor)) return true;
    }
    return false;
  }

  return dfs(source);
}

console.log(hasPathDFS(6, [[0,1],[0,2],[3,5],[5,4],[4,3]], 0, 5)); // false
console.log(hasPathDFS(3, [[0,1],[1,2],[2,0]], 0, 2)); // true
```

#### ⚡ Optimized — BFS

```javascript
function hasPathBFS(n, edges, source, destination) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];

  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
  }

  const visited = new Set([source]);
  const queue = [source];

  while (queue.length > 0) {
    const node = queue.shift();
    if (node === destination) return true;

    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }
  }

  return false;
}
```

**Simple Explanation:** Build the graph, then walk from the source using either DFS (going deep) or BFS (going wide). If we reach the destination, a path exists.

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### Question 2: Number of Connected Components

**Practice Links:** [LeetCode #323](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/number-of-provinces/1)

**Problem Statement:** Count the number of connected components in an undirected graph.

#### 🐢 Brute Force — DFS from Every Unvisited Node

```javascript
function countComponents(n, edges) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];

  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
  }

  const visited = new Set();
  let components = 0;

  function dfs(node) {
    visited.add(node);
    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) dfs(neighbor);
    }
  }

  for (let i = 0; i < n; i++) {
    if (!visited.has(i)) {
      dfs(i);       // Explore entire component
      components++; // Found a new component
    }
  }

  return components;
}

console.log(countComponents(5, [[0,1],[1,2],[3,4]])); // 2
console.log(countComponents(5, [[0,1],[1,2],[2,3],[3,4]])); // 1
```

**Simple Explanation:** Each time you find an unvisited node, you've discovered a new "island" (component). DFS explores the entire island, marking all its nodes as visited.

**Complexity:** Time: O(V + E), Space: O(V + E)

---

### Question 3: Clone a Graph

**Practice Links:** [LeetCode #133](https://leetcode.com/problems/clone-graph/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/clone-graph/1)

**Problem Statement:** Given a reference to a node in a connected undirected graph, return a deep copy.

#### ⚡ Optimized — BFS with Hash Map

```javascript
function cloneGraph(node) {
  if (!node) return null;

  const visited = new Map(); // Original node → Cloned node
  const queue = [node];

  // Create clone of first node
  visited.set(node, { val: node.val, neighbors: [] });

  while (queue.length > 0) {
    const current = queue.shift();

    for (const neighbor of current.neighbors) {
      if (!visited.has(neighbor)) {
        // Create clone of neighbor
        visited.set(neighbor, { val: neighbor.val, neighbors: [] });
        queue.push(neighbor);
      }
      // Connect cloned current to cloned neighbor
      visited.get(current).neighbors.push(visited.get(neighbor));
    }
  }

  return visited.get(node);
}
```

**Simple Explanation:** BFS through the original graph. For each node, create a clone and store the mapping (original → clone). When connecting edges, use the cloned versions. Like photocopying a map — create copies of each city and redraw the roads.

**Complexity:** Time: O(V + E), Space: O(V)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Find the Town Judge

**Practice Links:** [LeetCode #997](https://leetcode.com/problems/find-the-town-judge/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/town-judge/1)

**Problem Statement:** In a town of n people, the judge trusts nobody but everyone trusts the judge. Find the judge.

```javascript
function findJudge(n, trust) {
  const trustCount = new Array(n + 1).fill(0);

  for (const [a, b] of trust) {
    trustCount[a]--; // a trusts someone (not judge behavior)
    trustCount[b]++; // b is trusted by someone
  }

  for (let i = 1; i <= n; i++) {
    if (trustCount[i] === n - 1) return i; // Trusted by all others, trusts no one
  }

  return -1;
}

console.log(findJudge(3, [[1,3],[2,3]]));       // 3
console.log(findJudge(3, [[1,3],[2,3],[3,1]])); // -1
```

**Explanation:** The judge has in-degree n-1 (everyone trusts them) and out-degree 0 (they trust no one). Net trust = n-1.

**Complexity:** Time: O(E), Space: O(V)

---

### Problem 2: Check if Graph is Bipartite

**Practice Links:** [LeetCode #785](https://leetcode.com/problems/is-graph-bipartite/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/bipartite-graph/1)

```javascript
function isBipartite(graph) {
  const n = graph.length;
  const color = new Array(n).fill(-1); // -1 = uncolored

  for (let start = 0; start < n; start++) {
    if (color[start] !== -1) continue;

    const queue = [start];
    color[start] = 0;

    while (queue.length > 0) {
      const node = queue.shift();

      for (const neighbor of graph[node]) {
        if (color[neighbor] === -1) {
          color[neighbor] = 1 - color[node]; // Opposite color
          queue.push(neighbor);
        } else if (color[neighbor] === color[node]) {
          return false; // Same color = not bipartite
        }
      }
    }
  }

  return true;
}

console.log(isBipartite([[1,3],[0,2],[1,3],[0,2]])); // true
console.log(isBipartite([[1,2,3],[0,2],[0,1,3],[0,2]])); // false
```

**Explanation:** Try to 2-color the graph. If you can color it so no two adjacent nodes have the same color, it's bipartite. BFS and alternate colors. If a neighbor already has the same color, it fails.

**Complexity:** Time: O(V + E), Space: O(V)

---

### Problem 3: Find All Paths from Source to Target (DAG)

**Practice Links:** [LeetCode #797](https://leetcode.com/problems/all-paths-from-source-to-target/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/all-paths-from-source-to-target/1)

**Problem Statement:** Find all possible paths from node 0 to node n-1.

```javascript
function allPaths(graph) {
  const result = [];
  const target = graph.length - 1;

  function dfs(node, path) {
    path.push(node);

    if (node === target) {
      result.push([...path]);
    } else {
      for (const neighbor of graph[node]) {
        dfs(neighbor, path);
      }
    }

    path.pop(); // Backtrack
  }

  dfs(0, []);
  return result;
}

console.log(allPaths([[1,2],[3],[3],[]]));
// [[0,1,3], [0,2,3]]
```

**Explanation:** DFS from node 0 to the last node. Track the current path. When we reach the target, save the path. Backtrack to explore other routes.

**Complexity:** Time: O(2^V × V), Space: O(V)

---

### 🔗 Navigation
Prev: [17_Trie.md](17_Trie.md) | Index: [00_Index.md](00_Index.md) | Next: [19_Graphs_Traversal.md](19_Graphs_Traversal.md)
