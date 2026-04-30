# 📌 Topic: Docker Network Drivers (Bridge, Host, None)

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine your computer is a **Big Island**.
1. **Bridge (Default)**: Your containers live on a **Small Island** nearby. There is a bridge between the islands. If you want to talk to someone on the Small Island, you have to cross the bridge. (Isolated, but reachable).
2. **Host**: Your container lives **inside your own house** on the Big Island. It uses your phone, your address, and your mailbox. (No isolation).
3. **None**: Your container is in a **Submarine** with no radio. It can't talk to anyone, and no one can talk to it. (Total isolation).

🟡 **Practical Usage**
-----------------------------------
### 1. Bridge Network (The Standard)
Used for most apps. Containers can talk to each other if they are on the same bridge.
```powershell
# Default bridge
docker run -d nginx
```

### 2. Host Network
Used for maximum performance (no bridge overhead) or apps that need to manage the host's actual network.
```powershell
# Uses host's port 80 directly
docker run -d --network host nginx
```

### 3. Creating Your Own Network (Best Practice)
Don't use the default bridge! Create your own "Virtual Private Network."
```powershell
# Create a network
docker network create my-app-net

# Attach containers to it
docker run -d --name db --network my-app-net mongo
docker run -d --name web --network my-app-net my-node-app
```
**Benefit**: Containers on the same custom network can talk to each other using their **names** (e.g., Node app can just connect to `mongodb://db:27017`).

🔵 **Intermediate Understanding**
-----------------------------------
### Service Discovery (Internal DNS)
Docker has a built-in DNS server. 
- When `container-A` tries to ping `container-B`, Docker looks up the IP address of `container-B` in its internal database and returns it.
- **Note**: This only works on **User-defined networks**, not the default bridge.

### The `docker0` Interface
On Linux, when you install Docker, a virtual network interface called `docker0` is created. This is the "Bridge."

🔴 **Internals (Advanced)**
-----------------------------------
### Network Namespaces
Each container gets its own **Network Namespace**. This is a private copy of the network stack (IP addresses, routing tables, firewall rules).
- When a container starts, Docker creates a **veth pair** (Virtual Ethernet).
- One end is plugged into the container's namespace (`eth0`).
- The other end is plugged into the host's `docker0` bridge.

### ASCII Diagram: Bridge Networking
```text
[ Container 1 ] (172.17.0.2)      [ Container 2 ] (172.17.0.3)
      |                                  |
    [veth]                             [veth]
      |__________________________________|
                       |
               [ docker0 Bridge ] (172.17.0.1)
                       |
                [ Host Network ]
```

⚫ **Staff-Level Insights**
-----------------------------------
### Host vs. Bridge Performance
The Bridge network uses **NAT** (Network Address Translation). Every packet has to be rewritten as it crosses the bridge. This adds a few microseconds of latency. 
**Staff Tip**: For high-frequency trading apps or high-throughput databases, use `--network host` to save 10-15% network overhead.

### Overlay Networks
When you move to multiple servers (Swarm or Kubernetes), Bridge doesn't work. You need an **Overlay Network** (VXLAN), which creates a "tunnel" between servers so containers on Server A can talk to containers on Server B as if they were on the same switch.

🏗️ **Mental Model**
A Docker network is a **Virtual Switch**.

⚡ **Actual Behavior**
Docker uses **iptables** (Linux firewall) to handle the routing and port forwarding between the host and the containers.

🧠 **Resource Behavior**
- **IP Exhaustion**: A default bridge network usually has a `/16` subnet (65,000 IPs). You are unlikely to run out, but custom networks might have smaller subnets.

💥 **Production Failures**
- **DNS Lookup Failures**: You try to connect to `db` but it fails. 
  - **Reason**: You forgot to put them on the same custom network.
- **Port Conflict**: You run two containers with `--network host`. Both try to listen on port 80. The second one will crash.

🏢 **Best Practices**
- **Never use the default bridge** for production.
- **Isolate your layers**: Put your Web app and DB on the same network, but keep your DB off the public internet.
- Use meaningful names for containers to make DNS easier.

🧪 **Debugging**
```bash
# List all networks
docker network ls

# See which containers are on a network
docker network inspect my-app-net

# Run a ping from inside a container
docker exec -it web ping db
```

💼 **Interview Q&A**
- **Q**: How do two containers on different networks talk to each other?
- **A**: By default, they can't. You must connect one container to both networks or use a routing layer.
- **Q**: What is the advantage of a user-defined bridge over the default one?
- **A**: 1. Automatic DNS resolution by container name. 2. Better isolation.

---
Prev: [../Runtime/14_Resource_Limits_CPU_and_Memory.md](../Runtime/14_Resource_Limits_CPU_and_Memory.md) | Index: [00_Index.md](../00_Index.md) | Next: [16_Port_Mapping_and_NAT_Internals.md](16_Port_Mapping_and_NAT_Internals.md)
---
