# 🔨 Caching Strategies

## 📌 Topic Name
Build Caching: Accelerating Pipelines with Persistent State

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Keeping downloaded files (like Node modules) so the next build doesn't have to download them again.
*   **Expert**: In a modern CI environment utilizing **Ephemeral Agents** (Kubernetes), you lose the natural filesystem caching of static VMs. Every pod starts as a blank slate. Downloading 1GB of NPM packages or Maven dependencies for every PR drastically increases network ingress costs and build times. A Staff engineer implements **Distributed Caching Strategies**—using sidecar containers, persistent volume claims (PVCs), or S3-backed tarballs—to inject state into stateless runners without causing dependency pollution or "dirty workspace" race conditions.

## 🏗️ Mental Model
Think of Caching like a **Chef's Spice Rack**.
- **No Cache (Ephemeral)**: The chef goes to the supermarket to buy salt, pepper, and flour for every single meal they cook. (Slow, expensive).
- **Persistent Cache (Static VM)**: The chef keeps a massive spice rack. (Fast, but occasionally a spice goes bad and ruins the dish).
- **Managed Cache (S3 Tarballs/PVC)**: The chef gets a sealed, pre-measured spice box delivered instantly at the start of the meal, and throws away the leftovers.

## ⚡ Actual Behavior
- **Dependency Resolution**: Tools like Maven (`~/.m2`), NPM (`~/.npm`), and Go (`~/go/pkg`) by default download dependencies to the *user's home directory*, not the workspace. If you don't map these directories to a cache, they are wiped when the ephemeral agent dies.
- **Cache Invalidation**: The hardest part of caching is knowing when to discard it. If `package.json` doesn't change, the cache is valid. If it changes, the cache must be rebuilt.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Tarball Hashing**: A common strategy is to hash the dependency file (e.g., `md5sum package-lock.json`). The hash becomes the cache key (e.g., `cache-npm-a1b2c3d4.tar.gz`). If S3 has this file, download and extract it. If not, run `npm install`, then zip the `node_modules` and upload to S3 using that hash.
2.  **Docker Layer Caching**: If using `docker build` inside Jenkins, you must pass `--cache-from` and pull the previous image layer, otherwise Docker will rebuild from `RUN apt-get update` every time on a fresh agent.
3.  **Kubernetes PVCs**: Attaching a ReadWriteMany (RWX) Persistent Volume to your Jenkins pods to act as a shared `~/.m2` directory.

## 🔁 Execution Flow (S3-backed Tarball Cache)
1.  **Hashing**: Agent runs `md5sum pom.xml` -> `hash: 8f9b`.
2.  **Lookup**: Agent checks S3 for `s3://bucket/maven-cache-8f9b.tgz`.
3.  **Hit**: If found, downloads and runs `tar -xzf`. (Takes 5 seconds).
4.  **Miss**: If not found, S3 returns 404.
5.  **Execution**: Agent runs `mvn clean install`. (Takes 5 minutes to download internet).
6.  **Upload**: If Miss occurred, Agent runs `tar -czf` on `~/.m2` and uploads to S3 with key `8f9b`.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **CPU for Compression**: Tar-zipping a massive 2GB `node_modules` folder uses significant CPU and time. If creating the cache takes longer than simply re-downloading from NPM, the cache is a net-negative.
- **Network Bandwidth**: Pulling from a local S3 bucket in the same AWS Region is massively faster and cheaper than pulling from public registries (DockerHub, NPM) over the NAT Gateway.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS K8S POD ]
       |
       | 1. Hash `package.json` -> "Hash123"
       |
       | 2. Check Cache
