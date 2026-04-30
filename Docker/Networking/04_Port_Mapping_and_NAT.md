# 📌 Topic: Port Mapping and NAT (Userland Proxy)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Port mapping (`-p 80:3000`) is like a call forwarding service. When someone calls your host on port 80, the call is forwarded to the container on port 3000.
**Expert**: Port mapping is an implementation of **DNAT (Destination Network Address Translation)**. Docker uses two mechanisms to achieve this: **IPTables rules** (for high-performance kernel-level forwarding) and the **Userland Proxy** (a fallback process called `docker-proxy`). Staff-level engineering requires understanding that while the Userland Proxy is safe, it is extremely inefficient and can cause performance bottlenecks in high-concurrency environments. Modern systems should rely almost exclusively on IPTables for port forwarding.

## 🏗️ Mental Model
- **IPTables (Kernel)**: A high-speed sorting machine in a factory. It sees a box (packet) and instantly flings it onto the correct conveyor belt without stopping it.
- **Userland Proxy (User-space)**: A worker who picks up every box, reads the label, carries it across the room, and puts it on another belt. Much slower and more tiring.

## ⚡ Actual Behavior
- **External Traffic**: When a request hits the host on port 80, the kernel checks the `PREROUTING` chain in IPTables. It finds a match and changes the destination IP to the container's IP.
- **Loopback Traffic**: If you are *on the host* and try to connect to `localhost:80`, IPTables might miss it. This is where `docker-proxy` usually steps in to catch the traffic and forward it.

## 🔬 Internal Mechanics (The two paths)
1. **The Kernel Path (DOCKER Chain)**: Docker adds a custom chain to the `nat` table. Rules look like: `DNAT tcp --anywhere --anywhere tcp dpt:80 to:172.17.0.2:3000`. This is the "fast path."
2. **The Proxy Path (`docker-proxy`)**: For every mapped port, Docker spawns a small Go process. This process listens on the host port and pipes data to the container via a socket. You can see these with `ps aux | grep docker-proxy`.

## 🔁 Execution Flow
1. Packet arrives at Host NIC (Port 80).
2. Kernel checks IPTables `nat` table.
3. Match found: Rewrite packet to Destination `172.17.0.2:3000`.
4. Kernel routes packet to the `docker0` bridge.
5. Packet arrives at Container.

## 🧠 Resource Behavior
- **Memory**: Every `docker-proxy` process consumes ~5-10MB of RAM. If you map 1,000 ports, you waste 10GB of RAM.
- **CPU**: The Userland Proxy adds context-switch overhead for every packet, increasing latency.

## 📐 ASCII Diagrams (REQUIRED)

```text
       PORT MAPPING FLOW
       
[ Internet ] --( Port:80 )--> [ Host NIC ]
                                 |
           +---------------------+---------------------+
           |                                           |
 [ IPTables DNAT ] (Fast)               [ docker-proxy ] (Slow)
           |                                           |
           +---------------------+---------------------+
                                 |
                       [ Container eth0:3000 ]
```

## 🔍 Code (Checking NAT Rules)
```bash
# 1. Run a container with mapping
docker run -d -p 8080:80 nginx

# 2. See the kernel-level NAT rules
sudo iptables -t nat -L DOCKER -n

# 3. See the Userland Proxy process
ps aux | grep docker-proxy

# 4. Disable Userland Proxy (Advanced Optimization)
# Edit /etc/docker/daemon.json
# { "userland-proxy": false }
```

## 💥 Production Failures
- **The "Source IP Masking"**: Because of the way NAT works, your application inside the container might see the **Host's Bridge IP** as the source of all traffic instead of the **Actual User's IP**.
  *Fix*: Use `proxy_protocol` or look for the `X-Forwarded-For` header if using a Load Balancer (ALB/Nginx).
- **Port Conflicts**: You try to start two containers on port 80. The second fails because the host port is already "bound" by the first container's proxy or IPTables rule.

## 🧪 Real-time Q&A
**Q: Why does Docker still have the `docker-proxy` if IPTables is faster?**
**A**: Compatibility. Some older Linux kernels or specific configurations (like loopback routing) don't handle IPTables DNAT perfectly. The proxy is a "fail-safe" that ensures port mapping works 100% of the time, even if it's slower.

## ⚠️ Edge Cases
- **Expose vs Publish**: 
  - `EXPOSE 80` (Dockerfile): Purely documentation. It does NOT open ports.
  - `-p 80:80` (Runtime): Actually creates the NAT rules and opens the port.

## 🏢 Best Practices
- **Explicit Binding**: Use `-p 127.0.0.1:8080:80` to only allow local traffic. By default, `-p 80:80` binds to `0.0.0.0` (accessible from the whole internet!).
- **Disable Userland Proxy**: On high-performance production servers, set `"userland-proxy": false` to save RAM and reduce latency.
- **Use Host Networking for Speed**: If you have a ultra-high-traffic app (like a database), use `--network host` to bypass NAT entirely (but you lose isolation).

## ⚖️ Trade-offs
| Forwarding Method | Performance | Compatibility |
| :--- | :--- | :--- |
| **IPTables** | **High** | Medium |
| **docker-proxy** | Low | **High** |

## 💼 Interview Q&A
**Q: How does Docker forward traffic from the host to a container?**
**A**: Docker primarily uses **IPTables DNAT (Destination Network Address Translation)** rules. When a packet arrives on a mapped host port, the kernel rewrites the packet's destination to the container's private IP and port. Additionally, Docker runs a **Userland Proxy** process for each port as a fallback mechanism to handle cases where kernel-level routing might fail (like local loopback traffic).

## 🧩 Practice Problems
1. Map a port and find the corresponding rule in `iptables -t nat -S`.
2. Disable the `userland-proxy` in `daemon.json` and see if your `-p` mapping still works for external traffic.
3. Use `netstat -tulpn` on the host to see which process is listening on the mapped port.

---
Prev: [03_Service_Discovery_and_DNS.md](./03_Service_Discovery_and_DNS.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Connection_Lifecycle_TCP_TLS.md](./05_Connection_Lifecycle_TCP_TLS.md)
---
