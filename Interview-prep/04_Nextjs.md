# 🚀 Interview Preparation - Next.js

> **Domain:** Web Development / Full Stack  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What is Next.js and why is it used?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js is a React framework for building full-stack web applications. You use React Components to build user interfaces, and Next.js for additional features and optimizations.

**Why use it:**
- **Zero Config:** Automatic compilation and bundling.
- **SSR & SSG:** Out of the box support for Server-Side Rendering and Static Site Generation.
- **API Routes:** Easily create API endpoints.
- **Performance:** Automatic image, font, and script optimizations.

> 💡 **Interviewer Focus:** Understanding the difference between React (library) and Next.js (framework).
</details>
<hr/>

### ❓ Q2. **What is the difference between Next.js and React?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **React** is a JavaScript library for building user interfaces. It handles the view layer. You need to configure routing, bundling, and rendering strategies yourself.
- **Next.js** is a framework built on top of React. It provides routing, server-side rendering, static site generation, and API routes out of the box.

> 💡 **Interviewer Focus:** Library vs Framework distinction.
</details>
<hr/>

### ❓ Q3. **Explain Server-Side Rendering (SSR).**
<details>
<summary><b>👀 Show Answer</b></summary>

In SSR, the HTML is generated on the server for **every request**. When a user requests a page, the server fetches data and renders the HTML, then sends it to the client. This is good for dynamic content that changes frequently.

> 💡 **Interviewer Focus:** Good for SEO and initial load speed for dynamic data.
</details>
<hr/>

### ❓ Q4. **Explain Static Site Generation (SSG).**
<details>
<summary><b>👀 Show Answer</b></summary>

In SSG, the HTML is generated at **build time**. The HTML is then reused on each request. It can be cached by a CDN. This is the fastest rendering method but not ideal for data that changes constantly.

> 💡 **Interviewer Focus:** Best performance, great for blogs or documentation.
</details>
<hr/>

### ❓ Q5. **What is Client-Side Rendering (CSR) in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

In CSR, the server sends a minimal HTML file and the JavaScript bundle. The browser then executes the JS to render the page and fetch data. In Next.js, you get CSR by default if you don't use SSR or SSG methods (or by using `'use client'` in App Router).

> 💡 **Interviewer Focus:** Good for user-specific dashboards that don't need SEO.
</details>
<hr/>

### ❓ Q6. **How does file-based routing work in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js has a file-system based router.
- In **Pages Router**: Files in the `pages` directory automatically become routes (e.g., `pages/about.js` -> `/about`).
- In **App Router**: Folders in the `app` directory define routes, and a `page.js` file makes the route accessible (e.g., `app/about/page.js` -> `/about`).

> 💡 **Interviewer Focus:** Familiarity with Next.js folder structure.
</details>
<hr/>

### ❓ Q7. **What is the `Image` component in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

The Next.js `Image` component (`next/image`) is an extension of the HTML `<img>` element. It automatically optimizes images for:
- **Size:** Serves correctly sized images for each device.
- **Format:** Uses modern formats like WebP and AVIF.
- **Loading:** Lazy loads images by default.

> 💡 **Interviewer Focus:** Core performance feature of Next.js.
</details>
<hr/>

### ❓ Q8. **What is the purpose of the `Link` component?**
<details>
<summary><b>👀 Show Answer</b></summary>

The `Link` component (`next/link`) is used for client-side navigation between pages. It pre-fetches pages in the background as they appear in the viewport, making transitions near-instant.

> 💡 **Interviewer Focus:** Client-side navigation vs traditional anchor tags.
</details>
<hr/>

### ❓ Q9. **What are API Routes in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

API routes provide a solution to build your API with Next.js. Any file inside the `pages/api` (or `app/api` for App Router) directory is mapped to `/api/*` and will be treated as an API endpoint instead of a page.

> 💡 **Interviewer Focus:** Ability to build full-stack apps without a separate backend.
</details>
<hr/>

### ❓ Q10. **What is the difference between the `app` directory and the `pages` directory?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `pages` directory is the legacy routing system (Pages Router).
- `app` directory is the new routing system introduced in Next.js 13 (App Router). It supports React Server Components, nested layouts, and streaming.

