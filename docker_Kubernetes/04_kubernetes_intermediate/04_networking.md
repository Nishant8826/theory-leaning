# Networking

## Why This Exists
In Kubernetes, Pods are mortal. They are constantly created and destroyed, and every time a Pod is created, it gets a brand new, random IP address. If the Frontend needs to talk to the Backend, it cannot rely on the Backend's IP address. K8s Networking (specifically **Services** and **Ingress**) provides stable, permanent addresses and routing rules.

## Real World Analogy
Think of an **Office Building**:
*   **Pods** are **Employees**. They frequently move desks or quit, changing their direct phone line (IP address).
*   **Services** are **Department Extensions**. If you dial 500, it rings the HR department, no matter which HR employee picks up.
*   **Ingress** is the **Front Desk Receptionist**. When a package arrives from the outside world, the receptionist looks at the label ("For the Web Team") and routes it to the correct internal department extension.

## Core Concepts
*   **ClusterIP (Service):** The default. Gives your app a stable, internal IP. Only things *inside* the K8s cluster can reach it.
*   **NodePort (Service):** Opens a specific port (like 30000) on every single physical server in your cluster. Used for external access.
*   **LoadBalancer (Service):** Tells your Cloud Provider (AWS/GCP) to spin up a physical Load Balancer to route internet traffic into your cluster.
*   **Ingress:** A smart router that sits at the edge of your cluster and routes HTTP/HTTPS traffic based on URLs (e.g., `/api` goes to backend, `/` goes to frontend).

## Architecture / Flow
1. User types `myapp.com/api` in their browser.
2. The internet routes the request to the Cloud **LoadBalancer**.
3. The LoadBalancer hands it to the **Ingress Controller** inside the cluster.
4. Ingress reads the `/api` path and forwards it to the **Backend Service** (ClusterIP).
5. The Service acts as a traffic cop and forwards the request to one of the 3 healthy **Backend Pods**.

## Practical Commands
*   `kubectl get svc` - List all services.
*   `kubectl expose deployment my-app --port=80 --target-port=8080` - Quickly create a ClusterIP service.
*   `kubectl get ingress` - See your URL routing rules.
*   `kubectl port-forward svc/my-database 5432:5432` - A magical command that securely tunnels traffic from your local laptop directly into an internal K8s service for debugging.

## Hands-On Exercise
Create a Deployment of Nginx. Create a `ClusterIP` Service for it. Then, run a temporary `busybox` pod inside the cluster and use `wget` to fetch the Nginx webpage using the Service's name as the URL, proving internal DNS works.

## Mini Project
**"The Router"**
Deploy two different web apps (e.g., an Nginx pod and an Apache pod). Create an Ingress resource that routes traffic based on the path. `localhost/nginx` should show the Nginx page, and `localhost/apache` should show the Apache page.

## Real Production Usage
In production, almost all microservices communicate internally via ClusterIP. Only a tiny fraction of the apps are exposed to the public internet using an Ingress Controller (like Nginx-Ingress or Traefik), which also handles SSL/TLS certificates automatically (via Cert-Manager).

## Common Mistakes
*   **TargetPort vs Port:** `port` is the port the Service listens on. `targetPort` is the port your actual container code is running on. Mixing these up is the #1 cause of "Connection Refused".
*   **Using NodePort in Prod:** NodePorts are mostly for testing. Exposing raw high-numbered ports to the internet is a security and usability nightmare.

## Debugging Guide
*   **Can't reach an app?** Work backwards. 
    1. Check if the Pod is running (`kubectl get pods`). 
    2. Check if the Service sees the Pod (`kubectl get endpoints <service-name>`). 
    3. Check if Ingress is routing to the Service correctly.
*   **DNS Issues:** Inside a pod, run `nslookup <service-name>`. If it fails, your CoreDNS (K8s internal DNS system) might be broken.

## Best Practices
*   **Least Privilege Exposure:** Default to `ClusterIP`. Only expose a service to the internet if absolutely necessary.
*   **Use Ingress for HTTP:** Instead of buying 10 Cloud LoadBalancers for 10 websites (which is expensive), buy 1 LoadBalancer pointing to an Ingress Controller, and let Ingress route to the 10 websites.

## Interview Questions
*   **Q: What is the difference between a ClusterIP and a NodePort?**
    *   *A: ClusterIP is strictly for internal communication within the cluster. NodePort opens a port on the physical host machines, allowing external traffic to enter the cluster.*

## Summary
Kubernetes networking provides a layer of abstraction over highly volatile pods. By mastering Services and Ingress, you can build complex, microservice architectures where components seamlessly discover and communicate with each other.

---
Prev: [03_jobs_cronjobs.md](./03_jobs_cronjobs.md) | Index: [Index](../00_index.md) | Next: [05_autoscaling.md](./05_autoscaling.md)
