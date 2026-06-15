# Email Services

## What You Will Learn
* The SMTP (Simple Mail Transfer Protocol) basics.
* Direct SMTP servers vs. Transactional Email APIs (SendGrid, Mailgun, AWS SES).
* Sending transactional emails using Nodemailer.
* Compiling dynamic email templates using EJS.
* Offloading email sending tasks to background worker queues.

## Why This Matters
Sending an email requires connecting to an external mail server, which takes several seconds of network latency. If you send emails synchronously inside your Express route controllers (e.g. during user registration), the API response will hang, slowing down the registration process for users. Offloading email tasks to background worker queues is essential for maintaining fast API response times.

## Theory

### SMTP vs. Transactional APIs
* **SMTP (Simple Mail Transfer Protocol)**: The standard TCP protocol used to transmit emails across mail servers. Connecting directly to local SMTP servers is simple, but configuring them to maintain high email deliverability (avoiding spam filters) is complex.
* **Transactional Email APIs (e.g. SendGrid, Mailgun, AWS SES)**: Dedicated cloud mail providers that expose HTTP APIs to send emails. They handle IP reputation, email deliverability, bounce rates, and spam compliance, making them the standard choice for production applications.

### Asynchronous Email Pipelines
To keep APIs fast, never send emails inside user request paths.
* **Synchronous (Anti-Pattern)**: User clicks register -> App sends email (waits 3 seconds) -> App returns "User registered".
* **Asynchronous (Production-Grade)**: User clicks register -> App writes a "send welcome email" task to a background queue (takes 2ms) -> App returns "User registered". A separate background worker picks up the task and sends the email asynchronously.

## Deep Dive

### Dynamic Email Templates
Do not hardcode HTML strings inside your JavaScript code. Use a template engine (like **EJS** or **Handlebars**) to compile dynamic email templates:
* Create a dedicated HTML template file containing variables (e.g., `<p>Welcome, <%= username %>!</p>`).
* Compile the template with runtime variables before passing it to the email client.

## Visual Explanation

### Asynchronous Email Queue Pipeline
```text
  [ Client Signup Request ]
              │
              ▼ (Fast Write - 2ms)
   [ Express Controller ] ── Writes Task ──> [ Redis Queue (BullMQ / Bee-Queue) ]
              │                                          │
              ▼ (Instant Response)                       ▼ (Poll asynchronously)
     [ Return 201 Created ]                     [ Background Job Worker ]
                                                         │
                                                         ▼ (Network Call - 3s)
                                                [ Email Provider API ] ──> Sends Email
```

## Real-World Example
Consider an e-commerce checkout. When a user buys a product, they expect an immediate order confirmation screen. The server processes the payment, writes a task to a Redis-backed queue, and returns the success response instantly. A background worker picks up the task, compiles an HTML invoice template, and sends the email via SendGrid, keeping the checkout fast.

## Code Examples

### Nodemailer Setup, EJS Compilation, and Asynchronous Offloading

```javascript
// utils/email.js
// Dependencies required: npm install nodemailer ejs
const nodemailer = require('nodemailer');
const ejs = require('ejs');
const path = require('path');

// 1. Initialize Nodemailer Transporter
// In development, we use mailtrap.io or mock servers. In production, use SES/SendGrid.
const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST || 'sandbox.smtp.mailtrap.io',
  port: process.env.EMAIL_PORT || 2525,
  auth: {
    user: process.env.EMAIL_USER || 'mock-user-id',
    pass: process.env.EMAIL_PASS || 'mock-user-pass'
  }
});

// 2. Compile and Send HTML Email
async function sendWelcomeEmail(toEmail, username) {
  try {
    const templatePath = path.join(__dirname, '../templates/welcome.ejs');
    
    // Mock template content (simulating EJS file compilation)
    // Normally you read this file using: ejs.renderFile(templatePath, data)
    const mockTemplate = `
      <h1>Welcome, <%= name %>!</h1>
      <p>Thank you for registering. Your account is now active.</p>
    `;

    // Render HTML template with runtime variables
    const htmlContent = ejs.render(mockTemplate, { name: username });

    const mailOptions = {
      from: '"Production Backend" <noreply@app.com>',
      to: toEmail,
      subject: 'Welcome to our platform!',
      html: htmlContent
    };

    const info = await transporter.sendMail(mailOptions);
    console.log('[EMAIL SENT] Message ID:', info.messageId);
    return info;
  } catch (err) {
    console.error('Failed to send email:', err.message);
    throw err;
  }
}

module.exports = { sendWelcomeEmail };
```

