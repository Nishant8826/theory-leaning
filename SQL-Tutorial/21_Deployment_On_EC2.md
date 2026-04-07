# Deployment On EC2

> 📌 **File:** `21_Deployment_On_EC2.md` | **Level:** Beginner → MERN Developer

---

## What is it?

This guide walks you through deploying the complete ShopSQL application (Node.js + MySQL + React) on an **AWS EC2 instance** running Ubuntu. By the end, your e-commerce API will be live on the internet with a proper domain, SSL certificate, and production-grade setup.

---

## MERN Parallel — You Already Know This!

If you've deployed a MERN app before, the process is almost identical:

| MERN Deployment (You Know)             | SQL Deployment (You'll Learn)           |
|----------------------------------------|-----------------------------------------|
| MongoDB Atlas (cloud DB)               | MySQL on EC2 (self-managed)             |
| `npm start` or PM2                     | Same — PM2 for Node.js                 |
| Nginx reverse proxy                    | Same — Nginx for Express + React       |
| `.env` for MONGO_URI                   | `.env` for DB_HOST, DB_USER, DB_PASSWORD|
| `certbot` for SSL                      | Same — Certbot for HTTPS               |

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   AWS EC2 Instance (Ubuntu)                  │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Nginx (:80, :443)                     │ │
│  │  ┌──────────────────┐  ┌──────────────────────────────┐ │ │
│  │  │ React Build      │  │ Reverse Proxy                │ │ │
│  │  │ (Static Files)   │  │ /api/* → localhost:5000      │ │ │
│  │  │ / → index.html   │  │                              │ │ │
│  │  └──────────────────┘  └──────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                               │
│  ┌──────────────────┐  ┌────┴───────────────┐               │
│  │ PM2              │  │ MySQL Server       │               │
│  │ (Process Manager)│  │ (Port 3306)        │               │
│  │ Node.js :5000    │  │ ecommerce database │               │
│  └──────────────────┘  └────────────────────┘               │
│                                                              │
│  Security Groups: 22 (SSH), 80 (HTTP), 443 (HTTPS)          │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 1: Launch EC2 Instance

### In AWS Console

```
1. Go to EC2 Dashboard → Launch Instance

2. Configure:
   - Name: ShopSQL-Server
   - AMI: Ubuntu Server 22.04 LTS (or 24.04 LTS)
   - Instance type: t2.small (2 GB RAM minimum for MySQL)
     (t2.micro works for testing but may be slow)
   - Key pair: Create new → "shopsql-key" → Download .pem file
   - Storage: 20 GB gp3 (minimum for MySQL + data)

3. Network Settings → Edit:
   - Allow SSH (port 22) from My IP
   - Allow HTTP (port 80) from Anywhere
   - Allow HTTPS (port 443) from Anywhere

4. Launch Instance

5. Note the Public IP (e.g., 13.235.xx.xx)
```

### Configure Security Groups

```
Add these Inbound Rules:
┌───────────┬──────────────┬─────────────┬─────────────────────┐
│ Type      │ Port Range   │ Source      │ Purpose             │
├───────────┼──────────────┼─────────────┼─────────────────────┤
│ SSH       │ 22           │ My IP       │ Remote access       │
│ HTTP      │ 80           │ 0.0.0.0/0   │ Web traffic         │
│ HTTPS     │ 443          │ 0.0.0.0/0   │ Secure web traffic  │
│ Custom TCP│ 3306         │ My IP       │ MySQL remote (dev)  │
└───────────┴──────────────┴─────────────┴─────────────────────┘

⚠️ NEVER open port 3306 to 0.0.0.0/0 in production!
Only open it to your IP for remote management, or keep it closed.
```

---

## Step 2: Connect via SSH

```bash
# Windows (PowerShell or Git Bash)
ssh -i "shopsql-key.pem" ubuntu@13.235.xx.xx

# If permission error on Windows:
icacls "shopsql-key.pem" /inheritance:r /grant:r "%USERNAME%":"(R)"

# First thing after connecting:
sudo apt update && sudo apt upgrade -y
```

---

## Step 3: Install Node.js (via nvm)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Reload shell
source ~/.bashrc

# Install Node.js LTS
nvm install --lts
nvm use --lts

# Verify
node --version    # v20.x.x
npm --version     # 10.x.x
```

---

## Step 4: Install MySQL Server

```bash
# Install MySQL 8.0
sudo apt install mysql-server -y

# Check status
sudo systemctl status mysql

# Secure installation (IMPORTANT!)
sudo mysql_secure_installation

# Follow the prompts:
# - VALIDATE PASSWORD COMPONENT: Yes → Medium (1)
# - New root password: Enter a STRONG password (e.g., ShopSQL@2024Prod!)
# - Remove anonymous users: Yes
# - Disallow root login remotely: Yes
# - Remove test database: Yes
# - Reload privilege tables: Yes
```

### Create Database and User

```bash
# Login to MySQL as root
sudo mysql

# Or if root password was set:
sudo mysql -u root -p
```

```sql
-- Create the ecommerce database
CREATE DATABASE ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user (NEVER use root for your app!)
CREATE USER 'shopsql_user'@'localhost' IDENTIFIED BY 'ShopSQL_User@2024!';

-- Grant privileges on ecommerce database only
GRANT ALL PRIVILEGES ON ecommerce.* TO 'shopsql_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SELECT User, Host FROM mysql.user;

-- Exit
EXIT;
```

### Test Connection

```bash
# Login as the new user
mysql -u shopsql_user -p ecommerce
# Enter password: ShopSQL_User@2024!
```

```sql
-- Verify it works
SELECT VERSION();
SHOW TABLES;
EXIT;
```

### Enable Remote Access (Optional — for MySQL Workbench)

```bash
# Edit MySQL config
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Find and change:
# bind-address = 127.0.0.1
# To:
# bind-address = 0.0.0.0

# Save (Ctrl+X, Y, Enter)

# Create remote user
sudo mysql -u root -p
```

```sql
-- Create user that can connect from your IP
CREATE USER 'shopsql_remote'@'YOUR.IP.ADDRESS' IDENTIFIED BY 'Remote@2024!';
GRANT ALL PRIVILEGES ON ecommerce.* TO 'shopsql_remote'@'YOUR.IP.ADDRESS';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Restart MySQL
sudo systemctl restart mysql
```

---

## Step 5: Deploy Backend

### Clone Repository

```bash
# Install git (usually pre-installed on Ubuntu)
sudo apt install git -y

# Create app directory
sudo mkdir -p /var/www/shopsql
sudo chown ubuntu:ubuntu /var/www/shopsql
cd /var/www/shopsql

# Clone your repo
git clone https://github.com/yourusername/shopsql-api.git backend
cd backend

# Install dependencies
npm install --production
```

### Create .env File

```bash
nano .env
```

```env
# Server
PORT=5000
NODE_ENV=production

# MySQL
DB_HOST=localhost
DB_USER=shopsql_user
DB_PASSWORD=ShopSQL_User@2024!
DB_NAME=ecommerce
DB_PORT=3306

# JWT (if using auth)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# CORS
CORS_ORIGIN=https://yourdomain.com
```

### Initialize Database Schema

```bash
# Run your database initialization script
node initDb.js

# Or import SQL file directly
mysql -u shopsql_user -p ecommerce < schema.sql
mysql -u shopsql_user -p ecommerce < seed.sql
```

### Install and Configure PM2

```bash
# Install PM2 globally
npm install -g pm2

# Start the application
pm2 start server.js --name shopsql-api

# Useful PM2 commands
pm2 status          # Check running processes
pm2 logs shopsql-api  # View logs
pm2 restart shopsql-api  # Restart
pm2 stop shopsql-api     # Stop

# Auto-start on reboot
pm2 startup
pm2 save

# Monitor
pm2 monit
```

### Test Backend

```bash
curl http://localhost:5000/api/health
# Should return: {"status":"ok","database":"MySQL",...}
```

---

## Step 6: Deploy Frontend

### Build React App

```bash
cd /var/www/shopsql

# Clone frontend (or it's in the same repo)
git clone https://github.com/yourusername/shopsql-frontend.git frontend
cd frontend

# Install dependencies
npm install

# Set API URL for production
echo "VITE_API_URL=https://yourdomain.com/api" > .env.production
# or for Create React App:
echo "REACT_APP_API_URL=https://yourdomain.com/api" > .env.production

# Build for production
npm run build

# Copy build to Nginx directory
sudo cp -r dist /var/www/shopsql/frontend-build
# For CRA: sudo cp -r build /var/www/shopsql/frontend-build
```

---

## Step 7: Install and Configure Nginx

```bash
# Install Nginx
sudo apt install nginx -y

# Check status
sudo systemctl status nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/shopsql
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    # For testing without domain, use: server_name _;

    # React frontend (static files)
    root /var/www/shopsql/frontend-build;
    index index.html;

    # API reverse proxy
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # React Router support (SPA fallback)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
    gzip_min_length 256;
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/shopsql /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Test

```bash
# From your local machine, visit:
# http://13.235.xx.xx       → React app
# http://13.235.xx.xx/api/health → API response
```

---

## Step 8: Domain Setup

```
1. Buy a domain (Namecheap, GoDaddy, Route53)

2. Add DNS records:
   Type: A     Name: @    Value: 13.235.xx.xx
   Type: A     Name: www  Value: 13.235.xx.xx
   Type: CNAME Name: www  Value: yourdomain.com

3. Wait for DNS propagation (5 min to 48 hours)

4. Verify:
   ping yourdomain.com
   # Should resolve to your EC2 IP
```

---

## Step 9: SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (automatic!)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts:
# - Enter email
# - Agree to terms
# - Redirect HTTP to HTTPS: Yes (option 2)

# Certbot automatically:
# 1. Gets a free SSL certificate from Let's Encrypt
# 2. Modifies your Nginx config to use HTTPS
# 3. Sets up auto-renewal

# Test auto-renewal
sudo certbot renew --dry-run

# Verify HTTPS works
curl https://yourdomain.com/api/health
```

---

## Step 10: Security Best Practices

### Firewall (UFW)

```bash
# Enable firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Verify
sudo ufw status
# Should show: 22, 80, 443 allowed
```

### MySQL Security

```bash
# Check MySQL is only listening locally (unless needed remotely)
sudo ss -tlnp | grep 3306
# Should show: 127.0.0.1:3306 (not 0.0.0.0:3306)

# If you enabled remote access, revert for production:
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Set: bind-address = 127.0.0.1
sudo systemctl restart mysql
```

### Application Security

```bash
# Ensure .env is not in git
echo ".env" >> .gitignore

# Set proper file permissions
chmod 600 /var/www/shopsql/backend/.env

# Never run Node.js as root
# PM2 runs as the ubuntu user by default — this is correct
```

---

## Step 11: Database Backups

### Automated MySQL Backups

```bash
# Create backup script
sudo nano /opt/mysql-backup.sh
```

```bash
#!/bin/bash
# MySQL Backup Script

BACKUP_DIR="/opt/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_USER="shopsql_user"
DB_PASS="ShopSQL_User@2024!"
DB_NAME="ecommerce"

# Create backup directory
mkdir -p $BACKUP_DIR

# Dump database
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/ecommerce_$DATE.sql

# Compress
gzip $BACKUP_DIR/ecommerce_$DATE.sql

# Remove backups older than 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup completed: ecommerce_$DATE.sql.gz"
```

```bash
# Make executable
sudo chmod +x /opt/mysql-backup.sh

# Test it
sudo /opt/mysql-backup.sh

# Schedule daily backup (cron job)
sudo crontab -e
# Add this line (runs at 2 AM daily):
# 0 2 * * * /opt/mysql-backup.sh >> /var/log/mysql-backup.log 2>&1
```

### Restore from Backup

```bash
# Decompress
gunzip /opt/backups/mysql/ecommerce_20240115.sql.gz

# Restore
mysql -u shopsql_user -p ecommerce < /opt/backups/mysql/ecommerce_20240115.sql
```

---

## Step 12: Monitoring and Maintenance

### Monitor with PM2

```bash
# Real-time monitoring
pm2 monit

# View logs
pm2 logs shopsql-api --lines 100

# Set up log rotation
pm2 install pm2-logrotate
```

### Check MySQL Performance

```bash
# Login and check status
mysql -u shopsql_user -p -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -u shopsql_user -p -e "SHOW PROCESSLIST;"
mysql -u shopsql_user -p -e "SHOW GLOBAL STATUS LIKE 'Questions';"
```

### Application Health Check

```bash
# Quick health check script
curl -s http://localhost:5000/api/health | python3 -m json.tool
```

---

## Step 13: Scaling Basics

```
Vertical Scaling (Scale Up):
┌──────────────────────────────────┐
│ Current: t2.small (2GB RAM)     │
│    ↓                            │
│ Upgrade to: t3.medium (4GB)     │
│    ↓                            │
│ Or: t3.large (8GB)              │
│    ↓                            │
│ Stop instance → Change type     │
│ → Start instance                │
└──────────────────────────────────┘

Horizontal Scaling (Scale Out):
┌────────────┐
│ Load       │
│ Balancer   │
│ (ALB)      │
└─┬──┬──┬────┘
  │  │  │
┌─┴┐┌┴─┐┌┴─┐  ┌──────────┐
│E1││E2││E3│──│ RDS      │
│  ││  ││  │  │ (MySQL)  │
└──┘└──┘└──┘  │ Managed  │
EC2 Instances  └──────────┘

For serious scaling:
1. Use AWS RDS for managed MySQL
2. Use ElastiCache (Redis) for caching
3. Use S3 + CloudFront for static files
4. Use Application Load Balancer
5. Auto Scaling Group for EC2 instances
```

---

## Complete Deployment Checklist

```
Pre-Deployment:
☐ Code is in a git repository
☐ Environment variables are NOT in code
☐ All npm packages are in package.json
☐ Database schema SQL file is ready
☐ Seed data SQL file is ready

EC2 Setup:
☐ Instance launched (Ubuntu, t2.small+)
☐ Security groups configured (22, 80, 443)
☐ SSH key downloaded and secured
☐ Ubuntu updated (apt update/upgrade)

Software Installation:
☐ Node.js installed (via nvm)
☐ MySQL installed and secured
☐ Nginx installed
☐ PM2 installed
☐ Certbot installed

MySQL Setup:
☐ Root password set (mysql_secure_installation)
☐ ecommerce database created
☐ App-specific user created (not root!)
☐ Privileges granted
☐ Schema imported
☐ Seed data imported
☐ bind-address = 127.0.0.1 (production)

Application:
☐ Code cloned to /var/www/shopsql/
☐ npm install --production
☐ .env file created with production values
☐ PM2 running the app
☐ PM2 startup configured (auto-restart)

Frontend:
☐ Production build created (npm run build)
☐ Build copied to Nginx directory
☐ API URL points to production domain

Nginx:
☐ Site config created
☐ Reverse proxy configured (/api → :5000)
☐ Static files served (React build)
☐ Default site removed
☐ Config tested (nginx -t)

Domain & SSL:
☐ Domain DNS pointing to EC2 IP
☐ Certbot SSL certificate installed
☐ HTTP → HTTPS redirect enabled
☐ Auto-renewal configured

Security:
☐ UFW firewall enabled
☐ MySQL not exposed to internet
☐ .env has 600 permissions
☐ App runs as non-root user
☐ Security headers in Nginx

Backup & Monitoring:
☐ Backup script created
☐ Cron job for daily backups
☐ PM2 log rotation configured
☐ Health check endpoint working
```

---

## Common Issues and Fixes

| Issue                                    | Fix                                             |
|------------------------------------------|-------------------------------------------------|
| `ECONNREFUSED` on port 3306             | MySQL not running: `sudo systemctl start mysql`  |
| `Access denied for user 'root'`         | Use `sudo mysql` or check password               |
| Nginx 502 Bad Gateway                    | PM2 app crashed: `pm2 logs`, `pm2 restart all`   |
| React routes show 404                    | Add `try_files` fallback in Nginx config         |
| SSL cert not working                     | Check DNS propagation, run `certbot` again        |
| MySQL eating too much RAM                | Tune `innodb_buffer_pool_size` in my.cnf         |
| PM2 app not starting on reboot          | Run `pm2 startup` and `pm2 save`                 |
| Can't connect MySQL from Workbench      | Check bind-address and security group port 3306  |

---

## Impact

| If You Skip This...                      | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Don't secure MySQL installation          | Default password → database gets hacked          |
| Use root for app database connection     | App compromise → entire server compromised       |
| Don't set up backups                     | Data loss is permanent — no recovery             |
| Don't use PM2                            | App crashes at 3 AM → stays down until you notice|
| Don't use SSL                            | Passwords sent in plaintext → intercepted        |
| Don't set up firewall                    | All ports exposed → easy target for attackers    |

---

## Interview Q&A

**Q1: How would you deploy a Node.js + MySQL application?**
Use a cloud instance (EC2). Install Node.js, MySQL, Nginx, PM2. Configure MySQL with a non-root user. Use PM2 for process management. Use Nginx as reverse proxy (API) and static file server (React). Add SSL via Certbot. Set up backups and monitoring.

**Q2: Why use Nginx in front of Node.js?**
Nginx handles: static file serving (much faster than Node), SSL termination, load balancing, request buffering, gzip compression, rate limiting, and DDoS protection. Node.js should only handle application logic.

**Q3: How do you keep MySQL secure in production?**
Run `mysql_secure_installation`, use a non-root user for the app, bind to localhost only, use strong passwords, enable SSL for MySQL connections, keep MySQL updated, set up regular backups, and monitor slow query logs.

**Q4: What is PM2 and why use it?**
PM2 is a production process manager for Node.js. It provides: auto-restart on crash, cluster mode (multi-core), log management, startup scripts (auto-start on reboot), monitoring (CPU/memory), and zero-downtime reloads.

**Q5: You need to scale your MySQL-backed app. What are your options?**
Vertical: bigger instance (more RAM/CPU). Read replicas: put reads on replicas, writes on primary. Caching: Redis/Memcached for frequent queries. Query optimization: indexes, query rewrites. Use managed database (AWS RDS) for automated backups, patches, failover. Application-level: connection pooling, query result caching, pagination.

---

| [← Previous: Final Project](./20_Final_Project.md) | **🎉 Congratulations! Tutorial Complete!** |
|---|---|

---

## 🎉 What's Next?

You've completed the entire SQL tutorial! Here's what to do next:

1. **Build the Final Project** — Don't just read it, code it!
2. **Practice SQL daily** — Use LeetCode SQL, HackerRank SQL, or SQLZoo
3. **Learn PostgreSQL** — Very similar to MySQL but more features
4. **Explore Prisma** — Modern ORM that's gaining popularity
5. **Study database design patterns** — Partitioning, replication, sharding
6. **Contribute** — Build real applications with MySQL and add to your portfolio

**You are now a MERN + SQL Full Stack Developer. 🚀**