> 💡 **Interviewer Focus:** Awareness of the modern Next.js features.
</details>
<hr/>

## 🟡 Intermediate Level

### ❓ Q11. **Explain Incremental Static Regeneration (ISR).**
<details>
<summary><b>👀 Show Answer</b></summary>

ISR allows you to create or update static pages **after** you’ve built your site. You can use static-generation on a per-page basis, without needing to rebuild the entire site.
In Pages Router, you use the `revalidate` prop in `getStaticProps`. In App Router, you use `fetch(..., { next: { revalidate: 60 } })`.

> 💡 **Interviewer Focus:** Best of both worlds (SSG speed + dynamic updates).
</details>
<hr/>

### ❓ Q12. **How do you fetch data in the App Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

In the App Router, you can use standard `async/await` directly in React Server Components. You use the native `fetch` API, which Next.js extends to support caching and revalidation.
```javascript
async function Page() {
  const data = await fetch('https://api.example.com/...').then(r => r.json());
  return <div>...</div>;
}
```

> 💡 **Interviewer Focus:** Shift from `getStaticProps` to async Server Components.
</details>
<hr/>

### ❓ Q13. **What are Server Components vs Client Components in Next.js 13+?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Server Components:** Render on the server. They don't send JS to the client, cannot use hooks (like `useState`), and can access backend resources directly. Default in the `app` directory.
- **Client Components:** Render on the client. They use the `'use client'` directive at the top, can use hooks, and handle interactivity.

> 💡 **Interviewer Focus:** Understanding the paradigm shift in React 18 / Next 13.
</details>
<hr/>

### ❓ Q14. **How do you create dynamic routes in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

By using brackets in the file name or folder name.
- Pages Router: `pages/post/[id].js` accesses `/post/1`.
- App Router: `app/post/[id]/page.js` accesses `/post/1`.
You access the parameter via `useRouter` or from the `params` prop in the component.

> 💡 **Interviewer Focus:** Handling dynamic segments in URLs.
</details>
<hr/>

### ❓ Q15. **What is the purpose of `getStaticPaths` in Pages Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

If a page has dynamic routes and uses `getStaticProps`, it needs to define a list of paths to be statically generated at build time. `getStaticPaths` provides that list.

> 💡 **Interviewer Focus:** Required for dynamic SSG in Pages Router.
</details>
<hr/>

### ❓ Q16. **How does Middleware work in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Middleware allows you to run code before a request is completed. Based on the incoming request, you can modify the response by rewriting, redirecting, modifying the request or response headers, or responding directly. It runs on the Edge.

> 💡 **Interviewer Focus:** Used for auth checks, bot protection, and localization.
</details>
<hr/>

### ❓ Q17. **What is "Streaming" in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Streaming allows you to break down the page's HTML into smaller chunks and progressively send those chunks from the server to the client. This means parts of the page can be displayed sooner without waiting for all the data to load. Supported via `loading.js` files in App Router.

> 💡 **Interviewer Focus:** Improving perceived performance and Time to First Byte (TTFB).
</details>
<hr/>

### ❓ Q18. **How do you handle SEO in the App Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

By exporting a `metadata` object or generating it dynamically using `generateMetadata` function in your `layout.js` or `page.js`.
```javascript
export const metadata = { title: 'My Page' };
```

> 💡 **Interviewer Focus:** Shift from `next/head` to the Metadata API.
</details>
<hr/>

### ❓ Q19. **What is the difference between `getServerSideProps` and `getStaticProps`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `getServerSideProps` fetches data on **every request** (SSR).
- `getStaticProps` fetches data at **build time** (SSG).

> 💡 **Interviewer Focus:** Classical Pages Router question.
</details>
<hr/>

### ❓ Q20. **How do you optimize fonts in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js includes built-in automatic font optimization. Using `next/font`, you can use Google Fonts (or custom fonts) with zero layout shift. It downloads font files at build time and hosts them with your static assets.

> 💡 **Interviewer Focus:** Avoiding Layout Shift (CLS).
</details>
<hr/>

