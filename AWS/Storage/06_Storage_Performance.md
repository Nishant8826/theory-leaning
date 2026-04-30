# ⚡ Storage Performance

## 📌 Topic Name
AWS Storage Performance: Optimizing IOPS, Throughput, and Latency

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Some disks are faster than others. Buy more SSDs for more speed.
*   **Expert**: Storage performance in AWS is a function of the **Storage Substrate** and the **Network Pipe** connecting it to compute. Performance is measured by three key metrics: **IOPS** (number of read/write operations), **Throughput** (volume of data per second), and **Latency** (time per operation). A Staff engineer knows how to balance these against cost and how to leverage features like **EBS-Optimized Instances** and **NVMe** to eliminate bottlenecks.

## 🏗️ Mental Model
Think of Storage Performance as a **Water System**.
- **IOPS**: The number of faucets. More faucets mean more people can wash their hands (small random reads/writes).
- **Throughput**: The diameter of the main pipe. A larger pipe means you can fill a swimming pool faster (large sequential reads/writes like backups or video streaming).
- **Latency**: The time it takes for water to come out after you turn the handle.

## ⚡ Actual Behavior
- **EBS (gp3)**: Baseline of 3,000 IOPS and 125 MB/s throughput. You can pay to increase either independently up to 16,000 IOPS and 1,000 MB/s.
- **EBS (io2)**: For mission-critical apps. Up to 64,000 IOPS and 1,000 MB/s per volume (256,000 IOPS on Block Express).
- **S3**: Highly parallel. You get 3,500 PUT and 5,500 GET requests *per second per prefix*.

## 🔬 Internal Mechanics
1.  **I/O Credits (gp2 only)**: Older gp2 volumes used a "bucket" system where you earned credits during idle time to burst later. **Staff Tip**: Always use `gp3`; it’s cheaper and more predictable.
2.  **EBS-Optimized Instances**: These instances have a dedicated network connection for EBS traffic, preventing your application's internet traffic from interfering with disk I/O.
3.  **NVMe Protocol**: Modern Nitro instances use NVMe instead of Xen/para-virtual drivers, significantly reducing software-level latency.

## 🔁 Execution Flow (I/O Path)
1.  **Application**: Calls `write()` to the OS.
2.  **Filesystem/Kernel**: Buffers and prepares the block request.
3.  **Nitro Controller**: Intercepts the request and encapsulates it for the EBS network.
4.  **Network**: Packet travels over the dedicated 10Gbps+ EBS backbone.
5.  **Storage Cluster**: Data is written to physical media and replicated for durability.
6.  **Ack**: The response travels back the same way.

## 🧠 Resource Behavior
- **Volume Initialization**: When you restore from an EBS snapshot, the data is lazily loaded from S3. This causes a "first-read penalty" where latency is high. **Solution**: Use **Fast Snapshot Restore (FSR)** or "warm" the drive by reading all blocks.
- **Micro-bursting**: I/O spikes that happen so fast (milliseconds) that CloudWatch (which has 1-minute granularity) doesn't see them. You'll see "I/O Wait" in the OS but 0% utilization in AWS.

## 📐 ASCII Diagrams
```text
[ APP ] ----> [ OS / VFS ] ----> [ NITRO EBS CARD ]
                                        |
                                (Dedicated Fiber)
                                        |
[ STORAGE CLUSTER ] <-------------------+
 (Striped across many disks)
```

## 🔍 Code / IaC (Terraform)
```hcl
# High-performance DB volume
resource "aws_ebs_volume" "db_storage" {
  availability_zone = "us-east-1a"
  size              = 500
  type              = "gp3"
  iops              = 10000 # High IOPS for database
  throughput        = 500   # High throughput for backups
}

# Ensuring the instance is EBS-optimized
resource "aws_instance" "db_server" {
  instance_type        = "r6i.large" # All r6i are EBS-optimized
  ebs_optimized        = true
  # ...
}
```

## 💥 Production Failures
1.  **Throughput Bottleneck**: An instance has 10,000 IOPS (plenty) but only 125 MB/s throughput. A large database index build fails or takes hours because it's limited by the "pipe" size, not the "faucet" speed.
2.  **Queue Depth Overload**: Sending too many concurrent I/O requests. If the "Queue Depth" is too high, latency spikes because requests are waiting in line at the Nitro controller.
3.  **Shared Network Congestion**: On older non-EBS-optimized instances, a large S3 download consumes the same network bandwidth used by EBS, causing the local disk to "slow down."

## 🧪 Real-time Q&A
*   **Q**: What is the difference between IOPS and Throughput?
*   **A**: IOPS * BlockSize = Throughput. If you have 1000 IOPS and each block is 16KB, your throughput is 16MB/s.
*   **Q**: Why is my disk slow after I just restored it from a backup?
*   **A**: Because of "Lazy Loading." EBS is pulling data from S3 as you read it.

## ⚠️ Edge Cases
- **Stale I/O**: A rare condition where the network path to an EBS volume is severed, but the OS thinks the disk is still there, leading to "D state" processes that cannot be killed.
- **Jumbo Frames**: Using 9001 MTU within the VPC can slightly improve storage throughput by reducing the number of network packets.

## 🏢 Best Practices
1.  **Use GP3**: It is the best balance of cost and performance.
2.  **Monitor "Average Queue Length"**: If it’s consistently high, you need more IOPS.
3.  **Raid 0 for Speed**: If one volume isn't fast enough, you can use OS-level RAID 0 to stripe across multiple EBS volumes (but this increases the risk of failure).

## ⚖️ Trade-offs
*   **IOPS vs. Size**: In `gp2`, you get 3 IOPS per GB. In `gp3`, you get what you pay for regardless of size.
*   **Local NVMe vs. EBS**: Zero network latency but zero persistence (if instance stops) vs. millisecond latency and high durability.

## 💼 Interview Q&A
*   **Q**: A database is experiencing high "Disk I/O Wait" but the EBS volume metrics show it's only using 50% of its provisioned IOPS. What could be the problem?
*   **A**: 1. Throughput limit hit. 2. Instance-level EBS bandwidth limit hit. 3. Small I/O size (e.g., 4KB) causing high overhead. 4. Application-level locking or contention.

## 🧩 Practice Problems
1.  Calculate the required throughput for an EBS volume that needs to perform 5,000 IOPS with a 64KB block size.
2.  Use `fio` to benchmark the random read performance of an EC2 instance's root volume.

---
Prev: [05_Data_Lifecycle_Policies.md](../Storage/05_Data_Lifecycle_Policies.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [01_RDS_Internals.md](../Databases/01_RDS_Internals.md)
---
