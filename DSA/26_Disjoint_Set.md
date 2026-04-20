# 📌 Disjoint Set (Union-Find)

## 🧠 Concept Explanation (Story Format)

Imagine a **school** where students form friend groups. Initially, everyone is their own group. When two students become friends, their groups merge. You want to quickly answer: "Are Alice and Bob in the same group?" and "Merge Alice's group with Bob's group."

That's **Disjoint Set (Union-Find)** — a data structure that efficiently tracks which elements belong to which groups and can merge groups together.

### Two Key Operations

| Operation | What It Does | Time |
|-----------|-------------|------|
| **Find(x)** | Find which group x belongs to (its root/leader) | O(α(n)) ≈ O(1) |
| **Union(x, y)** | Merge the groups of x and y | O(α(n)) ≈ O(1) |

α(n) is the **inverse Ackermann function** — practically constant (≤ 4 for any realistic input).

### Two Optimizations

1. **Path Compression** (in Find): When finding the root, make every node point directly to the root. Like telling everyone "your leader is the CEO, not your manager."

2. **Union by Rank/Size** (in Union): When merging, attach the smaller tree under the larger tree. Like smaller companies being acquired by larger ones.

### Where Union-Find is Used

- **Connected components** in a graph
- **Kruskal's MST** algorithm (check for cycles)
- **Network connectivity** (are two computers connected?)
- **Image processing** (connected regions)
- **Social networks** (friend groups)

### Real-Life Analogy

Think of **political alliances**. Each country starts independent. When two countries form an alliance, their groups merge. To check if two countries are allied, find the "leader" of each group — if they share a leader, they're in the same alliance.

---

## 🐢 Brute Force Approach

### Simple Union-Find (No Optimization)

```javascript
class UnionFindBrute {
  constructor(n) {
    this.parent = Array.from({length: n}, (_, i) => i); // Each is its own parent
  }

  find(x) {
    while (this.parent[x] !== x) {
      x = this.parent[x]; // Walk up to root
    }
    return x;
  }

  union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);
    if (rootX !== rootY) {
      this.parent[rootX] = rootY; // Just attach one root to the other
    }
  }

  connected(x, y) {
    return this.find(x) === this.find(y);
  }
}

const uf = new UnionFindBrute(5);
uf.union(0, 1);
uf.union(2, 3);
console.log(uf.connected(0, 1)); // true
console.log(uf.connected(0, 2)); // false
uf.union(1, 3);
console.log(uf.connected(0, 2)); // true
```

### Problem: Without optimization, `find` can be O(n) in the worst case (tall tree).

---

## ⚡ Optimized Approach

### Union-Find with Path Compression + Union by Rank

```javascript
class UnionFind {
  constructor(n) {
    this.parent = Array.from({length: n}, (_, i) => i);
    this.rank = new Array(n).fill(0);
    this.count = n; // Number of connected components
  }

  find(x) {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]); // Path compression
    }
    return this.parent[x];
  }

  union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === rootY) return false; // Already connected

    // Union by rank — attach smaller tree under larger
    if (this.rank[rootX] < this.rank[rootY]) {
      this.parent[rootX] = rootY;
    } else if (this.rank[rootX] > this.rank[rootY]) {
      this.parent[rootY] = rootX;
    } else {
      this.parent[rootY] = rootX;
      this.rank[rootX]++;
    }

    this.count--; // One fewer component
    return true;
  }

  connected(x, y) {
    return this.find(x) === this.find(y);
  }

  getCount() {
    return this.count;
  }
}

const uf = new UnionFind(5);
uf.union(0, 1);
uf.union(2, 3);
uf.union(1, 3);
console.log(uf.connected(0, 2)); // true
console.log(uf.getCount());       // 2 (groups: {0,1,2,3} and {4})
```