+------v------------------+
|   S3 BUCKET (Cache)     |
|   - npm-Hash123.tar.gz  | <--- CACHE HIT!
+-------------------------+
       |
       | 3. Download & Extract (5 Seconds)
       |
       | 4. Run `npm build` (Uses local files)
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
              containers:
              - name: node
                image: node:16
                command: ['cat']
                tty: true
            '''
        }
    }
    stages {
        stage('Restore Cache') {
            steps {
                container('node') {
                    script {
                        def hash = sh(script: "md5sum package-lock.json | awk '{print \$1}'", returnStdout: true).trim()
                        env.CACHE_KEY = "npm-cache-${hash}.tar.gz"
                        
                        // Pseudo-code: Check if exists, download and extract
                        def cacheExists = sh(script: "aws s3api head-object --bucket my-cache --key ${env.CACHE_KEY}", returnStatus: true) == 0
                        if (cacheExists) {
                            sh "aws s3 cp s3://my-cache/${env.CACHE_KEY} . && tar -xzf ${env.CACHE_KEY}"
                        }
                    }
                }
            }
        }
        stage('Build') {
            steps {
                container('node') {
                    sh 'npm ci' // Will be instant if cache hit
                }
            }
        }
        stage('Save Cache') {
            steps {
                container('node') {
                    script {
                        // Only upload if we didn't hit the cache earlier
                        sh "tar -czf ${env.CACHE_KEY} node_modules/"
                        sh "aws s3 cp ${env.CACHE_KEY} s3://my-cache/${env.CACHE_KEY}"
                    }
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Corrupted Cache Poisoning**: A build fails halfway through downloading Maven dependencies, leaving a half-written `.jar` in the local `~/.m2`. The cache upload step still runs and zips this corrupted state. Every subsequent build downloads this poisoned cache and fails with `ZipException`. **Solution**: Only upload cache if the build stage succeeds perfectly.
2.  **Disk Exhaustion via Shared PVC**: An organization uses a shared Kubernetes PVC for the `.m2` directory across all pods. It grows infinitely. After 6 months, it hits 500GB, fills up, and halts all Java builds company-wide. **Solution**: Implement aggressive cache eviction/garbage collection policies.
3.  **Compression Overhead**: Zipping `node_modules` (which contains 100,000 tiny files) takes 3 minutes. The cache upload takes 1 minute. The actual `npm install` over the network would have only taken 2 minutes. The cache made the build *slower*.

## 🧪 Real-time Q&A
*   **Q**: Can I use a Jenkins plugin for caching?
*   **A**: Yes, plugins like "Job Cacher" exist and abstract away the S3 tarball logic. However, relying on OS-level bash scripts (`tar`, `aws s3`) is often faster, more transparent, and easier to debug.
*   **Q**: How do I cache Docker layers in a Kubernetes Agent (Kaniko/DinD)?
*   **A**: If using Docker-in-Docker, you must use `--cache-from`. If using Kaniko (best practice for K8s), use the `--cache=true` and `--cache-repo=my-registry/cache` flags to push/pull layers directly to a remote registry.

## ⚠️ Edge Cases
*   **Cross-OS Caching**: Never restore a cache generated on a Linux agent onto a Windows agent. Native bindings (like `node-sass`) compiled for Linux will crash immediately on Windows.

## 🏢 Best Practices
1.  **Cache Keys by Hash**: Always key your cache to the hash of the dependency lockfile (`package-lock.json`, `pom.xml`, `go.sum`).
2.  **Fallback Caches**: If the exact hash misses, try to download the cache from the `main` branch as a fallback. `npm ci` will quickly update the minor differences.
3.  **Local Mirrors**: Instead of complex tarballs, sometimes the best cache is simply running an Artifactory/Nexus caching proxy mirror inside your VPC.

## ⚖️ Trade-offs
*   **Tarballs vs Shared PVCs**:
    *   *Tarballs (S3)*: Safe, isolated, impossible to get concurrent write corruption. Slower to extract.
    *   *Shared PVC (EFS)*: Instant access, no extraction needed. High risk of concurrent build corruption and requires complex file-locking mechanisms.

## 💼 Interview Q&A
*   **Q**: You transitioned your Jenkins agents from static EC2 instances to ephemeral Kubernetes pods. Build times went from 2 minutes to 15 minutes. The developers are angry. What happened and how do you fix it?
*   **A**: The ephemeral pods start with empty filesystems, destroying the local caching of dependencies (like `~/.m2` or `node_modules`) that the static EC2 instances naturally accumulated. The build is spending 13 minutes downloading the internet. To fix this, I would implement an S3-based caching mechanism keyed to the hash of the dependency lockfile, injecting the dependencies into the pod before the build step runs.

## 🧩 Practice Problems
1.  Write a bash script that creates an MD5 hash of a `package.json` file.
2.  Configure a pipeline to use a `Jenkins Pipeline Cache` plugin or a custom S3 bash script to cache a specific folder between runs. Check the S3 bucket to verify the object exists.
