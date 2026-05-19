# Project 1: Deploying Full MERN Stack on EC2

## What Is This Project?
This project walks you through deploying a complete MERN (MongoDB, Express, React, Node.js) application on a single Amazon EC2 instance. We will manually install the runtime environment, configure a reverse proxy, and run the backend using a production process manager.

## Why Do This Project?
Before learning abstractions like Docker, Kubernetes, or Serverless, you must understand how Linux servers fundamentally work. This project teaches you SSH, Linux package management, NGINX routing, and PM2 process management—skills that are essential for debugging even advanced containerized systems.

## How to Build It (Step-by-Step)

### Step 1: Provision EC2 & Security Groups
1. Open the EC2 Dashboard and click **Launch Instance**.
2. Select **Ubuntu Server 22.04 LTS**.
3. Instance Type: `t3.micro` (or `t3.small`).
4. **Key Pair**: Create a new `.pem` key pair and download it.
5. **Network Settings**:
   - Ensure "Auto-assign Public IP" is enabled.
   - Create a Security Group allowing:
     - **SSH (22)** from your IP only.
     - **HTTP (80)** from Anywhere (0.0.0.0/0).
     - **HTTPS (443)** from Anywhere (0.0.0.0/0).
6. Click **Launch**.

### Step 2: Connect and Install Dependencies
1. Open your terminal and SSH into the server:
   ```bash
   ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
   ```
2. Update the system and install NGINX and Git:
   ```bash
   sudo apt-get update
   sudo apt-get install nginx git -y
   ```
3. Install Node.js using NVM (Node Version Manager):
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
   source ~/.bashrc
   nvm install 18
   ```
4. Install PM2 globally:
   ```bash
   npm install -g pm2
   ```

### Step 3: MongoDB Atlas Setup
1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a Database User and save the password.
3. In Network Access, allow access from `0.0.0.0/0` (or specifically whitelist your EC2 Public IP).
4. Copy the connection string (URI).

### Step 4: Deploy the Express Backend

> [!NOTE]
> **Where to clone?** Always clone your repository into the home directory of your user (usually `/home/ubuntu/`). Avoid cloning into `/root` or system directories as it causes permission issues.

1. Clone your MERN repository to the EC2 instance.
   ```bash
   cd ~
   git clone https://github.com/Nishant8826/ecom.git
   cd ecom/backend
   ```
2. Install dependencies: `npm install`.
3. Create a `.env` file and add your MongoDB URI:
   ```bash
   echo "MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/test" > .env
   ```
4. Start the server with PM2:
   ```bash
   pm2 start server.js --name "ecom-backend"
   pm2 save
   pm2 startup
   ```
   *(Your backend is now running on port 5000 in the background).*

### Step 5: Deploy the React Frontend (via NGINX)
1. Go to your client directory:
   ```bash
   cd ../client
   npm install
   npm run build
   ```
2. Configure NGINX to serve the React build and proxy API requests:
   ```bash
   sudo vi /etc/nginx/sites-available/default
   ```
3. In the `vi` editor, replace the boilerplate configuration with your custom block:
   - Type `ggdG` to delete all existing text.
   - Press `i` to enter Insert Mode.
   - Paste the following block:
   ```nginx
   server {
       listen 80;
       server_name _;

       # Serve React frontend
       location / {
            root /home/ubuntu/ecom/client/dist;
           index index.html index.htm;
           try_files $uri $uri/ /index.html;
       }

       # Proxy API requests to Node.js backend
       location /api/ {
           proxy_pass http://127.0.0.1:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```
   - Press `Esc`, then type `:wq` and press `Enter` to save and exit.
4. Restart NGINX:
   ```bash
   sudo systemctl restart nginx
   ```
5. Visit your EC2 Public IP in the browser. Your MERN app is live!

## Best Practices & Common Gotchas

### 1. PM2 Multi-User Behavior (Why is my list empty?)
**The Problem**: You SSH in, run `pm2 list`, and it shows no processes, but your website is still working on the external IP.
**The Cause**: PM2 isolates process lists by the Linux user that spawned the process. It stores state in `~/.pm2`.
- If user `ubuntu` starts the app, the state is in `/home/ubuntu/.pm2`.
- If you switch to `root` or another user and run `pm2 list`, it looks in `/root/.pm2` (which is empty).
**The Fix**:
- Always run PM2 commands as the user that owns the process.
- Use `sudo -u ubuntu pm2 list` or `su - ubuntu` to switch users.

### 2. NGINX Permissions (Permission Denied / 500 Error)
Never serve files from the `/root` directory. NGINX runs as the `www-data` user and usually does not have permission to read the `/root` folder, leading to `403 Forbidden` errors. Always clone your repository into the home directory of a standard user (like `/home/ubuntu/`) or `/var/www/`.

**The Home Directory Gotcha**: On many modern Ubuntu AMIs, the home directory `/home/ubuntu` defaults to permissions `750` (`drwxr-x---`), which prevents NGINX from accessing it even if the subdirectories are readable.
- **The Symptom**: `500 Internal Server Error` or `403 Forbidden` with "Permission denied" in `/var/log/nginx/error.log`.
- **The Fix**: Run `chmod o+x /home/ubuntu` to allow NGINX to traverse the directory.


## Production Impact
- **Cost**: Extremely low. A single instance costs ~$10-$15/month.
- **Maintenance**: High. You must manually run `sudo apt-get upgrade` to patch Linux vulnerabilities and manually pull code updates from Git.

## Knowledge Transfer (KT)
- **Why NGINX?** Node.js is excellent at processing data, but terrible at serving static files (images, CSS, JS). NGINX serves the React build files instantaneously using minimal RAM, offloading work from Node.
- **Why PM2?** If an unhandled promise crashes Node.js, the process exits. Without PM2, your site goes down permanently until you SSH back in. PM2 restarts the process instantly.

### NGINX Configuration Explained
Here is what the configuration block in Step 5 does:
- **`listen 80;`**: Listens for incoming HTTP traffic on port 80.
- **`location / { ... }`**: Handles frontend requests.
  - **`try_files $uri $uri/ /index.html;`**: Crucial for React! If a file/folder isn't found, it falls back to `index.html` so React Router can handle the URL in the browser.
- **`location /api/ { ... }`**: Handles backend requests.
  - **`proxy_pass http://127.0.0.1:5000;`**: Forwards requests starting with `/api/` to the Node.js app running on port 5000.


---
Prev : [../07_ProductionArchitecture/04_Cost_Optimization.md](../07_ProductionArchitecture/04_Cost_Optimization.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./02_Project_MERN_on_ECS.md](./02_Project_MERN_on_ECS.md)
---
