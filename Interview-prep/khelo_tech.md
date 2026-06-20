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

</details>

<hr/>

### ❓ Q5. What is the difference between streams and buffers and which holds complete data like images? (Hinglish Explained)
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Both streams and buffers are binary data ko handle karne ke liye use hote hain, par inka tarika aur memory allocation bilkul alag hota hai:**

    1.  **Buffer:**
        *   **Definition:** RAM (memory) ka ek temporary, fixed-size block hota hai (V8 engine heap se bahar) jo binary bytes store karta hai.
        *   **Data Handling:** Yeh **poore data** ko ek sath memory mein hold karta hai.
        *   **Use Case:** Files ko modify/edit karne ke liye, jaise poori image ko load karke crop/resize karna, config file parse karna, ya bytes ko manipulate karna.
    2.  **Stream:**
        *   **Definition:** Yeh data ko ek sath memory me load karne ki jagah **chunk-by-chunk (chote-chote tukdo mein)** process karne ka tarika hai.
        *   **Data Handling:** Yeh kabhi bhi poore data block ko RAM me nahi rakhta, jisse memory consumption minimal rehta hai.
        *   **Use Case:** Large files (videos, server logs, database exports) ko network ya file system par transfer karne ke liye.

    **Which holds complete data like images?**
    **Buffer** complete data ko hold karta hai. Jab aap `fs.readFile()` se image read karte hain, toh Node.js RAM mein us image ka complete binary Buffer return karta hai. Jabki **Stream** us image data ko chunk-by-chunk transport karne ke liye use hota hai (jaise S3 bucket se user response tak bhejte waqt bina server RAM waste kiye).

*   **Real-world Example:**
    *   **Using Buffer (Memory Intensive - Server crash ka darr):**
        ```javascript
        const fs = require('fs');
        // Pura 500MB image RAM me load ho jayega. High traffic me OOM crash ho sakta hai.
        fs.readFile('heavy_image.png', (err, buffer) => {
          if (err) throw err;
          console.log("Buffer length:", buffer.length); // Pura image memory me hai
        });
        ```
    *   **Using Stream (Memory Optimized - Safe for production):**
        ```javascript
        const fs = require('fs');
        const http = require('http');
        
        http.createServer((req, res) => {
          const stream = fs.createReadStream('heavy_image.png');
          // Chunks (default 64KB) ko directly response me pipe (flow) karega. RAM save hogi.
          stream.pipe(res);
        }).listen(3000);
        ```

</details>

<hr/>

### ❓ Q6. For the following event loop snippet, predict and explain the execution order.
<details>
<summary><b>👀 Show Answer</b></summary>

*   Here is the event loop code snippet to analyze:
    ```javascript
    const fs = require('fs');

    console.log("start");

    setTimeout(() => {
      console.log("setTimeOut");
    }, 1000);

    setImmediate(() => {
      console.log("setImmediate");
    });

    fs.readFile(__filename, () => {
      console.log("polling");
    });

    process.nextTick(() => {
      console.log("nextTick");
    });

    console.log("end");
    ```

    **Execution Order Tracing:**
    1.  `console.log("start")` executes synchronously. Prints: `start`.
    2.  `setTimeout` is registered with a 1000ms delay.
    3.  `setImmediate` registers a callback to execute in the Check phase.
    4.  `fs.readFile` requests an asynchronous read operation from the OS/libuv thread pool.
    5.  `process.nextTick` registers its callback in the high-priority nextTick microtask queue.
    6.  `console.log("end")` executes synchronously. Prints: `end`.
    7.  **Draining Microtasks:** The call stack is now empty. The nextTick queue is immediately drained, printing: `nextTick`.
    8.  **First Event Loop Cycle:**
        *   The loop checks the Check Phase because `setImmediate` is scheduled. It executes it and prints: `setImmediate`.
    9.  **Subsequent Cycles:**
        *   Once the file system reads the file, the Poll Phase receives the callback event and prints: `polling`.
        *   Finally, after 1000ms have elapsed, the timer expires and the Timers Phase executes the callback, printing: `setTimeOut`.

    **Final Output:**
    ```text
    start
    end
    nextTick
    setImmediate
    polling
    setTimeOut
    ```

