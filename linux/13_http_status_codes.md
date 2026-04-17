# 🚥 HTTP Status Codes: The Web's Secret Language

When you visit a website, the server "whispers" a 3-digit number back to you. This number tells you if it succeeded or failed.

## 🛡️ The 5 Categories
1.  **1xx (Informational):** "Hold on, I'm thinking."
2.  **2xx (Success):** "All Good! Here's your page."
3.  **3xx (Redirection):** "I've moved! Go to this other address."
4.  **4xx (Client Error):** "**YOU** made a mistake." (Wrong URL, not logged in).
5.  **5xx (Server Error):** "**I** made a mistake." (Server crashed or is too busy).

---

## 🛠️ The Famous Codes
*   **200 OK:** The gold standard! Everything worked.
*   **404 Not Found:** You asked for a file that doesn't exist.
*   **500 Internal Server Error:** Something went wrong on the server's side (The Dev's nightmare).
*   **403 Forbidden:** You are not allowed to see this page.
*   **502 Bad Gateway:** One server is talking to another, and the other one isn't replying.

## 🚀 Real-World DevOps Use Case
When monitoring a massive system (like Netflix or Uber), DevOps engineers look at a graph of these numbers. If they suddenly see a spike in **500s**, they know the site is breaking for thousands of people and start a "War Room" to fix it!

---

## ✍️ Hands-on Task
1. Use `curl` to see the status code of a website.
2. Type `curl -I https://google.com` (The `-I` means "Show headers only").
3. Look for the line that says `HTTP/2 200`.

## 🧠 Core Concepts Summary
*   **What:** Universal 3-digit numerical responses sent by the server to inform a client's browser if their web request succeeded, failed, or was blocked.
*   **Why:** These are fundamentally how frontend single-page apps (React) or debugging tools understand error logic from an API.
*   **How:** By classifying actions (200s for success, 400s for user error, 500s for server explosions) and reading them via networking hooks.
*   **Impact:** Rapid triage capability: seeing a 403 vs a 502 immediately dictates whether your problem is an authentication flaw or a crashed Docker container.

---
Prev: [12_service_management.md](12_service_management.md) | Index: [00_index.md](00_index.md) | Next: [14_system_monitoring.md](14_system_monitoring.md)
---
