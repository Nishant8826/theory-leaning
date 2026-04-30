# 📌 Topic: Bridge Network (Local Isolation)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: The Bridge Network is the default way containers talk to each other on a single computer. It's like a virtual Wi-Fi router inside your computer that all containers plug into.
**Expert**: The Docker Bridge is a **Virtual Layer 2 Switch** (implemented as a Linux Bridge device, usually `docker0`). It uses **veth (Virtual Ethernet) pairs** to connect the container's network namespace to the host's network namespace. Communication between containers on the same bridge is routed at the Data Link layer, while communication to the outside world is handled via **NAT (Network Address Translation)** and **IP Forwarding**. Staff-level engineering requires understanding the performance impact of the bridge and how to create "User-Defined Bridges" for better isolation and automatic DNS discovery.

## 🏗️ Mental Model
- **The virtual switch**: A physical ethernet switch sitting inside your server. Every container has a virtual cable (veth) plugged into one of the switch ports.

## ⚡ Actual Behavior
- **Default Bridge (`docker0`)**: Containers get an IP like `172.17.0.x`. They can talk to each other by IP, but NOT by name (no DNS).
- **User-Defined Bridge**: Containers can talk to each other by **Container Name**. Docker provides a built-in DNS server for these networks.

## 🔬 Internal Mechanics (veth pairs and IPTables)
1. **veth pair**: When a container starts, Docker creates two virtual interfaces. One (`eth0`) is moved inside the container namespace. The other (`vethXXXX`) is attached to the `docker0` bridge on the host.
2. **IPAM (IP Address Management)**: Docker assigns a unique IP to each container from the bridge's subnet.
3. **NAT (Masquerade)**: When a container sends a packet to the internet, the host kernel changes the "Source IP" to the host's physical IP using IPTables.

## 🔁 Execution Flow
1. Container A (172.17.0.2) pings Container B (172.17.0.3).
2. Packet goes out of A's `eth0`.
3. Packet arrives at the host's `docker0` bridge.
4. Bridge sees the MAC address of B and sends the packet to the `veth` connected to B.
5. Packet arrives at B's `eth0`.

## 🧠 Resource Behavior
- **Latency**: The bridge adds a tiny amount of latency (~0.1ms) compared to "Host" networking.
- **Throughput**: For high-performance apps (10Gbps+), the bridge's packet processing can become a bottleneck.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKER BRIDGE ARCHITECTURE
       
[ Container A ]        [ Container B ]
(eth0: 172.17.0.2)     (eth0: 172.17.0.3)
      |                      |
      +----( veth pair )-----+
      |                      |
+------------------------------------------+
|          docker0 (Linux Bridge)          |  <-- Layer 2 Switch
+------------------------------------------+
      |
      +----( IPTables / NAT )----> [ Physical Interface ] -> [ Internet ]
```

## 🔍 Code (Managing Bridges)
```bash
# 1. Create a user-defined bridge
docker network create --driver bridge my-isolated-net

# 2. Run containers on the new bridge
docker run -d --name db --network my-isolated-net redis
docker run -d --name app --network my-isolated-net my-app

# 3. Verify DNS discovery
docker exec app ping db
# Success! (Discovery only works on user-defined networks)

# 4. Inspect the bridge on the host
brctl show docker0
```

## 💥 Production Failures
- **The "IP Exhaustion"**: You have a bridge with a `/24` subnet (254 IPs). You run thousands of short-lived containers. Because of a bug, IPs aren't reclaimed fast enough. New containers fail to start with "No available IP."
- **Nesting Bridges**: Running Docker inside a VM that is also using a bridge. This can lead to "MTU (Maximum Transmission Unit)" mismatches, where small packets work but large packets (like web pages) hang forever.

## 🧪 Real-time Q&A
**Q: Should I use the default `docker0` bridge?**
**A**: **NO.** Always create a user-defined bridge. It provides better isolation (containers on different bridges can't talk) and, most importantly, it provides **Automatic Service Discovery** via container names.

## ⚠️ Edge Cases
- **Port Mapping**: When you use `-p 80:80`, Docker adds a DNAT rule to IPTables. This rule redirects incoming traffic from the host's port 80 to the container's IP on port 80.

## 🏢 Best Practices
- **Isolation**: Create a separate bridge for every "App Stack" (e.g., one for Frontend+API, one for DB+Cache).
- **Custom Subnets**: Define your own IP ranges to avoid conflicts with your company's internal VPN or office network.

## ⚖️ Trade-offs
| Network Mode | Isolation | Performance | Discovery |
| :--- | :--- | :--- | :--- |
| **Bridge (Default)** | Medium | High | None |
| **User Bridge** | **High** | High | **Automatic** |
| **Host** | None | **Highest** | Manual |

## 💼 Interview Q&A
**Q: How does Docker implement the "Bridge" network on Linux?**
**A**: Docker uses the Linux Kernel's `bridge` module to create a virtual Layer 2 switch. It then creates **veth (virtual ethernet) pairs**. One end of the pair is placed inside the container's network namespace as `eth0`, and the other end is attached to the virtual bridge on the host. Traffic between containers is switched by the bridge, while traffic going to the external network is routed through the host's IP stack and translated via **NAT (Masquerade)** rules in IPTables.

## 🧩 Practice Problems
1. Create two bridges. Run a container on each. Try to ping one from the other. Note that it fails.
2. Connect one container to BOTH bridges using `docker network connect`. Now ping both.
3. Inspect `iptables -t nat -L` on your host and find the MASQUERADE rules for the bridge.

---
Prev: [06_Rootless_Containers.md](../Containers/06_Rootless_Containers.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Overlay_Network.md](./02_Overlay_Network.md)
---