## 🔴 Advanced Level

### ❓ Q21. **Explain the concept of "Edge Runtime" in Next.js.**
<details>
<summary><b>👀 Show Answer</b></summary>

The Edge Runtime is a subset of Node.js APIs that are lightweight and can run on CDN edge nodes. It is much faster and has lower latency than a full Node.js server. Next.js uses it for Middleware and can use it for API routes and pages.

> 💡 **Interviewer Focus:** Understanding edge computing and its limitations (no native Node modules like `fs`).
</details>
<hr/>

### ❓ Q22. **How do you implement Server Actions in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Server Actions are asynchronous functions that are executed on the server. They can be defined in Server Components or separate files with the `'use server'` directive. They allow you to handle form submissions and data mutations without manually creating an API route.

> 💡 **Interviewer Focus:** Modern full-stack data mutation paradigm in Next.js.
</details>
<hr/>

### ❓ Q23. **What is "Parallel Routes" and when would you use them?**
<details>
<summary><b>👀 Show Answer</b></summary>

Parallel Routes allow you to simultaneously or conditionally render one or more pages in the same layout. They are defined using "slots" (e.g., `@folder`). Useful for complex dashboards or modals where you want to maintain state or independent loading states.

> 💡 **Interviewer Focus:** Advanced App Router feature for complex UIs.
</details>
<hr/>

### ❓ Q24. **What is "Intercepting Routes"?**
<details>
<summary><b>👀 Show Answer</b></summary>

Intercepting routes allows you to load a route within the current layout while keeping the context of the current page. For example, clicking a photo opens it in a modal over the feed, but reloading the URL opens the photo on its own page. Defined using `(..)folder` syntax.

> 💡 **Interviewer Focus:** Advanced UX patterns supported by the router.
</details>
<hr/>

### ❓ Q25. **How does caching work in the App Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js has 4 levels of caching:
1. **Request Memoization:** Reuses fetch data across a single render pass.
2. **Data Cache:** Persists data across user requests and deployments.
3. **Full Route Cache:** Caches the rendered HTML and RSC payload on the server.
4. **Router Cache:** Client-side cache of visited segments.

> 💡 **Interviewer Focus:** Deep understanding of Next.js performance architecture.
</details>
<hr/>

### ❓ Q26. **How do you handle authentication in Middleware?**
<details>
<summary><b>👀 Show Answer</b></summary>

Read the session cookie or token from the request. Verify it (e.g., using a JWT library that works on the Edge). If valid, proceed. If invalid, redirect to the login page using `NextResponse.redirect`.

> 💡 **Interviewer Focus:** Securing routes before they even reach the server.
</details>
<hr/>

### ❓ Q27. **What are the limitations of React Server Components?**
<details>
<summary><b>👀 Show Answer</b></summary>

- They cannot use State or Effects (no `useState`, `useEffect`).
- They cannot use browser-only APIs (like `window` or `document`).
- They cannot pass functions as props to Client Components (props must be serializable).

> 💡 **Interviewer Focus:** Understanding the boundaries between server and client.
</details>
<hr/>

### ❓ Q28. **How do you debug a Next.js application in production?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use structured logging (sent to a log management service like Datadog or Axiom). Use OpenTelemetry for tracing. Vercel provides built-in analytics and speed insights. Source maps can be enabled for production if secured.

> 💡 **Interviewer Focus:** Observability in production environments.
</details>
<hr/>

## 🟣 Expert Level

### ❓ Q29. **Architect a strategy for migrating a large Pages Router application to the App Router.**
<details>
<summary><b>👀 Show Answer</b></summary>

**Strategy:**
1. **Coexistence:** Next.js allows Pages and App router to coexist. Do not do a big bang rewrite.
2. **Start with Leaves:** Migrate simple, static pages or new features first in the `app` directory.
3. **Layouts first:** Identify common layouts in `pages/_app` and recreate them as root layouts in `app`.
4. **Component Audit:** Identify which components can be pure Server Components and which need `'use client'`.
5. **Data Fetching:** Convert `getServerSideProps` to async fetch in RSCs.

