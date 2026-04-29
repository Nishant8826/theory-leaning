# 🏗️ AWS Global Infrastructure

## 📌 Topic Name
AWS Global Infrastructure: The Physical Foundation of Distributed Systems

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: AWS has data centers all over the world. You pick one and run your code there.
*   **Expert**: AWS Global Infrastructure is a multi-layered hierarchy designed to provide low-latency connectivity and high-availability isolation. It consists of **Regions**, **Availability Zones (AZs)**, **Local Zones**, **Wavelength Zones**, and **Edge Locations**. The magic lies in the **AWS Global Network**—a private, high-capacity fiber network connecting every region with redundant paths.

## 🏗️ Mental Model
Think of AWS Global Infrastructure as a **Cellular Organism**.
*   **Regions** are the Organs (Isolated).
*   **AZs** are the Tissues (Redundant within organs).
*   **Edge Locations** are the Nerve Endings (Sensory/Delivery).
*   **AWS Global Network** is the Circulatory System (Data transport).

## ⚡ Actual Behavior
When you "choose a region," you are choosing a geographic area that contains at least three AZs. These AZs are physically separate but connected via ultra-low-latency (sub-10ms) private fiber. Unlike other providers, an AZ is often multiple data centers, not just one.

## 🔬 Internal Mechanics
1.  **Fault Domains**: Regions are logically isolated. A failure in `us-east-1` (while famous) does not technically impact `us-west-2`'s control plane.
2.  **Dark Fiber**: AWS owns or leases massive amounts of "dark fiber." When a packet leaves an EC2 instance in Tokyo for an S3 bucket in Dublin, it stays on the AWS backbone, avoiding the public internet until the last possible moment.
3.  **Nitro System**: Physical hardware that offloads virtualization overhead (Networking, Storage, Security) to dedicated cards, allowing nearly 100% of host resources for the VM.

## 🔁 Execution Flow
1.  **Request Initiation**: Client hits a Route 53 DNS entry.
2.  **Global Routing**: Route 53 (Edge) directs traffic to the nearest CloudFront/ALB.
3.  **Regional Entry**: Traffic enters the AWS backbone at an Edge Location.
4.  **AZ Routing**: Internal routers forward the packet to the specific Subnet/ENI in the target AZ.

## 🧠 Resource Behavior
*   **Control Plane**: The API layer (e.g., `ec2.us-east-1.amazonaws.com`).
*   **Data Plane**: The actual service performance (e.g., your EC2 instance processing requests).
*   **Critical Fact**: Data planes are designed to keep running even if the control plane goes down.

## 📐 ASCII Diagrams
```text
[ Global Network ]
       |
+--------------------------+
|      Region (e.g. us-east-1)
|  +--------+  +--------+  +--------+
|  |  AZ-A  |  |  AZ-B  |  |  AZ-C  |
|  | (DC 1) |  | (DC 3) |  | (DC 5) |
|  | (DC 2) |  | (DC 4) |  | (DC 6) |
|  +--------+  +--------+  +--------+
|       ^          ^           ^
|       |----------|-----------| Low Latency Fiber (<10ms)
+--------------------------+
       |
[ Edge Locations / Local Zones ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# Listing regions using CLI
# aws ec2 describe-regions --all-regions

# Deploying across multiple AZs for High Availability
resource "aws_subnet" "primary" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "secondary" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}
```

## 💥 Production Failures
*   **AZ Power Outage**: Rare, but happens. If your database is Single-AZ, your app is dead.
*   **Regional Control Plane Degradation**: You can't start *new* instances, but existing ones keep running. Engineers often panic and try to terminate/restart, which makes it worse.
*   **Fiber Cut**: AWS has redundant paths, but a major subsea cable cut can increase latency.

## 🧪 Real-time Q&A
*   **Q**: Is `us-east-1a` the same physical building for everyone?
*   **A**: No. AWS uses **AZ Mapping**. Your `us-east-1a` might be my `us-east-1c` to prevent everyone from piling into the first AZ alphabetically.

## ⚠️ Edge Cases
*   **Inter-AZ Latency**: While low, it's not zero. High-frequency trading or tight gossip protocols (like Cassandra) might feel the jitter.
*   **Data Residency**: Moving data across regions costs money and may violate GDPR/CCPA.

## 🏢 Best Practices
*   **Multi-AZ is non-negotiable** for production.
*   **Multi-Region is for Disaster Recovery (DR)**, not just "high availability."
*   Always use `Availability Zone ID` (e.g., `use1-az1`) instead of the name for consistent mapping across accounts.

## ⚖️ Trade-offs
*   **Latency vs. Availability**: Multi-AZ adds milliseconds of network hop but saves you from a DC fire.
*   **Cost vs. Performance**: Inter-AZ data transfer costs $0.01/GB. It adds up in chatty microservice architectures.

## 💼 Interview Q&A
*   **Q**: Why would you use a Local Zone?
*   **A**: For <10ms latency to a specific metro area (e.g., video editing, gaming) without managing your own DC.

## 🧩 Practice Problems
1.  Calculate the cost of transferring 10TB of data between two EC2 instances in different AZs in the same region.
2.  Design a strategy to ensure an application survives a complete regional outage of `us-east-1`.