#### Code Story
- This problem is about making Union-Find incredibly fast by keeping the trees short and flat.
- First, 'Path Compression' means whenever we find a leader, we point all nodes directly to that leader, shortening the path for next time.
- Then, 'Union by Rank' means we always attach the smaller tree to the taller one, preventing the structure from becoming too deep.
- Finally, these two tricks together make the whole process nearly instantaneous, even for millions of nodes.
- This works because flatter trees mean fewer 'jumps' to find the leader, which is the most common action we perform.

---

## 🔍 Complexity Analysis

| Operation | Without Optimization | With Optimization |
|-----------|---------------------|-------------------|
| Find | O(n) worst case | O(α(n)) ≈ O(1) |
| Union | O(n) worst case | O(α(n)) ≈ O(1) |
| Space | O(n) | O(n) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Number of Connected Components

**Problem Statement:** Given n nodes and edges, find the number of connected components.

#### 🐢 Brute Force — DFS

```javascript
function countComponentsDFS(n, edges) {
  const graph = {};
  for (let i = 0; i < n; i++) graph[i] = [];
  for (const [u, v] of edges) {
    graph[u].push(v);
    graph[v].push(u);
  }

  const visited = new Set();
  let count = 0;

  function dfs(node) {
    visited.add(node);
    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) dfs(neighbor);
    }
  }

  for (let i = 0; i < n; i++) {
    if (!visited.has(i)) {
      dfs(i);
      count++;
    }
  }

  return count;
}
```

#### ⚡ Optimized — Union-Find

```javascript
function countComponentsUF(n, edges) {
  const uf = new UnionFind(n);

  for (const [u, v] of edges) {
    uf.union(u, v);
  }

  return uf.getCount();
}

console.log(countComponentsUF(5, [[0,1],[1,2],[3,4]])); // 2
console.log(countComponentsUF(5, [[0,1],[1,2],[2,3],[3,4]])); // 1
```

**Simple Explanation:** Start with n components. Each union operation merges two components (reducing count by 1). After processing all edges, the remaining count is the number of connected components.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V + E) |
| Union-Find | O(E × α(V)) ≈ O(E) | O(V) |

---

### Question 2: Redundant Connection

**Problem Statement:** Find the edge that, when removed, makes the graph a tree (no cycles). Return the last such edge.


#### Code Story
- This problem is about finding exactly which edge in a network creates a circular loop.
- First, we take the edges one by one and try to 'Union' the two nodes they connect.
- Then, if we find that the two nodes already share the same leader before we even add the edge, we have a cycle!
- Finally, that edge is the one that created the loop, so we return it.
- This works because in a simple tree, every edge must connect two different groups; if it connects nodes in the same group, it's a loop.

#### ⚡ Optimized — Union-Find

```javascript
function findRedundantConnection(edges) {
  const n = edges.length;
  const uf = new UnionFind(n + 1); // 1-indexed

  for (const [u, v] of edges) {
    if (!uf.union(u, v)) {
      return [u, v]; // This edge creates a cycle!
    }
  }

  return [];
}

console.log(findRedundantConnection([[1,2],[1,3],[2,3]])); // [2, 3]
console.log(findRedundantConnection([[1,2],[2,3],[3,4],[1,4],[1,5]])); // [1, 4]
```

**Simple Explanation:** Process edges one by one. If both endpoints are already in the same group (connected), adding this edge creates a cycle. That's the redundant connection!

**Complexity:** Time: O(n × α(n)) ≈ O(n), Space: O(n)

---

### Question 3: Accounts Merge

**Problem Statement:** Given accounts (name + emails), merge accounts belonging to the same person. Two accounts are the same person if they share at least one email.

#### ⚡ Optimized — Union-Find

