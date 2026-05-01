# 📌 Topic: Low-Level Debugging (Post-Mortem)

## 🧠 Concept Explanation
Low-level debugging is like **Analyzing a Plane's Black Box after a Crash**.
**Analogy:** 
- **Standard Debugging:** You're sitting in the cockpit watching the gauges while the plane is flying.
- **Low-Level Debugging (Post-Mortem):** The plane has crashed and is a pile of metal on the ground. You take a "Core Dump" (a complete image of the plane's state at the moment of impact) and bring it to a lab. Using specialized tools, you reconstruct the state of every engine and the position of every switch to find out *exactly* what happened.

---

## 🏗️ Mental Model
When a Node.js process crashes or hangs in a way that standard logs can't explain, you look at the **System Level**. You analyze the interaction between the Node.js process and the OS Kernel.

---

## ⚡ Actual Behavior
*   **Core Dumps:** A file containing the full memory image of the process. Can be triggered manually or automatically on a crash.
*   **System Calls:** Tracking every time Node.js asks the OS for something (e.g., `open`, `read`, `write`, `socket`).
*   **GDB / LLDB:** Debuggers that let you inspect the C++ state of the Node.js runtime and the memory addresses of JS objects.

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **`strace` (Linux) / `dtruss` (macOS):** Intercepts and records the system calls which are called by a process and the signals which are received by a process.
*   **Post-Mortem Metadata:** V8 includes "debug constants" in the binary that tell tools like `gdb` how to translate raw memory addresses back into JavaScript object names.
*   **Abort on Uncaught Exception:** Using the `--abort-on-uncaught-exception` flag to force a core dump the moment a crash occurs.

---

## 🔁 Execution Flow (Post-Mortem Analysis)
1.  **Crash:** Node.js process dies.
2.  **Dump:** OS writes a `core` file to disk.
3.  **Inspect:** Load the core file into a tool like `mdb` or `llnode`.
4.  **Identify:** Find the stack trace at the time of the crash.
5.  **Examine:** Look at the values of variables in memory that caused the failure.

---

## 🧠 Resource Behavior
*   **Disk:** Core dumps are the size of your RAM usage. If Node was using 2GB of RAM, the dump will be 2GB.
*   **CPU:** Generating a core dump freezes the process for several seconds.

---

## 📐 ASCII Diagrams
```text
[ NODE.JS PROCESS ] --- (System Call) ---> [ OS KERNEL ]
        |                                       |
    (Crash!)                                    |
        |                                       |
  [ CORE DUMP FILE ] <--------------------------+
        |
  [ llnode / gdb ] (Analysis Tool)
        |
  [ RECONSTRUCTED JS STACK ]
```

---

## 🔍 Code Example (Latest Node.js - Generating a Core Dump)
```bash
# Start Node and tell it to dump core on crash
node --abort-on-uncaught-exception app.js

# Or, generate a dump for a running process (PID 1234)
gcore 1234

# Use 'llnode' to inspect a core file
# (Install via: npm install -g llnode)
llnode node -c core.1234

# Inside llnode:
# v8 help          (See available commands)
# v8 bt            (Get the JS backtrace from the core dump)
# v8 inspect <ptr> (Examine a specific memory address)
```

---

## 💥 Production Failures
*   **Segfaults:** A C++ module tries to access memory it doesn't own. Regular Node.js logs will simply say `Segmentation Fault` and provide zero info.
*   **Invisible Deadlocks:** Two threads in a native module are waiting for each other, causing the whole process to hang without using any CPU.

---

## 🧪 Real-time Scenarios
*   **Heisenbugs:** Bugs that disappear the moment you add logging. Core dumps capture the bug in its "natural state" without interference.
*   **Kernel Bottlenecks:** Using `strace` to find out that your app is spending 50% of its time just opening and closing the same configuration file over and over.

---

## ⚠️ Edge Cases
*   **Stripped Binaries:** If the Node.js binary was compiled without "symbols," low-level tools won't be able to tell you the names of functions, only memory addresses like `0x0045fa2`.
*   **Permissions:** On many systems, core dumps are disabled by default (`ulimit -c 0`).

---

## 🏢 Best Practices
1.  **Enable Core Dumps in Staging:** Always have it ready so you can catch crashes that don't happen in local dev.
2.  **Keep the exact binary:** You must use the exact same Node.js version/binary to analyze the core dump that was used to create it.
3.  **Use `llnode`:** It's specifically designed for Node.js and is much easier than raw `gdb`.

---

## ⚖️ Trade-offs
*   **Post-Mortem:** Extremely detailed, catches the "uncatchable," but very complex and requires specialized knowledge.
*   **Live Debugging:** Easier and faster, but can miss race conditions and doesn't help once the process has already crashed.

---

## 💼 Interview Q&A
*   **Q:** What is a Segmentation Fault?
*   **A:** It's an error raised by hardware with memory protection, notifying an OS that a process has attempted to access a restricted area of memory.

---

## 🧩 Practice Problems
1.  Use `strace -c node app.js` to see a summary of all system calls your application makes during a 10-second run.
2.  Install `llnode` and try to inspect a simple script that you have deliberately crashed using `process.abort()`.

---
Prev: [06_Performance_Profiling.md](./06_Performance_Profiling.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [../Architecture/01_REST_API_Design.md](../Architecture/01_REST_API_Design.md)