> 💡 **Interviewer Focus:** Pragmatic, low-risk migration strategy for production systems.
</details>
<hr/>

### ❓ Q30. **How would you optimize a Next.js site to achieve a perfect 100 score on Lighthouse (Core Web Vitals)?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. **LCP:** Use `next/image` with priority for above-the-fold images. Use SSG or ISR over SSR where possible.
2. **FID / INP:** Minimize Client-side JS. Use Server Components to ship zero JS for static parts.
3. **CLS:** Use fixed sizes for images or aspect ratio containers. Use `next/font` to prevent font swap layout shifts.
4. **General:** Use dynamic imports for heavy components not needed on initial load. Ensure efficient caching.

> 💡 **Interviewer Focus:** Practical knowledge of Core Web Vitals and Next.js optimization features.
</details>
<hr/>

### ❓ Q31. **Explain how partial prerendering (PPR) works in Next.js.**
<details>
<summary><b>👀 Show Answer</b></summary>

PPR allows you to combine static and dynamic rendering on the same page. The static parts of the page (like navigation and sidebar) are served instantly from the edge, while dynamic parts (like a personalized cart) are streamed in as they are generated on the server. It uses React Suspense to define the dynamic boundaries.

> 💡 **Interviewer Focus:** This is experimental/cutting edge. Shows deep engagement with the framework's future.
</details>
<hr/>

### ❓ Q32. **How would you handle global state management in a Next.js App Router application without causing everything to become a Client Component?**
<details>
<summary><b>👀 Show Answer</b></summary>

Do not put a Context Provider at the very root if it forces all children to be client components. Instead:
1. Wrap only the parts of the tree that need state in the Provider.
2. Pass Server Components as `children` to Client Component providers (children remain Server Components!).
3. Use URL state (search params) where possible for global state like pagination or filters, as it is accessible by Server Components.

> 💡 **Interviewer Focus:** Avoiding the "everything becomes a client component" anti-pattern.
</details>
<hr/>

### ❓ Q33. **How do you implement custom caching strategies for external API calls in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `fetch` API options extended by Next.js:
- `fetch(url, { cache: 'force-cache' })` - Cache indefinitely (like SSG).
- `fetch(url, { cache: 'no-store' })` - No cache (like SSR).
- `fetch(url, { next: { revalidate: 3600 } })` - Time-based revalidation (like ISR).
You can also use `unstable_cache` for non-fetch data operations (like DB queries).

> 💡 **Interviewer Focus:** Deep knowledge of Next.js data cache.
</details>
<hr/>

## 🔷 Scenario-Based & Real-World Questions

### ❓ Q34. **How would you implement a multi-language (i18n) site in Next.js App Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use dynamic segments for the locale (e.g., `app/[lang]/page.js`). Use middleware to detect the user's preferred language from headers and redirect them to the appropriate locale path if not present. Use a library like `next-intl` or manage dictionaries manually in Server Components.

> 💡 **Interviewer Focus:** Routing strategy for i18n in App Router.
</details>
<hr/>

### ❓ Q35. **How do you handle file uploads in Next.js without a custom Express server?**
<details>
<summary><b>👀 Show Answer</b></summary>

You can use API Routes (Pages Router) or Server Actions (App Router). For large files, it is best to generate a **Presigned URL** from a service like AWS S3 in the API/Server Action, send it back to the client, and let the client upload the file directly to S3 to avoid overloading the Next.js server.

> 💡 **Interviewer Focus:** Scalable architecture for file uploads.
</details>
<hr/>

### ❓ Q36. **What is the difference between `next/image` and a standard `<img>` tag in terms of performance?**
<details>
<summary><b>👀 Show Answer</b></summary>

`next/image` handles automatic optimization: it serves WebP/AVIF formats to supported browsers, resizes images based on device size, and prevents layout shift (CLS) by requiring width/height or a fill property. Standard `<img>` does none of this automatically.

> 💡 **Interviewer Focus:** Core Web Vitals impact.
</details>
<hr/>

### ❓ Q37. **How would you implement a custom 404 page in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

- Pages Router: Create a `pages/404.js` file.
- App Router: Create a `not-found.js` file at the root or within specific route segments.