*   **Real-world Example:**
    This execution sequence demonstrates that `process.nextTick` runs immediately after the synchronous block, long before standard event loop phases like Check (`setImmediate`), Poll (`polling`), or Timers (`setTimeout`), and that timers with non-zero delays yield execution to immediate and I/O tasks.

</details>

<hr/>

### ❓ Q7. Predict the console output order for the following async/await block.
<details>
<summary><b>👀 Show Answer</b></summary>

*   Here is the async/await execution snippet to analyze:
    ```javascript
    const fs = require('fs');

    async function run() {
      try {
        console.log("a");
        const resp = await fs.promises.readFile(__filename, "utf8");
        console.log("b");
      } catch (err) {}
    }

    console.log("c");
    run();
    ```

    **Execution Steps Tracing:**
    1.  `console.log("c")` runs synchronously first. Prints: `c`.
    2.  `run()` is called. Execution enters the async function synchronously.
    3.  `console.log("a")` runs synchronously. Prints: `a`.
    4.  `await fs.promises.readFile(...)` is encountered. The async execution of `run()` is suspended, and the remaining lines (logging `b`) are scheduled as a callback in the Microtask Queue once the file promise resolves.
    5.  Control returns to the main thread. Since there are no further synchronous lines to execute, the thread yields.
    6.  Once the file system completes the read operation, the promise resolves. V8 pushes the remaining part of `run()` onto the microtask queue, which is executed by the Event Loop. Prints: `b`.

    **Final Output:**
    ```text
    c
    a
    b
    ```

    **Alternative Scenario (Calling `run()` before `console.log("c")`):**
    If the code was structured as:
    ```javascript
    run();
    console.log("c");
    ```
    1.  `run()` is called. Prints: `a`.
    2.  `await` suspends execution and yields control back.
    3.  Main thread resumes and runs `console.log("c")`. Prints: `c`.
    4.  The file read completes, triggering the microtask execution. Prints: `b`.
    *Alternative Output:* `a` -> `c` -> `b`.

*   **Real-world Example:**
    This highlights that `async` functions execute synchronously *until* the first `await` is hit. The `await` returns control back to the outer execution context, and anything after it is deferred as a microtask.

</details>

<hr/>

### ❓ Q8. What is the output of the following closure snippet, and how does it work?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Here is the closure snippet to analyze:
    ```javascript
    function outer() {
      let a = "name";
      return function inner() {
        a = "class";
        console.log(a);
      };
    }

    const resp = outer();
    resp();
    ```

    **Execution Flow:**
    1.  `const resp = outer()` executes the `outer` function.
    2.  A variable `a` is declared in the local scope of `outer` and initialized with `"name"`.
    3.  `outer` returns the function definition of `inner` and finishes execution. Its local execution stack is destroyed.
    4.  However, because of **closures**, the returned `inner` function maintains a reference to its lexical environment (the scope in which it was declared), which includes the variable `a`.
    5.  `resp()` invokes the `inner` function.
    6.  Inside `inner`, `a = "class"` modifies the variable `a` inside the lexical scope of `outer`.
    7.  `console.log(a)` outputs `"class"`.

    **Final Output:**
    ```text
    class
    ```

*   **Real-world Example:**
    Closures are heavily used in JavaScript to create private variables or stateful factories:
    ```javascript
    function createCounter() {
      let count = 0; // Private variable
      return {
        increment: () => ++count,
        getCount: () => count
      };
    }
    const counter = createCounter();
    console.log(counter.increment()); // 1
    console.log(counter.getCount());  // 1
    ```

</details>

---

## 2. React & Frontend Integration

### ❓ Q9. What do useMemo and useCallback each do in React?
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

