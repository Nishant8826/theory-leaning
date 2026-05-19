# EC2 Deep Dive

## What Is This Service?
Amazon Elastic Compute Cloud (EC2) provides resizable, on-demand virtual servers in the cloud. It allows you to run Linux or Windows environments where you can deploy your Express APIs, background workers, or even host MongoDB instances manually.

## Why This Service Exists
Before EC2, developers had to wait weeks for IT to purchase and rack physical servers. EC2 exists to provide computing power instantly. You can spin up 1,000 servers in a minute and terminate them just as quickly, paying only for the seconds they are running.

## Real World Analogy
EC2 is like a **Rental Car**. 
You need a small car for a quick trip (a `t3.micro` for a simple Node script) or a massive cargo truck for heavy lifting (a `c6g.4xlarge` for video processing). You rent it, use it, and return it. AWS handles the maintenance (hardware) while you just drive (run your code).

## How It Works
AWS runs massive physical servers equipped with hypervisors (like Nitro). When you request an EC2 instance, the hypervisor carves out a Virtual Machine (VM) with your requested CPU, RAM, and storage, and attaches it to your VPC. You then SSH into this VM and install your Node.js runtime, Git, and Docker.

## Core Concepts
- **AMI (Amazon Machine Image)**: The template (OS + installed software) used to launch the instance (e.g., Ubuntu 22.04 LTS).
- **Instance Types**: Families of hardware tailored to specific workloads (e.g., `t` for general purpose burstable, `c` for compute-optimized).
- **EBS (Elastic Block Store)**: The virtual hard drive attached to your EC2 instance. If the instance stops, data on EBS persists.
- **User Data**: A shell script that automatically runs the very first time the instance boots (perfect for installing Node.js/Docker automatically).

## MERN Stack Integration
EC2 is the classic hosting destination for the Express/Node.js backend. You deploy the code to EC2 via GitHub Actions, use a process manager like `PM2` to keep the Express server running, and set up an NGINX reverse proxy to route traffic from port 80 to port 5000.

## Production Impact
- **Flexibility**: You have root access. You can tweak kernel parameters, run custom Node versions, or install C++ libraries.
- **Overhead**: With great power comes great responsibility. You are responsible for OS security patches, PM2 logs, and rotating SSH keys.

## Real Production Use Cases
- A video-rendering service for a Next.js app. When a user uploads a video, a massive compute-optimized `c5.2xlarge` EC2 instance is spun up to process the video with FFmpeg, and then instantly terminated to save costs.

## Production Best Practices
- **Never store state on EC2**: If the server crashes, it should be replaceable. Store uploads in S3 and data in MongoDB. Your EC2 instances should be "stateless" so Auto Scaling can kill or duplicate them freely.
- **Use ARM architecture (Graviton)**: Select `t4g` instances instead of `t3`. Graviton (ARM) processors are 20% cheaper and perform much better for Node.js workloads than Intel/AMD.

## Security Best Practices
- **No SSH Port 22**: Disable port 22 in your Security Groups. Use AWS Systems Manager (SSM) Session Manager to get a browser-based shell into your EC2 instances. It's infinitely more secure.
- **IAM Roles**: Attach an IAM Role to the EC2 instance instead of storing AWS keys in `.env`.

## Cost Optimization Tips
- **Spot Instances**: Use Spot Instances for background workers. They utilize spare AWS capacity and are up to 90% cheaper, but AWS can terminate them with a 2-minute warning.
- **Reserved Instances/Savings Plans**: If you know your Node.js API will run 24/7 for a year, buy a Compute Savings Plan to slash costs by ~40%.

## Common Mistakes
- Relying on the temporary Public IP. If you stop and start an EC2 instance, its Public IP changes. Always use an Elastic IP or rely on an Application Load Balancer to route traffic.
- Using a massive instance instead of horizontal scaling. Running one $500/mo server is bad practice. Running ten $50/mo servers behind a Load Balancer is highly available.

## Debugging & Troubleshooting
- **Instance Status Checks Failed**: If the System Status Check fails, the physical AWS hardware is broken. Stop and start the instance to migrate it to healthy hardware.
- **Out of Memory**: Node.js processes can memory leak and crash small `t2.micro` instances. Configure swap space or upgrade the instance type.

---
Prev : None | Index : [../00_Index.md](../00_Index.md) | Next : [./02_Load_Balancers_and_AutoScaling.md](./02_Load_Balancers_and_AutoScaling.md)
---
