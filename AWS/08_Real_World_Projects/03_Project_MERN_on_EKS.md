# Project 3: MERN Stack on Kubernetes (EKS)

## What Is This Project?
This project walks you through deploying the same containerized MERN backend onto Amazon Elastic Kubernetes Service (EKS) using declarative YAML files.

## Why Do This Project?
While ECS is AWS-native and easier, Kubernetes is the undisputed industry standard for multi-cloud enterprise container orchestration. Learning how to write Deployments, Services, and Ingress manifests is a critical skill for senior DevOps engineers.

## How to Build It (Step-by-Step)

### Step 1: Provision the EKS Cluster
*Do not use the AWS Console for this. It is too complex.*
1. Install [eksctl](https://eksctl.io/), [kubectl](https://kubernetes.io/docs/tasks/tools/), and the AWS CLI.
2. Run the following command to provision a cluster with 2 worker nodes:
   ```bash
   eksctl create cluster \
     --name mern-cluster \
     --region us-east-1 \
     --nodegroup-name standard-workers \
     --node-type t3.medium \
     --nodes 2 \
     --managed
   ```
   *(This takes ~15 minutes. It provisions a VPC, control plane, and EC2 nodes automatically).*
3. Verify connection: `kubectl get nodes`

### Step 2: Write the Kubernetes Deployment
Create a file named `backend-deployment.yaml`. This tells K8s how to run your Docker container.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mern-api
  template:
    metadata:
      labels:
        app: mern-api
    spec:
      containers:
      - name: express-container
        image: <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/mern-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: MONGO_URI
          value: "mongodb+srv://user:pass@cluster.mongodb.net/test"
```

### Step 3: Write the Kubernetes Service
Create a file named `backend-service.yaml`. This tells AWS to provision an Elastic Load Balancer (ELB) to route internet traffic to your Pods.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: express-service
spec:
  type: LoadBalancer
  selector:
    app: mern-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

### Step 4: Apply Manifests to the Cluster
1. Apply the deployment:
   ```bash
   kubectl apply -f backend-deployment.yaml
   ```
2. Verify pods are running:
   ```bash
   kubectl get pods
   ```
3. Apply the service:
   ```bash
   kubectl apply -f backend-service.yaml
   ```
4. Get the public Load Balancer URL:
   ```bash
   kubectl get svc express-service
   ```
   *(Look for the `EXTERNAL-IP` column. Copy that URL and paste it into your browser or Postman).*

### Step 5: Teardown (CRITICAL)
EKS control planes cost ~$73/month even if you run zero containers. You must delete the cluster when finished.
```bash
eksctl delete cluster --name mern-cluster --region us-east-1
```

## Production Impact
- **Declarative Infrastructure**: By storing `deployment.yaml` in Git, you have an exact, version-controlled history of your infrastructure. If a deployment fails, you can run `kubectl rollout undo deployment/express-backend` to instantly revert to the previous version.
- **Portability**: These exact same YAML files can be deployed to Google Kubernetes Engine (GKE) or Azure Kubernetes Service (AKS) in minutes.

## Knowledge Transfer (KT)
- **Pod Lifecycle**: Pods are ephemeral. Kubernetes might kill a Pod and reschedule it on a different node at any time. Because of this, the IP address of the Pod constantly changes. The `Service` abstraction provides a stable, permanent internal IP/DNS name that routes to whatever Pods are currently alive.
- **Secrets Management**: In a real production environment, you would NEVER hardcode `MONGO_URI` in the Deployment file. You would create a Kubernetes `Secret` object, and the Deployment would reference that secret.

---
Prev : [./02_Project_MERN_on_ECS.md](./02_Project_MERN_on_ECS.md) | Index : [../00_Index.md](../00_Index.md) | Next : [./04_Project_CI_CD_Pipeline.md](./04_Project_CI_CD_Pipeline.md)
---
