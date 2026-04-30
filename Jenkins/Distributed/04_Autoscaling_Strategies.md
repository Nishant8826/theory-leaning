# 🌐 Autoscaling Strategies

## 📌 Topic Name
Jenkins Scalability: Reactive vs Predictive Auto-Scaling

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Making sure you have enough servers to handle the rush of builds at 9:00 AM, but shutting them down at night to save money.
*   **Expert**: Jenkins natively utilizes a **Reactive Scaling** model driven entirely by Queue depth. When tasks block in the queue, Jenkins provisions infrastructure. At enterprise scale, this reactive delay (boot latency) damages developer velocity. A Staff engineer bridges Jenkins with cloud-native autoscalers (Cluster Autoscaler, Karpenter, or AWS Auto Scaling Groups) to implement **Predictive** or **Buffer-based** scaling. The goal is to decouple the Jenkins Queue from raw infrastructure provisioning, ensuring "Warm" compute is instantly available without overspending.

## 🏗️ Mental Model
Think of scaling like a **Supermarket Checkout**.
- **Reactive (Default Jenkins)**: You open a new register *only* after 5 people are standing in line. Those 5 people are angry they had to wait for the cashier to walk up and log in.
- **Buffer-based**: You always keep 1 empty register open. As soon as someone uses it, you instantly call a new cashier to open another empty one.
- **Predictive**: You know a bus arrives at 5:00 PM every day, so you open 3 registers at 4:55 PM.

## ⚡ Actual Behavior
- **The Queue Delay**: Jenkins evaluates the queue every few seconds. If an item needs a node, Jenkins calls the Cloud Plugin (e.g., EC2 or K8s).
- **The Infrastructure Delay**: If using Kubernetes, Jenkins creates a Pod. If the K8s cluster is full, the Pod goes `Pending`. *Then*, the K8s Cluster Autoscaler notices the Pending Pod and calls AWS to launch a Node. This "Double Delay" can take 5-10 minutes.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Node Provisioning Thresholds**: Plugins have configurations for how long an item must sit in the queue before Jenkins bothers to provision a node.
2.  **Karpenter Integration**: AWS Karpenter bypasses standard Auto Scaling Groups (ASGs). It reads the Pending Pod's requirements (e.g., `nodeSelector: graviton`) and directly launches the exact EC2 instance type needed in <60 seconds.
3.  **Zombie Protection**: If Jenkins requests an instance, but the API times out, Jenkins might "forget" it asked. AWS launches the instance, but it never registers as an agent. Proper scaling architectures require external garbage collection loops.

## 🔁 Execution Flow (Karpenter + Jenkins K8s)
1.  **Jenkins Queue**: Reaches 1 task.
2.  **Jenkins K8s Plugin**: Spawns Pod YAML into K8s cluster.
3.  **Kube-Scheduler**: Fails to place Pod (Cluster is full). Pod -> `Pending`.
4.  **Karpenter**: Observes `Pending` Pod. Calculates required CPU/RAM.
5.  **EC2 Fleet**: Karpenter calls AWS Fleet API, bypassing ASGs.
6.  **Node Ready**: EC2 instance boots, joins cluster (45-60 seconds).
7.  **Execution**: Kubelet pulls image, starts Pod. Jenkins connects.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Thrashing**: If scale-down policies are too aggressive, Jenkins will terminate an agent, only to provision a new one 30 seconds later when a new job arrives. This wastes money on AWS EC2 minimum-billing increments and destroys caches.
- **Controller API Spam**: In a reactive model, 500 queued jobs will cause the K8s plugin to spam the K8s API server with 500 Pod creation requests simultaneously, potentially crashing the K8s Control Plane.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS QUEUE ]
       | (Triggers)
       V
[ KUBERNETES API ]  ---> (Pod Pending)
       |
       | (Observes)
       V
[ KARPENTER / AUTOSCALER ]
       |
       | (API Call)
       V
