# Master Guide: Hosting React & Next.js Apps on AWS

This guide provides a comprehensive, step-by-step breakdown of how to host modern frontend applications on AWS. We separate the approaches based on the application architecture: **Static (React)** vs **Server-Side (Next.js)**.

---

## 🔑 Part 0: Server Authentication (AWS CLI & IAM)

Before you deploy, you may need to give your **Remote Ubuntu Server** permission to talk to other AWS services (like S3 or DynamoDB).

> **Legend:**
> - `[💻 LOCAL]` : Run this on your own Computer.
> - `[☁️ UBUNTU]` : Run this on your Remote EC2 Server.

### 1. Installing AWS CLI on Ubuntu
`[☁️ UBUNTU]` - Fresh Ubuntu machines do not have the AWS CLI. Run these to install it.
```bash
# 1. Update and install unzip
sudo apt update && sudo apt install unzip -y

# 2. Download the official AWS CLI installer
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# 3. Extract and run the installer
unzip awscliv2.zip
sudo ./aws/install

# 4. Verify installation
aws --version   # Should show aws-cli/2.x.x
```

### 2. Logging in via IAM (Authentication)
`[☁️ UBUNTU]` - To perform AWS operations (like `aws s3 sync`), you must log in.

**Method A: `aws configure` (The Beginner Way)**
*Use this only for learning. It stores your keys in plain text.*
1.  Go to your **AWS Console** -> **IAM** -> **Users** -> **(Your User)** -> **Security credentials**.
2.  Create an **Access Key**.
3.  On Ubuntu, run:
```bash
aws configure

# It will ask for:
# AWS Access Key ID [None]: YOUR_KEY_ID
# AWS Secret Access Key [None]: YOUR_SECRET_KEY
# Default region name [None]: us-east-1 (or your choice)
# Default output format [None]: json
```

**Method B: IAM Roles (The Professional/Secure Way)**
*In production, you never store keys on the server. Instead, you give the server its own "Identity".*

