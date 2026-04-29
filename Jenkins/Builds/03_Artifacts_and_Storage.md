# 🔨 Artifacts and Storage

## 📌 Topic Name
Artifact Management: Jenkins Storage vs External Repositories

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Saving the final `.jar` or `.zip` file so you can download it later.
*   **Expert**: Artifact generation is the primary output of CI. Jenkins has a native `archiveArtifacts` step, which transmits files from the Agent's workspace to the Controller's local filesystem (`$JENKINS_HOME/jobs/.../builds/.../archive`). A Staff engineer understands that **Jenkins is not a Binary Repository Manager**. Using Jenkins to store gigabytes of Docker images, RPMs, or fat JARs will rapidly saturate the Controller's disk I/O, network interface, and storage capacity. Architecture must mandate offloading immutable artifacts to dedicated systems like **Nexus, Artifactory, or Amazon S3**.

## 🏗️ Mental Model
Think of Jenkins as a **Factory Assembly Line**.
- **The Assembly Line (Jenkins)**: Great at putting parts together to build a car.
- **The Native Archive (Jenkins Disk)**: Parking the finished cars in the factory's own tiny employee parking lot. It fills up instantly, and traffic jams stop the factory.
- **The External Repository (Artifactory/S3)**: A massive, dedicated shipping warehouse. As soon as the car is built, you put it on a truck and send it to the warehouse.

## ⚡ Actual Behavior
- **Remoting Transfer**: When you call `archiveArtifacts`, the Agent zips the files, sends them over the TCP Remoting channel to the Controller, and the Controller unzips them to its disk. This consumes network bandwidth and Controller CPU.
- **Build Discarder Linkage**: Native Jenkins artifacts are tied to the lifecycle of the Build. If your "Build Discarder" deletes Build #10 after 7 days, the artifacts for Build #10 are deleted permanently.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Stash vs Archive**:
    - `stash`: Temporary storage meant to move files between stages in the *same* pipeline run. Deleted when the pipeline ends.
    - `archiveArtifacts`: Permanent storage (until build deletion) meant for end-users to download from the UI.
2.  **Fingerprinting**: Jenkins calculates an MD5 checksum for archived files. This allows Jenkins to track which specific build produced a `.jar`, and which downstream jobs consumed that exact `.jar` (providing basic traceability).
3.  **External Plugins**: Tools like the `S3 Publisher` or `Artifactory Plugin` bypass the Controller. The Agent streams the binary directly from its workspace to the external server via HTTPS.

## 🔁 Execution Flow (External Offloading)
1.  **Compile**: Agent compiles `app-v1.2.jar`.
2.  **Test**: Tests pass.
3.  **Publish Step**: Pipeline hits `sh 'curl -T app-v1.2.jar https://nexus.corp.com/repo/'`.
4.  **Direct Transfer**: Agent streams bytes directly to Nexus (Controller is bypassed).
5.  **Metadata**: (Optional) Pipeline sends the Nexus URL to the Controller to be saved as a string/link in the build logs.
6.  **Teardown**: Workspace is cleaned.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Controller Disk Saturation**: Storing 1GB artifacts for 100 builds = 100GB. Multiplied by 50 jobs = 5TB of expensive, high-IOPS block storage wasted on cold binaries.
- **Backup Bloat**: If artifacts are stored in `$JENKINS_HOME`, your nightly backup system will take hours and cost a fortune to back up immutable binaries that shouldn't be backed up alongside state.

