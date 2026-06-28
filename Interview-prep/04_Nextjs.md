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

---

### 🛠️ **Deep Dive: Additional Features & Optimizations**

While React is a library focused on the **View layer** (UI components), Next.js provides the complete application infrastructure. Here is a breakdown of the key features and optimizations Next.js handles for you:

#### 1. **Advanced Routing Capabilities**
* **File-System Routing:** No need to configure third-party routing libraries (e.g., `react-router-dom`). Next.js uses folders/files to define routes (`pages` or `app` directory).
* **Nested Layouts:** Share UI (headers, sidebars) between pages without re-rendering, maintaining state.
* **Specialized Routing (App Router):** 
  * **Parallel Routes (`@slot`):** Render multiple pages in the same layout (e.g., dashboards, split-screens).
  * **Intercepting Routes (`(..)folder`):** Load a route inline in a modal while keeping context (e.g., photo feeds).

#### 2. **Flexible Rendering & Data Fetching Models**
Next.js allows you to mix and match different rendering strategies on a per-route basis:
* **Server-Side Rendering (SSR):** Renders HTML on the server for *every request*. Best for dynamic, user-specific data.
* **Static Site Generation (SSG):** Generates pages as static HTML at *build time*. Extremely fast and CDN-cacheable.
* **Incremental Static Regeneration (ISR):** Updates static pages in the background *after* building, without rebuilding the whole site.
* **Client-Side Rendering (CSR):** Renders in the browser (standard React behavior, activated with `'use client'`).
* **React Server Components (RSC):** Components render on the server, sending zero JS to the client. This reduces bundle size significantly.
* **Partial Prerendering (PPR):** Combines static shells (served instantly) with dynamic components (streamed in as they finish loading).

#### 3. **Automatic Optimizations (Performance)**
* **Image Optimization (`next/image`):** 
  * Automatically resizes and compresses images.
  * Serves modern formats (WebP, AVIF).
  * Implements lazy loading by default.
  * Prevents Cumulative Layout Shift (CLS) by requiring explicit size/ratio declarations.
* **Font Optimization (`next/font`):** Automatically downloads and self-hosts Google Fonts (or custom web fonts) at build time, eliminating external HTTP requests and layout shifts.
* **Script Optimization (`next/script`):** Allows fine-grained control over when third-party scripts (like analytics) load using strategies like `lazyOnload` or `afterInteractive`.
* **Link Prefetching (`next/link`):** Automatically prefetches route resources in the background when a link enters the user's viewport, making navigation near-instant.

#### 4. **Modern Build Tooling**
* **Rust-based Compilation:** Uses **SWC** (replacing Babel) and **Turbopack** (replacing Webpack) for extremely fast compilation, bundling, and hot-module reloading.
* **Automatic Code Splitting:** Breaks the JavaScript bundles into page-specific chunks. Users only download the code needed for the page they are currently viewing.

#### 5. **Full-Stack Capabilities**
* **API Routes & Route Handlers:** Write backend code, connect to databases, and build API endpoints within the same project.
* **Server Actions:** Submit forms and mutate server data directly from components without having to manually set up API routes.
* **Edge Middleware:** Run lightweight, fast JS code at edge servers before a request is completed, enabling fast geolocation routing, authentication checks, and redirects.

> 💡 **Interviewer Focus:** Understanding the difference between React (library) and Next.js (framework). Next.js provides the structural, performance, and server-side features needed to build production-ready applications, removing the need to configure them manually in a raw React project.
</details>
<hr/>

### ❓ Q2. **What is the difference between Next.js and React?**
<details>
<summary><b>👀 Show Answer</b></summary>

The fundamental difference is that **React is a library**, whereas **Next.js is a full-stack framework** built on top of React. 

In short: **React is the core UI engine; Next.js is the fully equipped car built around it.**

---

### 1. 🏗️ The "Library vs. Framework" Distinction (Inversion of Control)
*   **React (Library):** *You* call the library. You choose and configure your own build tools (Vite, Webpack), routing (`react-router-dom`), state management (Redux, Zustand), and deployment setups. You have complete freedom, but must write massive amounts of boilerplate.
*   **Next.js (Framework):** The framework calls *your* code. Next.js enforces structure (like file-system routing) and automatically manages compilation, bundling, server-side execution, and deployment optimizations out of the box.

---

### 2. 📊 Detailed Comparison Table

| Feature | React (Vanilla Client-Side) | Next.js (Framework) |
| :--- | :--- | :--- |
| **Category** | JavaScript Library for UI. | Full-Stack React Framework. |
| **Rendering** | **Client-Side Rendering (CSR)** only. The browser receives a blank HTML file and constructs the UI on the client. | **Pre-rendering:** Server-Side Rendering (SSR), Static Site Generation (SSG), ISR, and Server Components (RSC). |
| **Routing** | None. Must install and configure third-party libraries like `react-router-dom`. | **File-System Routing:** Files added to the `app/` folder automatically become URL paths. |
| **SEO** | Poor out-of-the-box (crawlers see a blank HTML shell initially). | Excellent (crawlers receive fully populated HTML generated on the server). |
| **Backend / API** | Frontend only. Requires a separate backend server (Express, Django) for API endpoints. | **Server-Side API Routes:** Write backend API handlers (`/api/...`) inside the same repository. |
| **Optimizations** | Manual (Webpack configurations, lazy loading code-splitting, custom image compressing). | Automatic (SWC compiler, code splitting, Image/Font/Script components, link prefetching). |

---

### 3. 🔍 Deep Dive into Routing and Rendering Differences

#### **A. File-System Routing vs. Code Routing**
*   In **React**, you define routes programmatically in JS files:
    ```javascript
    // React Router setup
    <BrowserRouter>
      <Routes>
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </BrowserRouter>
    ```
*   In **Next.js (App Router)**, the folder structure determines the route. No routing code is written:
    ```text
    src/app/
    ├── layout.js          # Shared shell UI
    ├── page.js            # URL: /
    └── about/
        └── page.js        # URL: /about
    ```

#### **B. Rendering Pipeline & SEO**
*   **React:** The server sends a single file `index.html` containing `<div id="root"></div>`. The user's browser runs a heavy JavaScript bundle to render the content. 
*   **Next.js:** The server compiles the React components into static HTML. When the user visits, the browser receives populated HTML immediately (giving fast initial load time and perfect SEO indexing), then loads a small JS bundle to make the HTML interactive (a process called **Hydration**).

---

> 💡 **Interviewer Focus:** Explain the architectural difference (**Inversion of Control**). Contrast **Client-Side Rendering (CSR)** with Next.js's **Pre-rendering** (SSR/SSG), and discuss how **File-System Routing** and built-in full-stack capabilities (API routes) speed up development.
</details>
<hr/>

### ❓ Q3. **Explain Server-Side Rendering (SSR).**
<summary><b>👀 Show Answer</b></summary>

In **Server-Side Rendering (SSR)**, the HTML of the page is generated on the server for **every single request**. When a user navigates to a URL, the server fetches the necessary data, renders the complete HTML page, and sends it back to the client browser.

