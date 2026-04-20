# 📌 Greedy

## 🧠 Concept Explanation (Story Format)

Imagine you're at a **buffet** and you want to eat as much as possible, but your plate has limited space. The greedy strategy? **Always pick the food that fills you up the most per unit of space.** You make the best choice at each moment without looking ahead.

A **Greedy algorithm** makes the **locally optimal choice** at each step, hoping it leads to a **globally optimal solution**. It doesn't go back and reconsider — it commits to each choice.

### When Does Greedy Work?

Greedy works when the problem has:
1. **Greedy Choice Property:** A locally optimal choice leads to a global optimum.
2. **Optimal Substructure:** An optimal solution contains optimal solutions to subproblems.

### Greedy vs Dynamic Programming

| Feature | Greedy | Dynamic Programming |
|---------|--------|-------------------|
| Approach | Choose best at each step | Explore all options |
| Backtracks? | Never | Considers all subproblems |
| Speed | Usually faster | Usually slower |
| Correctness | Not always optimal | Always optimal |
| Use when | Greedy choice property holds | Need guaranteed optimum |

### Real-Life Analogy

**Making change:** To give $0.63 in the fewest coins (US coins), always pick the largest coin that fits: 50¢ + 10¢ + 1¢ + 1¢ + 1¢ = 5 coins. This greedy approach works for US coins (but not all coin systems!).

---

## 🐢 Brute Force Approach

### Problem: Activity Selection (Maximum Non-Overlapping Intervals)

```javascript
// Brute Force: Try all subsets, find the largest non-overlapping set
function activitySelectionBrute(activities) {
  let maxCount = 0;

  function backtrack(idx, lastEnd, count) {
    maxCount = Math.max(maxCount, count);

    for (let i = idx; i < activities.length; i++) {
      if (activities[i][0] >= lastEnd) {
        backtrack(i + 1, activities[i][1], count + 1);
      }
    }
  }

  activities.sort((a, b) => a[1] - b[1]);
  backtrack(0, 0, 0);
  return maxCount;
}

console.log(activitySelectionBrute([[1,4],[3,5],[0,6],[5,7],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[12,16]]));
// 4
```


#### Code Story
- This problem is about fitting as many tasks as possible into a single day without any overlap.
- First, we sort all the tasks by their Finish Times.
- Then, we always pick the task that finishes first, then jump to the next task that starts after it.
- Finally, we count how many tasks we managed to fit in.
- This works because by choosing the task that ends early, we leave the maximum possible amount of time for future tasks.

---

## ⚡ Optimized Approach

### Greedy: Sort by End Time, Pick Non-Overlapping

```javascript
function activitySelectionGreedy(activities) {
  // Sort by end time (finish earliest first)
  activities.sort((a, b) => a[1] - b[1]);

  let count = 1; // Always pick the first activity
  let lastEnd = activities[0][1];

  for (let i = 1; i < activities.length; i++) {
    if (activities[i][0] >= lastEnd) {
      count++;     // This activity doesn't overlap
      lastEnd = activities[i][1]; // Update end time
    }
  }

  return count;
}

console.log(activitySelectionGreedy([[1,4],[3,5],[0,6],[5,7],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[12,16]]));
// 4
```

### Why Greedy Works Here

By always choosing the activity that **ends earliest**, we leave the most room for future activities. It's provably optimal for this problem.

---

## 🔍 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(2ⁿ) | O(n) |
| Greedy | O(n log n) | O(1) |

---

## 💼 LinkedIn / Interview Questions (WITH FULL SOLUTIONS)

### Question 1: Jump Game

**Problem Statement:** Given an array where each element is the maximum jump length, determine if you can reach the last index.


#### Code Story
- This problem is about seeing if you can jump from the start of a list to the very end.
- First, we keep track of the 'farthest spot' we can possibly reach based on where we are right now.
- Then, as we move forward, we update our 'farthest reach' with any bigger jumps we find.
- Finally, if our farthest reach ever gets us to (or past) the end of the list, we return true.
- This works because as long as you can always reach a spot that can reach even further, you will eventually reach the finish line.

