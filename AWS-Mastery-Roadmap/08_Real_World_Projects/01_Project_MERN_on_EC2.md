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
1. Clone your MERN repository to the EC2 instance.
   ```bash
   git clone https://github.com/yourusername/mern-app.git
   cd mern-app/backend
   ```
2. Install dependencies: `npm install`.
3. Create a `.env` file and add your MongoDB URI:
   ```bash
   echo "MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/test" > .env
   ```
4. Start the server with PM2:
   ```bash
   pm2 start server.js --name "mern-backend"
   pm2 save
   pm2 startup
   ```
   *(Your backend is now running on port 5000 in the background).*

### Step 5: Deploy the React Frontend (via NGINX)
1. Go to your frontend directory:
   ```bash
   cd ../frontend
   npm install
   npm run build
   ```
2. Configure NGINX to serve the React build and proxy API requests:
   ```bash
   sudo nano /etc/nginx/sites-available/default
   ```
3. Replace the contents with:
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       # Serve React frontend
       location / {
           root /home/ubuntu/mern-app/frontend/build;
           index index.html index.htm;
           try_files $uri $uri/ /index.html;
       }

       # Proxy API requests to Node.js backend
       location /api/ {
           proxy_pass http://127.0.0.1:5000/;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```
4. Restart NGINX:
   ```bash
   sudo systemctl restart nginx
   ```
5. Visit your EC2 Public IP in the browser. Your MERN app is live!

## Production Impact
- **Cost**: Extremely low. A single instance costs ~$10-$15/month.
- **Maintenance**: High. You must manually run `sudo apt-get upgrade` to patch Linux vulnerabilities and manually pull code updates from Git.

## Knowledge Transfer (KT)
- **Why NGINX?** Node.js is excellent at processing data, but terrible at serving static files (images, CSS, JS). NGINX serves the React build files instantaneously using minimal RAM, offloading work from Node.
- **Why PM2?** If an unhandled promise crashes Node.js, the process exits. Without PM2, your site goes down permanently until you SSH back in. PM2 restarts the process instantly.

---
Prev : [../07_ProductionArchitecture/04_Cost_Optimization.md](../07_ProductionArchitecture/04_Cost_Optimization.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./02_Project_MERN_on_ECS.md](./02_Project_MERN_on_ECS.md)
---
