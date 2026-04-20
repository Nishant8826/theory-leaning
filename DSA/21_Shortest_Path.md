# 📌 Shortest Path

## 🧠 Concept Explanation (Story Format)

Imagine you're using **Google Maps** to navigate from your home to the airport. There are many possible routes, each with different distances. You want the **shortest one**. That's the shortest path problem!

In graphs, the **shortest path** is the path between two nodes that minimizes the total edge weight (or number of edges in unweighted graphs).

### Algorithms Overview

| Algorithm | Graph Type | Handles Negative? | Time |
|-----------|-----------|-------------------|------|
| **BFS** | Unweighted | N/A | O(V + E) |
| **Dijkstra** | Weighted (non-negative) | ❌ No | O((V + E) log V) |
| **Bellman-Ford** | Weighted | ✅ Yes | O(V × E) |
| **Floyd-Warshall** | All pairs | ✅ Yes | O(V³) |

### Real-Life Analogy

- **BFS:** All roads are the same length — just count steps.
- **Dijkstra:** Roads have different lengths — always expand the shortest known route.
- **Bellman-Ford:** Some roads have "discounts" (negative weights) — keep relaxing.

---

## 🐢 Brute Force Approach

### BFS for Unweighted Shortest Path

```javascript
function shortestPathBFS(graph, source, destination) {
  const visited = new Set([source]);
  const queue = [[source, 0]]; // [node, distance]

  while (queue.length > 0) {
    const [node, dist] = queue.shift();

    if (node === destination) return dist;

    for (const neighbor of (graph[node] || [])) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push([neighbor, dist + 1]);
      }
    }
  }

  return -1; // No path
}

const graph = { 0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3] };
console.log(shortestPathBFS(graph, 0, 4)); // 3
```

---

## ⚡ Optimized Approach

### Dijkstra's Algorithm

```javascript
// Dijkstra's Algorithm using a simple priority queue
function dijkstra(graph, source, n) {
  const dist = new Array(n).fill(Infinity);
  dist[source] = 0;

  // Simple priority queue (array of [distance, node])
  const pq = [[0, source]];
  const visited = new Set();

  while (pq.length > 0) {
    // Get node with smallest distance
    pq.sort((a, b) => a[0] - b[0]);
    const [d, node] = pq.shift();

    if (visited.has(node)) continue;
    visited.add(node);

    for (const [neighbor, weight] of (graph[node] || [])) {
      const newDist = d + weight;
      if (newDist < dist[neighbor]) {
        dist[neighbor] = newDist;
        pq.push([newDist, neighbor]);
      }
    }
  }

  return dist;
}

// Weighted graph: node → [[neighbor, weight], ...]
const weightedGraph = {
  0: [[1, 4], [2, 1]],
  1: [[3, 1]],
  2: [[1, 2], [3, 5]],
  3: [[4, 3]],
  4: []
};

console.log(dijkstra(weightedGraph, 0, 5)); // [0, 3, 1, 4, 7]
```

### Bellman-Ford Algorithm

```javascript
function bellmanFord(n, edges, source) {
  const dist = new Array(n).fill(Infinity);
  dist[source] = 0;

  // Relax all edges V-1 times
  for (let i = 0; i < n - 1; i++) {
    for (const [u, v, w] of edges) {
      if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
      }
    }
  }

  // Check for negative cycles
  for (const [u, v, w] of edges) {
    if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
      return null; // Negative cycle detected!
    }
  }

  return dist;
}

const edges = [[0,1,4], [0,2,1], [2,1,2], [1,3,1], [2,3,5], [3,4,3]];
console.log(bellmanFord(5, edges, 0)); // [0, 3, 1, 4, 7]
```

---

