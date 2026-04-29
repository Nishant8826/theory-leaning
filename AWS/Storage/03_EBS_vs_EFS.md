# 💾 EBS vs. EFS

## 📌 Topic Name
Block Storage vs. File Storage: Amazon EBS vs. Amazon EFS

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: EBS is a virtual hard drive for one instance; EFS is a shared folder for many instances.
*   **Expert**: EBS is a **Network-Attached Block Store** designed for low-latency, high-performance IOPS (Input/Output Operations Per Second). EFS is a **Serverless, Elastic File System** based on NFSv4, designed for massive throughput and parallel access from thousands of instances. The core difference lies in the **Access Pattern** and the **Latency Profile**.

## 🏗️ Mental Model
- **EBS**: A **Local Disk** (via a very fast network). Like a USB drive you plug into one laptop.
- **EFS**: A **Network Drive** (NAS). Like a shared folder in an office where everyone can open the same Excel file at the same time.

## ⚡ Actual Behavior
- **EBS**: Single-AZ (mostly). It is physically located in the same AZ as your instance to minimize latency. 
- **EFS**: Regional. Data is stored across multiple AZs automatically. You can mount it from any AZ in the region.

## 🔬 Internal Mechanics
1.  **EBS Performance (gp3)**: You can tune IOPS and Throughput independently of the volume size. It uses an SSD-based architecture.
2.  **EBS Performance (io2 Block Express)**: The highest performance EBS, using the Nitro System to provide sub-millisecond latency and up to 256,000 IOPS.
3.  **EFS Architecture**: EFS is a distributed file system. It doesn't have a "size"; it grows and shrinks as you add/remove files. It uses a "Bursting" or "Provisioned" throughput model to handle I/O.

## 🔁 Execution Flow (Mounting)
- **EBS**:
    1. Attach Volume to EC2.
    2. OS sees a new raw device (e.g., `/dev/nvme1n1`).
    3. `mkfs` and `mount`.
- **EFS**:
    1. Create EFS Mount Target in each AZ.
    2. Install `amazon-efs-utils`.
    3. `mount -t efs fs-123456:/ /mnt/efs`.

## 🧠 Resource Behavior
- **EBS Multi-Attach**: A special feature of `io1/io2` volumes that allows up to 16 Nitro-based instances to attach to the same volume (requires a cluster-aware file system like GFS2).
- **EFS Lifecycle**: Can automatically move infrequently accessed files to a "Lower Cost Storage" tier (EFS-IA).

## 📐 ASCII Diagrams
```text
      [ EC2-A ]        [ EC2-B ]        [ EC2-C ]
          |                |                |
    +-----V-----+    +-----V-----+    +-----V-----+
    |  [ EBS ]  |    |  [ EFS ] <-----+-----> [ EFS ]  |
    | (Private) |    | (Shared Folder Across AZs)      |
    +-----------+    +---------------------------------+
```

## 🔍 Code / IaC (Terraform)
```hcl
# EBS Volume
resource "aws_ebs_volume" "data" {
  availability_zone = "us-east-1a"
  size              = 100
  type              = "gp3"
  iops              = 3000
  throughput        = 125
}

# EFS File System
resource "aws_efs_file_system" "shared" {
  creation_token = "my-shared-fs"
  performance_mode = "generalPurpose"
  throughput_mode  = "bursting"
}

resource "aws_efs_mount_target" "alpha" {
  file_system_id = aws_efs_file_system.shared.id
  subnet_id      = aws_subnet.private_a.id
}
```

## 💥 Production Failures
1.  **EBS AZ Mismatch**: Trying to attach an EBS volume from `us-east-1a` to an instance in `us-east-1b`. This will fail; EBS is bound to the AZ.
2.  **EFS Throughput Exhaustion**: A high-traffic app performs thousands of small metadata operations (like `ls` or `chown`) on EFS. This consumes "Burst Credits" rapidly. When credits = 0, EFS throttles to a tiny baseline, and the app hangs.
3.  **Database on EFS**: Putting a heavy database (like Postgres) on EFS. Because EFS is a network-distributed system, the latency per write is much higher than EBS. The DB performance will be terrible.

## 🧪 Real-time Q&A
*   **Q**: Which one is cheaper?
*   **A**: EBS is cheaper per GB, but EFS is more cost-effective for sharing small amounts of data across many instances.
*   **Q**: Can I mount EFS on-premises?
*   **A**: Yes, via Direct Connect or VPN. You cannot do this with EBS.

## ⚠️ Edge Cases
*   **EBS Snapshots**: These are stored in S3 (internally) and are regional. You can restore a snapshot to a new volume in *any* AZ in the region.
*   **EFS Max I/O Mode**: Use this for high-parallelism workloads (like big data processing), but it has higher metadata latency than the "General Purpose" mode.

## 🏢 Best Practices
1.  **EBS for Databases**: Always use EBS for high-performance stateful apps.
2.  **EFS for Content**: Use EFS for web assets, user uploads, or home directories shared across a web fleet.
3.  **Backup**: Use **AWS Backup** to manage snapshots and backups for both services in a centralized way.

## ⚖️ Trade-offs
*   **EBS**: Low latency, high IOPS, restricted to one AZ.
*   **EFS**: High throughput, shared access, regional availability, higher latency.

## 💼 Interview Q&A
*   **Q**: Your application needs a shared file system that can be accessed by 100 EC2 instances simultaneously across 3 AZs. Which storage service do you choose?
*   **A**: Amazon EFS. It is designed for multi-AZ shared access and uses the standard NFS protocol, making it perfect for this use case.

## 🧩 Practice Problems
1.  Benchmark the time it takes to write a 1GB file to EBS vs. EFS.
2.  Set up an EBS volume with "Multi-Attach" and try to write to it from two different instances.