</details>

<hr/>

### ❓ Q10. What are SSR and CSR and which is more SEO-friendly?
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

</details>

---

## 3. Database Engineering & Caching

### ❓ Q11. What are ACID properties in databases? (Hinglish Explained)
<details>
<summary><b>👀 Show Answer</b></summary>

*   **ACID properties database transactions ko reliably process karne ke rules hain, jo system failure ke waqt bhi data integrity (correctness) banaye rakhte hain:**

    1.  **Atomicity ("All or Nothing" - Sab kuch ya kuch bhi nahi):**
        *   Transaction ko ek single unit mana jata hai. Ya toh transaction ke saare SQL commands execute honge (Commit), ya fir ek bhi execute nahi hoga aur purani state par rollback ho jayega. Beech ka koi rasta nahi hota.
    2.  **Consistency (Consistency bani rahe):**
        *   Transaction complete hone ke baad database hamesha ek valid state se dusri valid state mein hi jayega. Saare rules, foreign keys, triggers, aur constraints strictly follow honge.
    3.  **Isolation (Alag-alag execution):**
        *   Jab ek sath multiple transactions chal rahe hon, toh wo ek dusre ke intermediate (adhure) data ko nahi dekh sakte. Har transaction ko lagta hai ki wo database par akela execute ho raha hai. Isko Isolation Levels ke through manage kiya jata hai.
    4.  **Durability (Hamesha ke liye save):**
        *   Ek baar transaction `COMMIT` (save) ho gaya, toh uska data permanently disk/SSD par save ho jata hai. Iske baad agar database crash ho jaye, light chali jaye, ya OS restart ho jaye, tab bhi data lost nahi hoga.

*   **Real-world Example (BookMyShow Movie Ticket Booking):**
    Imagine aap BookMyShow par **Seat A1** book kar rahe hain jiske liye aapko **Rs 300** pay karne hain.
    ```sql
    START TRANSACTION;
    -- 1. User ke bank account se Rs 300 deduct karo
    UPDATE bank_accounts SET balance = balance - 300 WHERE user_id = 'Aman';
    -- 2. Seat A1 ko booked status par set karo
    UPDATE seats SET status = 'BOOKED', booked_by = 'Aman' WHERE seat_number = 'A1';
    COMMIT;
    ```
    *   **Atomicity:** Agar Step 1 chalne ke baad (paise cut gaye) aur Step 2 se pehle server crash ho jaye, toh database transaction ko automatically rollback kar dega. Aman ke paise bank account me wapas aa jayenge aur ticket book nahi hoga.
    *   **Consistency:** Database me rule hai ki ek seat par ek hi user map ho sakta hai (Unique Constraint). Transaction se pehle aur baad me yeh rule strictly check hota hai.
    *   **Isolation:** Agar Aman aur Rohit ek hi exact millisecond par Seat A1 book karne ka try karte hain, toh database isolation / row locks use karega. Jab tak Aman ka transaction chal raha hai, Rohit ka transaction wait karega. Rohit ko tab tak Seat A1 booked nahi dikhegi jab tak Aman ka confirm ya fail nahi ho jata.
    *   **Durability:** Jaise hi payment successfully complete ho jati hai aur screen par ticket confirm ho jata hai (COMMIT), data disk/SSD par permanently save ho jata hai. Iske baad agar BookMyShow ke servers down bhi ho jayein, restart hone par aapka ticket booked hi rahega.

</details>

<hr/>

### ❓ Q12. How should composite indexes be structured for effectiveness?
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

</details>

<hr/>

### ❓ Q13. How can a slow query be optimized? (Hinglish Explained)
<details>
<summary><b>👀 Show Answer</b></summary>

