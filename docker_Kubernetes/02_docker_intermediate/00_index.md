# 🐳 Docker Intermediate – Complete Revision Guide

Welcome to the Docker Intermediate module revision sheet. This document aggregates all key concepts, commands, configurations, topologies, production best practices, and interview-prep notes from every topic in this directory, allowing you to perform a complete revision from a single file.

---

## 📌 Module Navigation
- [01. Reverse Proxy with Nginx](#01-reverse-proxy-with-nginx)
- [02. Redis, MySQL, and MongoDB Containers](#02-redis-mysql-and-mongodb-containers)
- [03. Docker Logging](#03-docker-logging)
- [04. Docker Monitoring](#04-docker-monitoring)
- [05. Scaling Containers](#05-scaling-containers)
- [06. CI/CD with GitHub Actions and Docker](#06-cicd-with-github-actions-and-docker)
- [07. Production Deployments on AWS EC2](#07-production-deployments-on-aws-ec2)

---

## 01. Reverse Proxy with Nginx
🔗 **Full Lesson:** [01_reverse_proxy_nginx.md](./01_reverse_proxy_nginx.md)

* **Why It Exists**: Production servers should rarely expose application runtimes (Node, Python, Go) directly to the web. Nginx acts as a secure reverse proxy, handling heavy tasks like SSL decryption, load balancing, caching, and static asset serving, shielding app containers from direct exposure.
* **Real-World Analogy**: **Office Building Receptionist**. Visitors talk to the receptionist (Nginx), who verifies authorization, directs them to departments (routing), and ensures no single employee gets overwhelmed (load balancing).

### Key Commands:
```bash
docker run -d --name my-nginx -p 8080:80 nginx:alpine                     # Run default Nginx
docker run -d --name custom-nginx -v ./my-nginx.conf:/etc/nginx/nginx.conf:ro -p 80:80 nginx:alpine # Run with custom config
docker exec my-nginx nginx -s reload                                      # Reload Nginx configuration dynamically
```

### Config Template (`nginx.conf` Load Balancer):
```nginx
events {} # Handles connection processes
http {
    upstream myapp {
        server app1:3000; # Docker DNS translates service names
        server app2:3000;
    }
    server {
        listen 80;
        location / {
            proxy_pass http://myapp;
        }
    }
}
```

> [!NOTE]
> **502 Bad Gateway**: This error indicates Nginx is active but cannot connect to the backend container. Verify the backend service is running and listening on the designated internal port.

---

## 02. Redis, MySQL, and MongoDB Containers
🔗 **Full Lesson:** [02_redis_mysql_mongodb_containers.md](./02_redis_mysql_mongodb_containers.md)

* **Why It Exists**: Spinning up databases locally without conflicts, runtime environment pollution, or clean-up overhead. Since databases are **stateful** (the data must persist), we must configure volumes to ensure data survives container removals.
* **Real-World Analogy**: **Temporary Storage Locker**. If you store items directly inside the container locker and it is demolished, your data is gone. You must mount the locker to a **Permanent Safe** (Docker Volume) outside.

### Key Database Run Commands:
```bash
# 1. Redis (In-Memory Cache) with Volume
docker run -d --name my-redis -p 6379:6379 -v redis-data:/data redis:alpine
docker exec -it my-redis redis-cli                                         # Connect to Redis terminal CLI

# 2. MongoDB (NoSQL) with Credentials and Volume
docker run -d --name my-mongo -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -p 27017:27017 -v mongo-data:/data/db mongo:latest

# 3. MySQL (SQL) with DB Initialization and Volume
docker run -d --name my-mysql -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=myapp -p 3306:3306 -v mysql-data:/var/lib/mysql mysql:latest
```

---

## 03. Docker Logging
🔗 **Full Lesson:** [03_logging.md](./03_logging.md)

* **Why It Exists**: In Docker, containers are ephemeral. If an app writes logs to local files inside the container, those logs are wiped when the container is deleted. Docker captures the `stdout` and `stderr` streams directly.
* **Golden Rule**: **Always log to the console (stdout/stderr)**. Never write log files inside containers.

### Key Commands:
```bash
docker logs my-app                                                         # Dump logs
docker logs -f --tail 100 my-app                                           # Follow last 100 lines of logs
docker logs --since 10m my-app                                             # View logs from last 10 minutes
```

### Log Rotation (Disk Protection):
By default, Docker stores logs forever. If left unconfigured, log files will eventually fill the host disk. Limit log size at container run:
```bash
docker run -d --name logger --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 alpine sh -c "while true; do echo 'Logging...'; sleep 1; done"
```

### Logging Configuration (Docker Compose):
```yaml
services:
  web:
    image: nginx:alpine
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
```

---

## 04. Docker Monitoring
🔗 **Full Lesson:** [04_monitoring.md](./04_monitoring.md)

* **Why It Exists**: Prevents "flying blind." Monitoring allows tracking CPU, Memory, Disk, and Network telemetry in real-time, helping locate memory leaks or high-CPU bottlenecks.
* **The Monitoring Stack (cAdvisor + Prometheus + Grafana)**:
  1. **cAdvisor**: Google tool that collects metrics directly from container nodes.
  2. **Prometheus**: Time-series database that scrapes metrics from cAdvisor.
  3. **Grafana**: Visual dashboard that displays query metrics on graphs.

### Key Commands:
```bash
docker stats                                                               # Stream live resource statistics for all containers
docker stats --no-stream                                                   # Get single-frame snapshot of current stats
```

> [!WARNING]
> **OOMKilled (Exit Code 137)**: Occurs when a container exceeds its memory limits, prompting the Linux kernel to terminate the process. Check this with `docker inspect <container>` to identify memory bottlenecks.

---

## 05. Scaling Containers
🔗 **Full Lesson:** [05_scaling_containers.md](./05_scaling_containers.md)

* **Why It Exists**: Single containers represent a **Single Point of Failure**. Scaling scales app containers horizontally by spinning up identical replicas and load balancing traffic across them.
* **Real-World Analogy**: **Grocery Checkout Lanes**. Instead of making one cashier work infinitely fast (vertical scaling), you open 5 additional checkout lanes (horizontal scaling).

### Key Commands:
```bash
docker compose up -d --scale web=3                                         # Scale the 'web' service to 3 instances
docker compose up -d --scale web=1                                         # Scale down to 1 instance
```

> [!IMPORTANT]
> **Avoid Port Conflicts**: When scaling, you cannot map a static host port directly in the service block (e.g., `ports: - "8080:80"`). You must omit the host port mapping, use `expose: - "80"`, and place an Nginx container inside the same network to route public traffic.
> **Stateful Constraints**: scaled applications must be stateless. Store user sessions in **Redis** and uploads in **S3**, rather than the container's volatile memory or disk.

---

## 06. CI/CD with GitHub Actions and Docker
🔗 **Full Lesson:** [06_cicd_github_actions.md](./06_cicd_github_actions.md)

* **Why It Exists**: Manual building, tagging, and pushing is slow and error-prone. CI/CD pipelines automate building, testing, and pushing images to registries (Docker Hub, AWS ECR) upon every code commit.

### CI/CD Pipeline Configuration (`.github/workflows/react-ci.yml`):
```yaml
name: Production CI/CD

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push with layer cache
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/my-app:latest
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/my-app:buildcache
        cache-to: type=inline
```

### Running the image locally:
```bash
docker run -d -p 80:80 --name running-app username/my-app:latest
```

---

## 07. Production Deployments on AWS EC2
🔗 **Full Lesson:** [07_production_deployments_ec2.md](./07_production_deployments_ec2.md)

* **Why It Exists**: The final deployment step to make your containerized app accessible to the global internet on virtual servers in the cloud.
* **Topology**: Local commit ──► GitHub push ──► CI/CD Auto-Build ──► Docker Hub ──► EC2 pull and run.

### Key Deployment Script (`deploy.sh` on EC2):
```bash
#!/bin/bash
docker pull myusername/my-app:latest
docker stop my-running-app || true
docker rm my-running-app || true
docker run -d -p 80:3000 --name my-running-app myusername/my-app:latest
echo "Deployment Complete!"
```

### Server Shell Setup Commands:
```bash
ssh -i "my-key.pem" ubuntu@ec2-ip-address.compute-1.amazonaws.com           # Securely connect to EC2
sudo apt update && sudo apt install docker.io -y                            # Install Docker on Ubuntu EC2
sudo usermod -aG docker ubuntu                                              # Enable running docker without sudo (re-login required)
chmod 400 my-key.pem                                                        # Set correct permissions on SSH key
```

> [!WARNING]
> **AWS Security Groups**: If a deployed app is unreachable, the most common issue is that the AWS Security Group lacks inbound rules opening **HTTP (Port 80)** or **HTTPS (Port 443)** to the public internet (`0.0.0.0/0`).

---