#### ⚙️ How it works:
1. Browser requests a page.
2. Server fetches data from APIs/Database.
3. Server compiles React components into static HTML.
4. Browser receives populated HTML (instantly readable by crawlers/users) and displays it.
5. React **hydrates** (attaches event listeners to) the page to make it interactive.

```text
[ Browser ]                  [ Next.js Server ]            [ Database/API ]
     |                              |                              |
     |--- 1. Request Page --------->|                              |
     |                              |--- 2. Fetch Data ----------->|
     |                              |<-- 3. Return Data -----------|
     |                              |                              |
     |                              | [ Renders page HTML ]        |
     |<-- 4. Sends HTML ------------|                              |
     |                              |                              |
     | [ Displays HTML (static) ]   |                              |
     |<-- 5. Sends JS Bundle -------|                              |
     |                              |                              |
     | [ Hydration: page interactive]|                              |
```

#### 💻 Code Example:
* **App Router (Server Component):**
  ```javascript
  // app/page.js
  export default async function Page() {
    // cache: 'no-store' forces dynamic rendering on every request
    const res = await fetch('https://api.example.com/data', { cache: 'no-store' });
    const data = await res.json();
    
    return <main><h1>SSR Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```
* **Pages Router:**
  ```javascript
  // pages/index.js
  export async function getServerSideProps() {
    const res = await fetch('https://api.example.com/data');
    const data = await res.json();
    return { props: { data } };
  }
  
  export default function Page({ data }) {
    return <main><h1>SSR Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```

* **Analogy:** Like a made-to-order restaurant. The server compiles the page fresh for every request.
* **Industry Example:** A personalized user feed page (like Twitter/X or LinkedIn) or an e-commerce checkout page showing live stock availability and user-specific pricing.

> 💡 **Interviewer Focus:** Good for SEO, secure data fetches (hides API keys on server), but increases Server Load and Time to First Byte (TTFB).
</details>
<hr/>

### ❓ Q4. **Explain Static Site Generation (SSG).**
<details>
<summary><b>👀 Show Answer</b></summary>

In **Static Site Generation (SSG)**, the HTML of the page is generated once at **build time** (when you run `next build`). The pre-rendered HTML files are then stored and served from a Content Delivery Network (CDN), making them load almost instantly.

#### ⚙️ How it works:
1. Developer runs the build process.
2. Next.js fetches data and pre-renders components into static HTML/JSON files.
3. Files are deployed to a CDN.
4. When a user requests the page, the CDN serves the pre-built HTML instantly.

**At Build Time:**
```text
[ Developer ]                [ Next.js Build Engine ]      [ Database/API ]
     |                              |                              |
     |--- Runs 'next build' ------->|                              |
     |                              |--- 1. Fetch Data ----------->|
     |                              |<-- 2. Return Data -----------|
     |                              |                              |
     |                              | [ Pre-renders static HTML ]  |
     |                              | [ and JSON files ]           |
```

**At Request Time:**
```text
[ Browser ]                  [ CDN / Static Host ]
     |                              |
     |--- 1. Request Page --------->|
     |<-- 2. Serves Pre-built HTML -| (Instant response)
     |                              |
     | [ Displays HTML (static) ]   |
     |<-- 3. Serves JS Bundle ------|
     |                              |
     | [ Hydration: page interactive]|
```

#### 💻 Code Example:
* **App Router (Static by default):**
  ```javascript
  // app/page.js
  export default async function Page() {
    // Next.js caches fetch requests by default (force-cache)
    const res = await fetch('https://api.example.com/data');
    const data = await res.json();
    
    return <main><h1>SSG Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```
* **Pages Router:**
  ```javascript
  // pages/index.js
  export async function getStaticProps() {
    const res = await fetch('https://api.example.com/data');
    const data = await res.json();
    return { props: { data } };
  }
  
  export default function Page({ data }) {
    return <main><h1>SSG Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```

* **Analogy:** Like buying pre-packaged food at the store. The page is built once during build time.
* **Industry Example:** A company's marketing landing page, a public documentation site, or a privacy policy page that remains the same for all users and updates rarely.

> 💡 **Interviewer Focus:** Fastest page-load times and great SEO, but requires a full site rebuild if any page content changes.
</details>
<hr/>

### ❓ Q5. **What is Client-Side Rendering (CSR) in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

In **Client-Side Rendering (CSR)**, the server sends a minimal HTML shell (often just an empty `div`) and a large JavaScript bundle to the browser. The browser runs the JS to fetch data from APIs and construct the user interface dynamically.

In Next.js, you implement CSR by using the `'use client'` directive at the top of a component file, which tells the framework to bundle and execute it on the client side.

#### ⚙️ How it works:
1. Browser requests a page and gets an empty HTML file.
2. Browser downloads and executes the JavaScript bundle.
3. The React app runs, showing a loading state, and fetches data from the browser.
4. React renders the final content into the DOM.

```text
[ Browser ]                  [ Next.js Server ]            [ Database/API ]
     |                              |                              |
     |--- 1. Request Page --------->|                              |
     |<-- 2. Serves Empty HTML -----|                              |
     |    & JS bundle               |                              |
     |                              |                              |
     | [ Displays empty/loading ]   |                              |
     |                              |                              |
     |--- 3. Fetch Data (Client-side)----------------------------->|
     |<-- 4. Return Data JSON -------------------------------------|
     |                              |                              |
     | [ Renders UI on Client ]     |                              |
```

#### 💻 Code Example:
* **App/Pages Router (React hooks):**
  ```javascript
  'use client'; // Required at top in App Router
  
  import { useState, useEffect } from 'react';
  
  export default function Page() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
      fetch('https://api.example.com/data')
        .then((res) => res.json())
        .then((data) => {
          setData(data);
          setLoading(false);
        });
    }, []);
    
    if (loading) return <p>Loading...</p>;
    return <main><h1>CSR Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```

* **Analogy:** Like receiving a meal kit where you assemble/render the food in the browser.
* **Industry Example:** A private user dashboard behind a login wall (like a Trello board or SaaS analytics dashboard) where search engine indexing (SEO) is not needed, and interactions are highly stateful.

> 💡 **Interviewer Focus:** Poor SEO and slower initial page load, but rich and highly interactive user experience with zero server load after initial deployment.
</details>
<hr/>

### ❓ Q6. **Explain Incremental Static Regeneration (ISR).**
<details>
<summary><b>👀 Show Answer</b></summary>

**Incremental Static Regeneration (ISR)** allows developers to create or update static pages *after* the site has been built and deployed, without needing to rebuild the entire application. It combines the speed of SSG with the freshness of SSR.

#### ⚙️ How it works:
1. Page is built as static HTML (SSG) at build time.
2. A client requests the page. If the page is requested *before* the revalidation period (e.g., 60 seconds), Next.js serves the cached static page.
3. If requested *after* the revalidation period, the user still gets the cached page, but Next.js triggers a background page rebuild.
4. Once built successfully, the cache is updated, and future users see the new page.