*   Slow queries ko optimize karne ke liye hum 4 primary levels par approach karte hain:

    1.  **Diagnosis (Pata lagana ki problem kahan hai):**
        *   Slow Query Log ya APM tools se slow queries ko locate karein.
        *   Query ke aage `EXPLAIN` lagakar **Execution Plan** check karein ki data fetch kaise ho raha hai. (E.g., `type: ALL` to nahi hai? `key` NULL to nahi hai?).
    2.  **Database Level - Indexing lagana:**
        *   `WHERE`, `JOIN`, `ORDER BY` aur `GROUP BY` ke columns par indexes lagayein.
        *   Composite indexes banate waqt **ESR Rule** (Equality, Sort, Range) follow karein.
        *   **Covering Indexes** use karein taaki query ka saara selected data index tree se hi mil jaye aur disk par main table lookup na karna pade.
    3.  **Query Level - Query rewrite karna (Avoiding SELECT *):**
        *   **`SELECT *` bilkul use na karein:** Hamesha wahi columns mangayein jinhe use karna hai. Yeh network payload aur database disk I/O ko fast karta hai.
        *   Queries ko **Sargable** banayein. E.g., `WHERE DATE(created_at) = '2026-06-16'` (non-sargable) ki jagah ranges use karein `WHERE created_at >= '2026-06-16 00:00:00' AND ...` (sargable) taaki index use ho sake.
    4.  **Application Level - Solving N+1 Query & Caching:**
        *   **N+1 Query Problem solve karein:** Loop ke andar database query call karne ke bajaye (N+1 queries), **JOINs** ya ORM ki **Eager Loading** (e.g., Prisma's `include` ya Sequelize's `include`) ka use karein. Yeh database round-trips ko 101 se seedhe 1 ya 2 par le aayega.
        *   Read-heavy aur database calculation-heavy data ko **Redis** me cache (Cache-Aside pattern) karein.

*   **Real-world Example (N+1 Query vs Eager Loading):**
    *   *Bad Pattern (N+1 Queries - loop me call karna):*
        ```javascript
        // 1 query to get all posts (say 100 posts)
        const posts = await db.query('SELECT * FROM posts'); 
        for (let post of posts) {
          // 100 queries inside loop to get author details (N queries)
          const author = await db.query('SELECT * FROM users WHERE id = ?', [post.authorId]);
        }
        // Total queries = 1 + 100 = 101 queries!
        ```
    *   *Good Pattern (Eager Loading / JOIN - single query):*
        ```javascript
        // Single optimized JOIN query
        const postsWithAuthors = await db.query(`
          SELECT p.id, p.title, u.name as author_name 
          FROM posts p 
          JOIN users u ON p.authorId = u.id
        `);
        // Total queries = Only 1 query!
        ```

</details>

<hr/>

### ❓ Q14. What is a Query Execution Plan, and how do you analyze it? (Hinglish Explained)
<details>
<summary><b>👀 Show Answer</b></summary>

*   **Query Execution Plan** database engine (jaise MySQL ya PostgreSQL) dwara generate kiya gaya ek sequence of steps (roadmap) hota hai jo batata hai ki database query ka data fetch karne ke liye kaunsa raasta lega. Database optimizer is plan ko table ke metrics, indexes, aur filter conditions ke aadhar par banata hai.

    **How to Generate and Analyze Plan in MySQL (Hinglish):**
    Apni query statement ke pehle `EXPLAIN` ya `EXPLAIN ANALYZE` keyword lagayein.

    **Key Output Fields to Review (Important check points):**
    1.  **`type` (Access Method - Data kaise dhoondha ja raha hai):**
        *   `ALL` (Full Table Scan): Sabse bekar. Poore table ki ek-ek row ko disk par scan karta hai.
        *   `const`/`eq_ref`: Sabse best. Unique Primary Key lookup.
        *   `ref`/`range`: Acha hai. Index search ya specific range scan.
    2.  **`key` (Selected Index):** Kaunsa index search ke liye select hua. Agar `NULL` hai, toh matlab index use hi nahi ho raha.
    3.  **`rows` (Estimated rows):** Database ko kitne records check karne padenge. Row count jitna zyada hoga, query utni slow hogi.
    4.  **`Extra` (Additional info):**
        *   `Using index`: Bohat badhiya! Pura data index tree se hi mil gaya, table disk par jump nahi karna pada (Covering Index).
        *   `Using filesort`: Kharab sign. Database ko manual sorting karni pad rahi hai (slow performance).
        *   `Using temporary`: Kharab sign. Database ko temporary table banana pad raha hai results filter karne ke liye.

