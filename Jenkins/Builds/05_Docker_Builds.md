# 🔨 Docker Builds in Jenkins

## 📌 Topic Name
Docker Integration: DinD, Socket Binding, and Agent Execution

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Running your Jenkins build inside a Docker container so you don't have to install Node or Python directly on the Jenkins server.
*   **Expert**: The Jenkins Declarative Pipeline provides native syntactic sugar (`agent { docker 'node:16' }`) to isolate build execution within containers. Under the hood, Jenkins relies on the Agent OS having a running Docker daemon. It executes a `docker run` command, mounting the Agent's physical workspace directory into the container. A Staff engineer must navigate the severe security implications of **Docker Socket Binding (`/var/run/docker.sock`)**, the complexities of **UID/GID mismatch**, and the architectural shift towards rootless or daemonless builds (Kaniko) in Kubernetes environments.

## 🏗️ Mental Model
Think of the Jenkins Agent as a **Factory Floor**, and Docker as a **Portable Clean Room**.
- **Without Docker**: You pour chemicals (dependencies) directly on the factory floor. It gets messy.
- **With Docker**: You drop a sealed glass box (Container) onto the floor. You pipe the ingredients into the box, mix them, take the final product out, and then throw the glass box away.
- **The Security Flaw (Socket Binding)**: To let the worker inside the glass box build other boxes (Docker in Docker), you give them the master key to the factory (binding `/var/run/docker.sock`). If the worker is evil, they can use that key to destroy the entire factory.

## ⚡ Actual Behavior
- **Workspace Mounting**: When you use `agent { docker 'maven:3' }`, Jenkins translates this to `docker run -v /var/jenkins_home/workspace/job:/workspace -w /workspace maven:3 cat`. It keeps the container alive by running `cat` (or `sleep`), and then uses `docker exec` to run your `sh` steps inside it.
- **UID/GID Inheritance**: By default, Docker runs as `root`. If a Docker container writes a file to the mounted workspace, that file is owned by `root`. When the container dies, the Jenkins Agent (running as `jenkins` user) cannot delete the file, causing the workspace cleanup to fail.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Docker Pipeline Plugin**: Translates the declarative syntax into underlying shell commands.
2.  **Docker out of Docker (DooD)**: The most common pattern. The Agent runs a container, but maps the host's docker socket into the container (`-v /var/run/docker.sock:/var/run/docker.sock`). This allows the container to run `docker build`, but the sibling containers are actually spawned on the *host*, not inside the container.
3.  **Docker in Docker (DinD)**: Running a full Docker daemon *inside* a Docker container. Requires the `--privileged` flag. Highly discouraged due to severe security vulnerabilities and cgroup conflicts.

