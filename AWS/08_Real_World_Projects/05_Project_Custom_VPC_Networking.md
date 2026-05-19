# Project 5: Building a Custom VPC for MERN

## What Is This Project?
This project guides you through building a highly secure, custom Virtual Private Cloud (VPC) from scratch. We will create Public Subnets for Load Balancers, Private Subnets for Express/Node.js servers, an Internet Gateway (IGW) for inbound traffic, and a NAT Gateway for secure outbound traffic.

## Why Do This Project?
Deploying your application into the "Default VPC" is a massive security risk. The Default VPC places every EC2 instance into a Public Subnet, exposing them directly to the internet. To pass enterprise security audits, your backend servers and databases must reside in Private Subnets. This project teaches you exactly how to build that infrastructure.

## How to Build It (Step-by-Step)

### Step 1: Create the VPC & Subnets
1. Open the **VPC Dashboard** and click **Create VPC**.
2. Select **VPC only**.
   - Name tag: `MERN-Production-VPC`
   - IPv4 CIDR block: `10.0.0.0/16`
3. Go to **Subnets** > **Create subnet**. Select your new VPC.
   - Create **Public Subnet 1**: `10.0.1.0/24` (AZ: `us-east-1a`)
   - Create **Private Subnet 1**: `10.0.2.0/24` (AZ: `us-east-1a`)

### Step 2: Configure the Internet Gateway (IGW)
1. Go to **Internet Gateways** > **Create internet gateway**.
   - Name tag: `MERN-IGW`
2. Select the new IGW > Actions > **Attach to VPC**. Select `MERN-Production-VPC`.
   *(This gives the VPC the physical ability to connect to the internet).*

### Step 3: Configure the NAT Gateway
1. Go to **NAT Gateways** > **Create NAT gateway**.
   - Name tag: `MERN-NAT`
   - Subnet: Select **Public Subnet 1** (CRITICAL: NAT Gateways must live in a Public Subnet).
   - Elastic IP allocation ID: Click **Allocate Elastic IP**.
2. Click **Create**. *(This allows instances in the Private Subnet to download NPM packages).*

### Step 4: Set up Route Tables
1. Go to **Route Tables** > **Create route table**.
   - Name: `MERN-Public-RT`
   - VPC: `MERN-Production-VPC`
2. Select `MERN-Public-RT` > **Routes** > **Edit routes**.
   - Add Route: Destination `0.0.0.0/0`, Target `Internet Gateway` (`MERN-IGW`).
3. Select `MERN-Public-RT` > **Subnet associations** > **Edit**. Associate it with **Public Subnet 1**.
4. Create another route table named `MERN-Private-RT`.
   - Add Route: Destination `0.0.0.0/0`, Target `NAT Gateway` (`MERN-NAT`).
   - Associate it with **Private Subnet 1**.

### Step 5: Test the Private Subnet
1. Launch an EC2 instance into **Public Subnet 1** (Auto-assign public IP: Enable). This is your "Bastion Host".
2. Launch an EC2 instance into **Private Subnet 1** (Auto-assign public IP: Disable). This represents your Express Backend.
3. SSH into the Bastion Host. From the Bastion Host, SSH into the Private Instance.
4. Run `ping google.com` from the Private Instance.
   - *If it works, your NAT Gateway and Private Route Table are perfectly configured!*

## Production Impact
- **Absolute Isolation**: Your backend Express server has no Public IP. Hackers scanning the internet for open ports literally cannot see your server. It is invisible to the outside world.
- **Controlled Ingress**: The only way for a user to reach the Express server is through an Application Load Balancer placed in the Public Subnet, which forwards the traffic down to the Private Subnet.

## Knowledge Transfer (KT)
- **Why `/16` and `/24`?** `10.0.0.0/16` gives your VPC 65,536 total IP addresses. `10.0.1.0/24` gives a subnet 256 IPs. This allows you to slice the massive VPC into hundreds of organized subnets without running out of addresses.
- **NAT Gateway Cost**: NAT Gateways are expensive (~$32/month just to keep them running). If you are building a personal project, put your servers in the Public Subnet to save money, but know how to build a NAT for your job.

---
Prev : [./04_Project_CI_CD_Pipeline.md](./04_Project_CI_CD_Pipeline.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./06_Project_NextJS_Deployment.md](./06_Project_NextJS_Deployment.md)
---