*   **Real-world Example (GPS Navigator analogy):**
    Jaise Google Maps batata hai ki shortest root kaunsa hai (highway se jana hai ya galiyon se), vaise hi Execution Plan database ka map hai.
    *   **Without Index (Highway block - Galiyon se jana):**
        ```sql
        EXPLAIN SELECT * FROM orders WHERE status = 'SHIPPED';
        ```
        *Output Plan:*
        - `type`: `ALL` (Har order ko check karega)
        - `key`: `NULL` (Koi map/index nahi hai)
        - `rows`: `984,212` (Lagbhag 10 lakh rows scan karega - Very Slow)
    *   **With Index (Highway clear):**
        ```sql
        CREATE INDEX idx_status ON orders(status);
        EXPLAIN SELECT * FROM orders WHERE status = 'SHIPPED';
        ```
        *Output Plan:*
        - `type`: `ref` (Directly status match karega)
        - `key`: `idx_status` (Index highway use karega)
        - `rows`: `1,420` (Sirf matching rows ko scan karega - Instant Output)

</details>

<hr/>

### ❓ Q15. What is the security issue with constructing a SQL query by embedding an email variable directly?
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

    *   **Secure Code (Prepared Statement for `SELECT * FROM users WHERE email="rnishant@gmail.com"`):**
        ```javascript
        const query = 'SELECT * FROM users WHERE email = ?';
        db.query(query, ['rnishant@gmail.com']);
        ```
        *Resulting Action:* The database searches for a user whose email string is literally `rnishant@gmail.com`, rendering any query manipulation attempts completely harmless.

</details>

<hr/>

### ❓ Q16. Why is Redis faster than disk-backed databases?
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

</details>

<hr/>

### ❓ Q17. When generating a query and retrieving data from Redis, how do we retrieve data from Redis?
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

</details>

<hr/>

### ❓ Q18. How do you implement Redis SET (with TTL) and GET commands in Node.js?
<details>
<summary><b>👀 Show Answer</b></summary>

*   To perform basic operations in Redis using Node.js, we commonly use the `ioredis` or `redis` npm libraries. Writing data with a expiration window (TTL) helps prevent memory exhaustion.

    **Core Commands:**
    1.  **`SET` with TTL:** Writes a key-value pair to Redis and assigns it an expiration lifetime. This is handled using options like `EX` (seconds) or `PX` (milliseconds), or by using the specific `SETEX` command.
    2.  **`GET`:** Retrieves the value of a string-based key. If the key does not exist or has expired, it returns `null`.

*   **Real-world Example:**
    ```javascript
    const Redis = require('ioredis');
    const redis = new Redis(); // Connects to localhost:6379 by default

    async function handleSessionCache() {
      const key = "session:user:101";
      const value = JSON.stringify({ username: "rnishant", role: "admin" });
      const ttlInSeconds = 300; // 5 minutes

      // 1. SET key with value and TTL (using option syntax or setex)
      // Syntax A (Modern SET with EX option):
      const setResp = await redis.set(key, value, 'EX', ttlInSeconds);
      console.log("SET response:", setResp); // Prints: "OK"

      // Syntax B (Classic SETEX wrapper):
      // await redis.setex(key, ttlInSeconds, value);

      // 2. GET key from Redis
      const cachedVal = await redis.get(key);
      if (cachedVal) {
        const userObj = JSON.parse(cachedVal);
        console.log("GET response (Username):", userObj.username); // Prints: "rnishant"
      } else {
        console.log("Cache missed or expired.");
      }
    }
    ```