> 💡 **Interviewer Focus:** Framework conventions for error pages.
</details>
<hr/>

### ❓ Q38. **How do you handle environment variables in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js supports `.env.local` files out of the box.
- Variables accessible *only* on the server: `SECRET_KEY=123`
- Variables accessible on both server and client: `NEXT_PUBLIC_API_URL=https://...` (must prefix with `NEXT_PUBLIC_`).

> 💡 **Interviewer Focus:** Security and access control of environment variables.
</details>
<hr/>

### ❓ Q39. **What is the purpose of `unstable_cache` in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

`unstable_cache` allows you to cache the results of expensive operations (like database queries) instead of just fetch requests. It is useful for optimizing data fetching that doesn't use the standard `fetch` API (e.g., using Prisma or Mongoose).

> 💡 **Interviewer Focus:** Caching non-fetch operations in App Router.
</details>
<hr/>

### ❓ Q40. **How would you implement secure authentication using NextAuth.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Configure `NextAuth` in an API route or as a handler. Use the JWT strategy for session management to avoid database lookups on every request. Protect routes using Middleware for edge-speed checks, and use the `useSession` hook or `getServerSession` on the server to check auth status.

> 💡 **Interviewer Focus:** Knowledge of NextAuth.js ecosystem and security best practices.
</details>
<hr/>

### ❓ Q41. **How do you resolve a "Hydration Mismatch" error?**
<details>
<summary><b>👀 Show Answer</b></summary>

This happens when the server-rendered HTML differs from the first client render.
**Fixes:**
1. Ensure both use the same data (avoid `Math.random()` or `new Date()` in render logic).
2. Use `useEffect` to run code only on the client.
3. Use `suppressHydrationWarning` on the element (use sparingly).

> 💡 **Interviewer Focus:** Understanding the hydration process and common bugs.
</details>
<hr/>

### ❓ Q42. **How would you create a sitemap in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

In the App Router, you can create a file named `sitemap.js` (or `.ts`) in the root of the app directory. Export a default function that returns an array of URLs. Next.js will automatically generate the XML sitemap.

> 💡 **Interviewer Focus:** SEO automation features.
</details>
<hr/>

### ❓ Q43. **What is the difference between `revalidatePath` and `revalidateTag`?**
<details>
<summary><b>👀 Show Answer</b></summary>

Both are used for on-demand revalidation in the App Router.
- `revalidatePath('/blog')` revalidates all fetch requests on a specific path.
- `revalidateTag('posts')` revalidates only fetch requests that were tagged with `tags: ['posts']`, regardless of where they are in the app.

> 💡 **Interviewer Focus:** Granular cache invalidation strategies.
</details>
<hr/>

### ❓ Q44. **How do you handle redirects in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. In `next.config.js` for permanent/static redirects.
2. Using the `redirect()` function in Server Components or Server Actions.
3. Using `NextResponse.redirect()` in Middleware.

> 💡 **Interviewer Focus:** Different ways to handle navigation control.
</details>
<hr/>

### ❓ Q45. **What is the purpose of the `next/script` component?**
<details>
<summary><b>👀 Show Answer</b></summary>

It allows you to load third-party scripts optimally. You can control the strategy:
- `beforeInteractive`: Load before any Next.js code.
- `afterInteractive` (default): Load after the page becomes interactive.
- `lazyOnload`: Load during idle time.
- `worker`: Load in a web worker.

> 💡 **Interviewer Focus:** Performance impact of third-party scripts.
</details>
<hr/>

### ❓ Q46. **How would you implement a custom document in Pages Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

Create a `pages/_document.js` file. It is used to augment your application's `<html>` and `<body>` tags. This is necessary because Next.js pages skip the definition of the surrounding document markup.

> 💡 **Interviewer Focus:** Customizing the base HTML structure in Pages Router.
</details>
<hr/>

### ❓ Q47. **How do you use CSS Modules in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js supports CSS Modules using the `[name].module.css` file naming convention. CSS Modules locally scope CSS by automatically creating a unique class name.

