# 🛡️ Disaster Recovery & High Availability

## 📌 Topic Name
Jenkins HA: The Singleton Bottleneck and Active/Passive Architectures

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Making sure that if the Jenkins server crashes, another one takes over immediately so developers can keep working.
*   **Expert**: Standard Jenkins OSS does NOT support Active/Active High Availability. The architecture relies on the Controller JVM holding the state of all running builds in heap memory, and locking the filesystem (`$JENKINS_HOME`). If you run two Jenkins Controllers pointing at the same `$JENKINS_HOME`, they will corrupt the XML files and crash. A Staff engineer designs an **Active/Passive (Cold Standby)** architecture using cloud-native primitives (Auto Scaling Groups, EFS/NFS, Route53) or relies on **CloudBees CI** for true Active/Active HA.

## 🏗️ Mental Model
Think of Jenkins like a **Head Chef in a Kitchen**.
- **Active/Active (Impossible)**: You put two Head Chefs in the kitchen. They both try to read the same recipe book (Filesystem), they both shout orders to the same cooks (Agents). Chaos ensues. The food is ruined (Data Corruption).
- **Active/Passive (Standard)**: One Head Chef is working. A backup Head Chef is asleep in the office. If the working chef has a heart attack, the backup chef wakes up, walks in, reads where the recipe was left off, and continues. (Takes a few minutes).

## ⚡ Actual Behavior
- **The Filesystem Lock**: When Jenkins starts, it checks for a `.owner` or lock file in `$JENKINS_HOME`. If it exists, it knows another Controller is running and will refuse to start to prevent corruption.
- **Failover Latency**: In an Active/Passive setup, if the Active node dies, the Passive node must boot the JVM, parse all 10,000 XML files from the network disk (NFS/EFS), and re-establish connections to all Agents. This failover process can take 5 to 15 minutes.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Shared Storage (EFS)**: The key to Active/Passive is a shared network filesystem. The AWS Auto Scaling Group runs 1 EC2 instance. It mounts the EFS drive. If the EC2 instance dies, the ASG spins up a new one, mounts the exact same EFS drive, and starts Jenkins.
2.  **DNS Failover**: A Load Balancer (ALB) sits in front. When the new instance passes the HTTP health check (`/login`), the ALB routes traffic to it. Users experience a 5-minute outage but lose no data.
3.  **Remoting Reconnection**: When the new Controller boots, the Jenkins Agents notice the TCP connection dropped. They attempt to reconnect to the ALB. Once the new Controller is up, they connect, and the CPS engine resumes pipelines from the last `program.dat` save state.

## 🔁 Execution Flow (Auto Scaling Group Failover)
1.  **Healthy State**: ASG has Desired=1, Max=1. Instance A is running. Mounts EFS to `/var/jenkins_home`.
2.  **Failure**: Underlying AWS hardware fails. Instance A terminates.
3.  **Detection**: ASG health check fails. ASG provisions Instance B.
4.  **Boot**: Instance B runs UserData script: mounts EFS to `/var/jenkins_home`.
5.  **Start Application**: Jenkins service starts on Instance B. Parses XML from EFS.
6.  **Recovery**: ALB health checks pass. DNS resolves. Agents reconnect.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **EFS IOPS Bottleneck**: NFS/EFS has significantly higher latency than local NVMe SSDs. Parsing thousands of XML files over NFS during boot can make the failover time painfully slow.
- **Boot CPU Spike**: When Jenkins boots, it parses every single job configuration into heap memory. This maxes out the CPU for several minutes.

## 📐 ASCII Diagrams (MANDATORY)
```text
           [ ROUTE 53 / DNS ]
                   |
           [ LOAD BALANCER ]  <--- (Health Checks)
                   |
     +-------------+-------------+
     |                           |
[ EC2: ACTIVE ]             [ EC2: DEAD ] 
(Desired: 1)                (Auto Scaling Group replaces this)
     |                           X
     +-------------+-------------+
                   |
           (Network Mount)
                   v
       [ AMAZON EFS (Shared NFS) ]
       (Contains /var/jenkins_home)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# Kubernetes Active/Passive Strategy
# Using a Deployment with Replicas=1 and a ReadWriteOnce (RWO) PVC
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins-controller
spec:
  replicas: 1 # MUST BE 1. Never higher.
  strategy:
    type: Recreate # MUST BE Recreate. Kills old pod before starting new one.
  template:
    spec:
      containers:
      - name: jenkins
        image: jenkins/jenkins:lts
        volumeMounts:
        - name: jenkins-home
          mountPath: /var/jenkins_home
      volumes:
      - name: jenkins-home
        persistentVolumeClaim:
          claimName: jenkins-pvc # RWO EBS volume
```