```text
[ Browser ]                  [ Next.js Server / Cache ]    [ Database/API ]
     |                              |                              |
     |--- 1. Request Page --------->|                              |
     |                              | [ Checks cache validity ]    |
     |<-- 2. Serves Cached HTML ----| (Instant response)           |
     |                              |                              |
     |                              |--- 3. Trigger rebuild ------>|
     |                              |       (in background)        |
     |                              |                              |
     |                              |--- 4. Fetch Fresh Data ----->|
     |                              |<-- 5. Return Fresh Data -----|
     |                              |                              |
     |                              | [ Re-renders static HTML & ] |
     |                              | [ updates the Cache ]        |
```

#### 🛠️ Implementation & Code Example:
* **App Router:** Export a `revalidate` config variable.
  ```javascript
  // app/page.js
  export const revalidate = 60; // Revalidate this page every 60 seconds
  
  export default async function Page() {
    const res = await fetch('https://api.example.com/data');
    const data = await res.json();
    return <main><h1>ISR Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```
* **Pages Router:** Export `revalidate` prop from `getStaticProps`.
  ```javascript
  // pages/index.js
  export async function getStaticProps() {
    const res = await fetch('https://api.example.com/data');
    const data = await res.json();
    return { 
      props: { data },
      revalidate: 60, // Regenerate page in background after 60 seconds
    };
  }
  
  export default function Page({ data }) {
    return <main><h1>ISR Page</h1><pre>{JSON.stringify(data)}</pre></main>;
  }
  ```

* **Analogy:** Like a buffet. The food is pre-prepared, but the chef swaps out individual dishes in the background.
* **Industry Example:** A massive e-commerce site (like target.com) with 10,000+ products. Instead of rebuilding the entire site when product details change, ISR allows you to automatically update a specific product's page in the background on demand.

> 💡 **Interviewer Focus:** Solves the scale issue of SSG. Explain the "stale-while-revalidate" caching mechanism and how it reduces database/API load compared to SSR.
</details>
<hr/>

### ❓ Q7. **What are React Server Components (RSC) vs. Client Components?**
<details>
<summary><b>👀 Show Answer</b></summary>

With Next.js App Router, components are **Server Components (RSC)** by default. They can be explicitly defined as **Client Components** using the `'use client'` directive at the very top of the file.

#### 📊 Differences Table:

| Feature | Server Components (RSC) | Client Components |
| :--- | :--- | :--- |
| **Execution** | Executes only on the server. | Prerendered on server, hydrated/executed on client. |
| **JS Bundle Size** | Ships **0 KB** of JS to the client. | Ships JavaScript bundle for execution. |
| **Data Fetching** | Can fetch database data or use secure APIs directly. | Fetches data via standard client `fetch` / hooks. |
| **React Hooks** | Cannot use hooks (`useState`, `useEffect`, etc.). | Can use all React state and lifecycle hooks. |
| **Browser APIs** | No access to browser APIs (`window`, `localStorage`). | Has full access to browser APIs. |

```text
[ Browser ]                  [ Next.js Server ]            [ Database/API ]
     |                              |                              |
     |--- 1. Request Page --------->|                              |
     |                              |--- 2. Fetch Data (Direct DB) ->|
     |                              |<-- 3. Return Data -------------|
     |                              |                              |
     |                              | [ Renders RSCs to virtual ]  |
     |                              | [ DOM JSON payload ]         |
     |                              |                              |
     |<-- 4. Sends HTML & RSC ------|                              |
     |    payload (0 KB component JS)|                              |
     |                              |                              |
     | [ Displays page, downloads ] |                              |
     | [ Client Comp JS only ]      |                              |
```

#### 💻 Code Example:
* **ServerComponent.js (Default RSC):**
  ```javascript
  import ClientComponent from './ClientComponent';
  
  export default async function ServerComponent() {
    // Fetch data securely and directly on the server without API routes
    const users = await db.query('SELECT * FROM users'); 
    
    return (
      <div>
        <h1>Server Component (0 KB shipped JavaScript)</h1>
        {/* Pass fetched server data to a Client Component */}
        <ClientComponent initialUsers={users} />
      </div>
    );
  }
  ```
* **ClientComponent.js (Client Component):**
  ```javascript
  'use client';
  
  import { useState } from 'react';
  
  export default function ClientComponent({ initialUsers }) {
    const [likes, setLikes] = useState(0); // Interactive hooks allowed here
    
    return (
      <div>
        <button onClick={() => setLikes(likes + 1)}>Likes: {likes}</button>
        <ul>
          {initialUsers.map(user => <li key={user.id}>{user.name}</li>)}
        </ul>
      </div>
    );
  }
  ```

* **Analogy:** The server does the heavy lifting (e.g., fetching DB data) and sends only the final visual layout. The browser doesn't have to download or run JS to display it.
* **Industry Example:** A content-heavy help desk page that uses heavy external packages (like a Markdown-to-HTML parser or a syntax highlighter). Using RSC keeps these packages on the server, saving megabytes of JS from being downloaded by the browser.

> 💡 **Interviewer Focus:** RSCs are NOT a replacement for SSR. SSR is a rendering process; RSCs are a component architecture that reduces client-side JavaScript. They work together.
</details>
<hr/>

### ❓ Q8. **Explain how Partial Prerendering (PPR) works in Next.js.**
<details>
<summary><b>👀 Show Answer</b></summary>

**Partial Prerendering (PPR)** is an optimization that allows you to combine static and dynamic rendering on the same route. Next.js prerenders the static shell of a page and leaves dynamic "holes" that are streamed in as they are generated on the server using React Suspense.

#### ⚙️ How it works:
1. When a user requests a page, the static HTML shell (navbars, grids) is served immediately from the CDN.
2. The dynamic components (cart status, user recommendations) are executed on the server.
3. The server streams the HTML for the dynamic components into the open HTTP response as soon as they finish rendering.

```text
[ Browser ]                  [ Next.js Server / CDN ]      [ Database/API ]
     |                              |                              |
     |--- 1. Request Page --------->|                              |
     |<-- 2. Serves Pre-built HTML -|                              |
     |    Static Shell (instantly)  |                              |
     |                              |                              |
     | [ Displays Nav/Layout ]      |                              |
     |                              |--- 3. Fetch Dynamic Data --->| (streamed as they complete)
     |                              |<-- 4. Return Data -----------|
     |                              |                              |
     |                              | [ Renders dynamic components ]|
     |<-- 5. Streams HTML Chunks ---| (Progressive streaming)      |
     |    (via Suspense boundary)   |                              |
     |                              |                              |
     | [ Dynamic components appear ]|                              |
```

#### 💻 Code Example:
* **App Router with Suspense (PPR):**
  ```javascript
  import { Suspense } from 'react';
  import StaticShellHeader from './StaticShellHeader';
  import DynamicCartDetails from './DynamicCartDetails'; // contains async fetch
  
  export default function Page() {
    return (
      <main>
        {/* Prerendered statically at build time & served instantly */}
        <StaticShellHeader />
        
        {/* The Suspense fallback acts as a static shell boundary.
            Everything inside Suspense is dynamically generated on-demand
            and streamed over the wire once fetched. */}
        <Suspense fallback={<div>Loading Cart...</div>}>
          <DynamicCartDetails />
        </Suspense>
      </main>
    );
  }
  ```

