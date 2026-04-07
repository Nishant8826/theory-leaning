# Deployment On EC2

> 📌 **File:** 21_Deployment_On_EC2.md | **Level:** Beginner → MERN Developer

---

## What is it?
Deploying your local Node.js + Express + MySQL React application to the public internet using an Amazon Web Services (AWS) EC2 Virtual Ubuntu Machine.

## MERN Parallel — You Already Know This!
- Localhost MongoDB → Atlas / Local MySQL → Self-Hosted Ubuntu MySQL
- Next.js Vercel push → Manual SSH Nginx Proxy Building

## Why does it matter?
Understanding deep stack infrastructure sets senior developers apart. Modern platforms like Render or Heroku hide the magic. Setting up Nginx, PM2, and MySQL servers yourself teaches raw Linux devops.

## How does it work?
We rent an Ubuntu Server. We securely SSH via terminal. We install Node, Nginx, and MySQL Server natively. We clone our Git repository, build the React project into static HTML, use PM2 to keep the API running, and configure Nginx to route internet traffic to both.

## Visual Diagram
```ascii
[ Internet Port 80 ] ---> Nginx Server (Reverse Proxy)
                            |--> /api     --> [ PM2 Express Node.js :3000 ] --(TCP 3306)--> [ Local MySQL Server ]
                            |--> /* (SPA) --> [ React Build /var/www/html ]
```

## Step-by-Step EC2 Workflow

### 1. Launch EC2 & Security Groups
1. Open AWS Console -> EC2 -> Launch Instance.
2. Select **Ubuntu Server LTS**.
3. Create new Key Pair (e.g. `aws-key.pem`).
4. **Security Groups**: Allow SSH (22), HTTP (80), HTTPS (443). Do **NOT** open 3306 publicly.

### 2. Connect via SSH
```bash
chmod 400 aws-key.pem
ssh -i aws-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 3. Install Environment (Node + MySQL + Nginx)
```bash
sudo apt update && sudo apt upgrade -y

# Install Node via NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
source ~/.bashrc
nvm install node

# Install Nginx and MySQL Server
sudo apt install nginx mysql-server -y
```

### 4. MySQL Setup
```bash
# Secure the installation (Set strict passwords)
sudo mysql_secure_installation

# Log in as root to local DB
sudo mysql

-- Inside MySQL Prompt:
CREATE DATABASE ecommerce;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'StrongPwd123!';
GRANT ALL PRIVILEGES ON ecommerce.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
*(Note: To enable remote workbench access, set `bind-address=0.0.0.0` in `/etc/mysql/mysql.conf.d/mysqld.cnf` and open Port 3306 in AWS SG. Use with caution).*

### 5. Backend Deployment (Node.js)
```bash
# Clone API
git clone https://github.com/you/repo.git
cd repo/backend
npm install

# Setup env variables
nano .env # Add DB HOST=localhost, USER=admin, etc.

# PM2 Keeps Node alive forever
npm install -g pm2
pm2 start server.js --name "ecommerce-api"
pm2 save
pm2 startup
```

### 6. Frontend Deployment (React)
```bash
cd ~/repo/frontend
npm install
npm run build # Generates static files in /dist or /build

# Move to Nginx public folder
sudo cp -r dist/* /var/www/html/
```

### 7. Nginx Reverse Proxy Config
Nginx must route frontend requests to the static files, and backend requests to PM2.
```bash
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 80;
    server_name YOUR_PUBLIC_IP or domain.com;

    # Serve React Static Files
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html; # React Router Fix
    }

    # Proxy API calls to Node.js backend
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Restart to apply:
```bash
sudo systemctl test nginx
sudo systemctl restart nginx
```

### 8. Extras
- **SSL via Certbot:** `sudo snap install --classic certbot && sudo certbot --nginx`
- **Database Backups:** `mysqldump -u admin -p ecommerce > backup.sql`
- **Scaling:** Offload the local MySQL server to a Managed AWS RDS (Relational Database Service) for auto-failover safety.

## Practice Exercises
- **Easy (Setup)**: Successfully ping the public IP of Nginx resulting in the React load page.
- **Medium (Setup)**: Ensure node `.env` points properly to local OS unix-socket DB passwords causing no connection drops.
- **Hard (Setup)**: Use `mysqldump` to export local schema data and securely `scp` transfer it upward into the EC2 database instance seamlessly.

## Interview Q&A
1. **Core DevOps:** Why not run `node server.js` directly on Port 80?
   *Node requires root privileges for port 80. Also, Nginx handles DDOS, static file delivery, and SSL termination roughly 10x faster mechanically than express.*
2. **MERN integration:** In Mongo, we get a URI string from Atlas. Where is the URI here?
   *The data base is hosted locally ON the EC2 machine. So the connection is simply `localhost:3306`!*
3. **Architecture Check:** Should you open port 3306 to 0.0.0.0?
   *Only dynamically white-listed to your home IP address. If left fully public (0.0.0.0), hackers will instantly run brute-force bots against root.*

| Previous: [20_Final_Project.md](./20_Final_Project.md) | Next: None |
