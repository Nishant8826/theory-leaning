# Webhooks

Webhooks are a way for one application to **automatically send information to another** whenever something happens.  
You don’t have to keep checking for updates — the data comes to you instantly.

## Key Concepts 

- **Event-Based**  
  A webhook is triggered only when a specific event happens (like a payment success or a new order).

- **Automatic**  
  You don’t request data again and again — the other application sends it to you by itself.

- **Webhook URL**  
  A special URL (like your "address") where the source app sends the data using an HTTP request (mostly POST).

## Benefits

- **Instant updates** — You get data as soon as the event occurs.  
- **Saves resources** — No need for repeated checking (no polling).  
- **Runs in background** — It doesn’t block your code.  
- **Easy to use** — Simple to connect two apps.  
- **Good for automation** — Things happen automatically based on events.


## How Webhooks Work (Simple Explanation)

Webhooks work in a very simple event → message → receive flow.

### 1. You Provide a Webhook URL
- You give a **URL** (your endpoint) to another service.
- This URL is where you want to receive data.
- Example: `https://myapp.com/webhook`

### 2. An Event Happens
- Something happens in the other service.
- Example events:
  - A user makes a payment
  - A new order is created
  - A file is uploaded
  - A comment is posted

### 3. The Service Sends a Request to Your URL
- As soon as the event occurs, the service sends an **HTTP POST request** to your webhook URL.
- This request contains event details (usually in JSON format).




### 4. Your Server Receives the Data
- Your webhook URL receives the request.
- Your backend processes the data (save to DB, send email, update UI, etc.).

Example:
- Save the payment info
- Update the order status
- Trigger a notification

### 5. Your Server Responds
- Your server sends a simple response back, usually:
  - `200 OK` (successful)
  - or `400/500` if something went wrong

---

### Simple Real-Life Example

**It works like receiving a courier package:**
- You give your address → Webhook URL  
- Something happens → Package is prepared  
- Courier delivers package → POST request sent  
- You open the package → You process the data  

---

## Summary

- You give a URL  
- Event happens  
- Service POSTs data  
- Your app processes it  
- Response sent back  

Webhooks = **automatic, real-time messages sent from one app to another when something happens**.