## 📐 ASCII Diagrams (MANDATORY)
```text
❌ BAD: NATIVE ARCHIVING (Controller Bottleneck) ❌
[ AGENT ] --(Remoting: 5GB file)--> [ JENKINS CONTROLLER ]
                                         |
                                   [ LOCAL DISK ] (Fills up rapidly)

✅ GOOD: EXTERNAL REPOSITORY (Bypasses Controller) ✅
                                   [ JENKINS CONTROLLER ] (Only tracks status)
                                         ^
                                         | (Metadata/Success)
[ AGENT ] --(HTTPS: 5GB file)------------+
    |
    v
[ S3 / ARTIFACTORY / NEXUS ] (Infinite, cheap storage)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make dist' // Creates dist/app.tar.gz
            }
        }
    }
    post {
        success {
            // BAD (For large files): Stores on Jenkins Master
            // archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            
            // GOOD: Upload directly to S3 from the Agent
            withAWS(credentials: 'aws-upload-creds', region: 'us-east-1') {
                s3Upload(
                    file: 'dist/app.tar.gz', 
                    bucket: 'my-company-artifacts', 
                    path: "releases/${env.BUILD_NUMBER}/app.tar.gz"
                )
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Master Out of Space (No Space Left on Device)**: A team starts building Docker images using `docker save` and archives the 2GB `.tar` files using `archiveArtifacts`. The Controller disk fills up in 4 hours. Jenkins stops processing the queue, drops all agent connections, and the UI returns HTTP 500.
2.  **Stash Memory Crash**: A developer confuses `stash` with `archive`. They `stash` a 1GB database dump. The Controller tries to hold the stash in the JVM heap. The Controller crashes with `OutOfMemoryError`.
3.  **Lost Releases**: A company uses Jenkins native archiving for their production binaries. A junior admin configures the Build Discarder to keep only 5 builds to save disk space. The production release (Build #4) is pushed out of history by 5 subsequent failed builds. The production binary is permanently deleted.

## 🧪 Real-time Q&A
*   **Q**: When is it okay to use Jenkins native `archiveArtifacts`?
*   **A**: Only for small, diagnostic text files (e.g., test reports, coverage XMLs, tiny log files) that are under a few megabytes and are only relevant for debugging that specific build.
*   **Q**: How do I pass a compiled binary to a downstream job?
*   **A**: Have Job A push it to Artifactory/S3. Pass the URL/URI of the artifact as a String Parameter to Job B. Job B downloads it directly from Artifactory/S3.

## ⚠️ Edge Cases
*   **Jenkins as an RPM repo**: There are plugins to make Jenkins act like a Yum/RPM repository. *Do not use them in production.* They heavily abuse the Controller's web server.

## 🏢 Best Practices
1.  **Immutability Rule**: Jenkins is for compute; Artifactory/Nexus/S3 are for storage.
2.  **Semantic Versioning**: Never overwrite artifacts in the external repository. Always append the Build Number or Git SHA (e.g., `app-1.0.${BUILD_NUMBER}.jar`).
3.  **Artifact Retention**: Configure retention policies on the *external* repository (e.g., S3 Lifecycle policies to move old dev builds to Glacier), completely decoupled from Jenkins.

## ⚖️ Trade-offs
*   **Native Archiving**: Zero setup, just one line of code, visible directly in the Jenkins UI. But terrible for performance and scaling.
*   **External Repos**: Requires managing a second piece of infrastructure (Nexus/S3) and managing credentials, but offers infinite scaling and decoupling.

## 💼 Interview Q&A
*   **Q**: Your Jenkins server is experiencing massive network latency spikes, causing agents to disconnect randomly. Monitoring shows the Controller's network interface is maxed out at 1Gbps, and the disk write queue is extremely high. What is the most likely architectural flaw?
*   **A**: The teams are likely using the native `archiveArtifacts` (or `stash`) step for massive binaries (like Docker images or compiled games). This forces the agents to funnel gigabytes of data through the Jenkins Remoting TCP channel directly to the Controller's local disk. I would fix this by auditing the Jenkinsfiles and migrating all binary uploads to stream directly from the Agents to an external storage service like Amazon S3, bypassing the Controller entirely.

## 🧩 Practice Problems
1.  Use `archiveArtifacts` on a 10MB file. Navigate to `$JENKINS_HOME/jobs/<job>/builds/<build>/archive/` on the Controller filesystem to see where it was physically stored.
2.  Write a script using `sh` and `curl` to upload a file directly to a remote server (or an S3 bucket via AWS CLI) instead of using Jenkins native archiving.
