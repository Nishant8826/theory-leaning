# 📌 Topic: REST API Design

## 🧠 Concept Explanation
REST (Representational State Transfer) is not a protocol, but a set of architectural constraints. It treats everything in your application as a **Resource** that can be identified, manipulated, and transferred.

**The Restaurant Menu Analogy (Deep Dive):**
Imagine you are dining at a high-end restaurant.
*   **The Resource (The Dish):** Every item on the menu (e.g., "The Wagyu Burger") is a resource. It has a unique ID (The Name) and a state (Ingredients, Price).
*   **The URL (The Menu Item):** The menu lists the dishes. `/burgers/wagyu` is the path to that specific resource.
*   **The Verbs (Your Order):**
    *   **GET:** You look at the burger. You don't change it; you just see what it is.
    *   **POST:** You order a *new* burger to be created.
    *   **PUT:** You send a burger back and ask for a completely new one to replace it.
    *   **PATCH:** You ask the waiter to just add extra pickles to the existing burger.
    *   **DELETE:** You tell the waiter to take the burger away and cancel the charge.
*   **Statelessness:** The waiter has severe amnesia. Every time you speak, you must show your ticket and tell them exactly which table you are at. They don't remember that you ordered a drink 5 minutes ago unless you remind them.

---

## 🏗️ Mental Model
Think of REST as **Mapping URLs to Database Entities**.
*   **Nouns over Verbs:** You don't use `/getUsers`. You use `/users` and the `GET` method. The URL is the *thing*, the HTTP method is the *action*.
*   **Representation:** When you `GET /users/1`, the server doesn't send you the actual database row. It sends you a *representation* of it (usually as JSON). You could also ask for it as XML or HTML.
*   **HATEOAS (The Roadmap):** A truly RESTful response includes links to what you can do next. If you `GET` an order, the response should include a link to `/orders/1/cancel`.

---

## ⚡ Actual Behavior
When a REST request hits your Node.js server:
1.  **Routing:** Express looks at the path (`/users/:id`) and the method (`GET`). It finds the specific function (handler) responsible for that combination.
2.  **Payload Extraction:** Node.js parses the URL parameters, the query strings (e.g., `?sort=desc`), and the request body.
3.  **Content Negotiation:** The server checks the `Accept` header. If the client wants `application/json`, the server stringifies the JS object. If the client wants `text/plain`, it might just send a string.
4.  **Status Semantics:** The server doesn't just send data; it sends a status. `201 Created` for a successful POST, `204 No Content` for a successful DELETE.

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **HTTP Parsing:** Node.js uses a highly optimized C-based parser (`llhttp`) to read the incoming TCP stream. It identifies the method (GET/POST) and the path before the data even reaches your JavaScript code.
*   **Serialization Overhead:** `JSON.stringify()` is a synchronous, CPU-intensive operation in V8. If you are sending a 5MB JSON response, V8 will block the event loop for several milliseconds while it converts the JS object into a string.
*   **Streamed Responses:** For very large responses, instead of using `res.json()` (which builds the whole string in memory), you can stream data directly from the DB to the client. This uses the `res` object as a **Writable Stream**, keeping memory usage low.
*   **Header Case-Insensitivity:** Internally, Node.js converts all incoming HTTP headers to lowercase (e.g., `Content-Type` becomes `content-type`) to ensure your JavaScript code can find them reliably regardless of how the client sent them.

---

## 🔁 Execution Flow
1.  Client sends `GET /api/v1/orders/123`.
2.  Node.js parses the URL and extracts the ID `123`.
3.  Middleware validates the user's JWT.
4.  Controller calls Service -> Service calls DB.
5.  Data is returned as a JS Object.
6.  `res.json()` stringifies the object and sends it with a `200 OK` status.

---

## 🧠 Resource Behavior
*   **CPU:** Low for simple CRUD; spikes during complex filtering/sorting or JSON serialization.
*   **Bandwidth:** Large JSON payloads can be compressed with Gzip/Brotli to save transfer costs and time.

---

## 📐 ASCII Diagrams
```text
CLIENT (Browser/App)          REST API (Node.js)          DATABASE
       |                             |                       |
       | -- GET /users/42 ---------->|                       |
       |                             | -- SELECT * ... ----> |
       |                             | <--- { id: 42, ... }--|
       | <--- 200 OK { JSON } -------|                       |
```

---

## 🔍 Code Example (Latest Node.js - Clean Architecture)
```javascript
import express from 'express';
const router = express.Router();

// Resource: Users
router.get('/:id', async (req, res) => {
    const user = await userService.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json(user);
});

router.post('/', async (req, res) => {
    const newUser = await userService.create(req.body);
    // 201 Created is the correct code for POST success
    res.status(201).json(newUser);
});

router.delete('/:id', async (req, res) => {
    await userService.delete(req.params.id);
    // 204 No Content is standard for a successful DELETE
    res.status(204).send();
});
```

---

## 💥 Production Failures
*   **Leaking Database Schema:** Returning internal DB fields (like `__v` or `password_hash`) directly in the API response. Always use a Data Transfer Object (DTO) or a "ToJSON" transform.
*   **Ambiguous Status Codes:** Returning `200 OK` for everything, even when an error occurred, forcing the client to parse the response body to find the error.

---

## 🧪 Real-time Scenarios
*   **Filtering & Pagination:** Handling `GET /products?category=tech&page=2&limit=50` to avoid sending 10,000 products at once.
*   **HATEOAS:** Including links in the response that tell the client what they can do next (e.g., "Next Page" or "Cancel Order").

---

## ⚠️ Edge Cases
*   **PUT vs PATCH:** `PUT` replaces the entire resource. If you only send `{"name": "New"}`, all other fields in the DB should be cleared. `PATCH` only updates the fields you provide.
*   **Browser Pre-flights (CORS):** Browsers send an `OPTIONS` request before any `POST/PUT/DELETE` to ensure the server allows the request.

---

## 🏢 Best Practices
1.  **Use Nouns, Not Verbs:** Use `/users`, not `/getUsers`.
2.  **Pluralize Resources:** `/orders` is better than `/order`.
3.  **Always use JSON:** It is the industry standard for REST.
4.  **Implement Rate Limiting:** To prevent abuse of your endpoints.

---

## ⚖️ Trade-offs
*   **REST:** Simple, cached by browsers/CDNs, widely understood.
*   **GraphQL:** More flexible for complex data, avoids over-fetching, but harder to cache and more complex to implement.

---

## 💼 Interview Q&A
*   **Q:** What are the 4 levels of the Richardson Maturity Model?
*   **A:** Level 0 (The Swamp of POX), Level 1 (Resources), Level 2 (HTTP Verbs), Level 3 (Hypermedia Controls/HATEOAS).

---

## 🧩 Practice Problems
1.  Design the URL structure and methods for a "Library Management System" (Books, Authors, Loans).
2.  Implement a middleware that adds a `Link` header for pagination (First, Prev, Next, Last).

---
Prev: [../Expert/07_Low_Level_Debugging.md](../Expert/07_Low_Level_Debugging.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [02_GraphQL_Architecture.md](./02_GraphQL_Architecture.md)
