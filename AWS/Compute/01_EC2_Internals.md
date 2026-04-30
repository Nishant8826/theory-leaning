# 💻 EC2 Internals

## 📌 Topic Name
Elastic Compute Cloud (EC2): The Anatomy of a Virtual Machine

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: You rent a virtual server in the cloud.
*   **Expert**: EC2 is a **Virtualized Compute Instance** running on a custom-designed hardware substrate. Modern EC2 instances leverage the **AWS Nitro System**, which decomposes traditional hypervisor functions (Network, Storage, Management) into dedicated hardware and software components. This minimizes the "hypervisor tax" and provides performance nearly identical to bare metal.

## 🏗️ Mental Model
Think of EC2 as **Modular Lego Architecture**.
- **CPU/RAM**: The core bricks.
- **EBS**: The detachable external hard drive.
- **ENI**: The plug-in network card.
- **Nitro Card**: The invisible manager that handles all the background tasks so the CPU can focus on your code.

## ⚡ Actual Behavior
When you launch an instance, the **EC2 Control Plane** finds a physical host with available capacity in the requested AZ. It commands the **Nitro Controller** on that host to carve out a VM, attach the requested EBS volumes via NVMe over PCIe, and plug in an ENI. The OS boots, and you get access via SSH/RDP.

## 🔬 Internal Mechanics
1.  **The Nitro System**:
    *   **Nitro Cards**: Dedicated hardware for VPC, EBS, and Instance Storage.
    *   **Nitro Security Chip**: Hardware-based root of trust.
    *   **Nitro Hypervisor**: A lightweight KVM-based hypervisor that only handles CPU/Memory isolation.
2.  **Instance Store (Ephemeral)**: Physically attached SSDs to the host. If the instance stops or the host fails, data is LOST. Used for caches and temp files.
3.  **Bursting (T-Instances)**: Uses a **CPU Credit** system. If you stay below a baseline, you earn credits. If you spike, you spend them. When credits = 0, CPU is throttled to baseline.

## 🔁 Execution Flow (Launch)
1.  `RunInstances` API call.
2.  **Placement Engine**: Selects physical host based on instance type and AZ.
3.  **Host Allocation**: Nitro hypervisor allocates vCPUs (pinned to physical cores/threads).
4.  **Peripheral Attachment**: Nitro VPC card sets up the network; Nitro EBS card maps the volume.
5.  **Boot**: BIOS/UEFI starts, loading the AMI from EBS.

## 🧠 Resource Behavior
- **Stop vs Terminate**: Stopping releases the CPU/RAM but keeps the EBS volume. Terminating deletes everything (unless "Delete on Termination" is false).
- **Metadata Service (IMDSv2)**: A local HTTP service at `169.254.169.254` that provides the instance with its IP, role credentials, and userdata. IMDSv2 is session-based and more secure against SSRF.

## 📐 ASCII Diagrams
```text
[ Physical Server Rack ]
|-----------------------------------|
| [ Nitro Card: VPC ] [ Nitro: EBS ]| <--- Hardware Offload
|-----------------------------------|
| [ Nitro Hypervisor (KVM) ]        | <--- CPU/RAM Isolation
|-----------------------------------|
| [ VM 1 ]  [ VM 2 ]  [ VM 3 ]      | <--- Your EC2 Instances
| (App)     (DB)      (Web)         |
|-----------------------------------|
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "m5.large"
  
  # Enabling IMDSv2 for security
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" # Enforce IMDSv2
    http_put_response_hop_limit = 1
  }

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
  }
}
```

## 💥 Production Failures
1.  **CPU Credit Exhaustion**: A `t3.medium` runs a background job that consumes 100% CPU. Credits hit zero, and the web server response time jumps from 50ms to 5000ms.
2.  **EBS Stale I/O**: Network congestion between the EC2 host and the EBS storage cluster causes "I/O Wait" to spike, freezing the application even if CPU is low.
3.  **Instance Retirement**: AWS detects a hardware failure on the host and sends a "Scheduled Retirement" notice. If you don't stop/start the instance, it will be forcefully terminated.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between a vCPU and a physical core?
*   **A**: Usually, 1 vCPU = 1 Hyperthread. An `m5.large` has 2 vCPUs, which is 1 physical core with 2 threads.
*   **Q**: Why is my first SSH connection slow?
*   **A**: Often due to DNS reverse lookups on the server or the time taken for the Nitro system to fully plumb the ENI.

## ⚠️ Edge Cases
*   **Clock Drift**: Virtual machines can experience clock drift. Always run `chrony` or `ntp` synced to the Amazon Time Service (`169.254.169.123`).
*   **MAC Address Persistence**: The MAC address is tied to the ENI, not the instance. If you move an ENI, the MAC goes with it.

## 🏢 Best Practices
1.  **Use Nitro Instances**: (C5, M5, R5 and newer) for best performance.
2.  **IMDSv2**: Always enforce session-based metadata.
3.  **EBS-Optimized**: Ensure your instance type supports dedicated EBS bandwidth (standard on modern types).

## ⚖️ Trade-offs
*   **On-Demand vs. Spot**: Stability vs. 90% cost savings.
*   **Instance Store vs. EBS**: Speed (NVMe) vs. Persistence.

## 💼 Interview Q&A
*   **Q**: How does AWS isolate one customer's EC2 from another's on the same hardware?
*   **A**: Through the hypervisor (CPU/Memory isolation) and the Nitro system (hardware-level isolation of network and storage traffic).

## 🧩 Practice Problems
1.  Compare the disk latency of an Instance Store volume vs. a GP3 EBS volume.
2.  Configure an instance to automatically recover to a new host if the physical hardware fails.

---
Prev: [09_Cost_Model_and_Billing.md](../Core/09_Cost_Model_and_Billing.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_Auto_Scaling_Groups.md](../Compute/02_Auto_Scaling_Groups.md)
---
