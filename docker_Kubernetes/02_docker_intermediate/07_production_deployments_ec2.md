# Production Deployments on AWS EC2

## Why This Exists
You have containerized your app, tested it locally, and automated the build process. Now comes the final step: putting it on a real server in the cloud so that anyone in the world can access it.

**AWS EC2 (Elastic Compute Cloud)** is the most common way to get a virtual server in the cloud. Deploying Docker on EC2 is a fantastic, cost-effective way to host applications. Since the environment inside the container is identical to your local setup, "it works on my machine" translates perfectly to "it works on AWS."

## Real World Analogy
Think of deploying to EC2 like **Renting a Storefront**.
- Your local computer is your laboratory where you design products.
- An EC2 instance is a physical shop you rent in a busy city (The Internet).
- Docker allows you to pack your entire shop setup into a box and unpack it perfectly in the rented storefront without having to rebuild the shelves manually.

## Core Concepts
- **EC2 Instance**: A virtual computer in AWS.
- **SSH (Secure Shell)**: A protocol used to securely connect to the command line of your EC2 instance.
- **Security Groups**: AWS's virtual firewall that controls what traffic is allowed in and out of your EC2 instance.
- **Docker Hub**: Where we pull our production-ready images from.

## Architecture / Flow

```text
[ Local Machine ] --- (Git Push) ---> [ GitHub ]
                                         │
                                         ▼ (Auto Builds)
                                   [ Docker Hub ]
                                         │
                                         ▼ (Docker Pull)
                                   [ AWS EC2 Instance ]
                                         │
                                         ▼
                                   [ Running App ] <--- (Accesses) --- [ Users ]
```

## Practical Commands

### 1. Connect to EC2 via SSH
```bash
ssh -i "my-key-pair.pem" ubuntu@ec2-54-210-12-34.compute-1.amazonaws.com
```

### 2. Install Docker on Ubuntu EC2
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Allow the 'ubuntu' user to run docker without 'sudo'
sudo usermod -aG docker ubuntu
# (Log out and log back in for this to take effect)
```

### 3. Pull and Run your app
```bash
docker pull myusername/my-app:latest
docker run -d -p 80:3000 --name running-app myusername/my-app:latest
```

## Hands-On Exercise
Let's deploy a container manually on a fresh Ubuntu EC2 instance.

1. **Launch an EC2 Instance** on AWS (Ubuntu 24.04 LTS, t2.micro is free tier).
2. **Configure Security Groups**: Add an Inbound Rule to allow **HTTP (Port 80)** from "Anywhere (0.0.0.0/0)".
3. **SSH into the instance** using your terminal and the `.pem` key file.
4. **Install Docker** using the commands shown in the Practical Commands section above.
5. **Run a test container**:
   ```bash
   docker run -d -p 80:80 nginx:alpine
   ```
6. Copy the **Public IPv4 address** of your EC2 instance from the AWS console and paste it into your browser. You should see the Nginx welcome page!

## Mini Project
**Task**: Set up a continuous deployment script on your EC2 instance.

Instead of typing commands manually every time you update your app, create a script named `deploy.sh` on your EC2 instance:
```bash
#!/bin/bash
docker pull myusername/my-app:latest
docker stop my-running-app || true
docker rm my-running-app || true
docker run -d -p 80:3000 --name my-running-app myusername/my-app:latest
echo "Deployed successfully!"
```
Make it executable: `chmod +x deploy.sh`. Now, whenever you want to update the app, just SSH in and run `./deploy.sh`.

## Real Production Usage
- **Load Balancers**: In a real production environment, you don't expose port 80 directly from EC2. You put an **AWS Application Load Balancer (ALB)** in front of it. The ALB handles SSL certificates and forwards traffic to your EC2 instance.
- **Orchestration**: For larger apps, instead of raw EC2, you would use **AWS ECS (Elastic Container Service)** or **EKS (Elastic Kubernetes Service)** which handle scaling and healing automatically.

## Common Mistakes
- **Forgetting Security Groups**: The #1 reason people can't access their app on EC2 is that they forgot to open port 80 (HTTP) or 443 (HTTPS) in the AWS Security Group.
- **Key permissions**: If you get an error like "Permissions are too open" for your `.pem` file when SSHing, run `chmod 400 my-key-pair.pem`.

## Debugging Guide
- **Connection Timed Out**: Usually a Security Group issue. Ensure your IP is allowed to SSH (Port 22) and the world is allowed to access Port 80.
- **App is running but can't be reached**: Check if the app is listening on `0.0.0.0` inside the container, not `127.0.0.1`.

## Best Practices
- **Never store keys in the repo**: Keep your `.pem` files secure and never push them to GitHub.
- **Use AWS ECR**: For production, use AWS Elastic Container Registry instead of public Docker Hub to store private images securely within the AWS network.

## Interview Questions
1. **What is the most common reason you cannot access a web app running on an EC2 instance?**
   *Answer*: The Security Group assigned to the EC2 instance does not have an inbound rule allowing traffic on port 80 or 443.
2. **How do you ensure data is not lost when an EC2 instance is terminated?**
   *Answer*: By using Docker volumes mapped to AWS EBS (Elastic Block Store) volumes, or by storing data in external managed databases like AWS RDS.

## Summary
Deploying Docker on EC2 bridges the gap between development and the live internet. By mastering SSH, Security Groups, and Docker commands, you can host your applications reliably in the cloud.

---
Prev: [06_cicd_github_actions.md](./06_cicd_github_actions.md) | Index: [Index](../00_index.md) | Next: [Index](../00_index.md)