#### 🐢 Brute Force — Recursive

```javascript
function canJumpBrute(nums) {
  function jump(pos) {
    if (pos >= nums.length - 1) return true;
    if (nums[pos] === 0) return false;

    for (let i = 1; i <= nums[pos]; i++) {
      if (jump(pos + i)) return true;
    }
    return false;
  }
  return jump(0);
}

console.log(canJumpBrute([2, 3, 1, 1, 4])); // true
console.log(canJumpBrute([3, 2, 1, 0, 4])); // false
```

#### ⚡ Optimized — Greedy

```javascript
function canJumpGreedy(nums) {
  let maxReach = 0; // Farthest index we can reach

  for (let i = 0; i < nums.length; i++) {
    if (i > maxReach) return false; // Can't reach this index
    maxReach = Math.max(maxReach, i + nums[i]);
  }

  return true;
}

console.log(canJumpGreedy([2, 3, 1, 1, 4])); // true
console.log(canJumpGreedy([3, 2, 1, 0, 4])); // false
```

**Simple Explanation:** Track the farthest you can reach. At each position, update the farthest reach. If you ever land on a position beyond your reach, you're stuck.

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(2ⁿ) | O(n) |
| Greedy | O(n) | O(1) |

---

### Question 2: Minimum Number of Coins

**Problem Statement:** Given coin denominations and a target amount, find the minimum coins needed.

#### 🐢 Brute Force — Recursive

```javascript
function minCoinsBrute(coins, amount) {
  if (amount === 0) return 0;
  if (amount < 0) return Infinity;

  let min = Infinity;
  for (const coin of coins) {
    const result = minCoinsBrute(coins, amount - coin);
    min = Math.min(min, result + 1);
  }
  return min;
}
```

#### ⚡ Optimized — Greedy (only works for certain coin systems)

```javascript
function minCoinsGreedy(coins, amount) {
  coins.sort((a, b) => b - a); // Sort largest first
  let count = 0;

  for (const coin of coins) {
    const numCoins = Math.floor(amount / coin);
    count += numCoins;
    amount -= numCoins * coin;
  }

  return amount === 0 ? count : -1; // -1 if not possible
}

// Works for standard denominations
console.log(minCoinsGreedy([1, 5, 10, 25], 63)); // 6 (25+25+10+1+1+1)
```

**Note:** Greedy doesn't always work for coin change. For arbitrary coins, use Dynamic Programming (Chapter 24).

**Complexity:**
| Approach | Time | Space |
|----------|------|-------|
| Greedy | O(n) | O(1) |

---

### Question 3: Fractional Knapsack

**Problem Statement:** Given items with weights and values, maximize value in a knapsack of capacity W. You can take fractions of items.

#### ⚡ Optimized — Greedy (Sort by Value/Weight Ratio)

```javascript
function fractionalKnapsack(items, capacity) {
  // Sort by value-to-weight ratio (descending)
  items.sort((a, b) => (b.value / b.weight) - (a.value / a.weight));

  let totalValue = 0;

  for (const item of items) {
    if (capacity >= item.weight) {
      // Take the whole item
      totalValue += item.value;
      capacity -= item.weight;
    } else {
      // Take a fraction
      totalValue += item.value * (capacity / item.weight);
      capacity = 0;
      break;
    }
  }

  return totalValue;
}

const items = [
  { weight: 10, value: 60 },
  { weight: 20, value: 100 },
  { weight: 30, value: 120 }
];

console.log(fractionalKnapsack(items, 50)); // 240
```

**Simple Explanation:** Sort items by "bang for the buck" (value per kg). Take the most valuable items first. If the last item doesn't fit entirely, take a fraction.

**Complexity:** Time: O(n log n), Space: O(1)

---

### Question 4: Non-Overlapping Intervals (Minimum Removals)

**Problem Statement:** Find the minimum number of intervals to remove to make the rest non-overlapping.