```javascript
// registration-controller.js
const { sendWelcomeEmail } = require('./utils/email');

// Mock Queue system (simulating BullMQ / background workers)
const emailJobQueue = [];

// Worker processes jobs asynchronously
const startEmailWorker = () => {
  setInterval(async () => {
    if (emailJobQueue.length > 0) {
      const job = emailJobQueue.shift();
      console.log(`[WORKER] Processing email job for user: ${job.username}...`);
      try {
        await sendWelcomeEmail(job.email, job.username);
      } catch (err) {
        console.error(`[WORKER] Job failed for email: ${job.email}. Retrying later...`);
      }
    }
  }, 5000); // Check queue every 5 seconds
};

// Express Route Controller
exports.registerUser = async (req, res, next) => {
  try {
    const { username, email } = req.body;

    // 1. Save user to database...
    console.log(`[DB] User saved: ${username}`);

    // 2. Offload email task to queue (takes 1-2ms)
    emailJobQueue.push({ email, username });
    console.log('[QUEUE] Email job pushed to background queue.');

    // 3. Return response instantly (No waiting for mail server)
    res.status(201).json({
      message: 'Registration successful! A welcome email will be sent shortly.'
    });
  } catch (err) {
    next(err);
  }
};

// Start background worker
startEmailWorker();
```

## Best Practices
* **Never Send Emails Synchronously**: Do not await email transfers inside your HTTP route handlers. Write tasks to background queues to keep API responses fast.
* **Configure SPF, DKIM, and DMARC**: When sending emails in production, configure your domain's SPF, DKIM, and DMARC records to authenticate your emails and prevent them from landing in spam folders.
* **Log and Trace Email Jobs**: Implement logging and correlation IDs on your email queue tasks to trace email statuses and debug delivery failures.

## Interview Questions

### Beginner
* **What is SMTP?**
  *Answer*: SMTP stands for Simple Mail Transfer Protocol. It is the standard TCP protocol used to transmit emails across the internet.

### Intermediate
* **Why should you avoid sending transactional emails inside HTTP route controllers?**
  *Answer*: Sending an email requires connecting to an external mail server, which takes several seconds of network latency. Awaiting this connection inside HTTP route controllers blocks the API response, causing slow response times and timeouts for users.

### Advanced
* **Explain how to offload email sending tasks to background worker queues using a library like BullMQ.**
  *Answer*: To offload email tasks using BullMQ:
  1. Set up a Redis instance to act as the message broker queue.
  2. In your Express route handler, add an email job (containing the recipient's email address and template parameters) to the BullMQ queue instance (this is a fast operation taking 1-2ms).
  3. Respond to the client immediately.
  4. Create a separate background worker process that listens to the Redis queue, fetches jobs, compiles templates, and sends the emails asynchronously using a transactional email provider, decoupling the email transfer from the request lifecycle.

### Senior Architect
* **Discuss how you would design an email retry strategy inside a background worker queue to handle temporary mail server outages without duplicate sends.**
  *Answer*: To design a robust email retry strategy:
  1. **Define Exponential Backoff**: Configure the worker queue (e.g. BullMQ) to retry failed email jobs using exponential backoff (e.g. retrying after 1 minute, then 5 minutes, then 15 minutes) to avoid overwhelming the mail server.
  2. **Enforce Idempotency**: Assign a unique job ID based on the event (e.g. `welcome-email:user-101`). Redis will reject duplicate jobs with the same ID, preventing duplicate sends.
  3. **Use Circuit Breakers**: Implement a circuit breaker on the email client. If the mail provider is down for multiple requests, the breaker trips, and the application queues jobs locally without attempting network connections, preserving resources.
  4. **Dead Letter Queue (DLQ)**: If a job fails after maximum retries (e.g., 5 attempts due to invalid email address), move the job to a Dead Letter Queue for manual audit.

---
Previous : [44_File_Uploads.md] | Index : [00_index.md] | Next : [46_Event_Loop_Deep_Dive.md]
