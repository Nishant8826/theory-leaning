# Hosting Frontends: React & Next.js

---

### 2. What
Deploying your frontend means moving your User Interface onto the internet. 
- **Standard React (Vite/CRA):** These build purely into static CSS, JavaScript, and HTML files. They require absolutely no active server. We host them infinitely efficiently using an **S3 Bucket** paired securely with **CloudFront**.
- **Next.js:** Because Next.js contains Server-Side execution (Server Components/API Routes), it explicitly requires an active Node.js server. S3 cannot host a Next.js app. We must deploy Next.js onto an **EC2 Ubuntu** instance or Elastic Beanstalk.

✅ **Simple Analogy:**
- **Static React on S3:** Printing flyers and putting them in a mailbox. Anyone can grab one securely without you actively needing to hand it to them.
- **Next.js on EC2:** Operating a drive-thru window. You need a dedicated worker (server process) awake 24/7 inside the building to actively cook the order (Server-side rendering) and hand it through the window.

---

### 3. Why
Hosting a static React website on an EC2 instance is an anti-pattern. It costs $10+ a month, crashes during heavy traffic, and forces you to manage Linux updates. Hosting static React securely in S3 costs $0.50 a month and can effortlessly serve a million users simultaneously without crashing because there is no underlying server to overload.

---

### 4. How
For static frontends, we use the `aws s3 sync` CLI command. For Next.js frontends, we SSH into an EC2 server and use `npm run start` combined with a process manager cleanly.

---

### 5. Implementation

**A. Deploying a Static React App locally via CLI**

```bash
# 1. Build your optimized production artifacts locally
npm run build 

# 2. Create the S3 Bucket strictly configured for public website hosting
aws s3 mb s3://my-react-website-bucket
aws s3 website s3://my-react-website-bucket/ --index-document index.html

# 3. Add a Bucket Policy allowing the world to read the files!
# (Assume you placed the JSON text into a file called policy.json locally)
aws s3api put-bucket-policy --bucket my-react-website-bucket --policy file://policy.json

# 4. Sync your built local 'dist' folder securely into S3
aws s3 sync ./dist s3://my-react-website-bucket
```

**B. Deploying Next.js on Ubuntu EC2**

```bash
# 1. SSH into your running Ubuntu Server
ssh -i "mykey.pem" ubuntu@54.xx.xx.xx

# 2. Clone your Next.js Git repository cleanly
git clone https://github.com/me/my-next-app.git && cd my-next-app

# 3. Install dependencies and Build the heavy Next.js Production bundles
npm install
npm run build

# 4. Start the server using PM2 securely
sudo npm install -g pm2
pm2 start npm --name "next-website" -- start
```

---

### 6. Steps (Connecting Custom Domains)
1. Whether you use S3 or EC2, you must go to **Route 53**.
2. If using S3, explicitly generate a **CloudFront Distribution** pointing to your S3 bucket.
3. In Route 53, create an "A Record". Select "Alias" and point it directly to your massive CloudFront URL smoothly.

---

### 7. Integration

🧠 **Think Like This:**
* **Environment Variables:** If your React app connects to your Backend API, ensure you explicitly define the `VITE_API_URL` locally *before* running `npm run build`. The environment variables are permanently baked into the static JavaScript artifact natively during the build phase!
* **Next.js APIs:** If you have an `/api/login` route in Next.js, that specific logic relies strictly on the underlying Node.js Express architecture bundled deeply within the Next framework, which is exactly why hosting it on S3 would instantly fail.

---

### 8. Impact
📌 **Real-World Scenario:** By deploying a static landing page into S3 + CloudFront intelligently, your marketing website becomes totally "Serverless". During a Super Bowl commercial, traffic spikes from 100 users to 2,000,000 users. Your EC2-hosted competitors crash in seconds. Your S3 bucket handles it flawlessly dynamically, without you configuring a single Auto-Scaling group.

---

### 9. Interview Questions

Q1. Why is Amazon S3 ideal for hosting Client-Side Rendered (CSR) React applications natively?
Answer: Because CSR React applications compile strictly down to static HTML, CSS, and JS files. S3 is explicitly designed to store and serve static objects at infinite scale without the overhead of operating systems or live compute resources.

Q2. What occurs if you attempt to deploy a standard robust Next.js application purely to an S3 bucket?
Answer: It will fail. S3 only serves static content. It does not possess a Node.js runtime environment required to execute Next.js Server-Side Rendering (SSR) functionality or internal API routes.

Q3. When deploying to S3, what must you configure to ensure users do not receive a "403 Access Denied" error explicitly?
Answer: You must turn off "Block Public Access" selectively and explicitly attach a broad S3 Bucket Policy that grants public read (`s3:GetObject`) access strictly to your web files securely.

Q4. What CLI command is specifically used to deploy fresh distinct React artifact builds into S3?
Answer: The `aws s3 sync ./dist s3://your-bucket-name` command safely and efficiently synchronizes local build directories explicitly to the remote bucket.

Q5. How does CloudFront enhance an S3-hosted React website?
Answer: CloudFront caches the S3 static assets dynamically across heavily distributed global Edge Locations, ensuring users gracefully download the website from the server physically closest to them, erasing latency.

Q6. Explain the purpose of PM2 explicitly when deploying a Next.js application cleanly onto an EC2 server.
Answer: PM2 is a production process manager that daemonizes the Next.js active Node process cleanly, ensuring that if the app crashes, PM2 immediately securely restarts it, and keeps the server alive after the SSH session ends!

---

### 10. Summary
* Deploy static React cleanly directly to S3 combined smartly with CloudFront.
* Deploy server-heavy Next.js explicitly natively onto Ubuntu EC2 instances.
* Map custom domains seamlessly exclusively relying securely on Route 53.
* Static hosting offers extreme cost optimization gracefully and infinite scale completely natively.

---
Prev : [08_working_with_aws_cli_ec2.md](./08_working_with_aws_cli_ec2.md) | Next : [10_deploying_nodejs_backend.md](./10_deploying_nodejs_backend.md)