**Step 1: Create the Role (If it doesn't exist)**
1.  Go to **IAM Console** -> **Roles** -> **Create role**.
2.  **Trusted entity type:** Select **AWS service**.
3.  **Service or use case:** Select **EC2**.
4.  **Permissions:** Search for and check `AmazonS3FullAccess` (or the specific service you need).
5.  **Role name:** Give it a name like `EC2-S3-Full-Access`.
6.  Click **Create role**.

**Step 2: Attach the Role to your EC2 Instance**
1.  Go to **EC2 Console** -> **Instances**.
2.  Select **(Your Instance)** -> **Actions** -> **Security** -> **Modify IAM Role**.
3.  Choose the role you just created (`EC2-S3-Full-Access`) from the dropdown.
4.  Click **Update IAM role**.

**Step 3: Verify on Ubuntu**
`[☁️ UBUNTU]` - The AWS CLI will now work **without** you ever typing `aws configure`.
```bash
aws s3 ls  # Should now list your buckets without errors!
```

---

## 🚀 Part 1: Hosting React Applications (Static Hosting)

### 1. What
React applications (created with Vite or CRA) are **Client-Side Rendered (CSR)**. They do not "run" on a server; they "run" on the **User's Browser**.

**The Static Build Process:**
- When you run `npm run build`, the React compiler takes all your JSX and components and "flattens" them into a single `build` or `dist` folder.
- **Inside the folder:** Only pure **HTML, CSS, and JavaScript**. There is no live Node.js code or server logic.
- **The Core Concept:** Because these are just files (like a JPG or a PDF), you don't need an active server to "calculate" anything. You just needs a **Storage Bucket (S3)** to hold them and a **CDN (CloudFront)** to deliver them.

**Why CRA is "Static":**
- **The Browser does the work:** The server's only job is to be the "Mailman." Once the browser receives the `index.html` and `main.js`, it performs all the rendering logic locally on the user's computer.
- **Efficiency:** Hosting CRA statically means you are serving exactly the same files to every user, which makes it extremely fast and cheap.

### 2. Why
| Feature | Static Hosting (S3 + CloudFront) | Traditional Server (EC2) |
| :--- | :--- | :--- |
| **Cost** | Pennies per month (Free Tier friendly) | $10 - $20+ per month |
| **Scalability** | Infinite (No configuration needed) | Manual or Auto-Scaling required |
| **Maintenance** | Zero (No OS, No Updates) | High (Security patches, Node updates) |
| **Speed** | Global Edge caching (Low latency) | Limited by server location |

**Deep Dive: Why use Static Hosting?**
- **💰 Cost Efficiency:** Unlike EC2, where you pay for idle CPU time (even at 3 AM), S3 static hosting charges you only for **storage** and **bandwidth**. This can reduce a $20 monthly bill down to $0.50.
- **⚡ Infinite Scale:** Since there is no "live server process" involved, your site cannot "crash" during traffic spikes. AWS S3/CloudFront handles millions of concurrent requests effortlessly.
- **🌍 Global Latency (CDN):** By using CloudFront, your React assets are cached in **Edge Locations** globally. A user in Tokyo downloads your site from a Tokyo server, not from a single central server in the US.
- **🛡️ Enhanced Security:** No server-side OS means no operating system to patch and no open ports for hackers to attack. Your site is "read-only" and extremely secure by design.
- **🛠️ Zero Maintenance:** You never have to update Node.js versions, fix PM2 crashes, or monitor server health. Once the files are in S3, they stay live without any upkeep.

**🧠 Analogy:** 
- **Server Hosting (EC2):** Operating a **Restaurant**. You pay for the chef, waitstaff, and building even if no one is eating.
- **Static Hosting (S3):** Operating a **Vending Machine**. The products (files) are ready, and users grab them 24/7 with zero overhead.

### 3. How (Step-by-Step Implementation)

> **Legend:**
> - `[💻 LOCAL]` : Run this on your own Computer (Windows/Mac).
> - `[☁️ UBUNTU]` : Run this on your Remote EC2 Server.

#### Step 1: Generate Production Artifacts
`[💻 LOCAL]` - Build your project to create the `dist` or `build` folder.
```bash
npm run build
```

#### Step 2: Create and Configure S3 Bucket
`[💻 LOCAL]` - Use the AWS CLI to create a bucket and enable hosting.
```bash
# 1. Create the bucket
aws s3 mb s3://my-react-app-2026

# 2. Disable "Block Public Access"
aws s3api put-public-access-block --bucket my-react-app-2026 --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# 3. Enable Static Website Hosting
aws s3 website s3://my-react-app-2026/ --index-document index.html --error-document index.html
```

#### Step 3: Set Bucket Policy
`[💻 LOCAL]` - Apply the policy to allow public access.
```bash
aws s3api put-bucket-policy --bucket my-react-app-2026 --policy file://policy.json
```

#### Step 4: Sync Files
`[💻 LOCAL]` - Upload your local build directory to S3.
```bash
aws s3 sync ./dist s3://my-react-app-2026 --delete
```

#### Step 5: Add CloudFront (The Professional Way)
1. Go to **AWS Console** -> **CloudFront**.
2. **Origin Domain:** Choose your S3 bucket.
3. **Default Root Object:** `index.html`.

### 4. Pro-Tips / Common Pitfalls (React)
- **Environment Variables:** React environment variables (like `VITE_API_URL`) must be defined **before** running `npm run build`. They are statically "baked" into the JavaScript files. You cannot change them at runtime without rebuilding.
- **Root Object:** Always set the CloudFront Default Root Object to `index.html`.
- **Private Buckets:** For production, keep the S3 bucket private and use a CloudFront **Origin Access Control (OAC)** to grant access. This forces users to go through HTTPS/CDN and bypasses direct S3 access.

---

## ⚡ Part 2: Hosting Next.js Applications (Server-Side)

### 1. What
Next.js supports **Server-Side Rendering (SSR)** and **Incremental Static Regeneration (ISR)**. It needs a Node.js environment to run logic for every request.
- **The AWS Solution:** **EC2 (Ubuntu)** or **AWS Amplify**.

### 2. Why
React on S3 cannot handle SEO-heavy dynamic pages or API routes because there is no server to execute code. Next.js on EC2 allows for dynamic content generation and secure API handling.

### 3. How (Beginner's Master Guide: Local to Remote EC2)

> **Legend:**
> - `[💻 LOCAL]` : Run this on your own Computer (Windows/Mac).
> - `[☁️ UBUNTU]` : Run this on your Remote EC2 Server.

#### 🏗️ Architecture Visualization
```text
[ Local PC ] --- Git Push ---> [ GitHub ] --- Git Clone ---> [ EC2 Server ]
      |                                                            |
   (Code)                                                     (PM2 & Nginx)
      |                                                            |
      └------------- SSH / Secure Connection ----------------------┘
```

---

#### Phase 1: Local Machine Preparation
`[💻 LOCAL]` - Before touching AWS, ensure your code is ready.
1.  **Push to GitHub:**
    ```bash
    git add .
    git commit -m "Deployment ready"
    git push origin main
    ```

#### Phase 2: Connecting to your brand new EC2
`[💻 LOCAL]` - Connect to your remote server via SSH.
1.  **SSH into the server:**
    ```bash
    # Open your terminal and run:
    ssh -i "my-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
    ```

#### Phase 3: Provisioning the Ubuntu Server (The "Setup")
`[☁️ UBUNTU]` - Install Node.js on the fresh machine.

**The Installation Command Breakdown:**
You will often see this "one-liner":
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
```
**What does it do in simple language?**
1. **`curl`**: Downloads the Node.js "Setup Script" from the internet.
2. **`-fsSL`**: (Flags) Make the download fast, silent, and follow any "redirects" (like a shortcut) if the URL changed.
3. **`|` (The Pipe)**: This takes the download and immediately "feeds" it into the next command.
4. **`sudo -E bash -`**: This runs the script you just downloaded as an **Administrator** (`sudo`) using the **Bash** shell.

```bash
# 1. Update the system
# 'update' refreshes your "App Store" list. 'upgrade' actually installs the updates.
# '-y' means "Yes, don't ask me for permission, just do it."
sudo apt update && sudo apt upgrade -y

# 2. Add the NodeSource repository (Version 20)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# 3. Actually install the Node.js package
sudo apt install -y nodejs
```

#### Phase 4: Deploying your Code
`[☁️ UBUNTU]` - Pull your code from GitHub and build it.
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    cd YOUR_REPO_NAME
    ```
2.  **Install & Build:**
    ```bash
    npm install
    npm run build
    ```

#### Phase 5: Starting your app (The "Execution")
`[☁️ UBUNTU]` - Now you need to launch the server to make the site live.

**Method A: The Manual Way (For Testing)**
*Use this only for testing. If you close your terminal window, your website will die.*
```bash
# This runs the app in your current terminal session.
npm start
```
*   **Pro:** Quick and simple.
*   **Con:** You cannot close your computer or disconnect from the server, or the site will crash.

**Method B: The Professional Way (PM2 - Keeps it alive 24/7)**
*Use this for production. This butler keeps your app running in the background.*
```bash
# 1. Install PM2 globally
sudo npm install -g pm2

# 2. Start your Next.js app in the background
pm2 start npm --name "next-app" -- start

# 3. Ensure it starts even if the EC2 reboots
pm2 startup
pm2 save
```

#### Phase 6: Nginx Reverse Proxy (The Gateway)
`[☁️ UBUNTU]` - Link Port 3000 to the standard Web Port 80.

**What is Nginx?**
Think of Nginx as the **Front Desk / Receptionist** for your server.
*   **Without Nginx:** Users would have to visit `http://your-ip:3000`. This is ugly and insecure.
*   **With Nginx:** Users visit `http://your-ip` (standard Port 80). Nginx receives the request and "passes" it to your app running on Port 3000.

**Why are we using it?**
1. **The "Cleaner URL":** Standard websites use Port 80. Nginx lets you hide the messy `:3000` from the user.
2. **Security:** It acts as a shield. Users never talk directly to your Node.js app; they talk to Nginx first.
3. **Efficiency:** Nginx is incredibly fast at handling many simultaneous visitors and can manage SSL (HTTPS) much better than Node.js alone.

**How (Step-by-Step Implementation)**
1.  **Install Nginx:** `sudo apt install nginx -y`
2.  **Open the Config File:**
    ```bash
    sudo vi /etc/nginx/sites-available/default
    ```
3.  **Replace the `location /` block with this:**
    ```nginx
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    ```
4.  **Save and Restart:**
    ```bash
    sudo systemctl restart nginx
    ```

**The Impact**
By adding Nginx, you move from a "development-style" setup to a **Production-ready architecture**. Your app is now reachable via standard HTTP (Port 80) and has a defensive layer that can handle thousands of concurrent connections effortlessly.

---

### 🚀 Advanced: Multiple Apps & API Backends

**Scenario A: Hosting 2 Different Next.js Apps (e.g., `shop.com` and `admin.com`)**
Instead of having one big config, you use **`server_name`** to tell Nginx which domain goes to which port.

```nginx
# Config for App 1 (Running on Port 3000)
server {
    server_name shop.yourdomain.com;
    location / {
        proxy_pass http://localhost:3000;
    }
}

# Config for App 2 (Running on Port 4000)
server {
    server_name admin.yourdomain.com;
    location / {
        proxy_pass http://localhost:4000;
    }
}
```

**Scenario B: Next.js (Frontend) + Node.js (Backend) on the Same Server**
Most apps have a frontend (Next.js) and a backend (Node/Express). You can host both on one domain!

*   **Next.js:** localhost:3000
*   **Node/Express:** localhost:5000 (Backend)

**The Nginx Config:**
```nginx
server {
    listen 80;
    server_name myapp.com;

    # 1. Forward all "/api" requests to the backend (Port 5000)
    location /api {
        proxy_pass http://localhost:5000;
    }

    # 2. Forward everything else to the Frontend (Port 3000)
    location / {
        proxy_pass http://localhost:3000;
    }
}
```

**What is the impact?**
This is extremely cost-effective! You only pay for **one EC2 instance**, but it handles your website and your API simultaneously. Nginx acts like an "intelligent traffic controller," sending `/api` traffic to your Node backend and everything else to your Next.js frontend.

---

### 4. Pro-Tips / Common Pitfalls (Next.js)
- **Runtime Env Variables:** Unlike React, Next.js can read server-side environment variables at runtime if they are defined on the EC2 instance.
- **Port 3000:** Ensure your security group allows internal traffic if Nginx is hitting `localhost:3000`.

---

## 📘 Appendix: Linux Command Glossary (Cheat Sheet)

If you are new to Linux, here is exactly what those commands mean:

| Command | Meaning in Simple Language |
| :--- | :--- |
| **`sudo`** | **"SuperUser DO"**. Runs the command as an Administrator (Root). |
| **`apt`** | The "App Store" for Ubuntu. Use it to install, update, or remove software. |
| **`update`** | Refreshes the list of available software (doesn't install anything yet). |
| **`install`** | Downloads and sets up a new piece of software. |
| **`-y`** | Automatically says "Yes" to all confirmation prompts. |
| **`curl`** | **"Client URL"**. A tool to download or send data to/from a website via terminal. |
| **`ls`** | **"List"**. Shows you all files and folders in your current directory. |
| **`cd`** | **"Change Directory"**. Moves you into a different folder (e.g., `cd my-repo`). |
| **`vi`** | The industry-standard terminal editor. More complex than nano but incredibly powerful. |
| **`systemctl`** | A tool to manage background services (like starting/restarting Nginx). |
| **`&&`** | **"And Then"**. Runs the first command, and if it succeeds, runs the second. |
| **`|` (Pipe)** | Takes the output of one command and gives it to the next command. |
| **`unzip`** | Extracts files from a compressed ZIP folder. |
| **`ssh`** | **"Secure Shell"**. An encrypted way to log in to your remote server. |
| **`git clone`** | Downloads your code from GitHub to the server. |

---

### 🛠️ VI Editor Mastery (The "I'm Stuck in the Terminal" Guide)
In professional DevOps, `vi` (or `vim`) is the standard. Unlike VS Code, it uses **Modes**. If you don't know what mode you are in, you will get frustrated.

**The Golden Rule:** If you are confused, hit `Esc` 3 times. You are now in **Command Mode**.

| Scenario | Mode | Key / Command | Explanation |
| :--- | :--- | :--- | :--- |
| **Start Typing** | Edit | `i` | Enter **INSERT** mode at cursor. |
| **Append Text** | Edit | `a` | Enter **INSERT** mode after cursor. |
| **New Line Below** | Edit | `o` | Opens a new line below and enters Insert mode. |
| **Stop Editing** | Command | `Esc` | Returns to **COMMAND** mode (Standard). |
| **Save & Exit** | Command | `:wq` + `Enter` | **W**rite (Save) and **Q**uit. |
| **Force Exit** | Command | `:q!` + `Enter` | Quit **without saving** (Nuclear option). |
| **Delete Line** | Command | `dd` | Deletes the entire current line. |
| **Copy Line** | Command | `yy` | **Y**ank (Copy) the current line. |
| **Paste** | Command | `p` | **P**ut (Paste) below the cursor. |
| **Undo** | Command | `u` | Undo the last action. |
| **Go to Top** | Command | `gg` | Jumps to the first line. |
| **Go to Bottom** | Command | `G` | Jumps to the last line. |
| **Search** | Command | `/search_term` | Search forward for a word. |
| **Replace (Line)** | Command | `:s/old/new/g` | Replaces 'old' with 'new' in the current line. |
| **Replace (All)** | Command | `:%s/old/new/g` | Replaces every instance in the whole file. |
| **Line Numbers** | Command | `:set nu` | Shows line numbers (helpful for debugging). |

**Pro-Tip:** Most developers accidentally open `vi` and can't leave. Remember `:q!` if you ever mess up the configuration and want to start over!

### Node / NPM Commands (The "Kitchen")
- **`npm install`**: Downloads all the "ingredients" (dependencies/modules) needed for your app.
- **`npm run build`**: "Cooks" your raw code and turns it into a fast, optimized production version.
- **`npm start`**: Serves the "dish" (runs your code) so users can visit the website.

### PM2 Commands (The "Butler")
*PM2 is like a butler that keeps your app running even if you leave.*
- **`pm2 start`**: Launches your app in the background.
- **`pm2 startup`**: Tells the server: "If you reboot, make sure to start PM2 automatically."
- **`pm2 save`**: "Remember exactly which apps I'm running right now."

---

## 🕵️ Interview-Style Q&A

### **React / S3 Section**
**Q: Why don't we host React on EC2?**
**A:** It's inefficient and expensive. EC2 requires managing an OS and paying for idle CPU time. S3 is 90% cheaper and scales automatically without management.

**Q: What is the "404 on Refresh" problem in SPA?**
**A:** In a Single Page App (SPA), the browser handles routing. If a user refreshes on `/dashboard`, S3 looks for a folder named `dashboard` which doesn't exist. To fix this, CloudFront/S3 must be configured to point all errors back to `index.html`.

### **Next.js / EC2 Section**
**Q: Can Next.js be hosted on S3?**
**A:** Only if you use `output: 'export'` (Static Export). This converts Next.js into a static React app, but you lose SSR, ISR, and API Routes.

**Q: Why use PM2 instead of `npm start`?**
**A:** `npm start` is a foreground process. If it crashes or the SSH session ends, the site goes down. PM2 daemonizes the process, monitors it, and restarts it automatically on failure.

---

## 📝 Summary Table

| Requirement | React (CRA/Vite) | Next.js (SSR) | Next.js (Static) |
| :--- | :--- | :--- | :--- |
| **AWS Service** | S3 + CloudFront | EC2 / AWS Amplify | S3 + CloudFront |
| **Complexity** | Low | Medium/High | Low |
| **SEO** | Fair | Excellent | Good |
| **Runtime** | Browser | Node.js Server | Browser |

---
**Prev:** [08_working_with_aws_cli_ec2.md](./08_working_with_aws_cli_ec2.md) | **Next:** [10_deploying_nodejs_backend.md](./10_deploying_nodejs_backend.md)