</details>

<hr/>

### ❓ Q19. Write the database transaction logic for a secure wallet transfer between two users (`deductAmount` and `creditAmount`).
<details>
<summary><b>👀 Show Answer</b></summary>

*   A wallet transfer must execute atomically (all or nothing) and securely (preventing concurrent race conditions and double-spending). This requires wrapping database writes inside a transaction and acquiring lock handles.

    **Safe Implementation Principles:**
    1.  **Consistent Lock Order:** Always lock the smaller account ID first to prevent database deadlocks.
    2.  **Pessimistic Locking (`FOR UPDATE`):** Lock the sender's balance row to prevent balance modifications from concurrent processes.
    3.  **Validate Balance:** Check that the sender has sufficient funds *after* locking their row.
    4.  **Transaction Control:** Call `commit` on success or `rollback` on any exception to ensure atomicity.

*   **Real-world Example (Node.js & MySQL/Promise):**
    ```javascript
    const mysql = require('mysql2/promise');
    const dbPool = mysql.createPool({ host: 'localhost', database: 'wallet_db' });

    async function executeWalletTransfer(senderId, receiverId, amount) {
      const connection = await dbPool.getConnection();
      await connection.beginTransaction();

      try {
        // Step 1: Prevent deadlocks by sorting IDs
        const firstId = senderId < receiverId ? senderId : receiverId;
        const secondId = senderId < receiverId ? receiverId : senderId;

        // Step 2: Lock both rows in sorted order (pessimistic lock)
        await connection.query('SELECT balance FROM wallets WHERE user_id = ? FOR UPDATE', [firstId]);
        await connection.query('SELECT balance FROM wallets WHERE user_id = ? FOR UPDATE', [secondId]);

        // Step 3: Check sender's current balance
        const [senderRows] = await connection.query(
          'SELECT balance FROM wallets WHERE user_id = ?',
          [senderId]
        );
        const senderBalance = parseFloat(senderRows[0].balance);

        if (senderBalance < amount) {
          throw new Error('Insufficient balance');
        }

        // Step 4: Deduct amount from sender
        await connection.query(
          'UPDATE wallets SET balance = balance - ? WHERE user_id = ?',
          [amount, senderId]
        );

        // Step 5: Credit amount to receiver
        await connection.query(
          'UPDATE wallets SET balance = balance + ? WHERE user_id = ?',
          [amount, receiverId]
        );

        // Step 6: Log changes in an audit ledger (Optional but recommended)
        await connection.query(
          'INSERT INTO ledger (sender_id, receiver_id, amount) VALUES (?, ?, ?)',
          [senderId, receiverId, amount]
        );

        // Step 7: Commit transaction
        await connection.commit();
        return { success: true };
      } catch (error) {
        // Abort all changes if any query fails or validation throws
        await connection.rollback();
        console.error('Transfer failed, rolled back:', error.message);
        throw error;
      } finally {
        connection.release();
      }
    }
    ```

</details>

<hr/>

### ❓ Q20. What is the Cache-Aside pattern, and how is it implemented?
<details>
<summary><b>👀 Show Answer</b></summary>

*   The **Cache-Aside** (or Lazy Loading) pattern is a caching design pattern where the application itself coordinates reads and writes between a data cache (like Redis) and the primary database (like MySQL). The cache acts as a helper, and the primary database remains the source of truth.

    **Operations Flow:**
    *   **Read Workflow:**
        1.  Check if data exists in the cache.
        2.  *Cache Hit:* Return data immediately.
        3.  *Cache Miss:* Retrieve data from database, store it in cache with a TTL, and return it.
    *   **Write Workflow:**
        1.  Write data changes to the primary database.
        2.  Invalidate (delete) the corresponding key from the cache to prevent serving stale data.

