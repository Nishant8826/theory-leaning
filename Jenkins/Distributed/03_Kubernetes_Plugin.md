# 🌐 Jenkins on Kubernetes

## 📌 Topic Name
The Kubernetes Plugin: Cloud-Native Ephemeral CI/CD

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Running Jenkins workers as Pods in a Kubernetes cluster so you never have to manage virtual machines.
*   **Expert**: The Jenkins Kubernetes Plugin transforms Jenkins into a true cloud-native orchestrator. Instead of SSHing into static VMs, Jenkins uses the Kubernetes API to inject **PodSpecs** containing the required build tools. Every Pipeline execution runs in a brand new, ephemeral Pod. A Staff engineer masters the complexities of **Multi-Container Pods** (where the `jnlp` container handles Remoting and sidecars handle execution), **Kubernetes Workload Identity** (IRSA/OIDC) for secure cloud access, and container resource limits (Requests/Limits) to prevent noisy neighbor evictions.

## 🏗️ Mental Model
Think of Kubernetes Jenkins as an **Instant Pop-Up Office**.
- **The Request**: A pipeline needs to build a Go app.
- **The Provisioning**: Jenkins tells Kubernetes, "Build me an office. Give it one desk with a telephone (the `jnlp` container) and one desk with Go installed (the `golang` container)."
- **The Execution**: Kubernetes builds the office in 5 seconds. Jenkins calls the telephone, hands instructions to the Go worker, and waits.
- **The Teardown**: When the job is done, the office is bulldozed. No mess left behind.

## ⚡ Actual Behavior
- **The `jnlp` Container Requirement**: EVERY Pod provisioned by the plugin *must* contain a container named `jnlp`. This container runs the Jenkins `agent.jar` and establishes the inbound Remoting connection back to the Controller.
- **Container Switching**: The Declarative `container('name')` directive simply wraps the `sh` commands in `docker exec` or `kubectl exec` logic to route the shell execution to the specific sidecar container within the Pod.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **PodTemplate**: The blueprint for the Pod. Defined via YAML in the Jenkinsfile or globally in the UI. It defines containers, volumes (PVCs, emptyDir, hostPath), and ServiceAccounts.
2.  **Shared Workspace (emptyDir)**: How do multiple containers in a Pod share files? Kubernetes automatically mounts an `emptyDir` volume at the workspace path across all containers in the Pod. The Git checkout happens in the `jnlp` container, but the `golang` container can read the files because they share the underlying disk mount.
3.  **Inbound Connection**: The `jnlp` container connects to the Jenkins Controller via the `JENKINS_URL` and `JENKINS_TUNNEL` environment variables. If the Pod cannot resolve the Controller's DNS, the Pod will launch but the build will hang indefinitely.

## 🔁 Execution Flow
1.  **Pipeline**: Hits `agent { kubernetes { yaml "..." } }`.
2.  **API Call**: Controller sends Pod JSON to K8s API server.
3.  **Scheduling**: Kube-scheduler places the Pod on a Node.
4.  **Init**: Kubelet pulls images and starts containers (`jnlp` + custom).
5.  **Handshake**: `jnlp` container connects to Controller. Executor is registered.
6.  **Checkout**: Git runs (usually inside `jnlp`).
7.  **Execution**: Pipeline hits `container('maven') { sh 'mvn package' }`. Command routes to the Maven container.
8.  **Completion**: Controller sends termination signal to K8s API. Pod is deleted.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **OOMKilled**: If you do not set Memory Requests/Limits, a rogue Java compile or Webpack build will consume all Node memory, causing the Kubelet to `OOMKill` the container. Jenkins will report a cryptic "Agent disconnected" error.
- **Startup Latency**: If the Pod requests a 2GB Docker image that isn't cached on the K8s Node, image pulling will add 30-60 seconds to the pipeline start time.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS CONTROLLER ]
       ^    |
       |    | (2. Spawns Pod via K8s API)
       |    |
       |  [ KUBERNETES CLUSTER ]
       |        |
