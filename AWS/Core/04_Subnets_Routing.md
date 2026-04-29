# 🛣️ Subnets and Routing

## 📌 Topic Name
Subnets and Routing: The Traffic Control System of the Cloud

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Subnets divide your network; route tables tell traffic where to go.
*   **Expert**: Subnets are **AZ-bound IP address ranges** within a VPC. Routing in AWS is a **Distributed Routing Service** that implements a longest-prefix-match algorithm. Unlike physical routers, the AWS VPC router does not have a single physical chassis; it is a software-defined function that operates at the ENI (Elastic Network Interface) level.

## 🏗️ Mental Model
*   **Subnet**: A specific floor in a building (AZ).
*   **Route Table**: The directory in the elevator that tells you which button to press to get to a specific room.
*   **Local Route**: The default route (`10.0.0.0/16` -> `local`) that allows all subnets in a VPC to talk to each other. You cannot delete this.

## ⚡ Actual Behavior
When a packet leaves an instance, the VPC router checks the associated **Route Table**.
- If the destination is within the VPC CIDR, it's a `local` route.
- If it's `0.0.0.0/0`, it looks for a target like `igw-xxx` (Internet Gateway) or `nat-xxx` (NAT Gateway).
- If it's a specific CIDR for a Peered VPC, it goes to `pcx-xxx`.

## 🔬 Internal Mechanics
1.  **Implicit vs. Explicit Association**: Every subnet must be associated with a route table. If you don't pick one, it uses the "Main Route Table." **Staff Level Tip**: Never use the Main Route Table for production subnets; always create explicit ones.
2.  **Longest Prefix Match**: If you have a route for `10.1.0.0/16` to a Peering connection and a route for `10.1.1.0/24` to a VPN, a packet for `10.1.1.5` will go to the VPN.
3.  **Propagation**: BGP routes from a Direct Connect or VPN can be "propagated" automatically into your VPC route tables.

## 🔁 Execution Flow
1.  **ENI Egress**: Packet leaves the instance.
2.  **Source Check**: VPC verifies the source IP/MAC is valid (prevents spoofing).
3.  **Table Lookup**: The router identifies the Target for the destination IP.
4.  **Target Forwarding**: Packet is encapsulated and sent to the internal AWS service representing that target (IGW, NAT, Peering).

## 🧠 Resource Behavior
- **Public Subnet**: A subnet whose route table has a route to an Internet Gateway (`0.0.0.0/0 -> igw-id`).
- **Private Subnet**: A subnet whose route table does NOT have a route to an IGW. Usually, it has a route to a NAT Gateway (`0.0.0.0/0 -> nat-id`).
- **Isolated Subnet**: No route to the outside world at all.

## 📐 ASCII Diagrams
```text
[ Subnet A (Public) ]       [ Subnet B (Private) ]
        |                          |
[ Route Table A ]          [ Route Table B ]
| 10.0/16 -> Local |       | 10.0/16 -> Local |
| 0.0/0   -> IGW   |       | 0.0/0   -> NAT   |
        |                          |
        V                          V
  [ Internet GW ] <----------- [ NAT GW ]
        |
    (Internet)
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}
```

## 💥 Production Failures
1.  **Circular Routing**: Routing traffic to a middle-box (like an IDS) that then routes it back to the same table, causing a loop.
2.  **NAT Gateway Single Point of Failure**: Placing a NAT Gateway in only one AZ. If that AZ goes down, *all* private subnets across the whole VPC lose internet access.
3.  **Blackhole Routes**: A route points to a deleted Peering connection or NAT Gateway, causing traffic to be dropped silently.

## 🧪 Real-time Q&A
*   **Q**: Can I route between subnets in the same VPC using a firewall?
*   **A**: Yes, but you need to use **Inbound Routing** (Gateway Load Balancer or VPC Ingress Routing) which is a complex Staff-level pattern.
*   **Q**: Does adding a route increase latency?
*   **A**: No. The lookup is a high-speed O(1) operation in the SDN.

## ⚠️ Edge Cases
*   **Overlapping Routes**: If you peer with a VPC that has the same CIDR, you can't route to it.
*   **Route Limits**: There is a limit of 50 routes per route table (can be increased to 100, but impacts performance).

## 🏢 Best Practices
1.  **Multi-NAT**: One NAT Gateway per AZ for high availability.
2.  **Explicit Associations**: Always define your own route tables; don't rely on the "Main" one.
3.  **Naming**: Name route tables by their purpose (e.g., `rtb-public-us-east-1a`).

## ⚖️ Trade-offs
*   **NAT Gateway vs. NAT Instance**: NAT Gateway is managed and scales to 45Gbps but costs $0.045/hr + $0.045/GB. NAT instances are cheaper but you manage scaling and HA.

## 💼 Interview Q&A
*   **Q**: What makes a subnet "Public"?
*   **A**: A direct route to an Internet Gateway in its associated route table.

## 🧩 Practice Problems
1.  Set up a "DB Subnet" that can only be reached from the "App Subnet" and has no path to the internet.
2.  Explain how a packet from an instance in a private subnet reaches `google.com`.
