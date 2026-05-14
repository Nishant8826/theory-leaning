# Project 2: Containerized MERN on ECS Fargate

## What Is This Project?
This project modernizes the MERN stack by containerizing the Node.js backend using Docker, pushing it to Amazon ECR, and orchestrating it using Amazon ECS on AWS Fargate. The React frontend will be hosted on Amazon S3 and distributed via CloudFront.

## Why Do This Project?
This is the industry standard for production MERN deployments. It provides high availability, auto-scaling, and completely removes the need to manage underlying EC2 servers (Serverless compute via Fargate).

## How to Build It (Step-by-Step)

### Step 1: Frontend - S3 & CloudFront
1. Build your React app locally: `npm run build`.
2. **S3**: Create an S3 Bucket (e.g., `my-mern-frontend`). Upload the contents of the `build` folder.
3. **CloudFront**: Create a new Distribution.
   - Origin Domain: Select the S3 bucket.
   - Origin Access: Choose **Origin Access Control (OAC)** to keep the S3 bucket private.
   - Viewer Protocol Policy: Redirect HTTP to HTTPS.
   - Default Root Object: `index.html`.
4. Copy the generated CloudFront Policy and apply it to your S3 Bucket Permissions.
5. Note the CloudFront domain name (e.g., `d1234.cloudfront.net`). This is your frontend URL.

### Step 2: Dockerize the Backend
1. In your Express backend folder, create a `Dockerfile`:
   ```dockerfile
   FROM node:22-alpine
   WORKDIR /usr/src/app
   COPY package*.json ./
   RUN npm install --production
   COPY . .
   EXPOSE 5000
   CMD ["node", "server.js"]
   ```
2. Build it locally to test: `docker build -t mern-api .`

### Step 3: Push to Elastic Container Registry (ECR)
1. In the AWS Console, go to **ECR** and create a private repository named `mern-api`.
2. Click **View push commands**.
3. Run the provided `aws ecr get-login-password` command in your terminal to authenticate Docker.
4. Tag your image: `docker tag mern-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/mern-api:latest`
5. Push the image: `docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/mern-api:latest`

### Step 4: Configure the Application Load Balancer (ALB)
1. Go to EC2 > **Target Groups**. Create a target group:
   - Target Type: **IP addresses** (Required for Fargate).
   - Protocol/Port: HTTP 5000.
   - Health Check Path: `/api/health` (Ensure your Express app has this route!).
2. Go to EC2 > **Load Balancers**. Create an **Application Load Balancer**.
   - Scheme: Internet-facing.
   - Network: Select your default VPC and at least two Public Subnets.
   - Security Group: Create an `ALB-SG` allowing HTTP (80) from Anywhere.
   - Listener: Port 80 forwarding to the Target Group you just created.

### Step 5: Deploy to ECS Fargate
1. Go to **ECS** > Clusters > Create Cluster. Name it `Mern-Cluster` using AWS Fargate.
2. Go to **Task Definitions** > Create new Task Definition.
   - Launch Type: Fargate.
   - OS/Architecture: Linux/X86_64.
   - CPU: `0.25 vCPU` | Memory: `0.5 GB`.
   - Execution Role: Create new role.
   - **Container Setup**: 
     - Image: Paste your ECR Image URI.
     - Port Mappings: `5000` (TCP).
     - Environment Variables: Add `MONGO_URI` (Value: your Atlas connection string).
3. Go back to your Cluster > Services > **Create Service**.
   - Compute Options: Launch type -> Fargate.
   - Task Definition: Select the one you just created.
   - Desired Tasks: `2` (High Availability!).
   - Networking: Select your VPC and **Private Subnets**.
   - Security Group: Create an `ECS-SG` allowing Port 5000 ONLY from the `ALB-SG`.
   - Load Balancing: Select Application Load Balancer and choose your Target Group.
4. Click **Create**.

## Production Impact
- **Security**: The backend lives in private subnets with no public IPs. It can only be accessed through the Load Balancer.
- **Availability**: By requesting 2 tasks across different subnets, AWS automatically places them in separate Availability Zones. If a data center loses power, the ALB routes traffic to the surviving container.

## Knowledge Transfer (KT)
- **Why IP Target Type?** In ECS Fargate, you don't manage EC2 instances. Fargate provisions an Elastic Network Interface (ENI) with a specific private IP address directly to your container. Therefore, the Load Balancer must route traffic to an IP address, not an Instance ID.
- **CORS Requirements**: Because your CloudFront frontend and ALB backend have different domains, you MUST configure the `cors` middleware in Express to allow requests from the CloudFront domain.

---
Prev : [./01_Project_MERN_on_EC2.md](./01_Project_MERN_on_EC2.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./03_Project_MERN_on_EKS.md](./03_Project_MERN_on_EKS.md)
---