* **Analogy:** Like walking into a fast-food joint where they hand you a cup for your drink instantly (static shell), while you wait a moment for the burger (dynamic components) to cook.
* **Industry Example:** An Amazon-like product page. The page structure and description load instantly from a global CDN cache (static shell), while personalized recommendations and cart details stream in dynamically as they are fetched from databases.

> 💡 **Interviewer Focus:** PPR provides the speed of static sites (SSG) with the personalization of server sites (SSR) in a single page. It is enabled using React `Suspense` boundaries.
</details>
<hr/>

### ❓ Q9. **How does file-based routing work in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js has a file-system based router.
- In **Pages Router**: Files in the `pages` directory automatically become routes (e.g., `pages/about.js` -> `/about`).
- In **App Router**: Folders in the `app` directory define routes, and a `page.js` file makes the route accessible (e.g., `app/about/page.js` -> `/about`).

> 💡 **Interviewer Focus:** Familiarity with Next.js folder structure.
</details>
<hr/>

### ❓ Q10. **What is the `Image` component in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

The Next.js `Image` component (`next/image`) is an extension of the HTML `<img>` element. It automatically optimizes images for:
- **Size:** Serves correctly sized images for each device.
- **Format:** Uses modern formats like WebP and AVIF.
- **Loading:** Lazy loads images by default.

> 💡 **Interviewer Focus:** Core performance feature of Next.js.
</details>
<hr/>

## 🟡 Intermediate Level

### ❓ Q11. **What is the purpose of the `Link` component?**
<details>
<summary><b>👀 Show Answer</b></summary>

The `Link` component (`next/link`) is used for client-side navigation between pages. It pre-fetches pages in the background as they appear in the viewport, making transitions near-instant.

#### 🔄 Navigation Flow & Lifecycle:

```text
[ Link Component ] ---> (1. Enters Viewport) ---> [ Intersection Observer ]
                                                          |
                                                          v (2. Background Prefetch)
[ Router Cache ] <--- (3. Stores Payload & JS) <--- [ Next.js Server / CDN ]
       |
       v (4. User clicks Link)
[ Intercept Click ] ---> (5. Prevent Hard Refresh)
       |
       v
[ Cache Lookup ] ---(Hit)---> [ Render Immediately ] (6. Soft Navigation)
       |
    (Miss)
       v
[ Fetch from Server ]
```

1. **Viewport Detection:** In production, Next.js uses an `IntersectionObserver` to detect when a `<Link>` component enters the user's viewport.
2. **Prefetching:** Once visible, Next.js automatically prefetches the target page in the background:
   - *Static Routes:* Prefetches the entire route payload (React Server Component payload and JavaScript).
   - *Dynamic Routes:* Prefetches up to the nearest layout segment.
3. **Router Cache:** The prefetched payload is stored in the browser's in-memory Router Cache.
4. **Soft Navigation:** When clicked, Next.js prevents a full page reload (`event.preventDefault()`). It reads the route payload from the cache (or fetches it on-demand if a miss), updates the URL via HTML5 history API (`pushState`), and performs a client-side transition.
5. **Partial Render:** Only components within segments that changed are re-rendered; shared layouts (like navigation or sidebar) preserve their state and do not re-render.

#### 💡 `<a>` vs `<Link>` Comparison:
* **`<a>` tag:** Performs a hard navigation, causing a full page refresh. All React state is lost, and the browser re-downloads and re-executes all JS/CSS.
* **`<Link>` component:** Performs a soft navigation, preserving React state and layout state. It only downloads the code and payload for the specific page segment being navigated to.

> 💡 **Interviewer Focus:** Client-side navigation vs traditional anchor tags, background prefetching, and the in-memory Router Cache.
</details>
<hr/>

### ❓ Q12. **What are API Routes in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

API routes provide a solution to build your API with Next.js. Any file inside the `pages/api` (or `app/api` for App Router) directory is mapped to `/api/*` and will be treated as an API endpoint instead of a page.

> 💡 **Interviewer Focus:** Ability to build full-stack apps without a separate backend.
</details>
<hr/>

### ❓ Q13. **What is the difference between the `app` directory and the `pages` directory?**
<details>
<summary><b>👀 Show Answer</b></summary>

The `app` directory (App Router) and the `pages` directory (Pages Router) represent a paradigm shift in how Next.js applications are structured, rendered, and optimized.

#### 📊 Core Differences Comparison:

| Feature | `pages` Directory (Pages Router) | `app` Directory (App Router) |
| :--- | :--- | :--- |
| **Routing Model** | **File-based**: Any file in `pages/` becomes a route (e.g., `pages/about.js` -> `/about`). | **Folder-based**: Folders define paths; a special `page.js` file is required to make it accessible (e.g., `app/about/page.js` -> `/about`). |
| **Component Model** | Standard Client-side components. | **React Server Components (RSC)** by default. Opt-in to client interactivity using `"use client"`. |
| **Layouts** | Global layout in `_app.js` or custom per-page wrapper logic. Shared layouts re-render on navigation. | **Nested Layouts** natively supported via `layout.js`. Shared layouts preserve state and do not re-render. |
| **Data Fetching** | Page-level hooks only: `getStaticProps`, `getServerSideProps`, `getStaticPaths`. | Component-level fetching using standard `async/await` directly inside Server Components. |
| **Streaming & Suspense** | Not supported out-of-the-box (waits for full page render before sending to client). | Built-in streaming and progressive loading via React Suspense and `loading.js`. |
| **Metadata & SEO** | Managed manually using the `<Head>` component from `next/head`. | Native Metadata API (`export const metadata` or `generateMetadata()`). |
| **Special File Conventions** | `_app.js`, `_document.js`, `404.js`, `500.js` | `layout.js`, `page.js`, `loading.js`, `error.js`, `not-found.js`, `template.js` |

---

#### 🔍 Deep-Dive Details:

##### 1. Routing & Co-location
* **Pages Router:** Every file in the directory is treated as a route. This prevents you from co-locating tests, styles, or components alongside the page file (they had to live in separate folders like `/components` or `/styles`).
* **App Router:** Only `page.js` (or `route.js` for API endpoints) is mapped to the URL. You can freely co-locate other components, hooks, tests, or styling files in the same folder.

##### 2. Rendering Paradigm (RSC vs CSR/SSR)
* **Pages Router:** The entire page is bundled and shipped to the client, requiring hydration. Even if a component is purely static, its JS is shipped.
* **App Router:** Runs components on the server first. Static components compile to pure HTML/JSON and ship **0 KB of client-side JavaScript**. Client-side JS is only shipped for components marked with `"use client"`.

##### 3. Modern Data Fetching
* **Pages Router:** You had to fetch all data at the top-level page block (`getStaticProps`) and drill props down to children.
* **App Router:** You fetch data directly inside the component that needs it using standard `async/await`. Next.js extends the native `fetch` API to handle caching and revalidation automatically, rendering props drilling obsolete.