(3. Connects)   v
       +--- [ POD: 'jenkins-agent-abc12' ]
            |
            |-- [ CONTAINER: 'jnlp' ] (Jenkins Remoting / Git)
            |      \- (Shared Volume: /home/jenkins/agent) -+
            |                                               |
            |-- [ CONTAINER: 'maven' ] (Java Tools)         |
            |      \- (Shared Volume: /home/jenkins/agent) -+
            |                                               |
            |-- [ CONTAINER: 'docker' ] (Kaniko/Buildah)    |
                   \- (Shared Volume: /home/jenkins/agent) -+
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              serviceAccountName: "build-sa" # Injects AWS IAM or GCP roles
              containers:
              - name: jnlp # Mandatory for remoting connection
                image: jenkins/inbound-agent:alpine
              - name: maven
                image: maven:3.8-eclipse-temurin-11
                command: ['cat'] # Keeps container alive
                tty: true
                resources:
                  requests:
                    memory: "1Gi"
                    cpu: "500m"
            '''
        }
    }
    stages {
        stage('Build') {
            steps {
                // Switch execution into the Maven container
                container('maven') {
                    sh 'mvn clean verify'
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The "Offline Node" Hang**: The PodTemplate YAML has an error (e.g., requesting a non-existent Secret). The K8s API accepts the Pod, but it stays in `ContainerCreating` forever. Jenkins waits for the `jnlp` container to connect, which never happens. The build hangs for hours.
2.  **Resource Deadlock (Pending Pods)**: A pipeline requests a Pod with `cpu: "16"`. The cluster has no Nodes large enough, and the Cluster Autoscaler cannot provision one. The Pod stays in `Pending` state forever, starving the Jenkins queue.
3.  **HostPath Exploitation**: A developer defines a `hostPath` volume mount for `/var/run/docker.sock` or `/etc/` in their Jenkinsfile PodTemplate. They gain root execution on the underlying Kubernetes Node, breaking container isolation. **Solution**: Enforce Kubernetes Pod Security Standards (PSS) to block host mounts.

## 🧪 Real-time Q&A
*   **Q**: Why do I need `command: ['cat']` and `tty: true` in my custom containers?
*   **A**: Kubernetes expects containers to run a foreground process and exit. The Jenkins plugin needs the container to stay alive infinitely in the background so it can inject `sh` commands at will. `cat` with a TTY creates an infinite loop that consumes zero CPU.
*   **Q**: Can I run Docker inside these Pods?
*   **A**: Running DinD (Docker-in-Docker) requires `securityContext: privileged`, which is a massive security risk in K8s. The industry standard is to use **Kaniko**, which builds container images entirely in user-space without needing Docker daemon privileges.

## ⚠️ Edge Cases
*   **Controller in a different cluster**: If the Controller is not in the same K8s cluster as the Agents, you must configure the Kubernetes URL, CA Certificate, and a Service Account Token in the Jenkins Cloud configuration, and ensure the `jnlp` port (50000) is exposed via a LoadBalancer or Ingress.

## 🏢 Best Practices
1.  **Enforce Resource Limits**: Never allow a PodTemplate without `requests` and `limits`. Unbounded Pods will bring down your Kubernetes worker nodes.
2.  **Abstract YAML into Libraries**: Don't put 50 lines of YAML in every Jenkinsfile. Put it in a Shared Library function (e.g., `mavenPod { ... }`).
3.  **Use Workload Identity**: Bind the Kubernetes ServiceAccount (`serviceAccountName`) to an AWS IAM Role (IRSA) or GCP Service Account. Never pass static AWS Access Keys in Jenkins credentials.

## ⚖️ Trade-offs
*   **Kubernetes vs EC2 Agents**:
    *   *K8s*: Blazing fast startup (if images are cached), perfect isolation, zero idle cost.
    *   *EC2*: Slower startup, but provides full machine access for heavy kernel-level testing or running nested virtualization.

## 💼 Interview Q&A
*   **Q**: A pipeline running on Kubernetes fails randomly with no Jenkins error, just a message that the agent disconnected. How do you troubleshoot this?
*   **A**: This is the classic symptom of the Kubernetes Kubelet terminating the pod out of band. I would immediately check the Kubernetes event logs (`kubectl get events`) or the pod description before it gets garbage collected. It is almost certainly an `OOMKilled` (Out Of Memory) event because the Java/Node process exceeded the container's memory `limits`, or the Pod was evicted due to Node disk pressure. The fix is to increase the memory `limits` in the PodTemplate YAML.

## 🧩 Practice Problems
1.  Write a PodTemplate containing three containers: `jnlp`, `golang`, and `node`. Write a pipeline that switches between them using `container('...')`.
2.  Inspect the logs of a running `jnlp` container using `kubectl logs <pod-name> -c jnlp` to see the actual Jenkins Remoting handshake.