## 💥 Production Failures
1.  **The Split-Brain Corruption**: An admin accidentally sets the ASG `Max=2`. A network partition occurs. AWS spins up a second Jenkins Controller. Both Controllers mount the EFS drive and write to `config.xml` simultaneously. The entire Jenkins configuration is irreparably corrupted.
2.  **The EFS Burst Credit Exhaustion**: Jenkins does massive I/O on EFS. EFS uses a burst credit system. Jenkins exhausts the credits, and EFS throughput drops to 1 MB/s. The UI freezes, and failover takes 45 minutes because parsing XML at 1 MB/s is agonizing.
3.  **Session Loss**: After failover, all users are logged out and must re-authenticate because the Jetty HTTP session state is kept in RAM, not on the shared disk.

## 🧪 Real-time Q&A
*   **Q**: Does CloudBees CI fix this?
*   **A**: Yes. CloudBees CI (Enterprise) offers High Availability. It uses a database to manage locks and allows multiple Controllers to run in an Active/Active cluster, providing zero-downtime failover.
*   **Q**: What happens to running jobs during failover?
*   **A**: If it's a Pipeline job, it will pause. When the new Controller boots, it reads the `program.dat` and resumes the pipeline (assuming the Agent is still alive). If it's a Freestyle job, it is completely lost and marked as failed.

## ⚠️ Edge Cases
*   **NFS File Locks**: Sometimes when an EC2 instance dies violently, the NFS server (EFS) does not release the file locks. When the new EC2 instance boots and tries to mount the filesystem, it hangs indefinitely waiting for the lock to release.

## 🏢 Best Practices
1.  **Strictly Active/Passive**: Never attempt to run two Jenkins OSS processes pointing at the same home directory.
2.  **Use Provisioned IOPS**: If using EFS or NFS, ensure you configure provisioned IOPS to handle the massive burst of read operations required when Jenkins boots.
3.  **K8s StatefulSet**: In Kubernetes, deploy Jenkins as a `StatefulSet` or a `Deployment` with `strategy: Recreate` to absolutely guarantee two pods cannot run simultaneously.

## ⚖️ Trade-offs
*   **Cost vs Uptime**: An Active/Passive cloud architecture guarantees recovery from hardware failure within 5-10 minutes, which is acceptable for most CI/CD workloads. Paying $100,000+ for Enterprise Active/Active clustering is usually only justified for extreme, zero-downtime requirements (e.g., algorithmic trading).

## 💼 Interview Q&A
*   **Q**: Your manager asks you to deploy Jenkins behind a Load Balancer and spin up 3 instances of the Jenkins Controller to handle high traffic. Why is this a terrible idea, and what is the correct alternative?
*   **A**: Jenkins OSS is a stateful monolith designed as a Singleton. It holds pipeline state in the JVM Heap and relies on locking XML files on the disk. If 3 instances run behind a Load Balancer, they will fight over file locks and corrupt the `$JENKINS_HOME` directory, causing catastrophic failure. To handle high traffic, we scale *vertically* (larger Controller instance) and offload all build execution to *distributed agents*. For high availability, we use an **Active/Passive** setup (ASG of 1) with shared storage, ensuring only one Controller is ever active.

## 🧩 Practice Problems
1.  Review the AWS EFS documentation regarding "Bursting Throughput" vs "Provisioned Throughput". Calculate what happens to a Jenkins instance if it exhausts its burst credits.
2.  Inspect the Kubernetes YAML for the official Jenkins Helm Chart. Look at how it configures the `Deployment` strategy to ensure only one pod runs at a time.