## 🔍 Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V + E) | O(V) |
| Dijkstra (with min-heap) | O((V + E) log V) | O(V) |
| Bellman-Ford | O(V × E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Network Delay Time

**Problem Statement:** N nodes, given times as [u, v, w]. Find the time for all nodes to receive a signal from source.

#### 🐢 Brute Force — Bellman-Ford

```javascript
function networkDelayBellman(times, n, k) {
  const dist = new Array(n + 1).fill(Infinity);
  dist[k] = 0;

  for (let i = 0; i < n - 1; i++) {
    for (const [u, v, w] of times) {
      if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
      }
    }
  }

  const maxDist = Math.max(...dist.slice(1));
  return maxDist === Infinity ? -1 : maxDist;
}
```

#### ⚡ Optimized — Dijkstra

```javascript
function networkDelayDijkstra(times, n, k) {
  const graph = {};
  for (let i = 1; i <= n; i++) graph[i] = [];
  for (const [u, v, w] of times) graph[u].push([v, w]);

  const dist = new Array(n + 1).fill(Infinity);
  dist[k] = 0;
  const pq = [[0, k]];
  const visited = new Set();

  while (pq.length > 0) {
    pq.sort((a, b) => a[0] - b[0]);
    const [d, node] = pq.shift();

    if (visited.has(node)) continue;
    visited.add(node);

    for (const [neighbor, weight] of graph[node]) {
      const newDist = d + weight;
      if (newDist < dist[neighbor]) {
        dist[neighbor] = newDist;
        pq.push([newDist, neighbor]);
      }
    }
  }

  const maxDist = Math.max(...dist.slice(1));
  return maxDist === Infinity ? -1 : maxDist;
}

console.log(networkDelayDijkstra([[2,1,1],[2,3,1],[3,4,1]], 4, 2)); // 2
```

**Simple Explanation:** Run Dijkstra from the source. The answer is the maximum shortest distance among all nodes. If any node is unreachable (Infinity), return -1.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Bellman-Ford | O(V × E) | O(V) |
| Dijkstra | O((V + E) log V) | O(V + E) |

---

### Question 2: Cheapest Flights Within K Stops

**Problem Statement:** Find the cheapest price from source to destination with at most k stops.

#### ⚡ Optimized — Modified Bellman-Ford

```javascript
function findCheapestPrice(n, flights, src, dst, k) {
  let prices = new Array(n).fill(Infinity);
  prices[src] = 0;

  // K stops = K+1 edges at most
  for (let i = 0; i <= k; i++) {
    const temp = [...prices]; // Copy to avoid cascading updates

    for (const [from, to, price] of flights) {
      if (prices[from] !== Infinity && prices[from] + price < temp[to]) {
        temp[to] = prices[from] + price;
      }
    }

    prices = temp;
  }

  return prices[dst] === Infinity ? -1 : prices[dst];
}

console.log(findCheapestPrice(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1));
// 700 (0→1→3)
```

**Simple Explanation:** Modified Bellman-Ford that runs only k+1 iterations (for k stops). Each iteration allows one more edge. We use a copy of distances to prevent updating in a single round (ensures the stop limit).

**Complexity:** Time: O(k × E), Space: O(V)

---

### Question 3: Path With Minimum Effort

**Problem Statement:** In a grid, find a path from top-left to bottom-right minimizing the maximum height difference between consecutive cells.

#### ⚡ Optimized — Modified Dijkstra

```javascript
function minimumEffortPath(heights) {
  const rows = heights.length, cols = heights[0].length;
  const effort = Array.from({length: rows}, () => new Array(cols).fill(Infinity));
  effort[0][0] = 0;

  const pq = [[0, 0, 0]]; // [effort, row, col]
  const dirs = [[0,1],[0,-1],[1,0],[-1,0]];

  while (pq.length > 0) {
    pq.sort((a, b) => a[0] - b[0]);
    const [e, r, c] = pq.shift();

    if (r === rows - 1 && c === cols - 1) return e;
    if (e > effort[r][c]) continue;

    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
        const newEffort = Math.max(e, Math.abs(heights[nr][nc] - heights[r][c]));
        if (newEffort < effort[nr][nc]) {
          effort[nr][nc] = newEffort;
          pq.push([newEffort, nr, nc]);
        }
      }
    }
  }

  return 0;
}

console.log(minimumEffortPath([[1,2,2],[3,8,2],[5,3,5]])); // 2
```

**Simple Explanation:** Instead of minimizing total weight, minimize the MAXIMUM weight along the path. Use Dijkstra but instead of summing weights, take the max of the current effort and the new edge weight.

**Complexity:** Time: O(m × n × log(m × n)), Space: O(m × n)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Shortest Path in Binary Matrix

```javascript
function shortestPathBinaryMatrix(grid) {
  const n = grid.length;
  if (grid[0][0] === 1 || grid[n-1][n-1] === 1) return -1;

  const dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]];
  const queue = [[0, 0, 1]]; // [row, col, distance]
  grid[0][0] = 1; // Mark visited

  while (queue.length > 0) {
    const [r, c, dist] = queue.shift();
    if (r === n - 1 && c === n - 1) return dist;

    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] === 0) {
        grid[nr][nc] = 1;
        queue.push([nr, nc, dist + 1]);
      }
    }
  }

  return -1;
}

console.log(shortestPathBinaryMatrix([[0,1],[1,0]])); // 2
console.log(shortestPathBinaryMatrix([[0,0,0],[1,1,0],[1,1,0]])); // 4
```

**Explanation:** BFS on 8-directional grid. Each cell is either clear (0) or blocked (1). BFS guarantees shortest path.

**Complexity:** Time: O(n²), Space: O(n²)

---

### Problem 2: Floyd-Warshall (All Pairs Shortest Path)

```javascript
function floydWarshall(n, edges) {
  const dist = Array.from({length: n}, () => new Array(n).fill(Infinity));

  // Self-distance is 0
  for (let i = 0; i < n; i++) dist[i][i] = 0;

  // Initialize direct edges
  for (const [u, v, w] of edges) {
    dist[u][v] = w;
  }

  // Try every vertex as intermediate
  for (let k = 0; k < n; k++) {
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (dist[i][k] + dist[k][j] < dist[i][j]) {
          dist[i][j] = dist[i][k] + dist[k][j];
        }
      }
    }
  }

  return dist;
}

const result = floydWarshall(4, [[0,1,3],[0,3,7],[1,2,2],[2,3,1]]);
console.log(result[0][3]); // 6 (0→1→2→3)
```

**Explanation:** Try every node as a "middle point." For each pair (i, j), check if going through k is shorter. Like asking for every pair of cities: "Is it faster to go through city k?"

**Complexity:** Time: O(V³), Space: O(V²)

---

### 🔗 Navigation
Prev: [20_Topological_Sort.md](20_Topological_Sort.md) | Index: [00_Index.md](00_Index.md) | Next: [22_Minimum_Spanning_Tree.md](22_Minimum_Spanning_Tree.md)
