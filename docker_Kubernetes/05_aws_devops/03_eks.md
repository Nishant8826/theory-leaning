# Eks

## Why This Exists
Kubernetes consists of two parts: the "Control Plane" (the master brain) and the "Worker Nodes" (the servers running your apps). Managing the Control Plane yourself is a nightmare—if the database (etcd) corrupts, your whole cluster dies. EKS (Elastic Kubernetes Service) is AWS saying: "We will manage the highly complex brain for you; you just give us the worker servers."

## Real World Analogy
Think of building a house. 
Doing it yourself (DIY Kubernetes on EC2) means you have to be the **General Contractor**. You must hire the plumbers, electricians, and ensure the permits are valid. It's stressful.
EKS is like **Hiring a Professional General Contractor**. You pay them a fee to handle all the complex coordination, management, and disaster recovery. You simply hand them the blueprints (YAML files), and they make sure the workers (Nodes) build it.

## Core Concepts
*   **Managed Control Plane:** AWS runs the API Server and etcd across multiple Availability Zones for high availability. You never see these servers.
*   **Node Groups:** A group of EC2 instances that register themselves as workers to the EKS Control Plane.
*   **AWS IAM Authenticator:** EKS maps AWS IAM Users to Kubernetes RBAC. You log into K8s using your AWS credentials.
*   **Fargate:** An option to run pods completely serverless, without even managing the underlying EC2 worker nodes.

## Architecture / Flow
1. You click "Create Cluster" in EKS. AWS takes ~15 minutes to spin up the hidden Control Plane.
2. You create a "Managed Node Group" of three `t3.medium` EC2 instances.
3. These EC2 instances boot up and securely connect to the Control Plane.
4. You run `kubectl apply -f app.yaml` on your laptop.
5. The request hits the AWS-managed API Server, which then schedules the pod onto one of your EC2 Node Groups.

## Practical Commands
*   `eksctl create cluster --name my-cluster --region us-east-1` - The absolute easiest way to create a cluster.
*   `aws eks update-kubeconfig --region us-east-1 --name my-cluster` - Configures your local `kubectl` to talk to EKS.
*   `kubectl get nodes` - Verify the EC2 nodes have joined the cluster.

## Hands-On Exercise
Install the CLI tool `eksctl`. Use it to deploy a small development cluster. Once it's running, deploy a simple Nginx pod. **Crucial:** When you are done, run `eksctl delete cluster --name my-cluster` so you don't get charged $70 next month!

## Mini Project
**"The Scalable API"**
Deploy a Node.js API to EKS. Install the AWS Load Balancer Controller using Helm. Create an Ingress resource that automatically provisions an AWS Application Load Balancer to route internet traffic into your EKS cluster.

## Real Production Usage
EKS is the industry standard for running Kubernetes on AWS. Major corporations use it to run thousands of microservices, trusting AWS's SLA to keep the Control Plane online so their engineers can focus purely on application code.

## Common Mistakes
*   **Running EKS for a Personal Blog:** EKS charges ~$70/month *just for the Control Plane*, plus the cost of the EC2 instances. It is massive overkill and too expensive for simple, low-traffic sites.
*   **IAM Messes:** Creating the cluster with User A, and then trying to run `kubectl` as User B. Only the IAM entity that created the cluster has admin access initially!

## Debugging Guide
*   **`error: You must be logged in to the server (Unauthorized)`:** Your AWS CLI is likely using a different IAM User/Role than the one configured in the EKS `aws-auth` ConfigMap.
*   **Pods stuck in Pending?** Check if you actually attached a Node Group. EKS provides the brain, but if there are no worker bodies, pods can't run.

## Best Practices
*   **Use Managed Node Groups:** Instead of managing EC2 Auto Scaling groups manually, let EKS manage them. This allows for 1-click Kubernetes version upgrades for your worker nodes.
*   **VPC CNI Plugin:** Understand that EKS assigns real AWS VPC IP addresses to every single pod. Ensure your VPC has a large enough subnet (like a `/16`), or you will run out of IPs!

## Interview Questions
*   **Q: What is the difference between Amazon ECS and Amazon EKS?**
    *   *A: EKS runs open-source Kubernetes, making it easier to migrate to/from other clouds. ECS is AWS's proprietary container orchestrator; it is simpler to learn but locks you into the AWS ecosystem.*

## Summary
EKS removes the hardest, most dangerous parts of operating Kubernetes (the control plane), providing a robust, highly available platform for running containerized applications at enterprise scale.

---
Prev: [02_ecr.md](./02_ecr.md) | Index: [Index](../00_index.md) | Next: [04_load_balancer.md](./04_load_balancer.md)