[ AWS EC2 / CLOUD PROVIDER ] ---> (Boots Node)
       |
       +---> [ NODE JOINS CLUSTER ] ---> [ POD STARTS ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# Kubernetes Over-Provisioning (Buffer Strategy)
# Deploy "Pause" pods. They do nothing but take up space.
# When Jenkins requests a real Pod, it has higher priority and evicts the Pause pod.
# The evicted Pause pod goes Pending, triggering the Autoscaler in the background.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: overprovisioning
spec:
  replicas: 2 # Keep 2 "Warm" nodes ready
  template:
    spec:
      priorityClassName: low-priority # Lower priority than Jenkins builds
      containers:
      - name: reserve-resources
        image: k8s.gcr.io/pause:3.1
        resources:
          requests:
            cpu: 4000m
            memory: 16Gi
```

## 💥 Production Failures
1.  **The Double-Scaling Race Condition**: Jenkins provisions an EC2 agent via the EC2 plugin. The K8s autoscaler also provisions a node. They fight over IP space in the subnet. **Solution**: Choose ONE scaling authority. If using K8s, let K8s handle the infrastructure; Jenkins should only handle Pods.
2.  **The "Pending" Black Hole**: An engineer requests a Jenkins Pod with `gpu: 1`, but the cloud account has a Service Quota limit of 0 GPUs. Jenkins creates the Pod, it stays `Pending` forever, and the user waits infinitely for a build that will never start.
3.  **Scale-Down Eviction**: The K8s Cluster Autoscaler decides a Node is underutilized and terminates it. A Jenkins build was running on a Pod on that Node. The build is violently aborted. **Solution**: Use the `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"` annotation on Jenkins PodTemplates.

## 🧪 Real-time Q&A
*   **Q**: How do I stop the K8s Autoscaler from killing running builds?
*   **A**: Ensure your Jenkins PodTemplates include the annotation `"cluster-autoscaler.kubernetes.io/safe-to-evict": "false"`. This tells the autoscaler, "Do not scale down this physical node as long as this Pod is running."
*   **Q**: What is the most cost-effective scaling strategy?
*   **A**: Using Amazon EKS with Karpenter, requesting Spot Instances, and ensuring fallback to On-Demand if Spot capacity is unavailable.

## ⚠️ Edge Cases
*   **Subnet Exhaustion**: Extreme horizontal scaling can consume all available IP addresses in a VPC Subnet. When the autoscaler tries to launch a new node, it fails silently at the AWS network layer.

## 🏢 Best Practices
1.  **Over-Provisioning (Warm Pools)**: Use Kubernetes "Pause Pods" with low priority to force the autoscaler to keep a few empty nodes active. Jenkins pods will instantly evict the pause pods and start building with zero boot latency.
2.  **Spot Instances**: CI/CD is the perfect use case for Spot/Preemptible instances. Combine this with the Jenkins retry plugin for ultimate cost efficiency.
3.  **Predictive Cron**: If 100 developers arrive at 9:00 AM, configure a cron job to scale up the ASG minimum capacity at 8:45 AM, and scale it down at 6:00 PM.

## ⚖️ Trade-offs
*   **Reactive vs Buffer**:
    *   *Reactive*: Cheapest infrastructure cost, but high "Wait Time" cost for developer salaries.
    *   *Buffer (Warm Pool)*: Wastes some money keeping idle compute alive, but drastically improves developer velocity and CI/CD pipeline speed.

## 💼 Interview Q&A
*   **Q**: We use the Jenkins Kubernetes plugin. During peak hours, developers complain their pipelines take 5 minutes just to start the first stage. How do you eliminate this wait time without permanently over-provisioning the cluster?
*   **A**: The 5-minute wait is the combined latency of Jenkins creating a Pod, the K8s Cluster Autoscaler reacting to the Pending Pod, AWS booting an EC2 node, and the Kubelet pulling the Docker image. To eliminate this, I would implement **Kubernetes Priority Classes and Over-provisioning (Pause Pods)**. I would deploy a low-priority Deployment that requests enough CPU/RAM to force the Autoscaler to keep a few extra nodes warm. When Jenkins requests a build Pod (which has standard priority), K8s will instantly evict the Pause Pods, starting the build in seconds. The evicted Pause Pods then go into Pending state, triggering the Autoscaler in the background, effectively hiding the infrastructure boot time from the developers.

## 🧩 Practice Problems
1.  Research the Kubernetes `PriorityClass` resource and how it interacts with the Jenkins PodTemplate `yaml` configuration.
2.  Configure a Jenkins EC2 Cloud template. Find the `idleTerminationMinutes` setting and explain why setting it to `0` vs `30` drastically impacts the AWS bill and the pipeline duration.

---
Prev: [03_Kubernetes_Plugin.md](../Distributed/03_Kubernetes_Plugin.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [05_Network_Latency_Impact.md](../Distributed/05_Network_Latency_Impact.md)
---