> 💡 **Interviewer Focus:** Transition from client-first rendering to server-first architecture (RSC), native nested layouts, and component-level async data fetching.
</details>
<hr/>

### ❓ Q14. **How do you fetch data in the App Router?**
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

### ❓ Q15. **How do you create dynamic routes in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

By using brackets in the file name or folder name.
- Pages Router: `pages/post/[id].js` accesses `/post/1`.
- App Router: `app/post/[id]/page.js` accesses `/post/1`.
You access the parameter via `useRouter` or from the `params` prop in the component.

> 💡 **Interviewer Focus:** Handling dynamic segments in URLs.
</details>
<hr/>

### ❓ Q16. **What is the purpose of `getStaticPaths` in Pages Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

When using **Static Site Generation (SSG)** (`getStaticProps`) on a **dynamic route** (e.g., `pages/posts/[id].js`), Next.js needs to pre-render the pages at build time. 

Because the route is dynamic, Next.js does not know how many posts you have (should it build `/posts/1`, `/posts/2`, or `/posts/999`?). **`getStaticPaths` provides Next.js with a list of all dynamic paths to pre-render during the build process.**

---

#### ⚙️ How It Works:

1. **At Build Time:** Next.js runs `getStaticPaths`.
2. **Path Resolution:** The function queries your database/API to fetch all possible route parameters (e.g., all post IDs).
3. **Pre-rendering:** Next.js iterates over the returned path list and calls `getStaticProps` for each path, generating static HTML and JSON files.

---

#### 💻 Code Example:

```javascript
// pages/posts/[id].js

// 1. Tell Next.js which paths to pre-render at build time
export async function getStaticPaths() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();

  // Format required: { params: { id: '...' } }
  const paths = posts.map((post) => ({
    params: { id: post.id.toString() }, 
  }));

  return { 
    paths, 
    fallback: false // See fallback behaviors below
  };
}

// 2. Fetch the data for a single page at build time
export async function getStaticProps({ params }) {
  const res = await fetch(`https://api.example.com/posts/${params.id}`);
  const post = await res.json();

  return { props: { post } };
}

export default function PostPage({ post }) {
  return <h1>{post.title}</h1>;
}
```

---

#### 🔀 Fallback Behaviors (`fallback` key):

* **`fallback: false`:** 
  * If a user requests a path not returned by `getStaticPaths` (e.g., a new post created after the build), Next.js immediately returns a **404 page**.
* **`fallback: true`:** 
  * Next.js instantly serves a fallback/loading state (e.g., `router.isFallback === true`).
  * In the background, Next.js generates the requested HTML on the server.
  * Once finished, the browser swaps the loading state with the page content, and Next.js caches this page for future requests.
* **`fallback: 'blocking'`:**
  * The browser blocks/waits for the page to be rendered on the server (no loading state is shown; it behaves like SSR for the first load).
  * Once rendered, the page is served and cached for all future visitors.

---

#### 🎨 Analogy: The Custom Print Shop
* **Static page (`/about`):** A standard poster. You can print 100 copies in advance (at build time) because it is identical for everyone.
* **Dynamic page (`/posts/[id]`):** Customized posters for different clients.
  * **Without `getStaticPaths`:** You have no idea who your clients are, so you cannot print anything in advance.
  * **With `getStaticPaths`:** You fetch your VIP client list (`getStaticPaths`) and pre-print posters for those clients.
  * **`fallback: false`:** If a new client walks in, you refuse them service (404).
  * **`fallback: 'blocking'`:** If a new client walks in, you ask them to wait a few minutes while you print their poster on demand, and save a copy for anyone else with that name.

> 💡 **Interviewer Focus:** Dynamic SSG, the contract between `getStaticPaths` and `getStaticProps`, and the nuances of the three `fallback` behaviors (`false`, `true`, `'blocking'`).
</details>
<hr/>

### ❓ Q17. **How does Middleware work in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Middleware** in Next.js allows you to run code **before** a request is completed. It intercepts the incoming HTTP request and can inspect, modify, or block it before it reaches the routing system (pages or APIs).

---

#### 🌐 Execution & Placement (The Edge Runtime)
Middleware runs on the **Edge Runtime** (lightweight Node.js subset APIs) close to the user's geographical location. This ensures extremely fast response times, enabling checks (like auth or geolocation) to happen in milliseconds before server latency is incurred.

---

#### 🔄 Request Lifecycle Flow:

```text
[ Browser Request ]
        |
        v
[ Edge Middleware ]  <--- (Runs first: inspects cookies, headers, URL)
        |
        +------> [ Redirect ] ---------> (Sends 302/301 response immediately back to browser)
        |
        +------> [ Rewrite ] ----------> (Proxy: Internally changes page source, browser URL stays same)
        |
        +------> [ Block / Respond ] --> (Returns direct response, e.g. 401 JSON API response)
        |
        v [ Continue / Modify Headers ]
[ Next.js Page / API Router ] ---> [ Response back to Browser ]
```

---

#### 💻 Code Example:

Create a `middleware.js` (or `.ts`) file in the **root** of your project (same level as `pages` or `app`).

```javascript
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
  const token = request.cookies.get('session-token')?.value;

  // 1. Redirect if user is not authenticated and trying to access private dashboard
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. Add custom request headers (passed to server components/APIs)
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-custom-header', 'hello-from-middleware');

  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
}

