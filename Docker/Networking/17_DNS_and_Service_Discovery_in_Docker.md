# 📌 Topic: DNS and Service Discovery in Docker

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are in a **Company**. 
- You don't want to memorize everyone's desk number (IP address) because people move desks all the time.
- Instead, you use a **Directory**. You look up "Marketing Department" and the directory tells you where they are today.

In Docker, **Service Discovery** is that directory. 
If you have a container named `database`, your code doesn't need to know its IP (like `172.18.0.5`). Your code just connects to the name `database`. Docker's built-in DNS handles the rest.

🟡 **Practical Usage**
-----------------------------------
### The Requirement
Internal DNS **only works on custom networks**. It does not work on the default `bridge` network.

```powershell
# 1. Create a network
docker network create my-net

# 2. Start the database with a name
docker run -d --name my-db --network my-net mongo

# 3. Start the app on the same network
docker run -it --network my-net alpine sh

# 4. Inside the app, you can ping the DB by name!
/ # ping my-db
PING my-db (172.20.0.2): 56 data bytes
64 bytes from 172.20.0.2: seq=0 ttl=64 time=0.076 ms
```

🔵 **Intermediate Understanding**
-----------------------------------
### How it works
1. Every container has a file at `/etc/resolv.conf`.
2. Docker points this file to a special internal IP address (`127.0.0.11`).
3. This is the **Docker Embedded DNS Server**.
4. If you ask for a name like `my-db`, the DNS server returns the container's internal IP.
5. If you ask for `google.com`, the DNS server forwards the request to your host's DNS.

### Network Aliases
One container can have multiple names.
```bash
docker run -d --network my-net --network-alias search-engine elasticsearch
```
Now, other containers can reach it using the name `search-engine` or its own name.

🔴 **Internals (Advanced)**
-----------------------------------
### DNS Round-Robin (Load Balancing)
If you have multiple containers with the same **Alias**, Docker's DNS will return all their IPs in a random order every time you ask. This is a basic form of **Load Balancing**.

### The `127.0.0.11` Magic
How does Docker catch traffic going to `127.0.0.11`?
It uses **iptables rules** inside the container's namespace to intercept DNS packets (Port 53) and send them to the Docker Engine's management process.

⚫ **Staff-Level Insights**
-----------------------------------
### Search Domains and Performance
In large systems, if you look up a name that doesn't exist, the DNS might try adding suffixes (like `my-app.internal`, `my-app.local`) before giving up. This is called the "NDOTS" problem.
**Staff Tip**: If your app is doing thousands of DNS lookups per second, set `ndots:1` in your container configuration to skip unnecessary searches and reduce latency.

### CoreDNS
In Kubernetes, Docker's simple DNS is replaced by **CoreDNS**, which is much more powerful and can handle complex routing rules based on the "Namespace" or "Service" type.

🏗️ **Mental Model**
Docker DNS is a **Smart Phonebook** that updates itself automatically.

⚡ **Actual Behavior**
When a container starts or stops, Docker instantly updates its internal DNS records. There is no "propagation delay."

🧠 **Resource Behavior**
- **Memory**: The embedded DNS server is very tiny and part of the Docker Daemon.

💥 **Production Failures**
- **"Unknown Host" on Default Bridge**: You switched from a custom network to the default bridge, and your app stopped finding the database.
- **DNS Cache Poisoning/Stale Cache**: Some apps (like Java) cache DNS lookups **forever**. If your database container restarts and gets a new IP, the Java app will keep trying the old IP until you restart the Java app.
  - **Fix**: Set `networkaddress.cache.ttl=60` in Java security settings.

🏢 **Best Practices**
- Always use **User-defined networks**.
- Use descriptive container names or `--network-alias`.
- Don't hardcode IP addresses in your code or config files.

🧪 **Debugging**
```bash
# Check the DNS settings inside a container
docker exec <id> cat /etc/resolv.conf

# Use 'nslookup' to test resolution
docker exec <id> nslookup my-db
```

💼 **Interview Q&A**
- **Q**: Does container name resolution work on the default bridge network?
- **A**: No. It only works on user-defined (custom) networks.
- **Q**: What is the IP of the Docker embedded DNS server?
- **A**: `127.0.0.11`.

---
Prev: [16_Port_Mapping_and_NAT_Internals.md](16_Port_Mapping_and_NAT_Internals.md) | Index: [00_Index.md](../00_Index.md) | Next: [18_Advanced_Networking_Overlay_and_Macvlan.md](18_Advanced_Networking_Overlay_and_Macvlan.md)
---
