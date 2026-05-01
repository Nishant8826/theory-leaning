# 📌 Topic: Authorization (RBAC vs ABAC)

## 🧠 Concept Explanation
If Authentication is about "Identity," Authorization is about "Privilege." It's the set of rules that determines what an identified user can and cannot do within your system.

**The Hotel Keycard Analogy (Deep Dive):**
Imagine you are a guest at a high-tech hotel.
*   **Authentication (The Check-in):** You show your passport at the desk. The clerk confirms you are who you say you are and gives you a keycard.
*   **Authorization (The Keycard Permissions):**
    *   **RBAC (Role-Based Access Control):** Your keycard is coded with the "Guest" role. This role automatically grants access to the elevator, your specific room, and the pool. It does **not** grant access to the kitchen or the laundry room. If you were a "Staff" member, your card would open different doors.
    *   **ABAC (Attribute-Based Access Control):** This is a "Smart" card. It only opens the pool if **(Time is between 8 AM and 8 PM)** AND **(You are over 18 years old)** AND **(The pool isn't at maximum capacity)**. It doesn't care about your "Role" as much as it cares about the *context* of your request.
*   **Scopes (The Permission Slip):** Sometimes, you give your keycard to a delivery person (Third-party app via OAuth). You don't want them to have your full access, so you "scope" the card to only open the Lobby and the Package Room.

---

## 🏗️ Mental Model
Think of Authorization as a **Guard standing at every door (Route)**.
*   **Who? (Subject):** The user or service making the request (e.g., `req.user`).
*   **What? (Action):** What are they trying to do? (e.g., `read`, `write`, `delete`).
*   **Which? (Resource):** What "thing" are they acting upon? (e.g., `User Profile #45`).
*   **The Answer:** The guard either says "Pass" (`next()`) or "Halt" (`res.status(403)`).

---

## ⚡ Actual Behavior
In a Node.js/Express environment:
1.  **Middleware Chain:** Authorization always happens **after** authentication. You must know *who* someone is before you can decide what they can do.
2.  **Stateless Check:** If using JWTs, the user's "Role" is often encoded directly in the token. The server reads the token and immediately knows the role without a database lookup.
3.  **Data Ownership:** A common mistake is only checking the role. For example, "A user can edit a profile." But you must check: "Can *this* user edit *this* profile?" This usually requires a database query to check the `ownerId`.
4.  **Failure:** If authorization fails, the server returns a `403 Forbidden`. This is different from `401 Unauthorized`. 403 means "I know you, but the answer is still no."

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Policy Enforcement Point (PEP):** This is your middleware. It's the place in the code where the check is actually performed.
*   **Bitwise Permissions:** For systems with hundreds of permissions, using strings like `"can_edit_post_v2"` is slow. High-performance systems use a single integer. Each bit in the integer represents a permission. 
    *   `1` (0001) = Read
    *   `2` (0010) = Write
    *   `4` (0100) = Delete
    *   A user with a "7" (0111) has all three. V8 can check this using the `&` (AND) operator in nanoseconds, which is thousands of times faster than string comparison.
*   **Memory Caching:** If your ABAC rules are complex (e.g., "Must be from a specific IP range"), Node.js will often cache these rules in a `Map` or a Redis instance to avoid re-calculating them for every single request in a high-traffic API.
*   **ACLs vs. Capabilities:** 
    *   **ACL (Access Control List):** The *resource* has a list of who can access it.
    *   **Capability:** The *user* has a "key" that fits specific doors.
    Node.js typically implements Capabilities via JWT scopes.

---

## 🔁 Execution Flow
1.  Request arrives for `DELETE /order/555`.
2.  **Auth Middleware** identifies user as "Nishant" (Role: Editor).
3.  **Authz Middleware** checks: Does "Editor" have the `order:delete` permission?
4.  **Ownership Check (ABAC):** Did "Nishant" create order #555?
5.  If yes, proceed to Controller. If no, return `403 Forbidden`.

---

## 🧠 Resource Behavior
*   **CPU:** ABAC can involve multiple database lookups (to check ownership or resource state), increasing latency and CPU usage compared to simple RBAC.
*   **Memory:** No significant overhead unless you are caching thousands of complex permission rules.

---

## 📐 ASCII Diagrams
```text
[ REQUEST ] -> [ AUTHENTICATION ] -> [ AUTHORIZATION ] -> [ LOGIC ]
                      |                     |
                      v                     v
                (Who are you?)        (Can you do this?)
                                            |
                         +------------------+------------------+
                         |                                     |
                  [ RBAC: Roles ]                       [ ABAC: Rules ]
                  - Admin                               - Owner == User
                  - Editor                              - Time < 5PM
                  - User                                - Dept == 'HR'
```

---

## 🔍 Code Example (Latest Node.js - Simple RBAC Middleware)
```javascript
// middleware/authorize.js
export const authorize = (...allowedRoles) => {
    return (req, res, next) => {
        if (!req.user) return res.status(401).send('Unauthorized');
        
        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({
                message: `Role ${req.user.role} is not authorized to access this resource`
            });
        }
        next();
    };
};

// usage
app.delete('/users/:id', authenticate, authorize('admin'), (req, res) => {
    // Only admins get here
});
```

---

## 💥 Production Failures
*   **Insecure Direct Object Reference (IDOR):** You check if the user is logged in, but you don't check if they own the resource. A user can change the URL to `/api/profile/999` and see someone else's data. (Solution: Always check `where userId = req.user.id`).
*   **Hardcoded Roles:** Scattering `if (user.role === 'admin')` throughout your code makes it impossible to change role names or add new ones. (Solution: Use a central permission mapping).

---

## 🧪 Real-time Scenarios
*   **SaaS Platforms:** Where an "Account Owner" can do everything, but an "Invite" can only see specific dashboards.
*   **Content Management:** Where "Authors" can create posts but only "Editors" can publish them.

---

## ⚠️ Edge Cases
*   **Hierarchical Roles:** An Admin should automatically have all the permissions of an Editor and a User. Your code should handle this "inheritance."
*   **Dynamic Permissions:** Changing a user's role in the DB doesn't affect their current JWT. They keep their old permissions until the token expires. (Solution: Use short-lived tokens or a "Session Version" check).

---

## 🏢 Best Practices
1.  **Principle of Least Privilege:** Users should only have the minimum permissions they need to do their job.
2.  **Centralize Logic:** Use a library like `casl` or `accesscontrol` for complex rules.
3.  **Fail Closed:** If a permission check fails or crashes, the default answer should always be "No access."

---

## ⚖️ Trade-offs
*   **RBAC:** Simple, easy to audit, but inflexible for complex business logic.
*   **ABAC:** Extremely powerful, handles any scenario, but complex to implement and can be slow.

---

## 💼 Interview Q&A
*   **Q:** What is the difference between 401 and 403 status codes?
*   **A:** 401 (Unauthorized) means "I don't know who you are." 403 (Forbidden) means "I know who you are, but you aren't allowed to do this."

---

## 🧩 Practice Problems
1.  Implement a middleware that allows a user to `PUT /profile/:id` only if their `id` matches the `:id` in the URL.
2.  Research how a "Bitmask" is used for permissions and write a small script that checks if a user has the `DELETE` bit set.

---
Prev: [01_Authentication_JWT_OAuth.md](./01_Authentication_JWT_OAuth.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [03_Common_Vulnerabilities.md](./03_Common_Vulnerabilities.md)
