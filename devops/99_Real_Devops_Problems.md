# 🛠️ Real-World DevOps Problems: Common & Rare (Remediation & Prevention Guide)

> **File:** `99_Real_Devops_Problems.md`
> **Topic:** Common and Rare Production Incidents, Troubleshooting Playbook, Root Cause Analyses
> **Level:** 🔴 Advanced / Production Grade

---

## 📚 Table of Contents

1. [Common Infrastructure & Deployment Problems](#1-common-infrastructure--deployment-problems)
   - [Kubernetes: OOMKilled (Exit Code 137)](#kubernetes-oomkilled-exit-code-137)
   - [Docker: Disk Space & Inode Exhaustion](#docker-disk-space--inode-exhaustion)
   - [AWS: Connection Timeout to Private Database (RDS)](#aws-connection-timeout-to-private-database-rds)
   - [Jenkins: Indefinite Pipeline Hanging (Foreground Execution)](#jenkins-indefinite-pipeline-hanging-foreground-execution)
   - [Terraform: State Lock Acquisition Failures](#terraform-state-lock-acquisition-failures)
2. [Rare & Complex Production Incidents](#2-rare--complex-production-incidents)
   - [Kubernetes: Subnet CIDR IP Exhaustion](#kubernetes-subnet-cidr-ip-exhaustion)
   - [Linux: File Descriptor & Socket Exhaustion (Too many open files)](#linux-file-descriptor--socket-exhaustion-too-many-open-files)
   - [Docker: DNS Resolver Loops & Alpine Compatibility Issues](#docker-dns-resolver-loops--alpine-compatibility-issues)
   - [AWS: AWS KMS Key Rate Limiting (API Throttling)](#aws-aws-kms-key-rate-limiting-api-throttling)
   - [MLOps: Concept Drift & Model Performance Degradation](#mlops-concept-drift--model-performance-degradation)
3. [Quick-Reference Diagnostic Cheatsheet](#3-quick-reference-diagnostic-cheatsheet)

---

## 1. Common Infrastructure & Deployment Problems

### Kubernetes: OOMKilled (Exit Code 137)
* **Severity:** 🔴 Critical / High
* **Frequency:** 🔄 Very Common

#### 📖 Description & Symptoms
A pod running successfully suddenly terminates. When running `kubectl get pods`, the status shows `OOMKilled` or `Error`. Inspecting the pod events (`kubectl describe pod <pod-name>`) reveals:
```text
Last State:     Terminated
  Reason:       OOMKilled
  Exit Code:    137
```

#### 🤔 Root Cause Analysis
The application container consumed more RAM than the memory **limit** defined in the Kubernetes pod deployment manifest. The Linux kernel's Out-Of-Memory (OOM) killer stepped in and sent a `SIGKILL` (signal 9, hence exit code $128 + 9 = 137$) to immediately terminate the process to protect the host node from running out of system memory.

#### ⚙️ Solution & Remediation
1. **Check which container crashed:**
   ```bash
   kubectl describe pod <pod_name> | grep -A 5 "Last State"
   ```
2. **Fetch logs before the crash:**
   ```bash
   kubectl logs <pod_name> --previous
   ```
3. **Verify resource allocations in manifest:**
   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "100m"
     limits:
       memory: "512Mi"  # <- If app needs 600Mi, it gets killed here
       cpu: "500m"
   ```
4. **Temporary fix:** Patch the deployment to increase memory limit:
   ```bash
   kubectl set resources deployment/<deployment_name> --limits=memory=1Gi --requests=memory=512Mi
   ```

#### 🔒 Prevention Strategy
* Use a Java/Node profiler to check for memory leaks in the code.
* Implement Vertical Pod Autoscaler (VPA) in recommendation mode to analyze real-world memory utilization.
* Set up Prometheus rules to alert when container memory usage exceeds 85% of its limit.

---

### Docker: Disk Space & Inode Exhaustion
* **Severity:** 🔴 Critical
* **Frequency:** 🔄 Very Common

#### 📖 Description & Symptoms
Deployments fail on a virtual machine. Commands like `docker run` or `docker build` throw:
```text
Error response from daemon: write /var/lib/docker/...: no space left on device
```
*Note: In some rare cases, running `df -h` shows 40% free space, yet the system still reports "no space left"!*

#### 🤔 Root Cause Analysis
1. **Standard Block Exhaustion:** Unused build cache, dangling image layers, stopped containers, and container logs filled up `/var/lib/docker`.
2. **Inode Exhaustion:** Applications (especially Node.js or session caching systems) created millions of tiny files. The file system ran out of **Inodes** (index pointers), preventing new file creation even though raw gigabyte space was available.

#### ⚙️ Solution & Remediation
1. **Check disk space vs. inodes:**
   ```bash
   df -h  # Checks storage block usage
   df -i  # Checks inode count percentage
   ```
2. **Identify large files/directories:**
   ```bash
   sudo du -sh /var/lib/docker/* | sort -h
   ```
3. **Run aggressive Docker cleanup:**
   ```bash
   # Prune all stopped containers, dangling images, and build caches
   docker system prune -a --volumes -f
   ```
4. **Delete orphaned Docker volume folders (if necessary):**
   ```bash
   docker volume prune -f
   ```

#### 🔒 Prevention Strategy
* Implement **Docker log rotation** by default in `/etc/docker/daemon.json`:
  ```json
  {
    "log-driver": "json-file",
    "log-opts": {
      "max-size": "10m",
      "max-file": "3"
    }
  }
  ```
* Include a clean-up step in CI/CD pipelines (`docker system prune -f` at the end of build jobs).
* Set up alerts in Grafana for both `disk_use_percent` and `inode_use_percent`.

---

### AWS: Connection Timeout to Private Database (RDS)
* **Severity:** 🔴 Critical
* **Frequency:** 🔄 Very Common

#### 📖 Description & Symptoms
An application server launched on an EC2 instance fails to connect to the backend MySQL/PostgreSQL RDS instance. Application logs throw:
```text
Connection timed out (Connection failed to host rds.amazonaws.com)
```

#### 🤔 Root Cause Analysis
This is almost always a security network configuration block. Common causes:
1. The RDS security group lacks an **inbound rule** allowing traffic from the EC2 instance's security group or IP range on port 3306 (MySQL) or 5432 (PostgreSQL).
2. The EC2 instance and RDS instance are in different subnets that cannot route to each other, or the database is in a private subnet and the client is attempting to access it from the public internet without a Bastion Host.

#### ⚙️ Solution & Remediation
1. **Test basic network reachability from EC2:**
   ```bash
   nc -zv -w3 <rds-endpoint> 3306
   # If it hangs and says "timeout", it is blocked by firewall/security group
   ```
2. **Peering Security Groups (Best Practice):**
   - Go to RDS Dashboard → Databases → Select database → Connectivity & security.
   - Click the Security Group link.
   - Add an **Inbound Rule**:
     - **Type:** MySQL/Aurora (or PostgreSQL)
     - **Protocol:** TCP
     - **Port Range:** 3306 (or 5432)
     - **Source:** Select the *EC2 instance's Security Group ID* (e.g., `sg-0abc123def456`) instead of wide open `0.0.0.0/0`.
3. **Save Rules** and re-test with `nc`.

#### 🔒 Prevention Strategy
* Use Infrastructure as Code (Terraform) to automatically declare and link security group rules.
* Restrict databases to strictly private subnets and configure an AWS SSM Session Manager Bastion Host for manual administration.

---

### Jenkins: Indefinite Pipeline Hanging (Foreground Execution)
* **Severity:** 🟡 High
* **Frequency:** 🔄 Common

#### 📖 Description & Symptoms
A Jenkins pipeline build runs indefinitely. The console logs stop at the application startup command (e.g., `npm start` or `java -jar app.jar`), and the build never completes.

#### 🤔 Root Cause Analysis
The pipeline script executed a service daemon or persistent background server command in the **foreground**. Jenkins runs shell execution steps synchronously. Since the server runs forever waiting for requests, the shell script never exits with status 0, causing Jenkins to wait indefinitely.

#### ⚙️ Solution & Remediation
1. **Terminate the hanging build:** Click the Red `X` button in the Jenkins UI.
2. **Migrate the foreground task to run in the background:** Use `nohup` (No Hang Up) and redirect outputs.
   ```groovy
   // BAD:
   sh "java -jar target/app.jar"
   
   // GOOD:
   sh "nohup java -jar target/app.jar > app.log 2>&1 &"
   ```
3. **If using systemd (best practice):** Define a service file, start it, and let the systemd daemon manage the background runtime.
   ```bash
   sudo systemctl restart my-java-app.service
   ```

#### 🔒 Prevention Strategy
* Containerize all running services using Docker. Starting a container with `docker run -d` automatically runs in detached mode and returns execution immediately.
* Configure build timeout settings inside the Jenkinsfile:
  ```groovy
  options {
      timeout(time: 15, unit: 'MINUTES') 
  }
  ```

---

### Terraform: State Lock Acquisition Failures
* **Severity:** 🟡 High
* **Frequency:** 🔄 Common

#### 📖 Description & Symptoms
Running `terraform plan` or `terraform apply` fails immediately with:
```text
Error: Error acquiring the state lock
Error info: Lock Info:
  ID:        a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d
  Path:      my-bucket/terraform.tfstate
  Operation: OperationTypeApply
  Who:       user@workstation
  Created:   2026-07-13 06:00:00 UTC
```

#### 🤔 Root Cause Analysis
Terraform uses locking (e.g., via AWS DynamoDB or local file locks) to prevent concurrent executions from writing to the state file simultaneously (which corrupts the state). If a previous run crashed, was forcefully aborted (`Ctrl+C`), or network connectivity dropped mid-execution, the lock record was never cleared.

#### ⚙️ Solution & Remediation
1. **Ensure no other engineer is running Terraform:** Check with the team to make sure no active apply is running.
2. **Unlock the state using the Lock ID:**
   ```bash
   terraform force-unlock a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d
   ```
3. Run `terraform plan` to verify the lock is cleared.

#### 🔒 Prevention Strategy
* Execute all Terraform changes via CI/CD pipelines (e.g., GitHub Actions, GitLab CI) with strict concurrency locking enabled (`concurrency: production-deploy`).
* Avoid using `kill -9` on a running Terraform terminal; wait for it to clean up hooks.

---

## 2. Rare & Complex Production Incidents

### Kubernetes: Subnet CIDR IP Exhaustion
* **Severity:** 🔴 Critical
* **Frequency:** ❄️ Rare

#### 📖 Description & Symptoms
Pods are stuck in `Pending` state. Running `kubectl describe pod <pod-name>` yields:
```text
Events:
  Type     Reason            From               Message
  ----     ------            ----               -------
  Warning  FailedScheduling  default-scheduler  0/10 nodes are available: 10 Insufficient IP addresses.
```
*Note: Node CPU and RAM are under 30% utilization.*

#### 🤔 Root Cause Analysis
The Kubernetes cluster is running inside a VPC subnet with a very small CIDR block (e.g., `/26` or `/28`). Every worker node and every single pod deployed requires its own unique IP address from the subnet pool (especially when using AWS VPC CNI). The scale-out policy (HPA) spun up too many pods, exhausting all available IP addresses in the private subnet range.

#### ⚙️ Solution & Remediation
1. **Confirm IP availability in AWS/GCP subnets:** Check cloud portal VPC dashboards.
2. **Emergency Mitigation:** Scale down low-priority workloads:
   ```bash
   kubectl scale deployment/dev-app --replicas=0
   ```
3. **Long-Term Root Cause Resolution:**
   - Define a new, larger subnet in the VPC (e.g., `/20` or `/22`).
   - Create a new node pool pointing to the new subnet.
   - Drain and delete nodes in the old exhausted subnet:
     ```bash
     kubectl drain <old-node-name> --ignore-daemonsets --delete-emptydir-data
     ```

#### 🔒 Prevention Strategy
* Allocate large IP blocks for Kubernetes clusters from the outset (e.g., `/22` subnets).
* Configure CNI plugins to reuse IPs or use overlay networks (like Calico or Cilium) which assign pod IPs from an internal range rather than the physical VPC range.

---

### Linux: File Descriptor & Socket Exhaustion (Too many open files)
* **Severity:** 🔴 Critical
* **Frequency:** ❄️ Rare

#### 📖 Description & Symptoms
The application server stops responding to HTTP requests. System logs (`/var/log/syslog` or `/var/log/nginx/error.log`) throw:
```text
socket() failed (24: Too many open files)
```
Or:
```text
java.io.IOException: Too many open files
```

#### 🤔 Root Cause Analysis
In Linux, "Everything is a file" (files, sockets, pipes). The operating system enforces a default hard and soft limit on the number of open files/connections a single process can hold (often 1024 by default). A high-traffic application or an application with file/socket leaks exceeded this limit, blocking the kernel from opening new network ports or file threads.

#### ⚙️ Solution & Remediation
1. **Check limits of a running process:**
   ```bash
   cat /proc/<PID>/limits | grep "Max open files"
   ```
2. **Find which process has the most open files:**
   ```bash
   lsof -n | awk '{print $1, $2}' | sort | uniq -c | sort -nr | head -n 10
   ```
3. **Temporary increase limits for current session:**
   ```bash
   ulimit -n 65535
   ```
4. **Permanent Fix:** Edit `/etc/security/limits.conf` and add limits for the service user:
   ```text
   *               soft    nofile          65535
   *               hard    nofile          65535
   ```
5. Restart the server/service.

#### 🔒 Prevention Strategy
* Implement strict resource cleanup patterns in code (`try-with-resources`, socket timeouts, connection pools).
* Enable metrics alerts monitoring `filefd_allocated` in Prometheus Node Exporter.

---

### Docker: DNS Resolver Loops & Alpine Compatibility Issues
* **Severity:** 🟡 High
* **Frequency:** ❄️ Rare

#### 📖 Description & Symptoms
An application container starts successfully, but all outbound API calls fail with `Host resolution failed` or `UnknownHostException`. Other containers on the same host can access the internet fine.

#### 🤔 Root Cause Analysis
1. **DNS Resolver Loop:** Local loopback resolver settings (`127.0.0.53`) from Systemd-resolved on the host VM were copied into the container's `/etc/resolv.conf`. The container doesn't run systemd-resolved, causing lookup loops.
2. **Alpine `musl` vs `glibc`:** Alpine Linux uses `musl libc` instead of the standard GNU C Library (`glibc`). `musl` processes DNS lookups sequentially instead of concurrently and handles search domains differently, causing resolution failures on corporate networks.

#### ⚙️ Solution & Remediation
1. **Inspect resolv.conf inside container:**
   ```bash
   docker exec -it <container_id> cat /etc/resolv.conf
   ```
2. **Explicitly pass external DNS servers during startup:**
   ```bash
   docker run -d --dns=8.8.8.8 --dns=8.8.4.4 my-app
   ```
3. **Fix it globally in `/etc/docker/daemon.json`:**
   ```json
   {
     "dns": ["8.8.8.8", "1.1.1.1"]
   }
   ```
   Restart Docker service: `sudo systemctl restart docker`.

#### 🔒 Prevention Strategy
* If deploying java or node apps in enterprise networks, prefer `debian-slim` base images (like `node:20-slim`) over Alpine base images to ensure full `glibc` networking compatibility.

---

### AWS: AWS KMS Key Rate Limiting (API Throttling)
* **Severity:** 🔴 Critical
* **Frequency:** ❄️ Rare

#### 📖 Description & Symptoms
During autoscaling events or batch job processing, databases and disks fail to attach, and application logs show:
```text
KMS API Limit Exceeded (ThrottlingException: Rate exceeded)
```

#### 🤔 Root Cause Analysis
The account hit the AWS Key Management Service (KMS) requests-per-second limit. By default, KMS has limits (ranging from 10,000 requests/sec in large regions to 2,000 in smaller ones). If an application decrypts database credentials or accesses S3 files using KMS keys for *every single incoming HTTP request* without local caching, the API threshold is quickly crossed.

#### ⚙️ Solution & Remediation
1. **Configure KMS Envelope Encryption with Data Key Caching:** Cache the plaintext data key in application memory to decrypt payloads locally instead of invoking AWS KMS API for every single record.
2. **Increase AWS Quota:** Open an AWS Support ticket requesting a KMS rate-limit increase.
3. **Add Backoff & Retry Logic:** Configure the AWS SDK client to use exponential backoff:
   ```python
   import boto3
   from botocore.config import Config
   
   config = Config(
       retries = {
           'max_attempts': 10,
           'mode': 'adaptive'  # Automatically throttles requests
       }
   )
   client = boto3.client('kms', config=config)
   ```

#### 🔒 Prevention Strategy
* Use **AWS Secrets Manager** with client-side caching libraries (which cache secret data keys locally for 5-15 minutes).
* Restrict unnecessary KMS encrypt/decrypt operations in high-throughput data pipelines.

---

### MLOps: Concept Drift & Model Performance Degradation
* **Severity:** 🟡 High / Medium
* **Frequency:** ❄️ Rare (but inevitable over time)

#### 📖 Description & Symptoms
The Machine Learning API (e.g. FastAPI IT Career prediction model) is running perfectly at 100% uptime with sub-100ms latency. However, downstream business audits reveal that the *quality* of predictions is dropping, and the model is recommending incorrect decisions.

#### 🤔 Root Cause Analysis
**Concept Drift / Covariate Shift.** The statistical properties of the incoming real-world data changed over time (e.g., job descriptions post-2026 contain terms the 2024 model never saw). The code is correct, the container is healthy, but the *mathematical logic* inside the model binary (`model.pkl`) is stale.

#### ⚙️ Solution & Remediation
1. **Analyze predictions vs. actuals:** Compare predictions stored in logs with ground-truth outcomes.
2. **Trigger retraining pipeline:** Pull new baseline data and execute training script:
   ```bash
   python train.py --dataset=2026_latest.csv
   ```
3. **Compare Accuracy metric:** If the new model accuracy exceeds the baseline, package and build the new container.
4. **Deploy rolling update:** Update EKS pods to pull the newly trained model version:
   ```bash
   kubectl set image deployment/it-career-app api-container=vikas4cloud/it-career-api:v2.0
   ```

#### 🔒 Prevention Strategy
* Implement **Evidently AI** or **Great Expectations** in data pipelines to detect statistical distribution shifts.
* Set up automated pipelines that run retraining jobs monthly or when drift metrics exceed thresholds.

---

## 3. Quick-Reference Diagnostic Cheatsheet

| Symptom | Primary Tool | Common Remediation Command |
|---|---|---|
| Pod Crashed / Exit 137 | `kubectl describe pod` | `kubectl set resources --limits=memory=...` |
| "No space left on device" | `df -h` / `df -i` | `docker system prune -a --volumes -f` |
| DB Timeout Connection | `nc -zv -w3` | Add Client Security Group to DB Inbound Rules |
| Pipeline stuck forever | `top` / `ps aux` | Run commands in background: `nohup ... &` |
| "Acquiring state lock" | `terraform force-unlock` | `terraform force-unlock <LOCK_ID>` |
| "Too many open files" | `lsof` / `ulimit` | Set `nofile 65535` in `/etc/security/limits.conf` |
| Outbound API failure inside Docker | `cat /etc/resolv.conf` | Pass `--dns=8.8.8.8` to docker run |
