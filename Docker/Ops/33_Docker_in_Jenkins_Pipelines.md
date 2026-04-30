# 📌 Topic: Docker in Jenkins Pipelines

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you have a **Robot Chef** (Jenkins).
- Instead of the robot cooking directly on your kitchen counter (The Jenkins server), you give the robot a **Portable Kitchen** (A Docker Container).
- The robot goes inside the portable kitchen, cooks the meal, and then throws the kitchen away.
- This ensures your real kitchen stays clean, and the robot always has the exact tools (Node.js version, Python version) it needs for that specific recipe.

Using Docker in Jenkins means your builds are **Clean**, **Isolated**, and **Reproducible**.

🟡 **Practical Usage**
-----------------------------------
### The `Jenkinsfile` (Declarative)
This is how you tell Jenkins to use Docker.

```groovy
pipeline {
    agent {
        docker { 
            image 'node:18-alpine' 
            args  '-v /root/.npm:/root/.npm' // Add caching!
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

### Building and Pushing Images
```groovy
stage('Deliver') {
    steps {
        script {
            docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                def customImage = docker.build("my-repo/my-app:${env.BUILD_ID}")
                customImage.push()
            }
        }
    }
}
```

🔵 **Intermediate Understanding**
-----------------------------------
### Docker-outside-of-Docker (DooD)
When Jenkins runs a container, how does that container build *another* image?
- **The Secret**: You mount the host's `/var/run/docker.sock` into the Jenkins container. 
- This allows the Jenkins "Agent" to talk to the real Docker Engine on the server.

### Jenkins Sidecars
Sometimes your tests need a database. Jenkins allows you to run a "Sidecar" container.
```groovy
agent {
    docker {
        image 'node:18'
    }
}
services {
    database { image 'mysql:8' }
}
```

🔴 **Internals (Advanced)**
-----------------------------------
### Workspace Mounting
When you use `agent { docker ... }`, Jenkins doesn't copy your code into the container. 
1. It starts the container.
2. It **Bind Mounts** the Jenkins workspace folder (`/var/jenkins_home/workspace/...`) into the container.
3. Any files your build creates are actually written to the host's disk.

### User Mapping Issues
Jenkins inside a container often runs as user `jenkins` (UID 1000). If the container image uses a different UID, you might get **Permission Denied** when the container tries to write to the workspace.
**Fix**: Jenkins automatically tries to run the container with your current UID/GID using `--user`.

⚫ **Staff-Level Insights**
-----------------------------------
### Ephemeral Jenkins Agents
Don't run one giant Jenkins server.
**Staff Strategy**: Use the **Jenkins Docker Plugin**. 
- Jenkins stays idle. 
- When a build starts, Jenkins asks Docker to start a "Jenkins Agent" container. 
- The agent does the work and then **self-destructs**. 
- This saves massive amounts of money and ensures no "dirty" files are left between builds.

### Caching in CI
Docker builds in Jenkins are slow because the cache is lost every time.
**Staff Tip**: Use **`docker build --cache-from`** to pull the previous version of the image and use its layers as a cache for the new build.

🏗️ **Mental Model**
Jenkins is the **Director**, and Docker containers are the **Actors** who perform on stage and then leave.

⚡ **Actual Behavior**
Jenkins uses the `docker` CLI command internally. You must have Docker installed on the Jenkins agent machine for this to work.

🧠 **Resource Behavior**
- **Disk Space**: Jenkins build servers often crash because they accumulate hundreds of "Dangling" images and old containers. 
- **Staff Fix**: Run a cron job with `docker system prune -af --volumes` every night.

💥 **Production Failures**
- **Docker Socket Permission Denied**: The `jenkins` user doesn't have permission to talk to `/var/run/docker.sock`. 
  - **Fix**: `sudo usermod -aG docker jenkins` and restart Jenkins.
- **Out of Disk Space**: A build fails halfway, leaving a 2GB "In-progress" layer on the disk.

🏢 **Best Practices**
- Always use specific image tags (not `latest`).
- Use multi-stage builds to keep the final production image small.
- Clean up after yourself using `docker.image(...).inside { ... }` which automatically stops the container.

🧪 **Debugging**
```bash
# Check if the Jenkins user can run docker manually
sudo -u jenkins docker ps

# Inspect the logs of the Jenkins agent container
docker logs <agent_container_id>
```

💼 **Interview Q&A**
- **Q**: What is the advantage of using Docker in a Jenkins pipeline?
- **A**: It ensures the build environment is identical every time, regardless of what is installed on the Jenkins host.
- **Q**: How does a containerized Jenkins build another Docker image?
- **A**: By mounting the host's Docker socket (`/var/run/docker.sock`) into the Jenkins container.

---
Prev: [../Security/32_Capabilities_Seccomp_and_AppArmor.md](../Security/32_Capabilities_Seccomp_and_AppArmor.md) | Index: [00_Index.md](../00_Index.md) | Next: [34_Logging_Drivers_and_Aggregation.md](34_Logging_Drivers_and_Aggregation.md)
---
