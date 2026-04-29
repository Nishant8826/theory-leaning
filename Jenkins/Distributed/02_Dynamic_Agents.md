# 🌐 Dynamic Agents

## 📌 Topic Name
Dynamic Provisioning: Cloud Agents, Cost Optimization, and Boot Latency

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Instead of paying for servers that sit idle all night, Jenkins creates a server when a build starts and deletes it when the build finishes.
*   **Expert**: Dynamic Agents shift Jenkins from a static infrastructure model to an **Elastic Compute** model. Utilizing Cloud Plugins (EC2, Azure VM, GCP), the Jenkins Queue acts as the scaling trigger. When a task sits in the queue, Jenkins issues an API call to the cloud provider to provision a VM. A Staff engineer manages the critical trade-offs between **Startup Latency** (time to boot OS/JVM) and **Cost Savings**, heavily utilizing Custom AMIs, Spot Instances, and Retention Policies.

## 🏗️ Mental Model
Think of Dynamic Agents as **Ride-Sharing (Uber) for Builds**.
- **Static Agents (Owning a Car)**: You pay for it 24/7, even when it sits in the garage. But when you need to go, you jump in and drive instantly.
- **Dynamic Agents (Uber)**: You only pay when you take a ride. But when you request a ride, you have to wait 5 minutes for the driver to arrive (Boot Latency).

## ⚡ Actual Behavior
- **Queue Interception**: The Cloud plugin intercepts the Scheduler. If the queue has 5 items needing `label 'aws'`, and there are 0 agents, Jenkins calls `aws ec2 run-instances` 5 times.
- **Connection Handshake**: Jenkins waits for the instance to boot, waits for SSH to become available, connects, downloads `remoting.jar`, starts the JVM, and finally assigns the queued task. This can take anywhere from 1 to 10 minutes.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Cloud Templates**: You define "Templates" in Jenkins mapped to specific labels. E.g., Template `large-build` maps to `c5.2xlarge` using AMI `ami-12345`.
2.  **Idle Retention Strategy**: To mitigate boot latency, plugins use a retention strategy. When a build finishes, the instance isn't terminated immediately. It stays alive for $X$ minutes (e.g., 30 mins). If a new build arrives, it runs instantly. If the timer expires, the instance is terminated.
3.  **Spot Instances**: Requesting spare cloud capacity at an 80% discount. If the cloud provider reclaims the instance, Jenkins handles the disconnect (the build fails, but Jenkins provisions a new one).

## 🔁 Execution Flow
1.  **Demand**: Build enters Queue requesting `label 'ec2-linux'`.
2.  **Evaluate**: Jenkins sees 0 idle agents with that label.
3.  **Provision**: Jenkins calls AWS API to launch an EC2 instance.
4.  **Wait**: Job sits in queue as "Waiting for next available executor".
5.  **Init**: Instance boots, Jenkins SSHes in, installs Java (if missing), starts `agent.jar`.
6.  **Execute**: Job leaves queue, runs on the new EC2 instance.
7.  **Idle**: Job finishes. Instance sits idle for 30 minutes.
8.  **Terminate**: Timer expires. Jenkins calls AWS API to terminate the instance.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Controller API Limits**: If 1,000 jobs enter the queue, Jenkins might make 1,000 simultaneous API calls to AWS, triggering `RequestLimitExceeded` (Throttling) and preventing any agents from launching.
- **Cost Efficiency**: Dynamic agents ensure you pay exactly $0 for compute during weekends and nights.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS QUEUE ]
   |
(10 Items Pending)
   |
[ EC2 PLUGIN ] --(API Call: Launch 10 VMs)--> [ AWS EC2 CONTROL PLANE ]
                                                    |
                                          +---------+---------+
                                          |                   |
                                   [ INSTANCE 1 ]      [ INSTANCE 10 ]
                                  (Booting... 2m)     (Booting... 2m)
                                          |                   |
[ JENKINS REMOTING ] <---(SSH Handshake)--+-------------------+
   |
(Assigns 10 Items)
   |