```javascript
function accountsMerge(accounts) {
  const emailToId = new Map();  // email → account index
  const emailToName = new Map(); // email → name
  const uf = new UnionFind(accounts.length);

  // Map each email to its account index
  for (let i = 0; i < accounts.length; i++) {
    const name = accounts[i][0];
    for (let j = 1; j < accounts[i].length; j++) {
      const email = accounts[i][j];
      emailToName.set(email, name);

      if (emailToId.has(email)) {
        uf.union(i, emailToId.get(email)); // Same email → same person
      } else {
        emailToId.set(email, i);
      }
    }
  }

  // Group emails by root
  const groups = {};
  for (const [email, id] of emailToId) {
    const root = uf.find(id);
    if (!groups[root]) groups[root] = [];
    groups[root].push(email);
  }

  // Build result
  return Object.values(groups).map(emails => {
    emails.sort();
    return [emailToName.get(emails[0]), ...emails];
  });
}

console.log(accountsMerge([
  ["John", "john@mail.com", "john_newyork@mail.com"],
  ["John", "john@mail.com", "john00@mail.com"],
  ["Mary", "mary@mail.com"],
  ["John", "johnnybravo@mail.com"]
]));
```

**Simple Explanation:** Two accounts belong to the same person if they share an email. Use Union-Find: when the same email appears in two accounts, merge them. Then group all emails by their root account.

**Complexity:** Time: O(n × α(n) × k log k) where k = emails per account, Space: O(n × k)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Number of Islands (Union-Find Approach)

```javascript
function numIslandsUF(grid) {
  const rows = grid.length, cols = grid[0].length;
  const uf = new UnionFind(rows * cols);
  let waterCount = 0;

  const getIndex = (r, c) => r * cols + c;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === '0') {
        waterCount++;
        continue;
      }
      // Union with right and bottom neighbors
      if (r + 1 < rows && grid[r + 1][c] === '1') {
        uf.union(getIndex(r, c), getIndex(r + 1, c));
      }
      if (c + 1 < cols && grid[r][c + 1] === '1') {
        uf.union(getIndex(r, c), getIndex(r, c + 1));
      }
    }
  }

  return uf.getCount() - waterCount;
}
```

**Explanation:** Each land cell starts as its own component. Union adjacent land cells. Total components minus water cells gives the number of islands.

**Complexity:** Time: O(m × n × α(m × n)), Space: O(m × n)

---

### Problem 2: Earliest Moment When Everyone Becomes Friends

```javascript
function earliestFriends(logs, n) {
  logs.sort((a, b) => a[0] - b[0]); // Sort by timestamp
  const uf = new UnionFind(n);

  for (const [time, a, b] of logs) {
    uf.union(a, b);
    if (uf.getCount() === 1) return time; // Everyone connected!
  }

  return -1;
}

console.log(earliestFriends(
  [[0,2,0],[1,0,1],[3,0,3],[4,1,2],[7,3,1]],
  4
)); // 3
```

**Explanation:** Process friendships chronologically. After each union, check if everyone is in one group. The timestamp when the count becomes 1 is our answer.

**Complexity:** Time: O(E log E + E × α(V)), Space: O(V)

---

### Problem 3: Satisfiability of Equality Equations

```javascript
function equationsPossible(equations) {
  const uf = new UnionFind(26); // 26 lowercase letters

  // Process equalities first
  for (const eq of equations) {
    if (eq[1] === '=') {
      const a = eq.charCodeAt(0) - 97;
      const b = eq.charCodeAt(3) - 97;
      uf.union(a, b);
    }
  }

  // Check inequalities
  for (const eq of equations) {
    if (eq[1] === '!') {
      const a = eq.charCodeAt(0) - 97;
      const b = eq.charCodeAt(3) - 97;
      if (uf.connected(a, b)) return false; // Contradiction!
    }
  }

  return true;
}

console.log(equationsPossible(["a==b","b!=a"])); // false
console.log(equationsPossible(["a==b","b==c","a==c"])); // true
console.log(equationsPossible(["a==b","b!=c","c==a"])); // false
```

**Explanation:** First, process all equalities (union equal variables). Then check inequalities — if two variables that should be unequal are in the same group, it's a contradiction.

**Complexity:** Time: O(n × α(26)) ≈ O(n), Space: O(1)

---

### 🔗 Navigation
Prev: [25_Bit_Manipulation.md](25_Bit_Manipulation.md) | Index: [00_Index.md](00_Index.md) | Next: [27_Segment_Tree.md](27_Segment_Tree.md)
