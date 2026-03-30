# API Gateway & Load Balancer

## What is a Load Balancer?
Imagine you have a very popular restaurant. If only one waiter is working, they will get overwhelmed and customers will have to wait for a long time. 

A **Load Balancer** is like a "Manager" at the entrance of the restaurant who sees which waiter is free and sends the customer to that waiter. In the tech world, it is a device or software that sits in front of your servers and distributes incoming "traffic" (user requests) across multiple servers.

**Why it is needed?**
- **To handle more users:** One server has a limit. Multiple servers can handle millions of users.
- **Reliability:** If one server crashes, the Load Balancer sends users to the other working servers. Your website stays "Up."
- **Efficiency:** It prevents one server from being overloaded while others are sitting idle.

## Real-World Example (Load Balancer)
**Example: Netflix or YouTube**
Millions of people watch videos at the same time. If all those people connected to just **one** giant server, it would crash instantly. 

Instead, Netflix uses a Load Balancer. When you click "Play," the Load Balancer checks:
1. Server A is busy?
2. Server B is free? 
3. Okay, send this user to Server B!

## Types of Load Balancers (Algorithms)
How does the Manager decide where to send the user? They use simple rules called algorithms:

- **Round Robin:** The simplest way. It sends the first request to Server 1, the second to Server 2, the third to Server 3, and then starts again at Server 1. It’s like dealing cards in a game.
- **Least Connections:** The Load Balancer looks at which server is currently doing the *least* amount of work (has the fewest active users) and sends the new request there.
- **IP Hash:** It looks at the user’s IP address (their digital ID) and uses a math formula to always send that specific user to the *same* server. This is useful if the server needs to "remember" the user's session.

---

## What is an API Gateway?
An **API Gateway** is like the "Front Desk" or "Receptionist" of a big office building. Instead of you running around to different departments (User department, Payment department, Order department), you just talk to the person at the front desk.

It is a single entry point for all your microservices. It takes your request, figures out which service you need, and handles some common tasks for you.

**Why it is needed?**
- **Simplifies things for the client:** The user only needs to know **one** URL, not ten different ones for different services.
- **Security:** It checks if you are allowed to enter before letting you talk to the services.
- **Power:** It can do things like "Rate Limiting" (limiting how many times you can click a button) so your servers don't get attacked.

## Real-World Example (API Gateway)
**Example: Amazon Mobile App**
When you open your Amazon app, it needs to show:
1. Your Profile (User Service)
2. Your Cart (Cart Service)
3. Recommended Products (Product Service)

The app doesn't call 3 different URLs. It calls **one** API Gateway. The Gateway then talks to all three services, gathers the info, and gives it back to your app.

## Responsibilities of API Gateway
- **Routing:** Directing your request to the right place (e.g., "/orders" goes to the Order Service).
- **Authentication:** Checking "Who are you?" and "Do you have a valid login token?"
- **Rate Limiting:** Blocking a user if they try to refresh the page 100 times in 1 second (prevents spam).
- **Logging:** Keeping a record of every request that comes in so developers can see what's happening.

---

## Load Balancer vs API Gateway
Even though both sit in front of servers, they have different jobs:

| Feature | Load Balancer | API Gateway |
| :--- | :--- | :--- |
| **Main Job** | Spreads traffic across identical servers. | Manage and route requests to different services. |
| **Focus** | Infrastructure (Performance & Availability). | Application Logic (Security, Routing, API rules). |
| **Analogy** | A Traffic Cop directing cars to empty lanes. | A Receptionist directing you to the right office. |
| **Placement** | Usually at the very edge, before anything else. | Usually sits between the Load Balancer and the Services. |

## How They Work Together
In a real system, they work as a team:

1. **User** sends a request.
2. **Load Balancer** receives it first. It picks a "healthy" entry point.
3. **API Gateway** receives it from the Load Balancer. It checks security and decides which service (User, Order, etc.) should handle it.
4. **Services** do the actual work and send the data back.