// 3. Define matching paths (Which routes trigger this middleware)
export const config = {
  matcher: ['/dashboard/:path*', '/api/secure/:path*'],
};
```

---

#### 🛠️ 5 Common Actions in Middleware:

1. **`NextResponse.next()`**: Allows the request to proceed to its target destination.
2. **`NextResponse.redirect()`**: Redirects the client to another URL (changes the browser URL bar).
3. **`NextResponse.rewrite()`**: Rewrites the destination path internally (displays target content while keeping the original URL in the browser bar - perfect for A/B testing).
4. **Header Manipulation**: Appends custom request/response headers or cookies.
5. **Direct Response**: Returns direct HTML/JSON (useful for rate-limiting or API blocking).

---

#### 🎨 Common Use Cases:
* **Authentication/Authorization:** Checking token validity before hitting the server.
* **Localization (i18n):** Detecting user language preferences from headers and redirecting to `/[locale]/`.
* **A/B Testing:** Dynamically serving different buckets of code using internal rewrites.
* **Security & Bot Protection:** Blocking suspicious traffic or setting custom security headers.

> 💡 **Interviewer Focus:** Understanding the Edge Runtime execution, the differences between Redirect vs. Rewrite, and defining targeted routes using `matcher` config arrays.
</details>
<hr/>

### ❓ Q18. **What is "Streaming" in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Streaming allows you to break down the page's HTML into smaller chunks and progressively send those chunks from the server to the client. This means parts of the page can be displayed sooner without waiting for all the data to load. Supported via `loading.js` files in App Router.

> 💡 **Interviewer Focus:** Improving perceived performance and Time to First Byte (TTFB).
</details>
<hr/>

### ❓ Q19. **How do you handle SEO in the App Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

By exporting a `metadata` object or generating it dynamically using `generateMetadata` function in your `layout.js` or `page.js`.
```javascript
export const metadata = { title: 'My Page' };
```

> 💡 **Interviewer Focus:** Shift from `next/head` to the Metadata API.
</details>
<hr/>

### ❓ Q20. **What is the difference between `getServerSideProps` and `getStaticProps`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `getServerSideProps` fetches data on **every request** (SSR).
- `getStaticProps` fetches data at **build time** (SSG).

> 💡 **Interviewer Focus:** Classical Pages Router question.
</details>
<hr/>

### ❓ Q21. **How do you optimize fonts in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js includes built-in automatic font optimization. Using `next/font`, you can use Google Fonts (or custom fonts) with zero layout shift. It downloads font files at build time and hosts them with your static assets.

> 💡 **Interviewer Focus:** Avoiding Layout Shift (CLS).
</details>
<hr/>

## 🔴 Advanced Level

### ❓ Q22. **Explain the concept of "Edge Runtime" in Next.js.**
<details>
<summary><b>👀 Show Answer</b></summary>

The Edge Runtime is a subset of Node.js APIs that are lightweight and can run on CDN edge nodes. It is much faster and has lower latency than a full Node.js server. Next.js uses it for Middleware and can use it for API routes and pages.

> 💡 **Interviewer Focus:** Understanding edge computing and its limitations (no native Node modules like `fs`).
</details>
<hr/>

### ❓ Q23. **How do you implement Server Actions in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Server Actions are asynchronous functions that are executed on the server. They can be defined in Server Components or separate files with the `'use server'` directive. They allow you to handle form submissions and data mutations without manually creating an API route.

> 💡 **Interviewer Focus:** Modern full-stack data mutation paradigm in Next.js.
</details>
<hr/>

### ❓ Q24. **What is "Parallel Routes" and when would you use them?**
<details>
<summary><b>👀 Show Answer</b></summary>

Parallel Routes allow you to simultaneously or conditionally render one or more pages in the same layout. They are defined using "slots" (e.g., `@folder`). Useful for complex dashboards or modals where you want to maintain state or independent loading states.

> 💡 **Interviewer Focus:** Advanced App Router feature for complex UIs.
</details>
<hr/>

### ❓ Q25. **What is "Intercepting Routes"?**
<details>
<summary><b>👀 Show Answer</b></summary>

Intercepting routes allows you to load a route within the current layout while keeping the context of the current page. For example, clicking a photo opens it in a modal over the feed, but reloading the URL opens the photo on its own page. Defined using `(..)folder` syntax.

> 💡 **Interviewer Focus:** Advanced UX patterns supported by the router.
</details>
<hr/>

### ❓ Q26. **How does caching work in the App Router?**
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

### ❓ Q27. **How do you handle authentication in Middleware?**
<details>
<summary><b>👀 Show Answer</b></summary>

Read the session cookie or token from the request. Verify it (e.g., using a JWT library that works on the Edge). If valid, proceed. If invalid, redirect to the login page using `NextResponse.redirect`.

> 💡 **Interviewer Focus:** Securing routes before they even reach the server.
</details>
<hr/>

### ❓ Q28. **What are the limitations of React Server Components?**
<details>
<summary><b>👀 Show Answer</b></summary>

- They cannot use State or Effects (no `useState`, `useEffect`).
- They cannot use browser-only APIs (like `window` or `document`).
- They cannot pass functions as props to Client Components (props must be serializable).

> 💡 **Interviewer Focus:** Understanding the boundaries between server and client.
</details>
<hr/>

### ❓ Q29. **How do you debug a Next.js application in production?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use structured logging (sent to a log management service like Datadog or Axiom). Use OpenTelemetry for tracing. Vercel provides built-in analytics and speed insights. Source maps can be enabled for production if secured.

> 💡 **Interviewer Focus:** Observability in production environments.
</details>
<hr/>

## 🟣 Expert Level

### ❓ Q30. **Architect a strategy for migrating a large Pages Router application to the App Router.**
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

### ❓ Q31. **How would you optimize a Next.js site to achieve a perfect 100 score on Lighthouse (Core Web Vitals)?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. **LCP:** Use `next/image` with priority for above-the-fold images. Use SSG or ISR over SSR where possible.
2. **FID / INP:** Minimize Client-side JS. Use Server Components to ship zero JS for static parts.
3. **CLS:** Use fixed sizes for images or aspect ratio containers. Use `next/font` to prevent font swap layout shifts.
4. **General:** Use dynamic imports for heavy components not needed on initial load. Ensure efficient caching.

> 💡 **Interviewer Focus:** Practical knowledge of Core Web Vitals and Next.js optimization features.
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

### ❓ Q71. **How do you configure custom cache handlers with Redis in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js allows configuring custom cache storage (instead of local file-system caching) by setting up a custom Cache Handler.
- **Implementation:**
  - Create a `cache-handler.js` file.
  - Implement the `get`, `set`, and `revalidateTag` methods interface using a Redis client (like `ioredis`).
  - In `next.config.js`, configure the path: `experimental: { cacheHandler: require.resolve('./cache-handler.js') }`.
  - This is critical for scaling Next.js in containerized multi-node environments (like Kubernetes) where file-system cache is not shared.

> 💡 **Interviewer Focus:** Distributing page caches across load-balanced application instances.
</details>
<hr/>

### ❓ Q72. **Explain the difference between Edge Runtime and Node.js Runtime in Next.js.**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Node.js Runtime:**
  - Standard Node environment.
  - Supports all Node.js APIs and libraries (e.g. `fs`, net, full cryptography packages).
  - Higher cold start latency.
- **Edge Runtime:**
  - Built on V8 engine isolates (similar to Cloudflare Workers).
  - Supports only lightweight APIs (Subset of Web APIs like `fetch`, `Headers`, `Request`, `Response`).
  - Cannot access native Node.js APIs (e.g., no `fs`).
  - Near-zero cold starts, making it ideal for fast global routing.

> 💡 **Interviewer Focus:** Operational limits and API compatibility differences.
</details>
<hr/>

### ❓ Q73. **How do you secure Next.js Server Actions against CSRF and authorization vulnerabilities?**
<details>
<summary><b>👀 Show Answer</b></summary>

Server Actions behave like POST API endpoints, meaning they are vulnerable if not secured.
- **Security Protocols:**
  - **CSRF:** Next.js automatically sets checking headers for Server Actions to guard against simple CSRF attacks.
  - **Authentication:** Always fetch and verify session tokens (e.g. via `getServerSession()` or JWT tokens) *inside* the Server Action function body before executing write changes.
  - **Input Validation:** Enforce strict type validation using schemas (e.g. Zod) to block malicious payload injections.

> 💡 **Interviewer Focus:** Security: treating Server Actions with the same security checks as standard REST API endpoints.
</details>
<hr/>

### ❓ Q74. **How does React Server Component (RSC) streaming work under the hood?**
<details>
<summary><b>👀 Show Answer</b></summary>

RSC streaming allows sending HTML fragments to the client as soon as they are rendered.
- **Mechanism:**
  - Uses HTTP **Chunked Transfer-Encoding**.
  - Next.js opens a single HTTP connection. The server renders static layouts first and streams them.
  - Slow database-bound components wrapped in `<Suspense>` are replaced by placeholder skeletons.
  - Once the server resolves the data and renders the component, it streams the final HTML chunk along with inline script blocks to replace the fallback skeleton in the DOM dynamically.

> 💡 **Interviewer Focus:** Progressive rendering, connection streaming, and DOM replacements.
</details>
<hr/>

### ❓ Q75. **What is the difference between `revalidatePath` and `revalidateTag`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **`revalidatePath(path)`**: Purges cached data for a specific URL path. Useful for updating specific page layouts (e.g., `/products/123`).
- **`revalidateTag(tag)`**: Purges cached data across *any* route that fetched data using a specific tag parameter: `fetch(url, { next: { tags: ['products'] } })`. Offers finer control, allowing updates to multiple layouts with a single cache tag purge.

> 💡 **Interviewer Focus:** Granular caching and CDN purging strategies.
</details>
<hr/>

### ❓ Q76. **How do you configure dynamic route segment configurations like force-static and force-dynamic?**
<details>
<summary><b>👀 Show Answer</b></summary>

You configure page behavior by exporting segment config constants from the page file:
- `export const dynamic = 'force-static'`: Forces caching and static generation, ignoring headers or search parameters.
- `export const dynamic = 'force-dynamic'`: Disables caching, forcing server rendering on every request (similar to `getServerSideProps`).
- `export const revalidate = 60`: Sets ISR cache TTL to 60 seconds.

> 💡 **Interviewer Focus:** Page-level caching configurations.
</details>
<hr/>

### ❓ Q77. **Explain Intercepting Routes and provide a common use case.**
<details>
<summary><b>👀 Show Answer</b></summary>

Intercepting Routes allows loading a route from another part of the application inside the current layout.
- **Syntax:** `(.)` matches segments on the same level, `(..)` matches one level above.
- **Use Case: Photo Feed Modal.**
  - Clicking a photo in a feed opens the photo details inside a modal overlay overlay. The URL updates to `/photo/12` but the feed remains in the background (intercepted route).
  - Refreshing the page (or sharing the link) ignores the interception, loading the photo details as a full standalone page.

> 💡 **Interviewer Focus:** Dynamic routing and preserving page state.
</details>
<hr/>

### ❓ Q78. **How does Next.js handle Hydration Mismatches, and how do you resolve them?**
<details>
<summary><b>👀 Show Answer</b></summary>

A hydration mismatch occurs when the pre-rendered server HTML differs from the initial HTML rendered by the client browser.
- **Common Causes:**
  - Accessing browser-only globals (like `window` or `localStorage`) during initial render.
  - Rendering dynamic dates (like `new Date()`) that change between server render and client load.
- **Resolution:**
  - Use `useEffect` to trigger client-only renders after mount.
  - Disable SSR for specific components using `next/dynamic`: `const NoSSR = dynamic(() => import(...), { ssr: false })`.
  - Use the `suppressHydrationWarning` attribute (only for small discrepancies).

> 💡 **Interviewer Focus:** Hydration cycle mechanics and debugging tools.
</details>
<hr/>

### ❓ Q79. **How do you implement local static exports in Next.js, and what are its limitations?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Setup:** Configure `output: 'export'` in `next.config.js`. Running `next build` generates raw HTML, CSS, and JS assets in an `out` folder.
- **Limitations:**
  - Disables server features like API routes, middleware, redirects/rewrites, dynamic SSR, ISR, and standard Image Optimization (which requires a server).

> 💡 **Interviewer Focus:** Export architectures (building static sites for deployment on S3/Cloudflare Pages).
</details>
<hr/>

### ❓ Q80. **What is the purpose of the next/font component, and why is it preferred over Google Web Fonts?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **`next/font`**: Downloads font files at build time and hosts them locally inside the app bundle.
- **Why preferred:**
  - Eliminates network requests to Google Fonts APIs during page loads, improving privacy.
  - Zero Layout Shift (CLS): It automatically generates fallback system fonts with matching sizing descriptors, preventing layout shifts when the custom font loads.

> 💡 **Interviewer Focus:** Page performance optimization and CLS reduction.
</details>
<hr/>

### ❓ Q81. **Explain how you would deploy a Next.js app in a multi-tenant monorepo with Turborepo.**
<details>
<summary><b>👀 Show Answer</b></summary>

In Turborepo:
- Create separate packages for shared components (`@repo/ui`), configurations (`@repo/eslint-config`), and business logic.
- Reference these shared packages in the Next.js `package.json`.
- In `next.config.js`, configure `transpilePackages: ['@repo/ui']` so Next.js transpiles the shared TypeScript packages during bundling.

> 💡 **Interviewer Focus:** Monorepo architecture and build speed optimizations.
</details>
<hr/>

### ❓ Q82. **How do you write middleware in Next.js that runs only on specific routes?**
<details>
<summary><b>👀 Show Answer</b></summary>

Export a `config` object containing a `matcher` array from the `middleware.js` file:
```javascript
export const config = {
  matcher: ['/dashboard/:path*', '/api/secure/:path*']
};
```
This forces the middleware to run only on matching routes, bypassing static assets and public pages to save execution resources.

> 💡 **Interviewer Focus:** Performance tuning and limiting middleware execution scopes.
</details>
<hr/>

### ❓ Q83. **What is the purpose of unstable_cache in the App Router?**
<details>
<summary><b>👀 Show Answer</b></summary>

`unstable_cache` allows caching the results of expensive database calls or calculations across server requests:
```javascript
import { unstable_cache } from 'next/cache';
const getCachedUser = unstable_cache(
  async (id) => db.findUser(id),
  ['user-cache-key'],
  { tags: ['users'], revalidate: 3600 }
);
```

> 💡 **Interviewer Focus:** Cache abstraction outside standard fetch functions.
</details>
<hr/>

### ❓ Q84. **Explain how next/image optimizes images under the hood.**
<details>
<summary><b>👀 Show Answer</b></summary>

`next/image` performs multiple automatic optimizations:
1. **Format Conversion:** Converts images to modern formats (WebP/AVIF) based on browser support headers.
2. **Resizing:** Dynamically resizes images based on the requested layout width.
3. **Lazy Loading:** Images are lazy-loaded by default, loading only when they approach the viewport.
4. **Placeholder Skeletons:** Renders blur-up placeholders to prevent Layout Shift.

> 💡 **Interviewer Focus:** Automated asset optimization pipeline.
</details>
<hr/>

### ❓ Q85. **What is the difference between parallel routing and route interception?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Parallel Routing (`@slot`):** Renders multiple pages simultaneously inside the same layout (useful for dashboards with different panels or tabs).
- **Route Interception (`(.)route`):** Loads a route inside a modal overlay, while keeping the background context page active.

> 💡 **Interviewer Focus:** Advanced UI layouts in the App Router.
</details>
<hr/>

### ❓ Q86. **How do you handle redirects inside Server Actions?**
<details>
<summary><b>👀 Show Answer</b></summary>

Import `redirect` from `next/navigation`. Call it directly inside the Server Action:
```javascript
'use server';
import { redirect } from 'next/navigation';
export async function submitForm(data) {
  // process data
  redirect('/success');
}
```
*Note: Under the hood, `redirect` throws a special exception that Next.js catches to handle the redirect, so do not wrap it inside try/catch blocks.*

> 💡 **Interviewer Focus:** Control flow exception handling.
</details>
<hr/>

### ❓ Q87. **How do you configure security headers in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Define custom headers in `next.config.js`:
```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'Content-Security-Policy', value: "default-src 'self'" },
          { key: 'X-Frame-Options', value: 'DENY' }
        ]
      }
    ];
  }
};
```

> 💡 **Interviewer Focus:** Securing headers at the framework layer.
</details>
<hr/>

### ❓ Q88. **What is Draft Mode in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Draft Mode allows users to view draft content from a Headless CMS on static pages without rebuilding the entire site.
- **How it works:** Enabling Draft Mode sets a cookie. Subsequent requests bypass the static build cache and render pages dynamically on the server, fetching live draft content from the CMS.

> 💡 **Interviewer Focus:** Static site CMS editing workflows.
</details>
<hr/>

### ❓ Q89. **What are the limitations of using WebSockets inside Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Next.js is designed to run in serverless environments (like Vercel).
- **Limitations:**
  - Serverless functions have execution time limits and cannot maintain persistent TCP connections (WebSockets).
  - **Solution:** Host WebSocket servers separately (on ECS/EC2) or use managed pub/sub services (like Pusher or Ably) while calling them from Next.js client components.

> 💡 **Interviewer Focus:** Serverless limitations and persistent connection management.
</details>
<hr/>

### ❓ Q90. **How do you analyze package dependencies bundle size in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `@next/bundle-analyzer`:
1. Install the package.
2. Configure it in `next.config.js`.
3. Run `ANALYZE=true next build`. This generates interactive HTML reports showing size metrics for each JS bundle.

> 💡 **Interviewer Focus:** Eliminating bloated dependency libraries.
</details>
<hr/>

### ❓ Q91. **What is the difference between static metadata and dynamic metadata?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Static Metadata:** Defined by exporting a static `metadata` object from a page/layout.
- **Dynamic Metadata:** Defined by exporting a `generateMetadata` function. It receives routing parameters and dynamically fetches data (e.g. product title from DB) to return the metadata object, optimizing SEO.

```javascript
export async function generateMetadata({ params }) {
  const product = await getProduct(params.id);
  return { title: product.name };
}
```

> 💡 **Interviewer Focus:** Dynamic search engine optimization.
</details>
<hr/>

### ❓ Q92. **How does Partial Prerendering (PPR) work in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

PPR combines static shell pre-rendering with dynamic server streaming in the same request.
- The static layout shell is served instantly from the CDN cache.
- The dynamic holes (wrapped in `<Suspense>`) are streamed from the server and plugged into the page once resolved, providing the speed of static sites with the flexibility of SSR.

> 💡 **Interviewer Focus:** Hybrid rendering models.
</details>
<hr/>

### ❓ Q93. **What is the difference between React Server Components (RSC) and standard SSR?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **SSR (Server-Side Rendering):** Converts React components into HTML on the server. The client downloads this HTML along with the full JS bundle to hydrate the page and execute interactions.
- **RSC:** Components execute *only* on the server. The client receives a lightweight JSON-like serialization format representing the rendered virtual DOM tree, requiring zero JavaScript bundle download for those components, significantly reducing page bundle sizes.

> 💡 **Interviewer Focus:** Reducing client-side JavaScript overhead.
</details>
<hr/>

### ❓ Q94. **How do you prevent hydration errors when displaying local client timestamps?**
<details>
<summary><b>👀 Show Answer</b></summary>

- Initialize a boolean state `isMounted` to `false` and set it to `true` inside `useEffect`.
- Only render the dynamic timestamp if `isMounted` is `true`. This guarantees the initial server render matches the initial client render (before mount), avoiding mismatch alerts.

> 💡 **Interviewer Focus:** Handling dynamic data in SSR pages.
</details>
<hr/>

### ❓ Q95. **What is the difference between next/script beforeInteractive and afterInteractive strategies?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `beforeInteractive`: Injects the script tag directly in the initial HTML before hydration. Best for core dependencies (like security managers or bot checks).
- `afterInteractive` (Default): Loads the script after the page hydrates, preventing third-party trackers from blocking the initial page rendering performance.

> 💡 **Interviewer Focus:** Script prioritization.
</details>
<hr/>

### ❓ Q96. **How does Next.js handle revalidation triggers in ISR?**
<details>
<summary><b>👀 Show Answer</b></summary>

ISR uses a stale-while-revalidate model:
1. User requests a page. The server returns the cached stale page.
2. If the revalidation timer has expired, Next.js triggers a background regeneration page build.
3. Once the build completes, the cache is updated. Subsequent requests receive the updated page.

> 💡 **Interviewer Focus:** Background compilation and stale cache strategies.
</details>
<hr/>

### ❓ Q97. **Explain the purpose of the next.config.js experimental optimizePackageImports flag.**
<details>
<summary><b>👀 Show Answer</b></summary>

It instructs the compiler to transpile imports from specific packages (e.g. `@mui/icons-material`, `lucide-react`) dynamically, loading only the utilized icons instead of processing the entire icon set module, which speeds up development builds.
</details>

<hr/>

### ❓ Q98. **How do you implement local SSL for HTTPS in local Next.js development?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use tools like `mkcert` to generate local security certificates.
- Configure `next dev` to run with HTTPS by mapping the certificate files via command arguments: `next dev --experimental-https --key local-key.pem --cert local-cert.pem`.

> 💡 **Interviewer Focus:** Local development configurations.
</details>

<hr/>

### ❓ Q99. **How does Sentry integration track server-side errors in Next.js?**
<details>
<summary><b>👀 Show Answer</b></summary>

Sentry injects monitoring hooks inside `instrumentation.ts` or `sentry.server.config.js` to intercept uncaught exceptions in Server Actions, API routes, or SSR lifecycle steps, capturing detailed stack traces and request contexts.

> 💡 **Interviewer Focus:** Error tracking and reliability monitoring.
</details>

<hr/>

### ❓ Q100. **What is the default execution limit of Serverless Functions in Next.js on standard cloud hosts?**
<details>
<summary><b>👀 Show Answer</b></summary>

On Vercel Hobby accounts, it is **10 seconds** (can be configured up to 5 minutes on Pro plans). Workloads exceeding this threshold throw timeout errors; long-running operations should be offloaded to queues or asynchronous background services.

> 💡 **Interviewer Focus:** Serverless platform constraints.
</details>
<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ React & Redux](./03_React_Redux.md) | [Home](./00_Index.md) | [➡️ React Native](./05_ReactNative.md) |