> 💡 **Interviewer Focus:** Built-in styling solutions.
</details>
<hr/>

### ❓ Q48. **What is the benefit of using Turbopack in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Turbopack is an incremental bundler optimized for JavaScript and TypeScript, written in Rust. It is much faster than Webpack (up to 700x faster for large apps in dev mode) because it never does the same work twice.

> 💡 **Interviewer Focus:** Future of Next.js tooling and build performance.
</details>
<hr/>

### ❓ Q49. **How would you implement dynamic Open Graph (OG) images?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `@vercel/og` or the built-in `ImageResponse` in Next.js. You can create a route (e.g., `app/api/og/route.js`) that uses JSX and CSS to dynamically generate PNG images on the edge.

> 💡 **Interviewer Focus:** Dynamic social sharing image generation.
</details>
<hr/>

### ❓ Q50. **How do you handle analytics in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

You can use the `useReportWebVitals` hook in Pages Router or the `next/analytics` package on Vercel. For Google Analytics, use `next/script` with the `afterInteractive` strategy to avoid blocking page load.

> 💡 **Interviewer Focus:** Measuring performance and user behavior.
</details>
<hr/>

### ❓ Q51. **What is the difference between shallow routing and full routing?**
<details>
<summary><b>👀 Show Answer</b></summary>

Shallow routing allows you to change the URL without running data fetching methods again (`getStaticProps` or `getServerSideProps`). Useful for filtering or sorting UI state reflected in the URL.

> 💡 **Interviewer Focus:** Pages Router feature for URL state management.
</details>
<hr/>

### ❓ Q52. **How do you implement absolute imports in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

By configuring `paths` or `baseUrl` in `jsconfig.json` or `tsconfig.json`. This allows you to import like `import Button from '@/components/Button'` instead of relative paths like `../../components/Button`.

> 💡 **Interviewer Focus:** DX (Developer Experience) and clean imports.
</details>
<hr/>

### ❓ Q53. **How do you handle CORS in Next.js API routes?**
<details>
<summary><b>👀 Show Answer</b></summary>

You can use standard Node.js CORS middleware in the API route handler, or set response headers manually (e.g., `Access-Control-Allow-Origin`).

> 💡 **Interviewer Focus:** Security and API consumption from different origins.
</details>
<hr/>

### ❓ Q54. **What is the `next.config.js` file used for?**
<details>
<summary><b>👀 Show Answer</b></summary>

It is a regular Node.js module used to configure Next.js. You can use it to set up redirects, rewrites, custom Webpack config, image domains, environment variables, and experimental features.

> 💡 **Interviewer Focus:** Framework configuration capabilities.
</details>
<hr/>

### ❓ Q55. **How do you deploy a Next.js application?**
<details>
<summary><b>👀 Show Answer</b></summary>

The easiest way is to deploy to **Vercel** (the creators of Next.js), which provides automatic optimization for SSR, ISR, and Edge functions. You can also build it as a standard Node.js app (`next build` and `next start`) and host it on AWS, Docker, or any Node-compatible server.

> 💡 **Interviewer Focus:** Deployment options and Vercel benefits.
</details>
<hr/>

### ❓ Q56. **What is the difference between a rewrite and a redirect in `next.config.js`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Redirect:** Returns a 301/302 status code and instructs the browser to go to a new URL. The URL in the address bar changes.
- **Rewrite:** Acts as a proxy. It fetches data from the destination URL but keeps the source URL in the address bar. The user doesn't know the request was proxied.

> 💡 **Interviewer Focus:** Routing control and proxying.
</details>
<hr/>

### ❓ Q57. **How do you use TypeScript with Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js has built-in support for TypeScript. You just need to create a `tsconfig.json` file or use a `.ts`/`.tsx` extension, and Next.js will automatically install the necessary types and set up the config.

> 💡 **Interviewer Focus:** TypeScript integration ease.
</details>
<hr/>

### ❓ Q58. **How do you handle global CSS in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

- Pages Router: Import global CSS in `pages/_app.js`.
- App Router: Import global CSS in the root layout (`app/layout.js`).

> 💡 **Interviewer Focus:** Where to load global styles.
</details>
<hr/>

