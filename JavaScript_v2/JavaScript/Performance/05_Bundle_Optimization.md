# 📌 05 — Bundle Optimization

## 🧠 Concept Explanation

Bundle optimization reduces the amount of JavaScript delivered to the browser. Less JS = faster parse time, faster execution, lower Time to Interactive. Key techniques: tree shaking, code splitting, minification, compression, differential serving.

## 🔬 Internal Mechanics

### Tree Shaking (Dead Code Elimination)

Tree shaking works by static analysis of ES6 module import/export statements:
1. Bundler (Rollup/Webpack) builds the module dependency graph
2. Marks all exports that are imported somewhere as "used"
3. Removes all "unused" exports at build time

**Requirements for effective tree shaking:**
- ES6 modules (not CommonJS) — static imports enable analysis
- `sideEffects: false` in package.json — tells bundler no module has side effects
- Named exports (not default export objects)

## 🔍 Code Examples

### webpack.config.js — Production Optimization

```javascript
const TerserPlugin = require('terser-webpack-plugin')
const CompressionPlugin = require('compression-webpack-plugin')
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

module.exports = {
  mode: 'production',
  
  optimization: {
    minimizer: [new TerserPlugin({
      terserOptions: {
        compress: { 
          drop_console: true,  // Remove console.log in production
          passes: 2            // Multiple optimization passes
        },
        output: { comments: false }
      }
    })],
    
    splitChunks: {
      chunks: 'all',
      maxInitialRequests: 25,
      minSize: 20000,
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'initial',
          priority: 20
        },
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react',
          chunks: 'all',
          priority: 30  // Higher priority: extract first
        }
      }
    },
    
    runtimeChunk: 'single',  // Single runtime chunk for all entry points
  },
  
  plugins: [
    new CompressionPlugin({ algorithm: 'brotliCompress' }),
    process.env.ANALYZE && new BundleAnalyzerPlugin(),
  ].filter(Boolean)
}
```

### Differential Serving (Modern vs Legacy)

```html
<!-- Serve ES modules to modern browsers, legacy bundle to old -->
<script type="module" src="app.modern.js"></script>
<script nomodule src="app.legacy.js"></script>
<!-- Modern browsers: execute module script, ignore nomodule -->
<!-- IE11: ignore type=module, execute nomodule script -->

<!-- Modern bundle: no transpilation, ~30% smaller -->
<!-- Legacy bundle: full Babel transpilation, polyfills -->
```

## 🏢 Industry Best Practices

1. **Analyze first** — Run bundle-analyzer before optimizing to find biggest gains.
2. **Separate vendor and app bundles** — Vendor bundle changes rarely, cache hit rates improve.
3. **Compress** — Brotli compression reduces JS size by ~20-30% beyond gzip.
4. **Differential serving** — Modern browsers don't need Babel-transpiled code.
5. **HTTP/2** — Multiple small chunks are fine; HTTP/1.1 needs fewer larger chunks.

## 💼 Interview Questions

**Q1: Why does tree shaking require ES6 modules?**
> CommonJS `require()` is dynamic — the module path can be computed at runtime, imports can happen inside conditions and functions. Static analysis cannot determine all import/export relationships. ES6 `import/export` is static — all imports and exports must be at the top level (not inside conditions) and paths must be string literals. This allows bundlers to build a complete dependency graph at build time and determine which exports are never imported.

## 🔗 Navigation

**Prev:** [04_Lazy_Loading.md](04_Lazy_Loading.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Deoptimization_and_ICs.md](06_Deoptimization_and_ICs.md)