*   **Real-world Example:**
    ```text
    [Client] --------> (1. Request Data) --------> [App Server]
                                                       |
                      +------------ No (Miss) ---------+------ Yes (Hit) ----+
                      |                                                      |
                      v                                                      v
             [MySQL Primary DB]                                       [Redis Cache]
                      |                                                      |
              (2. Fetch Data)                                         (Return Value)
                      |
                      v
             [Update Redis Cache]
                      |
                      v
                (Return Value)
    ```

    **Code Implementation:**
    ```javascript
    async function getArticle(articleId) {
      const cacheKey = `article:${articleId}`;

      // 1. Try to read from cache
      const cachedArticle = await redis.get(cacheKey);
      if (cachedArticle) {
        return JSON.parse(cachedArticle); // Cache Hit
      }

      // 2. Fetch from DB on Cache Miss
      const article = await db.select('*').from('articles').where({ id: articleId }).first();
      
      if (article) {
        // 3. Write to cache with TTL (1800 seconds / 30 mins)
        await redis.setex(cacheKey, 1800, JSON.stringify(article));
      }

      return article;
    }

    async function updateArticle(articleId, updatedFields) {
      // 1. Update database
      await db('articles').where({ id: articleId }).update(updatedFields);

      // 2. Invalidate cache key
      await redis.del(`article:${articleId}`);
    }
    ```

</details>

---

## 4. Docker & Containerization

### ❓ Q21. What is the difference between a Dockerfile and a Docker Compose file?
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
        *   **Purpose:** Configures how multiple containers (e.g., Node.js API, Redis cache, MySQL database) interact. It defines port mappings, shared virtual networks, persistent storage volumes, environment variables, and service startup orders (`depends_on`).

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

</details>

<hr/>

### ❓ Q22. What is wrong with the following Dockerfile snippet and how would you optimize it?
<details>
<summary><b>👀 Show Answer</b></summary>

*   Here is the problematic Dockerfile snippet to evaluate:
    ```dockerfile
    From alpine-node:latest
    Workdir /app
    cp package.json ./app
    Apt npm install 
    Cp . ./app
    Apt run [‘node’,’start’]
    ```

    **Identified Errors & Problems:**
    1.  **Non-standard Base Image:** `alpine-node` is not an official Node.js image. Official Docker hub images are named `node:<version>-alpine`.
    2.  **Instruction Casing:** Commands like `From`, `Workdir`, `cp` are capitalized incorrectly. Dockerfile conventions dictate uppercase (`FROM`, `WORKDIR`, `COPY`).
    3.  **Invalid `cp` Commands:** `cp` is a shell command. Inside a Dockerfile, you must use the `COPY` instruction.
    4.  **Incorrect Destination Paths:** After setting `WORKDIR /app`, the current context is `/app`. Copying files to `./app` creates a nested folder `/app/app`.
    5.  **Invalid `Apt npm install` Command:** `Apt` is not a Docker instruction. In Alpine-based images, the package manager is `apk`, not `apt-get`. Also, to execute shell commands, you must use `RUN`.
    6.  **Incorrect `Apt run [...]` syntax:** To configure the default container startup execution command, use the `CMD` instruction. The array syntax must use straight standard double quotes (`"`), not smart curly quotes (`‘`, `’`).

*   **Real-world Example (Corrected and Optimized Production Dockerfile):**
    ```dockerfile
    # 1. Use official Node.js Alpine base image
    FROM node:20-alpine

    # 2. Set directory workspace
    WORKDIR /app

    # 3. Copy package locks first for Docker cache usage
    COPY package*.json ./

    # 4. RUN command to install packages (using npm ci for production)
    RUN npm ci --only=production

    # 5. COPY application code to workspace root
    COPY . .

    # 6. Expose internal port
    EXPOSE 3000

    # 7. Start container execution command with correct JSON double quotes
    CMD ["npm", "start"]
    ```

</details>

---

## 5. System Design, Security & Architecture

### ❓ Q23. How does JWT signature verification work and what alternatives exist?
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

</details>

<hr/>