```javascript
function eraseOverlapIntervals(intervals) {
  intervals.sort((a, b) => a[1] - b[1]); // Sort by end time

  let count = 0;
  let prevEnd = -Infinity;

  for (const [start, end] of intervals) {
    if (start >= prevEnd) {
      prevEnd = end; // No overlap — keep it
    } else {
      count++; // Overlap — remove this one
    }
  }

  return count;
}

console.log(eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]])); // 1
console.log(eraseOverlapIntervals([[1,2],[1,2],[1,2]]));       // 2
```

**Explanation:** Sort by end time. Always keep the interval that ends earliest (leaves most room). Count how many we skip.

**Complexity:** Time: O(n log n), Space: O(1)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Assign Cookies

```javascript
function findContentChildren(children, cookies) {
  children.sort((a, b) => a - b);
  cookies.sort((a, b) => a - b);

  let child = 0, cookie = 0;

  while (child < children.length && cookie < cookies.length) {
    if (cookies[cookie] >= children[child]) {
      child++; // Child is satisfied
    }
    cookie++; // Move to next cookie
  }

  return child;
}

console.log(findContentChildren([1, 2, 3], [1, 1]));    // 1
console.log(findContentChildren([1, 2], [1, 2, 3]));    // 2
```

**Explanation:** Sort both. Give the smallest cookie to the least greedy child. If the cookie satisfies them, move to the next child. Always try the next cookie.

**Complexity:** Time: O(n log n), Space: O(1)

---

### Problem 2: Gas Station

```javascript
function canCompleteCircuit(gas, cost) {
  let totalGas = 0, totalCost = 0;
  let tank = 0, start = 0;

  for (let i = 0; i < gas.length; i++) {
    totalGas += gas[i];
    totalCost += cost[i];
    tank += gas[i] - cost[i];

    if (tank < 0) {
      start = i + 1; // Can't start from any station before i+1
      tank = 0;
    }
  }

  return totalGas >= totalCost ? start : -1;
}

console.log(canCompleteCircuit([1,2,3,4,5], [3,4,5,1,2])); // 3
console.log(canCompleteCircuit([2,3,4], [3,4,3]));           // -1
```


#### Code Story
- This problem is about finding a starting point where you can drive around a circular road without running out of gas.
- First, we check if the total gas available is at least as much as the total gas needed (if not, it's impossible).
- Then, we try starting at index 0 and keep track of our current tank; if it hits zero, we realize we must start after the spot where we failed.
- Finally, we return the starting index that successfully makes it all the way around.
- This works because a failure at any point means every spot before that failure would also have failed at that same point.

**Explanation:** If total gas ≥ total cost, a solution exists. Track the running tank. If it goes negative, the start must be after this point. The first valid start we find works.

**Complexity:** Time: O(n), Space: O(1)

---

### Problem 3: Task Scheduler

```javascript
function leastInterval(tasks, n) {
  const freq = new Array(26).fill(0);
  for (const task of tasks) freq[task.charCodeAt(0) - 65]++;

  freq.sort((a, b) => b - a);
  const maxFreq = freq[0];
  let idleSlots = (maxFreq - 1) * n;

  for (let i = 1; i < freq.length; i++) {
    idleSlots -= Math.min(freq[i], maxFreq - 1);
  }

  idleSlots = Math.max(0, idleSlots);
  return tasks.length + idleSlots;
}

console.log(leastInterval(["A","A","A","B","B","B"], 2)); // 8
console.log(leastInterval(["A","A","A","B","B","B"], 0)); // 6
```

**Explanation:** The most frequent task creates the frame. Fill idle slots with other tasks. If there aren't enough tasks to fill idle slots, we must wait. Total time = tasks + remaining idle.

**Complexity:** Time: O(n), Space: O(1)

---

### 🔗 Navigation
Prev: [22_Minimum_Spanning_Tree.md](22_Minimum_Spanning_Tree.md) | Index: [00_Index.md](00_Index.md) | Next: [24_Dynamic_Programming.md](24_Dynamic_Programming.md)
