# 📌 Minimum Spanning Tree

## 🧠 Concept Explanation (Story Format)

Imagine you're a **city planner** connecting 10 villages with roads. Building roads costs money (edge weights). You want to connect ALL villages using the **minimum total cost**. You don't need every possible road — just enough to connect everyone.

A **Minimum Spanning Tree (MST)** is a subset of edges that connects all vertices with the minimum total edge weight, without any cycles.

### Key Properties

- Connects **all V vertices** using exactly **V-1 edges**
- **No cycles** (it's a tree)
- **Minimum total weight** among all possible spanning trees

### Two Main Algorithms

| Algorithm | Approach | Best For |
|-----------|----------|----------|
| **Kruskal's** | Sort edges, add cheapest non-cycle edge | Sparse graphs |
| **Prim's** | Grow tree from a starting node | Dense graphs |

### Real-Life Analogy

Think of laying **internet cables** between buildings. You want to connect all buildings using the least amount of cable. You don't need redundant connections — just one connected network with minimum total cable length.

---

## 🐢 Brute Force Approach

### Kruskal's Algorithm (Sort Edges + Union-Find)

```javascript
// Simple Union-Find for Kruskal's
class UnionFind {
  constructor(n) {
    this.parent = Array.from({length: n}, (_, i) => i);
    this.rank = new Array(n).fill(0);
  }

  find(x) {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]); // Path compression
    }
    return this.parent[x];
  }

  union(x, y) {
    const px = this.find(x), py = this.find(y);
    if (px === py) return false; // Already connected

    // Union by rank
    if (this.rank[px] < this.rank[py]) this.parent[px] = py;
    else if (this.rank[px] > this.rank[py]) this.parent[py] = px;
    else { this.parent[py] = px; this.rank[px]++; }

    return true;
  }
}

function kruskalMST(n, edges) {
  // Sort edges by weight
  edges.sort((a, b) => a[2] - b[2]);

  const uf = new UnionFind(n);
  const mst = [];
  let totalWeight = 0;

  for (const [u, v, w] of edges) {
    if (uf.union(u, v)) {
      mst.push([u, v, w]);
      totalWeight += w;

      if (mst.length === n - 1) break; // MST complete
    }
  }

  return { mst, totalWeight };
}

const edges = [[0,1,4],[0,7,8],[1,2,8],[1,7,11],[2,3,7],[2,8,2],[2,5,4],[3,4,9],[3,5,14],[4,5,10],[5,6,2],[6,7,1],[6,8,6],[7,8,7]];
const result = kruskalMST(9, edges);
console.log(result.totalWeight); // 37
console.log(result.mst);
```


#### Code Story
- This problem is about connecting every city with the least amount of road, without making any circular loops.
- First, we sort every possible road by its cost, from cheapest to most expensive.
- Then, we pick the cheapest road and add it—but only if it doesn't create a circle with the roads we already have.
- Finally, we repeat this until all cities are part of the same network.
- This works because always picking the absolute cheapest road that contributes to a new connection will eventually lead to the overall cheapest total.

### Line-by-Line Explanation

1. **Sort all edges** by weight (cheapest first).
2. **For each edge**, check if adding it creates a cycle (Union-Find).
3. If no cycle, **add it to MST**.
4. Stop when we have V-1 edges.

---

## ⚡ Optimized Approach

### Prim's Algorithm

```javascript
function primMST(n, adjList) {
  const inMST = new Array(n).fill(false);
  const key = new Array(n).fill(Infinity); // Minimum edge weight to reach node
  key[0] = 0;

  const parent = new Array(n).fill(-1);
  let totalWeight = 0;

  for (let count = 0; count < n; count++) {
    // Find minimum key vertex not in MST (simple approach)
    let minKey = Infinity, u = -1;
    for (let v = 0; v < n; v++) {
      if (!inMST[v] && key[v] < minKey) {
        minKey = key[v];
        u = v;
      }
    }

    inMST[u] = true;
    totalWeight += minKey;

    // Update keys for neighbors
    for (const [v, weight] of (adjList[u] || [])) {
      if (!inMST[v] && weight < key[v]) {
        key[v] = weight;
        parent[v] = u;
      }
    }
  }

  return { totalWeight, parent };
}

const adjList = {
  0: [[1,4],[7,8]], 1: [[0,4],[2,8],[7,11]],
  2: [[1,8],[3,7],[5,4],[8,2]], 3: [[2,7],[4,9],[5,14]],
  4: [[3,9],[5,10]], 5: [[2,4],[3,14],[4,10],[6,2]],
  6: [[5,2],[7,1],[8,6]], 7: [[0,8],[1,11],[6,1],[8,7]],
  8: [[2,2],[6,6],[7,7]]
};

console.log(primMST(9, adjList).totalWeight); // 37
```


#### Code Story
- This problem is about growing a forest of connections from a single starting point.
- First, we pick a starting city and look at all the roads connecting to its neighbors.
- Then, we use a Min-Heap to pick the cheapest road available to reach a new city.
- Finally, we add that city to our 'connected' group and repeat until everyone is in.
- This works because starting from one spot and always taking the 'closest unvisited neighbor' slowly and correctly builds the cheapest network.

---

## 🔍 Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| Kruskal's | O(E log E) | O(V + E) |
| Prim's (array) | O(V²) | O(V) |
| Prim's (heap) | O((V + E) log V) | O(V + E) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Min Cost to Connect All Points

**Practice Links:** [LeetCode #1584](https://leetcode.com/problems/min-cost-to-connect-all-points/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1)

**Problem Statement:** Given n points, find the minimum cost to connect all points (cost = Manhattan distance).


#### Code Story
- This problem is about finding the least total distance to connect a set of coordinates on a flat map.
- First, we calculate the 'Manhattan distance' (street distance) between every pair of points.
- Then, we treat those distances as roads in a graph and apply Prim's or Kruskal's.
- Finally, we return the total length of the 'skeleton' that connects every point.
- This works because it reduces a geometry problem into a graph problem that can be solved with standard Minimum Spanning Tree tools.

#### 🐢 Brute Force — Generate All Edges + Kruskal's

```javascript
function minCostConnectPoints(points) {
  const n = points.length;
  const edges = [];

  // Generate all edges with Manhattan distances
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const dist = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
      edges.push([i, j, dist]);
    }
  }

  // Kruskal's
  edges.sort((a, b) => a[2] - b[2]);
  const uf = new UnionFind(n);
  let totalCost = 0;
  let edgesUsed = 0;

  for (const [u, v, w] of edges) {
    if (uf.union(u, v)) {
      totalCost += w;
      edgesUsed++;
      if (edgesUsed === n - 1) break;
    }
  }

  return totalCost;
}

console.log(minCostConnectPoints([[0,0],[2,2],[3,10],[5,2],[7,0]])); // 20
```

#### ⚡ Optimized — Prim's

```javascript
function minCostPrims(points) {
  const n = points.length;
  const inMST = new Array(n).fill(false);
  const minDist = new Array(n).fill(Infinity);
  minDist[0] = 0;

  let totalCost = 0;

  for (let count = 0; count < n; count++) {
    let u = -1, minVal = Infinity;
    for (let v = 0; v < n; v++) {
      if (!inMST[v] && minDist[v] < minVal) {
        minVal = minDist[v];
        u = v;
      }
    }

    inMST[u] = true;
    totalCost += minVal;

    for (let v = 0; v < n; v++) {
      if (!inMST[v]) {
        const dist = Math.abs(points[u][0] - points[v][0]) + Math.abs(points[u][1] - points[v][1]);
        minDist[v] = Math.min(minDist[v], dist);
      }
    }
  }

  return totalCost;
}

console.log(minCostPrims([[0,0],[2,2],[3,10],[5,2],[7,0]])); // 20
```

**Simple Explanation:** Every pair of points can be connected. The cost is the Manhattan distance. Find the MST — the cheapest way to connect all points. Prim's is efficient here because the graph is dense (every point connects to every other).

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Kruskal's | O(n² log n) | O(n²) |
| Prim's | O(n²) | O(n) |

---

### Question 2: Connecting Cities with Minimum Cost

**Practice Links:** [LeetCode #1135](https://leetcode.com/problems/connecting-cities-with-minimum-cost/) | [GeeksforGeeks](https://www.geeksforgeeks.org/problems/minimum-cost-to-connect-all-cities/1)

```javascript
function minimumCost(n, connections) {
  connections.sort((a, b) => a[2] - b[2]);
  const uf = new UnionFind(n + 1); // 1-indexed

  let totalCost = 0;
  let edgesUsed = 0;

  for (const [u, v, cost] of connections) {
    if (uf.union(u, v)) {
      totalCost += cost;
      edgesUsed++;
      if (edgesUsed === n - 1) return totalCost;
    }
  }

  return edgesUsed === n - 1 ? totalCost : -1; // -1 if not fully connected
}

console.log(minimumCost(3, [[1,2,5],[1,3,6],[2,3,1]])); // 6
```

**Explanation:** Classic MST. Sort edges by cost, greedily add cheapest non-cycle edges using Union-Find.

**Complexity:** Time: O(E log E), Space: O(V)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Check if MST is Unique

```javascript
function isMSTUnique(n, edges) {
  edges.sort((a, b) => a[2] - b[2]);

  // Find MST weight
  const uf1 = new UnionFind(n);
  let mstWeight = 0;

  for (const [u, v, w] of edges) {
    if (uf1.union(u, v)) mstWeight += w;
  }

  // Try removing each MST edge and see if same weight MST exists
  for (let skip = 0; skip < edges.length; skip++) {
    const uf2 = new UnionFind(n);
    let weight = 0;
    let edgeCount = 0;

    for (let i = 0; i < edges.length; i++) {
      if (i === skip) continue;
      const [u, v, w] = edges[i];
      if (uf2.union(u, v)) {
        weight += w;
        edgeCount++;
      }
    }

    if (edgeCount === n - 1 && weight === mstWeight) {
      return false; // Another MST exists with same weight
    }
  }

  return true; // MST is unique
}
```

**Explanation:** Find the MST weight. Then try skipping each edge and rebuild. If you can build a spanning tree with the same total weight, the MST is not unique.

**Complexity:** Time: O(E² × α(V)), Space: O(V)

---

### Problem 2: Critical and Pseudo-Critical Edges in MST

**Practice Links:** [LeetCode #1489](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)

```javascript
function findCriticalAndPseudo(n, edges) {
  // Add index to edges for tracking
  const indexed = edges.map((e, i) => [...e, i]);
  indexed.sort((a, b) => a[2] - b[2]);

  function getMSTWeight(n, edges, include, exclude) {
    const uf = new UnionFind(n);
    let weight = 0;

    if (include !== -1) {
      const [u, v, w] = edges[include];
      uf.union(u, v);
      weight += w;
    }

    for (let i = 0; i < edges.length; i++) {
      if (i === exclude) continue;
      const [u, v, w] = edges[i];
      if (uf.union(u, v)) weight += w;
    }

    // Check if all connected
    let root = uf.find(0);
    for (let i = 1; i < n; i++) {
      if (uf.find(i) !== root) return Infinity;
    }
    return weight;
  }

  const mstWeight = getMSTWeight(n, indexed, -1, -1);
  const critical = [], pseudo = [];

  for (let i = 0; i < indexed.length; i++) {
    // Critical: removing it increases MST weight
    if (getMSTWeight(n, indexed, -1, i) > mstWeight) {
      critical.push(indexed[i][3]);
    }
    // Pseudo: including it doesn't increase weight (but it's not critical)
    else if (getMSTWeight(n, indexed, i, -1) === mstWeight) {
      pseudo.push(indexed[i][3]);
    }
  }

  return [critical, pseudo];
}
```

**Explanation:** A critical edge, when removed, increases MST weight. A pseudo-critical edge can be in SOME MST but not all. Test by removing/including each edge.

**Complexity:** Time: O(E² × α(V)), Space: O(V)

---

### 🔗 Navigation
Prev: [21_Shortest_Path.md](21_Shortest_Path.md) | Index: [00_Index.md](00_Index.md) | Next: [23_Greedy.md](23_Greedy.md)
