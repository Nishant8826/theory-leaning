# 📌 Project 04 — Build React-Like useState & useEffect

## 🎯 Goal

Build a simplified React hooks implementation to deeply understand how useState, useEffect, and the rendering model work.

## ✅ Complete Solution

```javascript
let currentComponent = null
let hookIndex = 0
let hooks = []

function useState(initialValue) {
  const capturedIndex = hookIndex
  
  if (hooks[capturedIndex] === undefined) {
    hooks[capturedIndex] = { value: typeof initialValue === 'function' ? initialValue() : initialValue }
  }
  
  const setState = (newValue) => {
    hooks[capturedIndex].value = typeof newValue === 'function'
      ? newValue(hooks[capturedIndex].value)
      : newValue
    render()  // Trigger re-render
  }
  
  hookIndex++
  return [hooks[capturedIndex].value, setState]
}

function useEffect(callback, deps) {
  const capturedIndex = hookIndex
  const prevHook = hooks[capturedIndex]
  
  const hasChanged = !prevHook
    || !deps
    || deps.some((dep, i) => dep !== prevHook.deps[i])
  
  if (hasChanged) {
    // Schedule cleanup and new effect
    if (prevHook?.cleanup) prevHook.cleanup()
    
    queueMicrotask(() => {
      const cleanup = callback()
      hooks[capturedIndex] = { deps, cleanup: typeof cleanup === 'function' ? cleanup : undefined }
    })
  }
  
  hookIndex++
}

function useMemo(factory, deps) {
  const capturedIndex = hookIndex
  const prevHook = hooks[capturedIndex]
  
  const hasChanged = !prevHook || deps.some((dep, i) => dep !== prevHook.deps[i])
  
  if (hasChanged) {
    hooks[capturedIndex] = { value: factory(), deps }
  }
  
  hookIndex++
  return hooks[capturedIndex].value
}

function useCallback(fn, deps) {
  return useMemo(() => fn, deps)
}

function render() {
  hookIndex = 0
  // Simulate component rendering
  if (currentComponent) currentComponent()
}

// Demo component:
function Counter() {
  const [count, setCount] = useState(0)
  const [name, setName] = useState('World')
  
  useEffect(() => {
    document.title = `Count: ${count}`
    return () => { document.title = 'App' }  // Cleanup
  }, [count])
  
  const increment = useCallback(() => setCount(c => c + 1), [])
  
  console.log(`Render: count=${count}, name=${name}`)
  return { count, name, increment, setName }
}

currentComponent = Counter
render()
```

## 🔗 Navigation

**Prev:** [03_Build_LRU_Cache.md](03_Build_LRU_Cache.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Build_Rate_Limiter.md](05_Build_Rate_Limiter.md)