## 🔁 Execution Flow (Declarative Docker Agent)
1.  **Allocation**: Pipeline allocates standard Jenkins Executor on an Agent.
2.  **Pull**: Agent runs `docker pull node:18`.
3.  **Run**: Agent runs `docker run -t -d -u 1000:1000 -v /workspace:/workspace node:18 cat`.
4.  **Execute**: Pipeline hits `sh 'npm install'`. Agent runs `docker exec <container_id> npm install`.
5.  **Output**: `npm` logs are streamed from `docker exec` back to the Controller.
6.  **Teardown**: Agent runs `docker stop <container_id>` and `docker rm`.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Image Pull Latency**: A 2GB Docker image takes time to pull. If the Agent doesn't have it cached, this adds 30+ seconds to every build start time.
- **I/O Penalty**: Mounting host volumes into Docker containers (especially on macOS/Windows agents) introduces a massive I/O penalty. Compiling code inside a mounted volume is significantly slower than native compilation.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS AGENT (OS User: jenkins) ]
      |
      |-- /var/run/docker.sock (Docker Daemon)
      |
      |-- [ WORKSPACE DIR ]
      |
      +---- [ DOCKER CONTAINER (node:18) ]
            |-- Mounts WORKSPACE DIR to /workspace
            |-- Runs 'npm build'
            |-- Writes output to /workspace/dist
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent none
    stages {
        stage('Build Frontend') {
            agent {
                docker { 
                    image 'node:18-alpine'
                    // CRITICAL: Forces container to run as the Jenkins host user
                    // preventing root-ownership file permission issues.
                    args '-u $(id -u):$(id -g)' 
                }
            }
            steps {
                sh 'npm install && npm run build'
            }
        }
        stage('Build Docker Image') {
            agent { label 'docker-host' }
            steps {
                // This requires the host to have Docker installed and the 
                // Jenkins user to be in the 'docker' group.
                script {
                    def app = docker.build("myorg/myapp:${env.BUILD_ID}")
                    app.push()
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Root Permission Trap**: A pipeline runs `agent { docker 'python' }`. It creates a coverage report. The `post { cleanup { cleanWs() } }` runs on the host agent, but gets a `Permission Denied` error because the report is owned by `root`. The workspace is left dirty.
2.  **Socket Binding Root Exploit (RCE)**: A malicious developer modifies the `Jenkinsfile` to run `docker run -v /:/hostOS ubuntu rm -rf /hostOS`. Because they have access to the Docker socket, they effectively have `root` on the underlying EC2 instance and destroy the agent.
3.  **DooD Port Collisions**: Two concurrent builds on the same agent both run `docker run -p 8080:80 nginx` for integration testing. The second build fails instantly because port 8080 on the host is already bound by the first build.

## 🧪 Real-time Q&A
*   **Q**: Why not just use Kaniko?
*   **A**: Kaniko is the modern best practice. It builds Docker images *without* requiring a Docker daemon or root privileges. It is highly recommended over DinD/DooD, especially in Kubernetes environments.
*   **Q**: Can I cache Docker image builds in Jenkins?
*   **A**: Yes, by passing `--cache-from` to your `docker build` command, or by using Kaniko's native caching arguments.

## ⚠️ Edge Cases
*   **Multiple Containers**: You can define multiple containers using the `parallel` directive or by using the `docker-compose` plugin, but managing the network bridges between them dynamically is notoriously fragile in Jenkins.

## 🏢 Best Practices
1.  **Always Map UIDs**: Always pass `-u $(id -u):$(id -g)` in your `agent { docker {} }` blocks to prevent root-owned workspace files.
2.  **Ban DinD**: Never run Docker-in-Docker (`--privileged`). It is a massive security risk.
3.  **Transition to Kaniko/Buildah**: For building OCI images within CI, move away from the Docker Daemon entirely.

## ⚖️ Trade-offs
*   **Docker Agent vs Native Agent**:
    *   *Docker*: Perfect reproducibility, no toolchain management (`apt-get install node`).
    *   *Native*: Much faster I/O, utilizes local OS caches, but vulnerable to dependency drift ("It worked last week!").

## 💼 Interview Q&A
*   **Q**: We are running Jenkins Agents on EC2. Developers are using the Jenkins `docker` pipeline step to build containers. Security audited the EC2 instance and found that the `jenkins` user has effectively unrestricted root access to the machine. Why?
*   **A**: To allow Jenkins to execute `docker build` commands, the `jenkins` user was likely added to the `docker` Linux group, or the `/var/run/docker.sock` was made writable. Anyone with access to the Docker socket can launch a privileged container, mount the host's root filesystem `/`, and modify `/etc/shadow` or SSH keys, gaining instant root access. To secure this, we must remove Docker socket access and transition to daemonless image builders like Kaniko or Buildah.

## 🧩 Practice Problems
1.  Write a pipeline that uses `agent { docker 'alpine' }` *without* passing the `-u` argument. Create a file via `sh 'touch test.txt'`. Attempt to `sh 'rm test.txt'` outside the docker block. Observe the permission denied error.
2.  Refactor a `docker.build()` step to use Kaniko via a Kubernetes pod template.

---
Prev: [04_Caching_Strategies.md](../Builds/04_Caching_Strategies.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [01_Distributed_Builds.md](../Distributed/01_Distributed_Builds.md)
---