### ❓ Q24. How does rate limiting protect services and what response is returned when limits are exceeded?
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

</details>

<hr/>

### ❓ Q25. How do Razorpay/Stripe integrations and webhooks work in a payment flow? (Hinglish Explained)
<details>
<summary><b>👀 Show Answer</b></summary>

*   Ek secure online payment flow sensitive card details (like Card number, CVV) ko aapke app server par aane se rokta hai (PCI-DSS compliance ke liye) aur saara heavy security work Stripe/Razorpay handle karta hai.

    **Step-by-Step Payment Flow (Hinglish):**
    1.  **Initiation (Shooruaat):** User frontend par "Buy Now" button click karta hai.
    2.  **Order Creation (Backend):** Aapka backend server, Stripe/Razorpay APIs ko ek secure server-to-server request bhejta hai (amount aur currency details ke sath). Gateway wahan se ek `client_secret` (Stripe) ya `order_id` (Razorpay) return karta hai.
    3.  **UI Render (Frontend):** Frontend is ID ko receive karta hai aur Stripe/Razorpay ka payment library (modal/iframe) load karta hai. User card details direct is iframe ke andar fill karta hai jo secure way me gateway se linked hota hai.
    4.  **Authorization (Bank se permission):** Gateway details ko process karta hai aur user ke bank ke sath authenticate karta hai (jaise OTP validation).
    5.  **Redirect & Webhook Dispatch:**
        *   Payment successful hote hi, browser user ko redirect karta hai success page par.
        *   **Sabse Important Step:** Same time par, gateway backend server ko ek asynchronous **Webhook** event (HTTP POST request) bhejta hai (e.g. `payment_intent.succeeded` event) payment success confirm karne ke liye.
    6.  **Fulfillment (Order delivery):** Aapka backend webhook ka **signature verify** karta hai, user ka status paid mark karta hai, aur payment gateway ko `200 OK` response bhej deta hai.

    **Why Webhooks are Mandatory (Webhooks kyun zaroori hain?):**
    Maan lo user ne payment kar di, bank se paise bhi cut gaye, par usi microsecond par user ka browser freeze ho gaya, tab close ho gayi, ya internet disconnect ho gaya. 
    Aise case me client-side frontend aapke backend ko "Success" notification nahi bhej payega, aur user ke paise katne par bhi use order deliver nahi hoga. **Webhook ek secure server-to-server link hai** jo guaranteed data transfer ensure karta hai chahe client (browser) down hi kyun na ho jaye.

*   **Real-world Example (Stripe Webhook Handler in Node.js):**
    ```javascript
    const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

    app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
      const sig = req.headers['stripe-signature'];
      let event;

      try {
        // 1. Signature check karna zaroori hai taaki koi fake request na bhej sake
        event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
      } catch (err) {
        console.error(`Webhook signature verification failed: ${err.message}`);
        return res.status(400).send(`Webhook Error: ${err.message}`);
      }

      // 2. Event type check karo aur database update karo
      if (event.type === 'payment_intent.succeeded') {
        const paymentIntent = event.data.object;
        console.log(`Payment successful for amount: ${paymentIntent.amount}`);
        // Yahan database update karein (e.g., markOrderAsPaid(orderId))
      }

      // 3. Gateway ko 200 OK bhein taaki wo dobara same event retry na kare
      res.json({ received: true });
    });
    ```

</details>

<hr/>

### ❓ Q26. What is idempotency and how is it implemented?
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

</details>

<hr/>

### ❓ Q27. How should a simple wallet system be designed at the database level?
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

</details>

<hr/>

### ❓ Q28. Can a socket running on one server be accessed directly from other servers when multiple servers host socket.io?
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

</details>

<hr/>

### ❓ Q29. What should be considered when uploading images to production to keep uploads safe?
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

</details>

<hr/>

### ❓ Q30. What are queues and when are they used?
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

</details>

---

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Angular](./06_Angular.md) | [Home](./00_Index.md) | 🚫 *None* |