**The Flow:**
`Client → Load Balancer → API Gateway → Services`

---

## Diagrams (Simple Visuals)

**1. Basic Load Balancer Flow:**
`Client → Load Balancer → [Server A, Server B, Server C]`

**2. Basic API Gateway Flow:**
`Client → API Gateway → [User Service, Product Service, Order Service]`

**3. Full Professional Flow:**
`Client → Load Balancer → API Gateway → Services (User, Order, etc.)`

---

## Real-World System Example: E-Commerce App
Imagine you are building an app like Flipkart.

**The Flow:**
1. **User** clicks "Place Order."
2. **Load Balancer:** Receives the click and sends it to one of the active API Gateway instances.
3. **API Gateway:** 
   - Checks if the user is logged in (Authentication).
   - Checks if the user is clicking too fast (Rate Limiting).
   - Routes the request to the **Order Service**.
4. **Order Service:** Saves the order in the **Database**.
5. **Database:** Confirms the save.
6. **Response:** Travels back through the Gateway and LB to the User’s screen: "Success!"

---

## Practical Tasks

### Task 1: Design a simple system using load balancer
You are building a news website that gets 10,000 visitors per minute. You have 3 servers. 
- **Question:** Which Load Balancer algorithm would you choose if all 3 servers have the same power (CPU/RAM)? 
- **Goal:** Think about why "Round Robin" is good here.

### Task 2: Add API Gateway in a Microservices setup
Your company used to have one big app (Monolith). Now you have split it into 3 small apps: `User-App`, `Payment-App`, and `Search-App`. 
- **Problem:** The mobile app developers are complaining that they now have to manage 3 different URLs.
- **Solution:** How will an API Gateway help them? (Hint: One URL to rule them all).

### Task 3: Design rate limiting (Thinking-based)
A hacker is trying to guess user passwords by trying 500 different passwords every second on your login page.
- **Question:** Where would you put the "blocking" logic? In the Database? In the Service? Or in the API Gateway? Why?

### Task 4: Where to place the Load Balancer?
You have a website and a database. You decide to add a Load Balancer. 
- **Scenario:** Do you put it *between the user and the website*, or *between the website and the database*? Or both? Explain your reasoning.

---

## Interview Questions

**1. What is a Load Balancer and why is it needed?**
- **Answer:** It’s a tool that distributes incoming traffic across multiple servers. It’s needed to prevent slow-downs, handle many users, and keep the site running if one server fails.

**2. Difference between API Gateway and Load Balancer?**
- **Answer:** A Load Balancer distributes work across *identical* servers for performance. An API Gateway routes requests to *different* specific services and handles tasks like security and logging.

**3. Can an API Gateway replace a Load Balancer?**
- **Answer:** Technically, some Gateways can do basic load balancing, but usually, they are used together. The LB handles the heavy traffic at the entry, and the Gateway handles the complex application rules.

**4. What is Rate Limiting?**
- **Answer:** It is a rule that limits how many requests a user can make in a certain time (e.g., 5 requests per second). It protects your system from being overwhelmed or attacked.

**5. How do you scale APIs when traffic grows?**
- **Answer:** You "Horizontal Scale" by adding more server instances and using a Load Balancer to share the new traffic among them.

**6. Where do you place a Load Balancer in the architecture?**
- **Answer:** At the very front (facing the internet) to handle user traffic, and sometimes internally between services or between services and databases.

**7. What happens if the API Gateway fails?**
- **Answer:** This is called a "Single Point of Failure." To fix this, we usually run multiple copies (instances) of the API Gateway and put a Load Balancer in front of them!

**8. What is 'Stickiness' or 'Session Persistence' in Load Balancers?**
- **Answer:** It’s a feature (often using IP Hash) that ensures a specific user always talks to the same server for their entire session, so their login info or cart doesn't get "lost" between servers.
