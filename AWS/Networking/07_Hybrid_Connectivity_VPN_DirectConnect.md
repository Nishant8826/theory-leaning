# 🌐 Hybrid Connectivity: VPN and Direct Connect

## 📌 Topic Name
Hybrid Networking: Bridging On-Premises and AWS

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Connect your office to AWS using a VPN (internet) or Direct Connect (private line).
*   **Expert**: Hybrid connectivity is about extending the **Private Address Space** of your organization into the AWS Cloud. **Site-to-Site VPN** provides an encrypted tunnel over the public internet, while **AWS Direct Connect (DX)** provides a dedicated, physical network connection from your premises to an AWS Direct Connect location. DX offers higher throughput, lower latency, and more consistent performance than VPN.

## 🏗️ Mental Model
- **VPN**: A **Tunnel through the City**. You take your own car, but you're driving through public streets. It’s encrypted (locked car), but you’re at the mercy of traffic (internet congestion).
- **Direct Connect**: A **Private Subway Line**. It’s a physical track from your house to the office. No one else is on it, and the travel time is exactly the same every single time.

## ⚡ Actual Behavior
- **VPN**: Uses IPsec. Setup takes minutes. Limited to ~1.25 Gbps per tunnel.
- **Direct Connect**: Setup takes weeks/months (requires physical cabling). Speeds from 50 Mbps up to 100 Gbps. Data transfer costs are lower than VPN for large volumes.

## 🔬 Internal Mechanics
1.  **Virtual Private Gateway (VGW)**: The AWS-side anchor for both VPN and Direct Connect. It can be attached to a single VPC.
2.  **Transit Gateway (TGW)**: The modern replacement for VGW, allowing a single VPN or DX to connect to thousands of VPCs.
3.  **BGP (Border Gateway Protocol)**: Both VPN (Dynamic) and DX use BGP to exchange routing information between your on-premise router and AWS.
4.  **MACsec**: Available for 10G/100G Direct Connect connections for point-to-point hardware encryption.

## 🔁 Execution Flow (Direct Connect)
1.  **Request**: You request a DX connection in the AWS Console.
2.  **LOA-CFA**: AWS provides a "Letter of Authorization."
3.  **Cabling**: You (or your provider) give the LOA to the data center manager to run a fiber patch cable between your router and the AWS router.
4.  **Virtual Interface (VIF)**: You create a Public, Private, or Transit VIF to access specific AWS resources.
5.  **BGP Peering**: You establish a BGP session to exchange routes.

## 🧠 Resource Behavior
- **Redundancy**: A single Direct Connect is a single point of failure. AWS recommends at least two connections in two different DX locations for maximum resilience.
- **VPN as Backup**: A common Staff pattern is to use Direct Connect as the primary path and a Site-to-Site VPN as the failover path.

## 📐 ASCII Diagrams
```text
[ ON-PREMISES ] <---(Public Internet)--- [ AWS VPN ]
      |                                      |
      +----(Dedicated Fiber)----> [ DIRECT CONNECT ] --- [ VPC ]
                                      (DX Location)
```

## 🔍 Code / IaC (Terraform)
```hcl
# Site-to-Site VPN Connection
resource "aws_customer_gateway" "main" {
  bgp_asn    = 65000
  ip_address = "203.0.113.12"
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"
  static_routes_only  = false
}
```

## 💥 Production Failures
1.  **BGP Flapping**: An unstable router on-premise causes the BGP session to drop and reconnect repeatedly, causing routing instability in the VPC.
2.  **MTU Issues**: VPN tunnels add overhead (encapsulation). If your app sends 1500-byte packets, they will be fragmented, leading to performance degradation or dropped packets. **Solution**: Use MSS Clamping to 1350-1380 bytes.
3.  **Direct Connect Router Failure**: Relying on a single DX provider or a single physical cable. When the fiber is cut by a backhoe, your whole hybrid cloud goes dark.

## 🧪 Real-time Q&A
*   **Q**: Is Direct Connect encrypted?
*   **A**: By default, NO. It is a private line but not encrypted. If you need encryption, you must run an IPsec VPN *over* the Direct Connect (Public VIF) or use MACsec.
*   **Q**: Can I use DX to reach S3?
*   **A**: Yes, via a Public VIF or an Interface VPC Endpoint.

## ⚠️ Edge Cases
*   **Direct Connect Gateway (DXGW)**: A global resource that allows you to connect a DX in London to a VPC in Tokyo.
*   **Accelerated VPN**: Uses AWS Global Accelerator to route your VPN traffic to the nearest AWS edge location, reducing latency over the public internet.

## 🏢 Best Practices
1.  **Resilience**: Use two DX connections in separate locations.
2.  **Monitor BGP**: Set up alerts for BGP session status changes.
3.  **Direct Connect vs. VPN**: Use VPN for dev/test or as backup; use DX for production production data and consistent latency.

## ⚖️ Trade-offs
*   **VPN**: Fast to set up, low cost for low traffic, but unpredictable performance.
*   **Direct Connect**: High performance, lower data transfer costs, but high setup time and fixed monthly port costs.

## 💼 Interview Q&A
*   **Q**: How would you design a highly available hybrid connection for a financial institution?
*   **A**: I would recommend two **Direct Connect** connections at two different Direct Connect locations for 99.99% availability. I would also set up a **Site-to-Site VPN** as a tertiary backup path. I would use **BGP** with appropriate `AS_PATH` prepending to ensure that the DX paths are preferred over the VPN.

## 🧩 Practice Problems
1.  Diagram the packet flow from an on-premise server to an S3 bucket using a Private VIF.
2.  Explain the purpose of "AS Path Prepending" in a multi-region hybrid network.

---
Prev: [06_NAT_Gateway_and_Internet.md](../Networking/06_NAT_Gateway_and_Internet.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [08_Connection_Lifecycle.md](../Networking/08_Connection_Lifecycle.md)
---
