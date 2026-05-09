# MERN on EC2 (Monolith)

## What Is This Service?
This is the classic, traditional approach to deploying a full MERN stack. It involves spinning up a raw Linux Virtual Machine (Amazon EC2) and manually installing, configuring, and managing MongoDB, Express, React, and Node.js directly on the operating system.

## Why This Service Exists
While modern architectures heavily favor containers (ECS) and Serverless, the EC2 monolith remains the absolute best way to learn how the internet actually works. It forces you to understand Linux networking, SSH, reverse proxies, process managers, and firewall rules without the "magic" of abstraction layers.

## Real World Analogy
Deploying MERN on EC2 is like **Building a Custom PC from scratch**.
You buy the motherboard, CPU, and RAM (EC2), install the OS (Ubuntu), install the fans and cooling (NGINX), and wire everything together yourself. It takes time and expertise, but you have absolute, uncompromising control over every single component.

## How It Works
1. **Provisioning**: You launch a `t3.medium` EC2 instance in a public subnet with a Security Group allowing SSH (22), HTTP (80), and HTTPS (443).
2. **Setup**: You SSH into the server and install Node.js (via NVM), MongoDB community server, Git, and NGINX.
3. **Deployment**: You clone your GitHub repo directly onto the server.
4. **Execution**: You use `PM2` to keep your Node.js Express API running in the background on port 5000. You build your React app and point NGINX to serve the static `build` folder.
5. **Routing**: You configure NGINX as a reverse proxy to route `/api` requests to `localhost:5000`, and all other requests to the React static files.

## Core Concepts
- **PM2**: A production process manager for Node.js. If your Express app crashes due to an unhandled exception, PM2 instantly restarts it.
- **NGINX**: A high-performance web server. It acts as the front door, serving static files (React) 100x faster than Node.js can, and securely proxies API requests to your Node backend.
- **Certbot / Let's Encrypt**: A free tool to automatically provision and install SSL/TLS certificates on your NGINX server, upgrading your site from HTTP to HTTPS.

## MERN Stack Integration
In this architecture, the entire MERN stack lives on `localhost`:
- Express connects to MongoDB at `mongodb://127.0.0.1:27017`.
- NGINX intercepts `domain.com/api/users` and internally forwards it to `http://127.0.0.1:5000/api/users`.
- Network latency between your API and your database is exactly 0 milliseconds.

## Production Impact
- **Simplicity**: For a small startup MVP or a hobby project, having everything on one box is incredibly easy to reason about.
- **Single Point of Failure**: If this specific EC2 instance crashes, or the underlying AWS hardware fails, your entire business goes offline. There is no High Availability.

## Real Production Use Cases
- Internal company tools, staging environments, or simple B2B SaaS MVPs that do not require 99.99% uptime and handle less than 1,000 concurrent users.

## Production Best Practices
- **Do not run MongoDB on the same server in production**: The database and Node.js will fight for RAM. If Node memory leaks, the OS might kill the MongoDB process, corrupting your data. Always offload the database to MongoDB Atlas or Amazon RDS, even if using an EC2 monolith for the backend.
- **Automate with User Data**: Write a bash script in the EC2 "User Data" field to automatically run `apt-get update`, install Node, and configure NGINX the moment the server boots.

## Security Best Practices
- **Restrict MongoDB Binding**: Ensure MongoDB is strictly bound to `127.0.0.1` in `/etc/mongod.conf`. If it is bound to `0.0.0.0` and you misconfigure your Security Group, the entire internet can access and delete your database.
- **Disable Root SSH**: Never SSH as the `root` user. Use the default `ubuntu` user and rely on `sudo`.

## Cost Optimization Tips
- A monolithic architecture is extremely cheap. You can run a small MERN application entirely on a single `t3.small` instance for ~$15/month, avoiding the base costs of Load Balancers, NAT Gateways, and managed databases.

## Common Mistakes
- **Forgetting PM2**: Starting the Node app using `node server.js` over SSH, and then closing the terminal window. The app will immediately die. Always use `pm2 start server.js`.
- **Losing the .pem key**: If you lose the SSH key pair downloaded when the instance was created, you are permanently locked out of your server. Always switch to AWS Systems Manager Session Manager for access.

## Debugging & Troubleshooting
- **502 Bad Gateway**: This means NGINX is working perfectly, but it cannot reach the Express app on port 5000. Express either crashed or hasn't been started. Check `pm2 logs`.
- **Connection Refused on Port 80**: NGINX is not running. Run `sudo systemctl status nginx`.

---
Prev : None | Index : [../00_Index.md](../00_Index.md) | Next : [./02_MERN_on_ECS.md](./02_MERN_on_ECS.md)
---
