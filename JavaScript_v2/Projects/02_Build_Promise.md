# 📌 Project 02 — Build Promise From Scratch

## 🎯 Goal

Implement a Promises/A+ compliant Promise class from scratch. This tests deep understanding of async mechanics, microtask scheduling, and the promise resolution procedure.

## ✅ Complete Solution

```javascript
class MyPromise {
  static PENDING = 'pending'
  static FULFILLED = 'fulfilled'
  static REJECTED = 'rejected'
  
  constructor(executor) {
    this.state = MyPromise.PENDING
    this.value = undefined
    this.reason = undefined
    this.onFulfilledCallbacks = []
    this.onRejectedCallbacks = []
    
    const resolve = (value) => {
      if (this.state !== MyPromise.PENDING) return
      
      // Handle thenable resolution
      if (value instanceof MyPromise) {
        value.then(resolve, reject)
        return
      }
      
      this.state = MyPromise.FULFILLED
      this.value = value
      queueMicrotask(() => {
        this.onFulfilledCallbacks.forEach(fn => fn(this.value))
      })
    }
    
    const reject = (reason) => {
      if (this.state !== MyPromise.PENDING) return
      this.state = MyPromise.REJECTED
      this.reason = reason
      queueMicrotask(() => {
        this.onRejectedCallbacks.forEach(fn => fn(this.reason))
      })
    }
    
    try {
      executor(resolve, reject)
    } catch(e) {
      reject(e)
    }
  }
  
  then(onFulfilled, onRejected) {
    onFulfilled = typeof onFulfilled === 'function' ? onFulfilled : v => v
    onRejected = typeof onRejected === 'function' ? onRejected : e => { throw e }
    
    return new MyPromise((resolve, reject) => {
      const handleFulfilled = (value) => {
        try {
          const result = onFulfilled(value)
          resolvePromise(result, resolve, reject)
        } catch(e) {
          reject(e)
        }
      }
      
      const handleRejected = (reason) => {
        try {
          const result = onRejected(reason)
          resolvePromise(result, resolve, reject)
        } catch(e) {
          reject(e)
        }
      }
      
      if (this.state === MyPromise.FULFILLED) {
        queueMicrotask(() => handleFulfilled(this.value))
      } else if (this.state === MyPromise.REJECTED) {
        queueMicrotask(() => handleRejected(this.reason))
      } else {
        this.onFulfilledCallbacks.push(handleFulfilled)
        this.onRejectedCallbacks.push(handleRejected)
      }
    })
  }
  
  catch(onRejected) { return this.then(undefined, onRejected) }
  finally(fn) {
    return this.then(
      value => MyPromise.resolve(fn()).then(() => value),
      reason => MyPromise.resolve(fn()).then(() => { throw reason })
    )
  }
  
  static resolve(value) {
    if (value instanceof MyPromise) return value
    return new MyPromise(resolve => resolve(value))
  }
  
  static reject(reason) {
    return new MyPromise((_, reject) => reject(reason))
  }
  
  static all(promises) {
    return new MyPromise((resolve, reject) => {
      if (!promises.length) return resolve([])
      const results = new Array(promises.length)
      let completed = 0
      promises.forEach((p, i) => {
        MyPromise.resolve(p).then(v => {
          results[i] = v
          if (++completed === promises.length) resolve(results)
        }, reject)
      })
    })
  }
  
  static allSettled(promises) {
    return MyPromise.all(promises.map(p =>
      MyPromise.resolve(p)
        .then(value => ({ status: 'fulfilled', value }))
        .catch(reason => ({ status: 'rejected', reason }))
    ))
  }
  
  static race(promises) {
    return new MyPromise((resolve, reject) => {
      promises.forEach(p => MyPromise.resolve(p).then(resolve, reject))
    })
  }
  
  static any(promises) {
    return new MyPromise((resolve, reject) => {
      let rejectedCount = 0
      const errors = new Array(promises.length)
      promises.forEach((p, i) => {
        MyPromise.resolve(p).then(resolve, reason => {
          errors[i] = reason
          if (++rejectedCount === promises.length) {
            reject(new AggregateError(errors, 'All promises were rejected'))
          }
        })
      })
    })
  }
}

function resolvePromise(value, resolve, reject) {
  if (value instanceof MyPromise) {
    value.then(resolve, reject)
  } else if (value && (typeof value === 'object' || typeof value === 'function')) {
    try {
      const then = value.then
      if (typeof then === 'function') {
        let called = false
        try {
          then.call(value,
            v => { if (!called) { called = true; resolvePromise(v, resolve, reject) } },
            r => { if (!called) { called = true; reject(r) } }
          )
        } catch(e) {
          if (!called) reject(e)
        }
      } else {
        resolve(value)
      }
    } catch(e) {
      reject(e)
    }
  } else {
    resolve(value)
  }
}
```

## 🔗 Navigation

**Prev:** [01_Build_Event_Emitter.md](01_Build_Event_Emitter.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Build_LRU_Cache.md](03_Build_LRU_Cache.md)