### ❓ Q59. **What is the benefit of Server-Side Rendering over Client-Side Rendering?**
<details>
<summary><b>👀 Show Answer</b></summary>

SSR provides better SEO because search engine crawlers receive a fully rendered HTML page. It also improves perceived performance (FCP) because the user sees content immediately instead of a blank screen while JS loads.

> 💡 **Interviewer Focus:** SEO and initial load performance.
</details>
<hr/>

### ❓ Q60. **How do you handle dynamic imports in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `next/dynamic`. It is an extension of `React.lazy` that supports SSR. It allows you to load components only when they are needed, reducing the initial bundle size.

> 💡 **Interviewer Focus:** Code splitting and optimization.
</details>
<hr/>

### ❓ Q61. **What are "Catch-all" routes?**
<details>
<summary><b>👀 Show Answer</b></summary>

By using `[...slug]` in the file or folder name, you can match paths with multiple segments. For example, `app/shop/[...slug]/page.js` matches `/shop/clothes`, `/shop/clothes/tops`, etc.

> 💡 **Interviewer Focus:** Advanced routing patterns.
</details>
<hr/>

### ❓ Q62. **What are "Optional Catch-all" routes?**
<details>
<summary><b>👀 Show Answer</b></summary>

By using `[[...slug]]` (double brackets), it works like a catch-all route but also matches the path without parameters. For example, `app/shop/[[...slug]]/page.js` also matches `/shop`.

> 💡 **Interviewer Focus:** Nuances of catch-all routing.
</details>
<hr/>

### ❓ Q63. **How do you use Sass in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js has built-in support for Sass. You just need to install the `sass` package, and you can import `.scss` or `.sass` files directly.

> 💡 **Interviewer Focus:** Styling ecosystem support.
</details>
<hr/>

### ❓ Q64. **How do you optimize images from external domains?**
<details>
<summary><b>👀 Show Answer</b></summary>

To optimize images from external domains, you must list them in the `images.remotePatterns` array in `next.config.js` for security reasons.

> 💡 **Interviewer Focus:** Security and configuration for images.
</details>
<hr/>

### ❓ Q65. **What is the purpose of `generateStaticParams`?**
<details>
<summary><b>👀 Show Answer</b></summary>

In the App Router, it replaces `getStaticPaths`. It is used to generate a list of static paths for dynamic segments that will be generated at build time.

> 💡 **Interviewer Focus:** Modern SSG dynamic paths.
</details>
<hr/>

### ❓ Q66. **How do you handle API route errors?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use standard `try/catch` blocks. In the catch block, return a response with an appropriate status code (e.g., 500) and an error message JSON.

> 💡 **Interviewer Focus:** Error handling in backend code.
</details>
<hr/>

### ❓ Q67. **How do you set custom headers in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

In `next.config.js`, you can export a `headers` function that returns an array of path and header objects.

> 💡 **Interviewer Focus:** Security headers and configuration.
</details>
<hr/>

### ❓ Q68. **What is the difference between `next dev` and `next start`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `next dev` starts Next.js in development mode with hot reloading and error reporting.
- `next start` starts Next.js in production mode, which requires running `next build` first.

> 💡 **Interviewer Focus:** Development vs Production workflows.
</details>
<hr/>

### ❓ Q69. **How do you read cookies in a Server Component?**
<details>
<summary><b>👀 Show Answer</b></summary>

Import `cookies` from `next/headers`. You can read cookies using `cookies().get('name')`.

> 💡 **Interviewer Focus:** Accessing request data in server components.
</details>
<hr/>

### ❓ Q70. **What is the purpose of `useRouter` in App Router vs Pages Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

- In Pages Router, `useRouter` from `next/router` provides the router object with pathname, query, etc.
- In App Router, `useRouter` from `next/navigation` only provides navigation methods (`push`, `replace`, `back`). To get search params, use `useSearchParams`.

> 💡 **Interviewer Focus:** Breaking changes between routers.
</details>
<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ React & Redux](./03_React_Redux.md) | [Home](./00_Index.md) | [➡️ React Native](./05_ReactNative.md) |
