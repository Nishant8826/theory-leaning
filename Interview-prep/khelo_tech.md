# Khelo Tech & Strategy — Back-End Developer (Node.js) Interview Prep Guide

This guide is custom-tailored to the Job Description of **Khelo Tech & Strategy Pvt. Ltd.** for a **Back-End Developer (3 Years Experience)**. It covers JavaScript, Node.js, databases (MySQL, Redis), system design, containerization, security, and React full-stack patterns.

All answers are wrapped in `<details>` tags to enable active recall. Try to answer the question yourself before expanding the accordion!

---

## Table of Contents
1. [JavaScript & Node.js Core](#1-javascript--nodejs-core)
2. [React & Frontend Integration](#2-react--frontend-integration)
3. [Database Engineering & Caching](#3-database-engineering--caching)
4. [Docker & Containerization](#4-docker--containerization)
5. [System Design, Security & Architecture](#5-system-design-security--architecture)

---

## 1. JavaScript & Node.js Core

### ❓ Q1. How does the JavaScript event loop work and what is an example?
<details>
<summary><b>👀 Show Answer</b></summary>

*   JavaScript is a single-threaded language, meaning it has one **Call Stack** and executes one piece of code at a time. To handle asynchronous operations (like network requests, file I/O, or timers) without blocking the thread, JavaScript relies on the **Event Loop** environment, typically provided by the hosting environment (browser or Node.js).

    The mechanism comprises:
    1.  **Call Stack:** Executes synchronous functions sequentially.
    2.  **Web/C++ APIs:** Asynchronous tasks are delegated here (e.g., `setTimeout`, `fetch`, database queries). Once complete, their callbacks are pushed to the queues.
    3.  **Microtask Queue:** Holds high-priority callbacks, such as `Promise.resolve().then(...)` and `MutationObserver` callbacks.
    4.  **Macrotask Queue (Callback Queue):** Holds standard callbacks, such as `setTimeout`, `setInterval`, and I/O tasks.
    5.  **Event Loop:** Continuously monitors the Call Stack. If the Call Stack is empty, it first drains **all** tasks in the Microtask Queue (including any microtasks queued *during* this drain process). Once the Microtask Queue is completely empty, it takes the first task from the Macrotask Queue, pushes it onto the Call Stack for execution, and repeats the cycle.

*   **Real-world Example:**
    Consider the following code snippet:
    ```javascript
    console.log("1. Start");

    setTimeout(() => {
      console.log("2. Timeout (Macrotask)");
    }, 0);

    Promise.resolve().then(() => {
      console.log("3. Promise (Microtask)");
    });

    console.log("4. End");
    ```

    **Execution Order Tracing:**
    1.  `console.log("1. Start")` runs synchronously and prints immediately.
    2.  `setTimeout` is registered. Its callback is scheduled to enter the Macrotask Queue.
    3.  `Promise.resolve().then()` is registered. Its callback enters the Microtask Queue.
    4.  `console.log("4. End")` runs synchronously and prints.
    5.  The synchronous code finishes; Call Stack is now empty.
    6.  The Event Loop checks the Microtask Queue, finds the Promise callback, and executes it: printing `3. Promise (Microtask)`.
    7.  The Microtask Queue is empty. The Event Loop checks the Macrotask Queue, finds the timeout callback, and executes it: printing `2. Timeout (Macrotask)`.

    **Final Output:**
    ```text
    1. Start
    4. End
    3. Promise (Microtask)
    2. Timeout (Macrotask)
    ```

*   **Common Mistakes:**
    *   Thinking `setTimeout(fn, 0)` executes exactly after 0 milliseconds. It only schedules the task; execution waits until the Call Stack and all pending microtasks are cleared.
    *   Assuming JavaScript is multi-threaded because it handles concurrent tasks. The runtime leverages system-level multi-threading (via the browser or libuv), but the JS code itself always executes on a single main thread.

*   **Follow-up Questions:**
    *   *What is CPU starvation, and how does a long synchronous loop affect the event loop?* It freezes the entire application because the Call Stack is never cleared, preventing the event loop from picking up any microtasks or macrotasks.
    *   *In what order do microtasks run if a promise handler itself schedules another promise?* The newly scheduled promise is appended to the current Microtask Queue and will still execute in the same cycle before the event loop yields to the Macrotask Queue.

</details>

<hr/>

### ❓ Q2. What is the Node.js event loop and how are microtasks and macrotasks processed?
<details>
<summary><b>👀 Show Answer</b></summary>

*   The Node.js event loop is managed by **libuv**, a C library that orchestrates non-blocking, asynchronous I/O operations using the operating system's native capabilities or a thread pool. Unlike the browser, the Node.js event loop contains **6 distinct phases** executed in a specific order:

    1.  **Timers:** Executes expired callbacks scheduled by `setTimeout()` and `setInterval()`.
    2.  **Pending Callbacks:** Executes deferred system-level I/O callbacks, such as TCP connection errors (`ECONNREFUSED`).
    3.  **Idle, Prepare:** Used internally by libuv for internal housekeeping.
    4.  **Poll:** Retrieves new I/O events (network, database, file system). The loop blocks here when idle to wait for updates unless timers or immediate actions are scheduled.
    5.  **Check:** Executes callbacks scheduled by `setImmediate()`.
    6.  **Close Callbacks:** Executes clean-up callbacks, such as `socket.on('close', ...)`.

    **Microtask Processing in Node.js:**
    Node.js handles microtasks differently from standard phases. The Microtask Queue is divided into two parts:
    -   `process.nextTick` callbacks (highest priority).
    -   Standard Promises / `async/await` resolutions.

    **Execution Rule:** The microtask queues are completely drained **immediately after the current operation finishes**, before the event loop transitions to the next phase, and between individual callback executions within a phase.

*   **Real-world Example:**
    ```javascript
    const fs = require('fs');

    fs.readFile(__filename, () => {
      setTimeout(() => console.log('1. Timeout (Timer Phase)'), 0);
      setImmediate(() => console.log('2. Immediate (Check Phase)'));
      process.nextTick(() => console.log('3. nextTick (Microtask)'));
      Promise.resolve().then(() => console.log('4. Promise (Microtask)'));
    });
    ```

    **Execution Order Tracing:**
    1.  The I/O operation finishes, executing the wrapping callback in the **Poll Phase**.
    2.  Inside the callback, `setTimeout` and `setImmediate` are scheduled.
    3.  A `nextTick` and a `Promise` microtask are scheduled.
    4.  The current execution context clears. Before transitioning to the next phase, the Event Loop checks microtasks.
    5.  It drains the `nextTick` queue: printing `3. nextTick (Microtask)`.
    6.  It drains the `Promise` queue: printing `4. Promise (Microtask)`.
    7.  The loop proceeds. Since there are `setImmediate` tasks, it exits the Poll Phase and transitions to the **Check Phase**, executing the immediate callback: printing `2. Immediate (Check Phase)`.
    8.  In the next loop iteration, the timer expires, and the **Timers Phase** runs: printing `1. Timeout (Timer Phase)`.

*   **Common Mistakes:**
    *   Starving the event loop by calling recursive `process.nextTick()` chains. Since V8 must drain the microtask queue completely before passing to the next phase, recursive nextTicks will lock the loop indefinitely, preventing I/O operations or timers from running.

*   **Follow-up Questions:**
    *   *How does the thread pool size affect the Poll phase?* If the libuv thread pool (default 4 threads) is saturated with heavy disk I/O or cryptography tasks, incoming I/O callbacks will be delayed in the Poll phase.
    *   *How can you change the thread pool size in libuv?* By setting the environment variable `process.env.UV_THREADPOOL_SIZE`.

</details>

<hr/>

### ❓ Q3. What is the difference between process.nextTick and setImmediate?
<details>
<summary><b>👀 Show Answer</b></summary>

*   While both methods schedule callbacks to be executed asynchronously, they fire at completely different times in the execution cycle:

    1.  **`process.nextTick()`:**
        *   **Phase:** It does **not** belong to the event loop phases.
        *   **Execution Time:** Runs immediately after the current operation on the Call Stack finishes, before the event loop continues to any other phase.
        *   **Use Case:** Executing code that must run before the event loop proceeds, such as cleaning up resources, parsing options, or firing event listeners before external calls are made.
    2.  **`setImmediate()`:**
        *   **Phase:** Runs during the **Check Phase** of the event loop.
        *   **Execution Time:** Invoked after I/O polling operations in the Poll Phase.
        *   **Use Case:** Offloading a callback to run after all current I/O polling is complete, yielding execution control to let other events process first.

*   **Real-world Example:**
    ```javascript
    const fs = require('fs');

    fs.readFile(__filename, () => {
      setImmediate(() => console.log('1. setImmediate'));
      process.nextTick(() => console.log('2. process.nextTick'));
    });
    ```
    **Output:**
    ```text
    2. process.nextTick
    1. setImmediate
    ```
    *Explanation:* Inside an I/O callback, the nextTick queue is drained immediately when the active operation ends. Only then does the event loop move forward to the Check phase where `setImmediate` is executed.

*   **Common Mistakes:**
    *   Confusing `setImmediate` with `process.nextTick` based on names. Historically, "next tick" sounds like the next cycle of the loop, but it actually executes immediately. "Immediate" sounds like it should execute instantly, but it is actually queued for the Check phase later in the loop.

*   **Follow-up Questions:**
    *   *What happens if setImmediate is called in the main module (not inside an I/O callback) alongside setTimeout(..., 0)?* The execution order is non-deterministic (depends on system load) because the event loop starts and might reach the Timers phase before or after the timer registration completes.
    *   *Is process.nextTick safe to run recursively?* No, it blocks the event loop because it continuously queues tasks in the microtask queue, which must be fully drained before any phase can run.

</details>

<hr/>

### ❓ Q4. For an async/await snippet with try/catch and logs before and after awaiting a promise, what will the output order be?
<details>
<summary><b>👀 Show Answer</b></summary>

*   The `async/await` syntax is syntactic sugar built on top of JavaScript Promises.
    -   When an `async` function is called, it executes **synchronously** until it encounters the `await` keyword.
    -   When `await <expression>` is evaluated, execution of the async function is suspended, and the remaining execution (including any code in `try/catch` blocks after the await) is scheduled as a callback in the **Microtask Queue**.
    -   Control immediately returns to the calling function, which continues running its synchronous code.
    -   Once the awaited promise resolves or rejects, the suspended function's remaining steps are pushed to the Call Stack via the Microtask Queue.

*   **Real-world Example:**
    ```javascript
    async function executeWorkflow() {
      console.log("2. Inside function: Before await");
      try {
        const result = await Promise.resolve("Secret Code");
        console.log("4. Inside function: Resolved await:", result);
      } catch (err) {
        console.log("5. Inside function: Catch block");
      }
      console.log("6. Inside function: End");
    }

    console.log("1. Main: Start");
    executeWorkflow();
    console.log("3. Main: End");
    ```

    **Execution Steps Tracing:**
    1.  `console.log("1. Main: Start")` runs and prints.
    2.  `executeWorkflow()` is called.
    3.  `console.log("2. Inside function: Before await")` runs and prints.
    4.  `await Promise.resolve("Secret Code")` is hit. The promise resolves immediately, but the remaining lines of `executeWorkflow` are packaged and queued in the **Microtask Queue**.
    5.  Control returns to the main thread.
    6.  `console.log("3. Main: End")` runs and prints.
    7.  The main synchronous thread finishes. The Event Loop pulls the pending microtask from the queue.
    8.  `console.log("4. Inside function: Resolved await:", "Secret Code")` executes and prints.
    9.  `console.log("6. Inside function: End")` executes and prints.

    **Final Output:**
    ```text
    1. Main: Start
    2. Inside function: Before await
    3. Main: End
    4. Inside function: Resolved await: Secret Code
    6. Inside function: End
    ```

*   **Common Mistakes:**
    *   Expecting code *after* an await to print before code *outside* the function calls. Even if a Promise is already resolved, `await` forces execution to yield to the microtask queue, pushing the remaining statements to the next microtask cycle.

*   **Follow-up Questions:**
    *   *What happens if the awaited promise rejects?* The remainder of the function is still scheduled as a microtask, but control jumps directly to the `catch` block.
    *   *If we await a non-promise value like await 42, does it still suspend execution?* Yes, the value is wrapped in `Promise.resolve(42)` and yielding occurs, pushing the next line to the microtask queue.

</details>

<hr/>

### ❓ Q5. What is the difference between streams and buffers and which holds complete data like images?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Both streams and buffers are used to handle binary data, but they differ fundamentally in memory allocation and data processing patterns:

    1.  **Buffer:**
        *   **Definition:** A fixed-size chunk of memory allocated outside the V8 JavaScript engine heap, storing raw binary bytes.
        *   **Data Handling:** Holds the **complete** dataset in memory at once.
        *   **Use Case:** Storing and editing complete files, like loading an entire image to crop/resize, parsing a config file, or manipulating small strings of bytes.
    2.  **Stream:**
        *   **Definition:** A data-handling concept where data is processed chunk-by-chunk over time rather than loaded all at once.
        *   **Data Handling:** Never keeps the entire data block in memory; it processes chunks sequentially, maintaining a tiny memory footprint.
        *   **Use Case:** Transferring large files (videos, logs, database exports) across networks or file systems.

    **Which holds complete data like images?**
    A **Buffer** holds complete data. When you read an image file using `fs.readFile()`, Node.js returns a Buffer containing the complete binary contents of the image in RAM. A **Stream** is used to *transport* that image data chunk-by-chunk (e.g., from an S3 bucket or local disk straight to an HTTP response) without consuming server memory.

*   **Real-world Example:**
    *   **Using Buffer (Memory Intensive):**
        ```javascript
        const fs = require('fs');
        // Loads the ENTIRE 500MB image into RAM. High risk of OOM under load.
        fs.readFile('heavy_image.png', (err, buffer) => {
          if (err) throw err;
          console.log("Buffer length:", buffer.length); // Complete image in memory
        });
        ```
    *   **Using Stream (Memory Optimized):**
        ```javascript
        const fs = require('fs');
        const http = require('http');
        
        http.createServer((req, res) => {
          const stream = fs.createReadStream('heavy_image.png');
          // Pipes chunks directly to the response. Max memory used is just highWaterMark (default 64KB)
          stream.pipe(res);
        }).listen(3000);
        ```

*   **Common Mistakes:**
    *   Reading large user uploads (like profile pictures or documents) into memory buffers on server endpoints. Under heavy concurrent traffic, this leads to Out-Of-Memory (OOM) errors and crashes the Node.js process. Always stream uploads directly to secure object storage (like AWS S3).

*   **Follow-up Questions:**
    *   *What is backpressure in streams?* It occurs when the reader/writable stream consumes data slower than the writer/readable stream produces it, leading to buffer accumulation.
    *   *How does pipeline avoid memory issues?* The `stream.pipeline` function automatically handles backpressure and cleans up system descriptors when streams throw errors.

</details>

---

## 2. React & Frontend Integration

### ❓ Q6. What do useMemo and useCallback each do in React?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Both hooks are performance optimization tools in React used to cache (memoize) calculations and function instances across component re-renders. They prevent unnecessary computations and reference changes that trigger downstream renders:

    1.  **`useMemo`:**
        *   **Purpose:** Memoizes the **result value** of an expensive calculation.
        *   **Mechanism:** Runs the function during rendering and caches its return value. It only recalculates the value if one of the variables in its dependency array changes.
        *   **Use Case:** Filtering a large array, sorting complex lists, or performing heavy statistical math calculations.
    2.  **`useCallback`:**
        *   **Purpose:** Memoizes the **function definition instance** itself.
        *   **Mechanism:** Returns a cached, referentially identical instance of a callback function across renders. It only creates a new function instance if the dependencies change.
        *   **Use Case:** Passing event handlers or callbacks to child components that are optimized using `React.memo`, preventing child re-renders caused by new function references on every render.

*   **Real-world Example:**
    ```jsx
    import React, { useState, useMemo, useCallback } from 'react';

    // Optimized Child Component
    const TaskButton = React.memo(({ onClick }) => {
      console.log("Child render");
      return <button onClick={onClick}>Click Me</button>;
    });

    export default function Dashboard() {
      const [count, setCount] = useState(0);
      const [items, setItems] = useState([10, 50, 30, 20]);

      // 1. useMemo: Caches the calculated maximum value
      const maxItem = useMemo(() => {
        console.log("Calculating max...");
        return Math.max(...items);
      }, [items]); // Only recalculates if 'items' array changes

      // 2. useCallback: Preserves reference equality for the callback
      const handleClick = useCallback(() => {
        console.log("Button clicked!");
      }, []); // Empty deps: function instance never changes

      return (
        <div>
          <p>Count: {count}</p>
          <button onClick={() => setCount(count + 1)}>Increment Count</button>
          <p>Max Item: {maxItem}</p>
          <TaskButton onClick={handleClick} />
        </div>
      );
    }
    ```
    *Behavior:* Clicking "Increment Count" triggers a re-render of `Dashboard`. Because `handleClick` is wrapped in `useCallback` and has no dependencies, its reference does not change, and `TaskButton` does **not** re-render. Similarly, `maxItem` does not recalculate.

*   **Common Mistakes:**
    *   Using `useMemo` and `useCallback` everywhere. Both hooks add memory overhead and dependency array checks. Wrapping a simple computation (like `a + b`) or a standard inline button handler makes code *slower* and harder to maintain. Only use them for heavy processing or to preserve referential integrity.

*   **Follow-up Questions:**
    *   *What is the relationship between useCallback(fn, deps) and useMemo?* `useCallback(fn, deps)` is equivalent to `useMemo(() => fn, deps)`.
    *   *What does shallow comparison mean in React.memo?* It checks if the new props have the exact same memory reference (for objects/arrays/functions) or values (for primitives) as the old props.

</details>

<hr/>

### ❓ Q7. What are SSR and CSR and which is more SEO-friendly?
<details>
<summary><b>👀 Show Answer</b></summary>

*   These are two different strategies for rendering web applications:

    1.  **Client-Side Rendering (CSR):**
        *   **Flow:** The server sends a bare-bones HTML page (typically just a `<div id="root"></div>`) containing a reference to a JavaScript bundle. The browser downloads the JS, executes it, builds the DOM tree, fetches data from APIs, and renders the UI.
        *   **Pros:** Fast page transitions, minimal server workload.
        *   **Cons:** Slower initial page load (Time to Interactive), poor SEO capabilities out-of-the-box.
    2.  **Server-Side Rendering (SSR):**
        *   **Flow:** Upon receiving a request, the server fetches necessary data, renders the complete HTML string representing the page, and sends the fully populated HTML back to the browser. Once the page is rendered in the browser, client-side JS is loaded to attach listeners (Hydration).
        *   **Pros:** Instant initial content render (First Contentful Paint), superior SEO.
        *   **Cons:** Higher server CPU overhead, slightly longer Time to First Byte (TTFB).

    **Which is more SEO-friendly?**
    **SSR** is vastly more SEO-friendly. Search engine crawlers download HTML files to index content. If a crawler encounters a CSR site, it receives an empty HTML wrapper. While some advanced crawlers (like Googlebot) execute JavaScript, they may timeout or skip JS rendering if resources are limited, failing to index your content. SSR guarantees that crawlers get a fully rendered HTML page immediately.

*   **Real-world Example:**
    *   **CSR HTML Response (Vite/CRA):**
        ```html
        <!DOCTYPE html>
        <html>
          <head><title>My CSR App</title></head>
          <body>
            <div id="root"></div> <!-- Empty! Crawlers see nothing here -->
            <script src="/static/bundle.js"></script>
          </body>
        </html>
        ```
    *   **SSR HTML Response (Next.js):**
        ```html
        <!DOCTYPE html>
        <html>
          <head><title>My SSR App</title></head>
          <body>
            <div id="root">
              <h1>Welcome to Khelo Tech</h1>
              <p>Active Games: 1,429</p> <!-- Fully Rendered Content -->
            </div>
            <script src="/_next/static/chunks/main.js"></script>
          </body>
        </html>
        ```

*   **Common Mistakes:**
    *   Assuming SSR means there is no JS executing in the browser. In SSR, the browser still downloads a JavaScript bundle to handle interactivity (hydration).
    *   Accessing browser-only globals (like `window`, `document`, or `localStorage`) in components during SSR. Since this code also executes on the Node.js server, it will throw reference errors. These must be placed inside `useEffect` or client-only gates.

*   **Follow-up Questions:**
    *   *What is static hydration mismatch?* It occurs when the server-rendered HTML doesn't match the first client-side render tree, often caused by using non-deterministic states like `Date.now()` or random IDs during render.
    *   *What is Static Site Generation (SSG)?* A rendering method where HTML pages are pre-built at compile-time, combining the speed of static hosting with the SEO benefits of SSR.

</details>

---

## 3. Database Engineering & Caching

### ❓ Q8. What are ACID properties in databases?
<details>
<summary><b>👀 Show Answer</b></summary>

*   ACID is a set of properties that guarantee database transactions are processed reliably, preserving data integrity even during system failures:

    1.  **Atomicity ("All or Nothing"):**
        *   Ensures that a transaction is treated as a single unit of work. Either all operations inside the transaction succeed (commit), or the entire transaction is aborted and rolled back to its original state.
    2.  **Consistency:**
        *   Guarantees that a transaction can only transition the database from one valid state to another, enforcing all schema constraints, foreign keys, triggers, and unique index rules.
    3.  **Isolation:**
        *   Ensures that concurrent execution of transactions leaves the database in the same state as if they had run sequentially. It prevents transactions from seeing incomplete states of other transactions, managed via isolation levels.
    4.  **Durability:**
        *   Guarantees that once a transaction has committed, its changes are permanently written to non-volatile storage (disk/SSD). They will not be lost even in the event of a system crash, power outage, or OS failure.

*   **Real-world Example:**
    A transaction transferring $100 from Account A to Account B:
    ```sql
    START TRANSACTION;
    -- 1. Deduct money from A
    UPDATE accounts SET balance = balance - 100 WHERE id = 'A' AND balance >= 100;
    -- 2. Add money to B
    UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
    COMMIT;
    ```
    *   *Atomicity:* If the server crashes after step 1 but before step 2, the database rolls back step 1, ensuring money does not disappear.
    *   *Consistency:* If Account B's ID does not exist, the transaction fails due to foreign key constraints.
    *   *Isolation:* A third transaction checking Account A's balance concurrently won't see intermediate states.
    *   *Durability:* Once `COMMIT` returns success, the changes are stored in the write-ahead log (WAL) on disk, guaranteeing they survive sudden reboot events.

*   **Common Mistakes:**
    *   Confusing "Consistency" in ACID with "Consistency" in the CAP Theorem. ACID Consistency is about database schema rules and constraints. CAP Consistency is about replication synchronization across multiple distributed nodes.

*   **Follow-up Questions:**
    *   *What is Write-Ahead Logging (WAL)?* A family of techniques where changes are written to a log file on disk before they are applied to the database files, ensuring durability and recovery.
    *   *How does InnoDB manage Isolation without locking every reader?* By using Multi-Version Concurrency Control (MVCC), which presents readers with historical snapshots of data.

</details>

<hr/>

### ❓ Q9. How should composite indexes be structured for effectiveness?
<details>
<summary><b>👀 Show Answer</b></summary>

*   A composite index (compound index) contains multiple columns in a single index structure. For composite indexes to be effective, you must structure the column order based on two key principles:

    1.  **The Left-to-Right Rule (Prefix Rule):**
        *   A composite index on `(A, B, C)` can speed up queries filtering on `(A)`, `(A, B)`, or `(A, B, C)`.
        *   It **cannot** optimize queries filtering on `(B)`, `(C)`, or `(B, C)` because the search path must start from the leftmost column.
    2.  **The ESR Rule (Equality, Sort, Range):**
        When designing a composite index for a specific query, order the columns as follows:
        *   **E - Equality (`=`):** Columns searched for exact values first.
        *   **S - Sort (`ORDER BY`):** Columns used for ordering results next. This allows the database to retrieve pre-sorted keys, avoiding an expensive memory/disk filesort operation.
        *   **R - Range (`>`, `<`, `BETWEEN`, `LIKE 'abc%'`):** Columns queried with inequalities last. A range filter halts index-based sorting for columns placed after it in the index.

*   **Real-world Example:**
    Consider this query from a game backend:
    ```sql
    SELECT * FROM match_history
    WHERE status = 'COMPLETED' 
      AND score > 1500 
    ORDER BY played_at DESC;
    ```

    **Evaluating Index Options:**
    *   *Option A: `(score, status, played_at)`* -> Bad. The range query on `score` is placed first, which prevents the optimizer from using the index for filtering `status` or sorting `played_at`.
    *   *Option B: `(status, score, played_at)`* -> Suboptimal. The range query on `score` is placed before the sort column `played_at`, forcing a `filesort`.
    *   *Option C: `(status, played_at, score)`* -> **Best (ESR)**.
        -   `status` (Equality) is first.
        -   `played_at` (Sort) is second, avoiding filesort.
        -   `score` (Range) is third.

*   **Common Mistakes:**
    *   Creating multiple single-column indexes on columns that are queried together. Databases can rarely combine multiple indexes effectively. A single composite index is far more performant.
    *   Placing high-cardinality range fields at the front of a composite index.

*   **Follow-up Questions:**
    *   *What is an Index Skip Scan?* An optimization where the database can use a composite index even when the leftmost column is omitted from the WHERE clause, provided that column has low cardinality.
    *   *Does the order of columns in the SQL WHERE clause matter?* No, the database query parser automatically reorders query criteria to match indexes; however, the order of columns *within* the index declaration itself is critical.

</details>

<hr/>

### ❓ Q10. How can a slow query be optimized?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Optimizing slow queries requires a structured diagnostic and remediation workflow:

    1.  **Locate the Bottleneck:** Identify queries exceeding threshold durations using the database **Slow Query Log** or Application Performance Monitoring (APM) tools.
    2.  **Analyze the Execution Plan:** Prepend the query with `EXPLAIN` or `EXPLAIN ANALYZE` (MySQL 8.0+) to inspect:
        *   `type`: Look for `ALL` (Full Table Scan) or `index` (Full Index Scan) which are slow. Aim for `const`, `ref`, or `range`.
        *   `key`: The index actually chosen. Check if it is `NULL`.
        *   `rows`: The estimated number of rows examined.
        *   `Extra`: Watch out for `Using filesort` or `Using temporary`.
    3.  **Optimize Indexing:**
        *   Add indexes to columns used in `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses.
        *   Construct composite indexes following the Left-to-Right and ESR rules.
        *   Create **Covering Indexes** (where all selected columns are inside the index tree) to avoid lookup disk jumps to the main table.
    4.  **Rewrite the Query:**
        *   Avoid `SELECT *`; retrieve only necessary columns to reduce I/O and network payload.
        *   Make queries **Sargable** (Search Argument Able). Do not apply functions to indexed columns. E.g., change `WHERE YEAR(created_at) = 2026` to `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`.
        *   Avoid wildcards at the start of search patterns (e.g. `LIKE '%abc'`), which disable index scans.
    5.  **Refactor Schema & Cache:**
        *   Denormalize highly relational tables if joins are bottlenecking.
        *   Cache persistent, read-heavy query results in Redis.

*   **Real-world Example:**
    *   *Slow Non-Sargable Query:*
        ```sql
        SELECT id, name FROM users WHERE DATE(created_at) = '2026-06-16';
        ```
        *Explain:* Applying the `DATE()` function prevents the database from using an index on `created_at`.
    *   *Optimized Sargable Query:*
        ```sql
        SELECT id, name FROM users 
        WHERE created_at >= '2026-06-16 00:00:00' 
          AND created_at <= '2026-06-16 23:59:59';
        ```
        *Index:* `CREATE INDEX idx_created_at ON users(created_at);`
        *Result:* The database performs an efficient index range scan (`type: range`), scanning only matching rows.

*   **Common Mistakes:**
    *   Adding indexes to tables without measuring performance. Writing indexes slows down INSERT, UPDATE, and DELETE operations.
    *   Failing to run `ANALYZE TABLE` to update index statistics, causing the query optimizer to make incorrect plans based on stale metrics.

*   **Follow-up Questions:**
    *   *What is the difference between a filesort and an index sort?* An index sort retrieves rows pre-sorted by the index tree. A filesort happens in memory (or temp files on disk) because the database has to sort unsorted rows.
    *   *How does table fragmentation affect query performance?* Over time, insertions and deletions leave gaps in index files, requiring more disk seeks to read data. Running `OPTIMIZE TABLE` defragments the table.

</details>

<hr/>

### ❓ Q11. What is the security issue with constructing a SQL query by embedding an email variable directly?
<details>
<summary><b>👀 Show Answer</b></summary>

*   The security issue with constructing queries by embedding or concatenating variables directly (e.g., using string interpolation `` `SELECT * FROM users WHERE email = '${email}'` ``) is that it introduces a vulnerability called **SQL Injection (SQLi)**. 

    If an input variable is concatenated directly, the database treats the user input as executable SQL code rather than a literal value. Attackers can exploit this by entering inputs containing SQL control characters (like quotes, comments, or semicolons) to alter the query's structural logic.

    **Mitigation:**
    Always use **Prepared Statements (Parameterized Queries)**. In a prepared statement, the database compiles the SQL query structure first, placeholder markers (`?` or `:email`) are defined, and the user variables are sent separately. The database treats the variables strictly as literal data, neutralising any SQL commands embedded within them.

*   **Real-world Example:**
    *   **Vulnerable Code:**
        ```javascript
        const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;
        db.query(query);
        ```
        *Attack Input:* `attacker@khelo.com' OR '1'='1`
        *Resulting SQL:* `SELECT * FROM users WHERE email = 'attacker@khelo.com' OR '1'='1'`
        *Consequence:* The condition `'1'='1'` is always true, returning all users in the database and bypassing authentication.

    *   **Secure Code (Prepared Statement):**
        ```javascript
        const query = 'SELECT * FROM users WHERE email = ?';
        db.query(query, [req.body.email]);
        ```
        *Attack Input:* `attacker@khelo.com' OR '1'='1`
        *Resulting Action:* The database searches for a user whose email string is literally `attacker@khelo.com' OR '1'='1'`, rendering the injection attempt completely harmless.

*   **Common Mistakes:**
    *   Relying solely on regex parsing, character escaping, or client-side validation to clean strings. Attackers can bypass filters using alternative encodings. Parameterization is the only reliable defense.

*   **Follow-up Questions:**
    *   *Do modern ORMs (like Prisma or Sequelize) protect against SQLi?* Yes, they use parameterized queries automatically under the hood for their default query methods.
    *   *What is Blind SQL Injection?* An exploit where the attacker cannot see data directly on the screen, but reconstructs database contents by asking the database true/false questions and observing differences in page rendering or server response delays.

</details>

<hr/>

### ❓ Q12. Why is Redis faster than disk-backed databases?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Redis is an open-source, in-memory key-value data structure store capable of handling over 100,000 requests per second. It is significantly faster than disk-backed relational databases (like MySQL) due to several design choices:

    1.  **In-Memory Storage:**
        *   All data resides in RAM. RAM access speeds are measured in nanoseconds, whereas disk accesses (even SSDs/NVMe) take microseconds or milliseconds.
    2.  **Single-Threaded Execution Model:**
        *   Redis executes commands on a single main thread. This completely eliminates CPU overhead associated with context switching, thread synchronization, thread pool management, and lock contention.
    3.  **Optimized C Data Structures:**
        *   Redis structures (Strings, Hashes, Lists, Sets, Sorted Sets) are written in optimized C. They use structures like skip lists (for Sorted Sets) and ziplists (for compact memory representations) to ensure operations run at optimal time complexities (e.g., $O(1)$ or $O(\log N)$).
    4.  **Asynchronous Non-Blocking I/O Multiplexing:**
        *   It uses event loops (via system calls like `epoll` or `kqueue`) to monitor thousands of concurrent client connections simultaneously, handling request routing without spawning new processes or threads.

*   **Real-world Example:**
    *   **RAM vs. Disk Latency:**
        -   RAM read/write latency: ~10-100 nanoseconds.
        -   SSD read/write latency: ~10-100 microseconds.
        -   HDD read/write latency: ~5-15 milliseconds.
    *   When fetching a user session, MySQL must execute a query, verify indexes, and potentially fetch database blocks from disk (or buffers). Redis reads the session key from RAM directly via a hash table lookup, completing the operation instantly.

*   **Common Mistakes:**
    *   Assuming Redis has no persistence. Redis can save data to disk using RDB (periodic point-in-time snapshots) and AOF (append-only logs of every write command) in the background without affecting the performance of the main execution thread.
    *   Running heavy blocking commands (like `KEYS *` or `FLUSHALL`) on production instances. Since Redis is single-threaded, these commands block the main thread, freezing all other client requests.

*   **Follow-up Questions:**
    *   *What is the alternative to using KEYS * in production?* Use the `SCAN` command, which iterates over keys incrementally without blocking the server.
    *   *What is Redis Eviction?* When Redis memory reaches its configured limit, it removes keys according to a policy (like LRU - Least Recently Used, or LFU - Least Frequently Used) to make room for new data.

</details>

<hr/>

### ❓ Q13. When generating a query and retrieving data from Redis, how do we retrieve data from Redis?
<details>
<summary><b>👀 Show Answer</b></summary>

*   To retrieve data from Redis, you query the database using the **Cache-Aside (Lazy Loading)** pattern. The application acts as the coordinator between the cache (Redis) and the primary database (MySQL).

    **Workflow:**
    1.  **Generate a Cache Key:** Create a unique, consistent string key based on the query parameters (e.g., `user:profile:9982`).
    2.  **Read from Redis:** Query Redis using the appropriate command based on the data structure (e.g., `GET` for string-serialized JSON, or `HGETALL` for hashes).
    3.  **Cache Hit:** If data is found, deserialize it and return it immediately.
    4.  **Cache Miss:** If data is not found (returns `null`):
        a. Query the primary database.
        b. Serialize the database results (e.g., `JSON.stringify(data)`).
        c. Write the data to Redis using `SETEX` (set value with a TTL expiration) so future queries hit the cache.
        d. Return the data to the client.

*   **Real-world Example:**
    ```javascript
    const Redis = require('ioredis');
    const redis = new Redis();

    async function getUserProfile(userId) {
      const cacheKey = `user:profile:${userId}`;
      
      // 1. Attempt to fetch from Redis
      const cachedData = await redis.get(cacheKey);
      
      if (cachedData) {
        console.log("Cache Hit!");
        return JSON.parse(cachedData); // Deserialize
      }

      console.log("Cache Miss! Querying database...");
      // 2. Fetch from primary DB
      const userProfile = await db.select().from('users').where({ id: userId }).first();
      
      if (userProfile) {
        // 3. Write back to Redis with a TTL of 1 hour (3600 seconds)
        await redis.setex(cacheKey, 3600, JSON.stringify(userProfile));
      }

      return userProfile;
    }
    ```

*   **Common Mistakes:**
    *   Failing to set a TTL (Time-To-Live) on cached items. Without a TTL, stale data stays in Redis indefinitely, consuming RAM and eventually causing Out-Of-Memory errors.
    *   Failing to invalidate the cache when data is updated in the primary database. If user profiles are updated, your code must delete the cache key (`redis.del(cacheKey)`) or update it.

*   **Follow-up Questions:**
    *   *What is Cache Penetration?* A scenario where requests target keys that do not exist in either the cache or the primary database, forcing database lookups for every request. Mitigate by caching empty values with short TTLs or using Bloom filters.
    *   *What is Cache Stampede?* When a highly popular cache key expires, and multiple concurrent requests try to fetch the data from the database simultaneously, overloading the database. Mitigate using lock/mutex wrappers.

</details>

---

## 4. Docker & Containerization

### ❓ Q14. What is the difference between a Dockerfile and a Docker Compose file?
<details>
<summary><b>👀 Show Answer</b></summary>

*   While both files are critical tools in containerization workflow, they serve different scopes:

    1.  **Dockerfile:**
        *   **Scope:** Focuses on building a **single container image**.
        *   **Format:** A sequential list of CLI commands (`FROM`, `RUN`, `COPY`, `EXPOSE`, `CMD`).
        *   **Purpose:** Defines the base operating system, system dependencies, environment variables, copy paths, port declarations, and startup command needed to package **one service** into a portable image.
    2.  **Docker Compose (`docker-compose.yml`):**
        *   **Scope:** Focuses on orchestrating **multiple containers** as a unified application stack.
        *   **Format:** A declarative YAML file mapping services, networks, volumes, and dependencies.
        *   **Purpose:** Configures how multiple containers (e.g., Node.js API, Redis cache, MySQL database) interact. It defines port mappings, shared virtual networks, persistent storage volumes, environment files, and service startup orders (`depends_on`).

*   **Real-world Example:**
    *   **`Dockerfile` (Builds the API image):**
        ```dockerfile
        FROM node:20-alpine
        WORKDIR /app
        COPY package*.json ./
        RUN npm ci --only=production
        COPY . .
        EXPOSE 3000
        CMD ["node", "index.js"]
        ```
    *   **`docker-compose.yml` (Orchestrates the entire stack):**
        ```yaml
        version: '3.8'
        services:
          api-server:
            build: . # Builds using the local Dockerfile
            ports:
              - "3000:3000"
            environment:
              - DB_HOST=db-mysql
              - REDIS_HOST=cache-redis
            depends_on:
              - db-mysql
              - cache-redis
            networks:
              - app-network

          cache-redis:
            image: redis:7-alpine
            networks:
              - app-network

          db-mysql:
            image: mysql:8
            environment:
              MYSQL_ROOT_PASSWORD: secretpassword
            volumes:
              - db_data:/var/lib/mysql
            networks:
              - app-network

        volumes:
          db_data:
        networks:
          app-network:
        ```

*   **Common Mistakes:**
    *   Confusing the use cases. Trying to install system software and compile source code using docker-compose settings, or trying to link multiple running servers inside a single Dockerfile.
    *   Forgetting to run `docker compose build` after modifying a Dockerfile, resulting in Docker Compose launching outdated container images.

*   **Follow-up Questions:**
    *   *What is the difference between a container image and a container?* An image is a read-only template containing instructions to build a container. A container is a runnable, isolated instance of that image.
    *   *How does docker-compose verify depends_on?* By default, it only checks if the dependency container has *started*, not if the application inside it is *ready* (e.g., MySQL initialization). To check readiness, configure healthcheck scripts in compose.

</details>

---

## 5. System Design, Security & Architecture

### ❓ Q15. How does JWT signature verification work and what alternatives exist?
<details>
<summary><b>👀 Show Answer</b></summary>

*   A JSON Web Token (JWT) is composed of three parts separated by dots: **Header.Payload.Signature**.
    -   **Header:** Identifies the token type and signing algorithm (e.g., HS256, RS256).
    -   **Payload:** Contains base64-encoded JSON claims (userId, expiration, roles).
    -   **Signature:** Created by hashing the encoded Header and Payload together with a secret or private key.

    **Signature Verification Workflow:**
    1.  The client sends the JWT in the `Authorization` header (`Bearer <token>`).
    2.  The server splits the token into Header, Payload, and Signature components.
    3.  The server takes the Header and Payload strings, concatenates them, and hashes them using the configured algorithm and the **server's secret key** (for symmetric encryption like HS256) or the **public key** (for asymmetric encryption like RS256).
    4.  The server compares its newly generated signature string with the Signature string sent by the client.
    5.  If they match, the token is verified as authentic and untampered. If they do not match, or if the `exp` (expiration) timestamp has passed, the server rejects the request.

    **Alternatives to JWT:**
    1.  **Session-based Authentication:** The server generates a random session ID, stores the session data in a fast database (like Redis), and sends the ID to the client via secure cookies. The client's identity state resides entirely on the server.
    2.  **Paseto (Platform-Agnostic Security Tokens):** A modern security standard designed to eliminate JWT implementation flaws (like the "none" algorithm exploit) by using predefined, non-negotiable cryptographic suites.

*   **Real-world Example (Node.js Verification):**
    ```javascript
    const jwt = require('jsonwebtoken');

    function authenticateToken(req, res, next) {
      const authHeader = req.headers['authorization'];
      const token = authHeader && authHeader.split(' ')[1]; // Bearer <token>

      if (!token) return res.sendStatus(401);

      // Verify recalculated signature matches
      jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, user) => {
        if (err) return res.status(403).json({ error: "Invalid or expired token" });
        req.user = user;
        next();
      });
    }
    ```

*   **Common Mistakes:**
    *   Failing to check the signing algorithm in the verification code. In early JWT libraries, attackers could alter the Header algorithm to `none`, sign the token themselves, and bypass security. Modern libraries block this, but verify you use secure methods.
    *   Storing sensitive user PII (like passwords or emails) in the JWT payload. Anyone can easily base64-decode a JWT payload.

*   **Follow-up Questions:**
    *   *Why is RS256 preferred over HS256 in microservices?* Because only the Authentication service needs the Private Key to generate tokens. All other microservices use the Public Key to verify signatures without ever exposing the signing secrets.
    *   *How do you invalidate a JWT before its expiration date?* Store a blacklist of revoked JWT tokens in Redis with a TTL matching the token's remaining lifespan, and check this cache during request auth checks.

</details>

<hr/>

### ❓ Q16. How does rate limiting protect services and what response is returned when limits are exceeded?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Rate limiting is a technique to control the rate of incoming network traffic by limiting the number of API requests a user, IP address, or API key can make within a specified time window.

    **Key Protections:**
    *   **Prevents DDoS / DoS:** Stops malicious bots from overloading server CPUs and database connections.
    *   **Blocks Brute-force Attempts:** Prevents attackers from guessing passwords or API keys rapidly.
    *   **Controls API Costs:** Prevents resource abuse that would inflate server hosting or cloud provider bills.

    **Response on Exceeded Limits:**
    When a client exceeds their rate limit, the server rejects the request and returns:
    *   **HTTP Status Code:** **`429 Too Many Requests`**.
    *   **Headers:**
        *   `Retry-After`: The number of seconds the client must wait before sending another request.
        *   `X-RateLimit-Limit`: The maximum number of allowed requests in the window.
        *   `X-RateLimit-Remaining`: The remaining number of requests allowed in the current window.
        *   `X-RateLimit-Reset`: The Unix timestamp when the rate limit window resets.

    **Common Algorithms:**
    *   *Token Bucket:* Tokens are added to a bucket at a set rate. Requests consume tokens. Allows traffic bursts.
    *   *Leaky Bucket:* Requests enter a queue and are processed at a constant, steady rate. Smooths out traffic spikes.
    *   *Fixed Window Counter:* Resets request counters at fixed intervals (e.g. every hour). Prone to bursts at window boundaries.
    *   *Sliding Window Log:* Tracks individual timestamps. Highly accurate but memory intensive.

*   **Real-world Example (Express Integration):**
    Using Redis to track request counters across multiple API nodes:
    ```javascript
    const rateLimit = require('express-rate-limit');
    const RedisStore = require('rate-limit-redis');
    const Redis = require('ioredis');

    const redisClient = new Redis();

    const apiLimiter = rateLimit({
      store: new RedisStore({
        sendCommand: (...args) => redisClient.call(...args),
      }),
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // Limit each IP to 100 requests per window
      message: { error: 'Too many requests, please try again later.' },
      standardHeaders: true, // Return standard rate limit headers
      legacyHeaders: false,
    });

    app.use('/api/', apiLimiter);
    ```

*   **Common Mistakes:**
    *   Storing rate-limiting counts in application memory. If you run multiple servers behind a load balancer, memory caches are separate, allowing clients to bypass limits by hitting different nodes. Always use a shared Redis store.

*   **Follow-up Questions:**
    *   *How do you handle users sharing the same NAT IP address?* Use API keys or authenticated user IDs for rate limiting instead of raw IP addresses.
    *   *What is the difference between rate limiting and throttling?* Rate limiting rejects requests above a limit. Throttling slows down response delivery or delays request processing rather than rejecting requests immediately.

</details>

<hr/>

### ❓ Q17. How do Razorpay/Stripe integrations and webhooks work in a payment flow?
<details>
<summary><b>👀 Show Answer</b></summary>

*   A secure online payment flow separates the sensitive credit card handling from your primary application servers to comply with PCI-DSS guidelines.

    **Step-by-Step Payment Flow:**
    1.  **Initiation:** The user clicks "Buy Now" on the frontend.
    2.  **Order Creation (Backend):** Your backend makes a secure server-to-server call to Stripe/Razorpay to create a PaymentIntent/Order, detailing the amount and currency. The gateway returns a `client_secret` or `order_id`.
    3.  **Secure UI Rendering (Frontend):** The frontend receives the ID, initializes the payment library (Stripe Elements or Razorpay Modal), and collects payment details directly in an isolated iframe.
    4.  **Transaction Authorization:** The payment gateway processes the payment with the user's bank.
    5.  **Redirect & Webhook Dispatch:**
        *   The gateway redirects the user back to your site.
        *   Simultaneously, the gateway sends an asynchronous **Webhook** (an HTTP POST payload) directly to your backend to confirm the success/failure of the transaction (e.g. `payment_intent.succeeded` event).
    6.  **Backend Fulfillment:** Your backend verifies the webhook's signature using a shared secret key, processes the business logic (crediting wallets or marking orders as paid), and returns a `200 OK` to the gateway.

    **Why Webhooks are Mandatory:**
    If the user's browser freezes, the network drops, or the tab is closed immediately after payment authorization, the frontend will fail to notify your backend. Webhooks act as a reliable, server-to-server confirmation channel.

*   **Real-world Example (Stripe Webhook Handler):**
    ```javascript
    const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

    app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
      const sig = req.headers['stripe-signature'];
      let event;

      try {
        // Verify signature to prove request came from Stripe
        event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
      } catch (err) {
        console.error(`Webhook signature verification failed: ${err.message}`);
        return res.status(400).send(`Webhook Error: ${err.message}`);
      }

      // Handle the event
      if (event.type === 'payment_intent.succeeded') {
        const paymentIntent = event.data.object;
        console.log(`Payment for ${paymentIntent.amount} succeeded!`);
        // Fulfill the purchase (e.g., update database)
      }

      // Return 200 to acknowledge receipt
      res.json({ received: true });
    });
    ```

*   **Common Mistakes:**
    *   Processing payment notifications without verifying the webhook signature. An attacker could send forged HTTP POST requests directly to your `/webhook` endpoint to unlock features for free.
    *   Performing slow synchronous operations (like PDF generation or sending transactional emails) inside the webhook handler. Webhooks must respond with `200 OK` quickly to prevent gateway timeout and retries. Delegate heavy work to a background queue.

*   **Follow-up Questions:**
    *   *How do you handle duplicate webhook events?* Make the webhook handler idempotent by logging processed payment IDs in a database and checking this list before applying changes.
    *   *What is PCI-DSS compliance?* A global security standard that websites must follow if they store, process, or transmit cardholder data. Using hosted checkout forms offloads this compliance overhead to the payment provider.

</details>

<hr/>

### ❓ Q18. What is idempotency and how is it implemented?
<details>
<summary><b>👀 Show Answer</b></summary>

*   An operation is **idempotent** if executing it multiple times yields the same system state and outcome as executing it once. 

    In payment processing or distributed systems, retries are common due to network hiccups. If a request is retried without idempotency, it could cause issues like charging a customer twice or duplicating data.

    **Implementation Architecture:**
    1.  **Idempotency Key:** The client generates a unique UUID (Idempotency Key) for every transactional action and sends it in the HTTP headers (e.g., `Idempotency-Key: f47ac10b-58cc-4372-a567-0e02b2c3d479`).
    2.  **Distributed Lock/Cache Lookup:** The server intercepts the request and checks a fast database (like Redis) for the key.
    3.  **Request Status Management:**
        *   **If the key is processing:** The server returns a `409 Conflict` or waits, blocking concurrent duplicate calls.
        *   **If the key succeeded:** The server returns the **saved response body** directly from cache, skipping execution.
        *   **If the key is not found (First Request):** The server registers the key in Redis as "processing" (with a lock/NX flag).
    4.  **Execution:** The server performs the database queries inside a transaction.
    5.  **Store Response:** Once done, the server updates the Redis record with the final response payload (e.g., with a 24-hour TTL) and returns the response.

*   **Real-world Example:**
    ```javascript
    const Redis = require('ioredis');
    const redis = new Redis();

    app.post('/wallet/charge', async (req, res) => {
      const idempotencyKey = req.headers['idempotency-key'];
      if (!idempotencyKey) return res.status(400).send('Missing Idempotency-Key');

      const cacheKey = `idempotency:${idempotencyKey}`;

      // Try to acquire lock and check cache
      const existing = await redis.get(cacheKey);
      if (existing) {
        const record = JSON.parse(existing);
        if (record.status === 'processing') {
          return res.status(409).send('Request already processing. Please wait.');
        }
        return res.status(record.statusCode).json(record.body); // Return cached response
      }

      // Lock key as processing (TTL 10 minutes to prevent zombie locks)
      await redis.setex(cacheKey, 600, JSON.stringify({ status: 'processing' }));

      try {
        // Perform transaction
        const result = await processWalletDebit(req.body.userId, req.body.amount);
        
        const responseData = { success: true, balance: result.newBalance };
        
        // Save success response in cache (TTL 24 hours)
        await redis.setex(cacheKey, 86400, JSON.stringify({
          status: 'success',
          statusCode: 200,
          body: responseData
        }));

        return res.status(200).json(responseData);
      } catch (err) {
        await redis.del(cacheKey); // Release lock on processing failures to allow retry
        return res.status(500).send('Internal Error');
      }
    });
    ```

*   **Common Mistakes:**
    *   Generating the idempotency key on the server. If the request fails to reach the server due to network loss, the client cannot retry safely. The key must be generated by the client.
    *   Not deleting the lock when execution fails, which blocks the client from retrying a valid transaction.

*   **Follow-up Questions:**
    *   *Which HTTP methods are naturally idempotent?* `GET`, `PUT`, `DELETE`, `HEAD`, and `OPTIONS`. `POST` is NOT naturally idempotent.
    *   *How do you handle race conditions where two identical requests arrive at the exact same millisecond?* Use Redis `SET key value NX` (set if not exists) to ensure only one thread can initialize execution.

</details>

<hr/>

### ❓ Q19. How should a simple wallet system be designed at the database level?
<details>
<summary><b>👀 Show Answer</b></summary>

*   A financial wallet system must be designed to be auditable, accurate, and resilient to race conditions. 

    **Core Database Schema Design:**
    1.  **Never rely only on updating a single balance column.** You must use a **Double-Entry Ledger** pattern.
    2.  **`wallets` Table:** Tracks the current balance.
        *   `id` (Primary Key)
        *   `user_id` (Unique, indexed)
        *   `balance` (Decimal, e.g. `DECIMAL(15, 4)` to prevent floating-point rounding errors)
        *   `version` or `updated_at` (used for optimistic locking)
    3.  **`wallet_ledger` Table:** Logs every credit and debit. Records are immutable.
        *   `id` (Primary Key)
        *   `wallet_id` (Foreign Key)
        *   `amount` (Positive for credits, negative for debits)
        *   `type` (Enum: `DEPOSIT`, `WITHDRAWAL`, `GAME_ENTRY`, `WINNINGS`)
        *   `reference_id` (UUID linked to orders or matches)
        *   `created_at`

    **Concurrency and Balance Safety:**
    To prevent **Double-Spending** (when a user triggers two purchases simultaneously before the balance is updated), use:
    *   **Pessimistic Locking:** Acquire a row-level lock (`SELECT ... FOR UPDATE`) inside a transaction to block other operations on that wallet until execution commits.
    *   **Conditional Updates:** Ensure updates check constraints directly, e.g. `UPDATE wallets SET balance = balance + :amount WHERE id = :id AND balance >= :abs_amount`.

*   **Real-world Example (Node.js & MySQL Transaction):**
    ```javascript
    const mysql = require('mysql2/promise');

    async function debitWallet(connection, userId, amountToDeduct) {
      // Must run inside a transaction
      await connection.beginTransaction();

      try {
        // 1. Lock the wallet row for update
        const [wallets] = await connection.query(
          'SELECT id, balance FROM wallets WHERE user_id = ? FOR UPDATE',
          [userId]
        );

        if (wallets.length === 0) throw new Error('Wallet not found');
        const wallet = wallets[0];

        // 2. Check sufficient funds
        if (wallet.balance < amountToDeduct) {
          throw new Error('Insufficient funds');
        }

        // 3. Update the wallet balance
        await connection.query(
          'UPDATE wallets SET balance = balance - ? WHERE id = ?',
          [amountToDeduct, wallet.id]
        );

        // 4. Record entry in ledger
        await connection.query(
          'INSERT INTO wallet_ledger (wallet_id, amount, type) VALUES (?, ?, ?)',
          [wallet.id, -amountToDeduct, 'GAME_ENTRY']
        );

        await connection.commit();
        return { success: true };
      } catch (err) {
        await connection.rollback();
        throw err;
      }
    }
    ```

*   **Common Mistakes:**
    *   Using floating-point types (`FLOAT` or `DOUBLE`) to store currency values. Float types represent numbers using binary approximations, leading to fractional errors (like `0.1 + 0.2 = 0.30000000000000004`). Always use `DECIMAL` or store currency in cents/integers.
    *   Checking the balance on the backend web server, releasing the thread, and then executing the database update later without locks. This creates a race condition vulnerability.

*   **Follow-up Questions:**
    *   *What is the advantage of maintaining a ledger table?* It provides transaction history, auditing compliance, and allows reconstructing current balances if database corruption occurs.
    *   *How do you handle wallet scaling under hot-spot loads?* Batch ledger writes using a message queue, and cache balances in Redis to serve read traffic.

</details>

<hr/>

### ❓ Q20. Can a socket running on one server be accessed directly from other servers when multiple servers host socket.io?
<details>
<summary><b>👀 Show Answer</b></summary>

*   **No, they cannot be accessed directly.** 

    WebSockets maintain a stateful, persistent TCP connection between a specific client and a specific server process. If Client A is connected to Server Node 1, Server Node 2 has no way to access Client A's socket descriptor in memory.

    **The Solution: Socket.io Adapter (Pub/Sub):**
    To enable multi-server communication, we link all server nodes using a **Redis Pub/Sub Broker** alongside a Socket.io adapter (e.g. `@socket.io/redis-adapter`).

    **Workflow:**
    1.  When Server Node 1 needs to broadcast a message to a room or emit to Client A (who is connected to Server Node 2), it publishes the event details to a Redis channel.
    2.  All other Server Nodes are subscribed to the Redis channels.
    3.  Server Node 2 receives the Redis broadcast message, checks its local memory pool for matching clients or rooms, and sends the payload over the local TCP socket to Client A.

*   **Real-world Example:**
    ```text
    [Client A] --------(TCP Link)--------> [Server Node 1] 
                                                  | (Emit to 'Room-X')
                                                  v
                                            [Redis Adapter] (Publishes)
                                                  |
                                                  v
    [Client B] <-------(TCP Link)--------- [Server Node 2] (Subscribed)
    ```

    **Node.js Configuration:**
    ```javascript
    const { Server } = require('socket.io');
    const { createAdapter } = require('@socket.io/redis-adapter');
    const Redis = require('ioredis');

    const pubClient = new Redis({ host: 'redis-broker', port: 6379 });
    const subClient = pubClient.duplicate();

    const io = new Server(3000);
    // Bind Redis adapter to share room/socket states
    io.adapter(createAdapter(pubClient, subClient));

    io.on('connection', (socket) => {
      socket.on('join_game', (gameId) => {
        socket.join(gameId); // Shared across all nodes
      });

      socket.on('send_move', (data) => {
        // Emits to all players in gameId across all server instances
        io.to(data.gameId).emit('receive_move', data.move);
      });
    });
    ```

*   **Common Mistakes:**
    *   Scaling WebSockets servers horizontally without adding a Redis adapter. This results in users connected to different nodes being isolated from one another.
    *   Forgetting to configure **Sticky Sessions (Session Affinity)** on the Load Balancer (Nginx/ALB). During the Socket.io initial HTTP handshake, multiple HTTP polling requests must land on the same server instance to upgrade to a WebSocket connection. Without sticky sessions, the handshake fails.

*   **Follow-up Questions:**
    *   *What is the file descriptor bottleneck in WebSocket scaling?* Every open TCP connection is treated as an open file descriptor in Linux. By default, processes are capped at 1024. You must tune `/etc/security/limits.conf` (`nofile`) to scale to tens of thousands of connections.
    *   *How do you handle graceful shutdowns on WebSocket servers?* Disallow new connections, signal clients to disconnect and trigger reconnects with random delays (jitter), and wait for active connections to drain before stopping the container.

</details>

<hr/>

### ❓ Q21. What should be considered when uploading images to production to keep uploads safe?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Allowing file uploads is a high-risk security vector. To keep production systems safe, consider the following controls:

    1.  **Content Verification (Magic Numbers):**
        *   Do not trust client-supplied extensions (e.g. `.png`) or the `Content-Type` header. Attackers can upload malicious PHP/JS files disguised as images. Use libraries like `file-type` to read the **file header bytes** (magic numbers) to verify the actual file structure.
    2.  **Size Limits:**
        *   Restrict maximum upload file sizes (e.g. 5MB) at the proxy level (Nginx `client_max_body_size`) and the code level (`multer` limits) to prevent disk fill-up and DoS attacks.
    3.  **Filename Hashing:**
        *   Never store files with their user-supplied names. Attackers can exploit path traversal payloads (e.g. `../../etc/passwd`). Generate a unique identifier (like UUID or SHA256 hashes) on the server to rename the files.
    4.  **Isolated Storage:**
        *   Never store uploaded files on the local application server filesystem. If a server executes script files in upload folders, attackers can run Remote Code Execution (RCE) scripts. Upload files directly to dedicated object storage (AWS S3) and serve them as static assets.
    5.  **Exif Metadata Stripping:**
        *   Strip EXIF tags (GPS locations, camera info) from images using image processing libraries (e.g. `sharp`) to protect user privacy and remove malicious payload scripts hidden in metadata headers.
    6.  **Presigned S3 URLs:**
        *   To avoid consuming server network bandwidth and CPU cycles, generate a short-lived **Presigned Upload URL** on the backend and return it to the frontend. The frontend uploads the file directly to AWS S3.

*   **Real-world Example (Safe Node.js Upload Validation):**
    ```javascript
    const multer = require('multer');
    const crypto = require('crypto');
    const { fromBuffer } = require('file-type');

    // 1. Configure Multer memory storage and limits
    const upload = multer({
      storage: multer.memoryStorage(),
      limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
    }).single('avatar');

    app.post('/upload', upload, async (req, res) => {
      if (!req.file) return res.status(400).send('No file uploaded.');

      // 2. Validate magic numbers
      const type = await fromBuffer(req.file.buffer);
      const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
      
      if (!type || !allowedTypes.includes(type.mime)) {
        return res.status(400).send('Invalid file type. Only JPEG, PNG, and WebP are allowed.');
      }

      // 3. Generate secure hash name
      const fileHash = crypto.createHash('sha256').update(req.file.buffer).digest('hex');
      const secureName = `${fileHash}.${type.ext}`;

      // 4. Upload secureName to AWS S3 (pseudo-code)
      // await s3.upload(req.file.buffer, secureName);

      res.status(200).json({ filename: secureName });
    });
    ```

*   **Common Mistakes:**
    *   Deploying an upload directory inside a public Apache/Nginx web route with executable permissions, allowing uploaded scripts to run directly on the host machine.
    *   Omitting size limits on file formats, which allows users to upload multi-gigabyte files that freeze the event loop during buffer allocation.

*   **Follow-up Questions:**
    *   *How do presigned URLs improve server performance?* They bypass the Node.js process completely for the file data upload step, avoiding RAM allocation and network bandwidth bottlenecks on the API servers.
    *   *What is MIME sniffing?* A browser behavior where it tries to guess a file's content type by reading its bytes, which can lead to XSS if a browser executes script tags inside a text file disguised as an image. Prevent by setting the `X-Content-Type-Options: nosniff` header.

</details>

<hr/>

### ❓ Q22. What are queues and when are they used?
<details>
<summary><b>👀 Show Answer</b></summary>

*   A queue is a linear data structure that follows the **FIFO (First-In-First-Out)** execution pattern. In system architecture, message queues (like RabbitMQ, BullMQ, or AWS SQS) act as asynchronous communication buffers between different processes or microservices.

    **When to Use Queues:**
    1.  **Offloading Slow Tasks (Asynchronous Processing):**
        *   API endpoints must respond within milliseconds. Offload slow operations (sending emails, video transcoding, PDF generation, or database synchronization) to a queue. The API returns a fast receipt confirmation, and background worker processes consume and execute the tasks asynchronously.
    2.  **Smoothing Out Traffic Spikes (Load Leveling):**
        *   During high traffic events (e.g., ticket sales or game updates), a database can crash under high concurrent write loads. Queues buffer these incoming actions, letting worker processes consume and write to the database at a controlled, sustainable rate.
    3.  **Service Decoupling:**
        *   Queues allow microservices to interact without direct dependency. Service A pushes a message to the queue and doesn't need to know if Service B is currently online, scaling, or restarting.
    4.  **Resilience and Retry Handling:**
        *   If a background task fails (e.g., an external email API is down), the queue tracks the failure, handles backoff delays, and retries the job later. Persistent messages are not lost.

*   **Real-world Example (API with BullMQ Background Job):**
    ```text
    [Client] ---(HTTP POST Request)---> [Express API] ---(Returns 202 Accepted)
                                             | (Pushes task)
                                             v
                                      [Redis Queue (BullMQ)]
                                             |
                                             v (Pulls task)
                                      [Worker Process] ---> (Sends Email / Video Compresses)
    ```

    **Node.js Implementation:**
    ```javascript
    const { Queue, Worker } = require('bullmq');
    const Redis = require('ioredis');

    const connection = new Redis({ host: 'redis-server' });

    // 1. Define the Queue (Used by the API Server)
    const emailQueue = new Queue('emails', { connection });

    app.post('/register', async (req, res) => {
      // Create user in database...
      
      // Push email task to the queue and return 202 immediately
      await emailQueue.add('sendWelcomeEmail', {
        email: req.body.email,
        name: req.body.name
      }, { attempts: 3, backoff: 5000 }); // Retry 3 times, wait 5s between retries

      res.status(202).json({ message: 'Registration processing...' });
    });

    // 2. Define the Worker (Can run on a completely separate server)
    const emailWorker = new Worker('emails', async (job) => {
      console.log(`Processing job ${job.id}: Sending email to ${job.data.email}`);
      // Send email logic (e.g., Nodemailer / SendGrid)
      await sendActualEmail(job.data.email, job.data.name);
    }, { connection });
    ```

*   **Common Mistakes:**
    *   Using queues for synchronous interactions where the client must wait for the job results before rendering the page. (Use REST/gRPC instead).
    *   Failing to set up alert monitoring for queue lengths. If workers fail or crash, jobs accumulate in the queue, causing a delay in processing without generating typical API crash alerts.

*   **Follow-up Questions:**
    *   *What is a Dead Letter Queue (DLQ)?* A dedicated queue where messages that fail repeatedly after all retry attempts are sent for developers to inspect and debug manually.
    *   *How does a FIFO queue differ from Pub/Sub?* In a queue, each message is consumed by exactly **one** worker. In Pub/Sub (Publish-Subscribe), a message is broadcasted and consumed by **all** active subscribers.

</details>
