# 📌 Project 03 — Build LRU Cache

## 🎯 Goal

Implement an O(1) get and put Least Recently Used (LRU) cache using a doubly-linked list + HashMap. This is a classic data structure interview project.

## 🔬 Algorithm

**Data structures:**
- `HashMap` (Map) for O(1) key lookup
- Doubly-linked list for O(1) insertion/deletion at any position
- Head: most recently used; Tail: least recently used

**Operations:**
- `get(key)`: O(1) — find in map, move to head
- `put(key)`: O(1) — add to head, evict tail if full

## ✅ Complete Solution

```javascript
class ListNode {
  constructor(key, value) {
    this.key = key
    this.value = value
    this.prev = null
    this.next = null
  }
}

class LRUCache {
  constructor(capacity) {
    this.capacity = capacity
    this.map = new Map()
    
    // Sentinel nodes (dummy head and tail)
    this.head = new ListNode(0, 0)
    this.tail = new ListNode(0, 0)
    this.head.next = this.tail
    this.tail.prev = this.head
  }
  
  _remove(node) {
    node.prev.next = node.next
    node.next.prev = node.prev
  }
  
  _addToHead(node) {
    node.next = this.head.next
    node.prev = this.head
    this.head.next.prev = node
    this.head.next = node
  }
  
  get(key) {
    if (!this.map.has(key)) return -1
    
    const node = this.map.get(key)
    this._remove(node)
    this._addToHead(node)
    return node.value
  }
  
  put(key, value) {
    if (this.map.has(key)) {
      const node = this.map.get(key)
      node.value = value
      this._remove(node)
      this._addToHead(node)
    } else {
      const node = new ListNode(key, value)
      this.map.set(key, node)
      this._addToHead(node)
      
      if (this.map.size > this.capacity) {
        // Evict LRU (tail.prev)
        const lru = this.tail.prev
        this._remove(lru)
        this.map.delete(lru.key)
      }
    }
  }
  
  // Debug: show cache in MRU order
  toArray() {
    const result = []
    let curr = this.head.next
    while (curr !== this.tail) {
      result.push([curr.key, curr.value])
      curr = curr.next
    }
    return result
  }
}
```

## 🔗 Navigation

**Prev:** [02_Build_Promise.md](02_Build_Promise.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Build_React_Like_State.md](04_Build_React_Like_State.md)