[ EXECUTE & TERMINATE ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# JCasC Configuration for the EC2 Plugin
jenkins:
  clouds:
    - amazonEC2:
        name: "aws-us-east"
        credentialsId: "aws-credentials"
        region: "us-east-1"
        templates:
          - ami: "ami-0abcdef1234567890" # Custom AMI with Java pre-installed
            description: "Standard Linux Agent"
            labels: "linux docker ec2"
            type: T3_LARGE
            # CRITICAL: Keep alive for 30 mins to avoid boot tax on next job
            idleTerminationMinutes: "30" 
            spotConfig:
              fallbackToOndemand: true
```

## 💥 Production Failures
1.  **The "Boot Loop" Debt**: The configured AMI does not have Java installed, and the init script fails to install it. Jenkins provisions the VM. Jenkins tries to connect via SSH and fails because Java is missing. Jenkins marks the node offline, terminates it, and provisions a *new* VM to try again. This loops infinitely, generating massive AWS bills for instances that run for 5 minutes and die.
2.  **The Throttling Deadlock**: An aggressive queue causes Jenkins to hit AWS API rate limits. AWS drops the `RunInstances` calls. The queue continues to grow. Jenkins keeps retrying, staying permanently rate-limited.
3.  **Spot Reclaim Chaos**: Using Spot instances for a 4-hour compilation job. 3 hours in, AWS reclaims the instance. The job fails and starts over. It takes 3 days to complete because it keeps getting reclaimed. **Solution**: Use On-Demand for jobs longer than 1 hour.

## 🧪 Real-time Q&A
*   **Q**: How do I reduce the 5-minute boot latency?
*   **A**: Use "Custom AMIs" (Golden Images) baked with Packer. Ensure Java, Docker, and Git are pre-installed. Do not use UserData bash scripts to run `apt-get update` on every boot.
*   **Q**: How is this different from Kubernetes agents?
*   **A**: EC2 agents provide full Virtual Machines (great for heavy Docker-in-Docker or kernel-level testing). K8s agents are Pods sharing a host kernel (faster startup, less isolation).

## ⚠️ Edge Cases
*   **Stale Nodes**: Sometimes the Jenkins API call to terminate the instance fails. The EC2 instance stays running forever (a "Zombie" instance), costing money but doing no work. Use an AWS Lambda function to reap EC2 instances tagged by Jenkins that have had zero CPU usage for 24 hours.

## 🏢 Best Practices
1.  **Bake, Don't Fry**: Pre-bake AMIs using HashiCorp Packer. A VM that just needs to turn on and accept an SSH connection boots in 30 seconds.
2.  **Combine with Spot**: Use Spot Instances for 90% of CI workloads (unit tests, linting) to reduce compute costs by up to 80%.
3.  **Minimum Instance Count**: If developer velocity is critical, configure the template to always keep `Minimum Instances: 1` alive during business hours.

## ⚖️ Trade-offs
*   **Latency vs Cost**: You can have zero queue wait time (Static Agents / High Minimums), but you will pay a massive infrastructure bill. You can have a tiny bill (Dynamic Agents / Zero Minimums), but developers will complain about wait times.

## 💼 Interview Q&A
*   **Q**: Your dynamic EC2 agents take 8 minutes to become available to the queue. Walk me through how you would profile and eliminate this latency.
*   **A**: I would break down the 8 minutes into phases.
    1. **AWS Provisioning Time**: EC2 instance state pending -> running. Usually 1-2 mins. Can't optimize this much.
    2. **OS Boot Time**: From running -> SSH open. If this takes 3 minutes, the AMI is likely running a massive `cloud-init` script. I would eliminate `cloud-init` by pre-baking all software into the AMI using Packer.
    3. **Jenkins Handshake**: Jenkins downloading `remoting.jar`. I would bake the `remoting.jar` directly into the AMI. By optimizing the AMI, I can usually reduce an 8-minute boot to under 90 seconds.

## 🧩 Practice Problems
1.  Identify the exact AWS IAM permissions required for the Jenkins EC2 Plugin to function (`ec2:RunInstances`, `ec2:TerminateInstances`, `ec2:DescribeInstances`).
2.  Calculate the cost difference between running a static `c5.2xlarge` for 730 hours a month vs running it dynamically for only the 100 hours a month builds are actively running.
