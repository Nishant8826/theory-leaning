# 📌 Topic: Service Discovery and DNS (Embedded Resolver)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Service Discovery is like a contact list for your containers. Instead of remembering that the Database is at `172.17.0.5`, your API can just ask for "db" and Docker will provide the current IP address.
**Expert**: Docker implements an **Embedded DNS Server** at the IP address `127.0.0.11` for every container on a user-defined network. This resolver is a recursive DNS server that first checks the Docker Engine's internal map of container names to IPs. If no match is found, it forwards the request to the host's configured DNS servers. Staff-level engineering requires understanding **VIP-based Load Balancing** vs **DNS Round-Robin** and how to handle DNS caching in application runtimes (like Java/Node).

## 🏗️ Mental Model
- **The Operator**: In the old days, you picked up a phone and said "Connect me to the Police." The operator (Docker DNS) looked at their board and plugged your wire into the correct socket. You didn't need to know the direct phone number of the police station.

## ⚡ Actual Behavior
- **Dynamic Updates**: If a container crashes and restarts with a new IP, Docker updates the internal DNS record instantly. Your application doesn't need to restart; it just resolves the name again.
- **Service Aliases**: A container can have multiple names (`--network-alias`). This is useful for migrating services (e.g., a container responds to both `old-api` and `new-api`).

## 🔬 Internal Mechanics (127.0.0.11)
1. **IPTables Rule**: Docker adds an IPTables rule to every container that intercepts DNS queries (Port 53) and sends them to `127.0.0.11`.
2. **Gossip Protocol**: In a multi-host Swarm, DNS records are shared across all nodes via the Gossip protocol.
3. **Virtual IP (VIP)**: For Swarm services, the DNS name resolves to a single VIP. The kernel (via IPVS) then load-balances traffic from that VIP to the individual container IPs.

## 🔁 Execution Flow
1. App: `curl http://orders-db/api`.
2. OS looks at `/etc/resolv.conf` (contains `nameserver 127.0.0.11`).
3. Query `orders-db` goes to Docker's Embedded DNS.
4. Docker DNS looks up the name: `orders-db` -> `10.0.1.5`.
5. App receives `10.0.1.5` and opens a TCP connection.

## 🧠 Resource Behavior
- **Zero Latency**: Since the DNS server is embedded in the Docker Engine process, lookups are extremely fast (<1ms).
- **TTL**: Docker DNS records have a Time-To-Live (TTL) of 0 (usually), meaning they are never cached, ensuring instant updates.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKER EMBEDDED DNS
       
[ Container ] --( Query: "auth" )--> [ 127.0.0.11 ]
      |                                  |
      |                          ( Internal Map )
      |                          - "auth" -> 10.0.1.2
      |                          - "db"   -> 10.0.1.3
      |                                  |
      + <----------( Response: 10.0.1.2 )+
      |
( Connect to 10.0.1.2 )
```

## 🔍 Code (Discovery in Action)
```bash
# 1. Create a network
docker network create my-net

# 2. Run a "server" with a specific name
docker run -d --name my-redis --network my-net redis

# 3. Run a "client" and use the name
docker run --rm --network my-net alpine ping -c 2 my-redis

# 4. Check the resolver config inside the container
docker run --rm --network my-net alpine cat /etc/resolv.conf
# output: nameserver 127.0.0.11
```

## 💥 Production Failures
- **The "Java DNS Cache" Trap**: By default, the JVM (Java) caches DNS lookups *forever*. If your DB container restarts with a new IP, the Java app will keep trying the old IP until the JVM is restarted.
  *Fix*: Set `networkaddress.cache.ttl=60` in the JVM security policy.
- **Search Domain Issues**: Your app pings `myservice`. Docker appends search domains (like `myapp.internal`). If not found, it goes to the internet. If an external site exists with that name, your traffic might go to the wrong place.

## 🧪 Real-time Q&A
**Q: Does Service Discovery work on the default `docker0` bridge?**
**A**: **NO.** This is a common point of confusion. DNS-based service discovery is only enabled on **User-Defined Networks**. On the default bridge, you have to use `--link` (deprecated) or manually manage IP addresses.

## ⚠️ Edge Cases
- **DNS Round Robin**: You can configure a service to return *multiple* IP addresses instead of a VIP (`--endpoint-mode dnsrr`). This is useful for older load balancers or when you want the client to handle the balancing.

## 🏢 Best Practices
- **Use Container Names for internal communication**: Never hardcode IP addresses.
- **Implement Retries**: Network discovery can have a brief blip during container restarts. Your app should retry connections with exponential backoff.
- **Short TTLs**: Ensure your application runtime (Node/Java/Python) is configured to honor short DNS TTLs.

## ⚖️ Trade-offs
| Discovery Method | Scalability | Complexity |
| :--- | :--- | :--- |
| **Static IPs** | Low | Low |
| **Docker DNS (VIP)** | **High** | Medium |
| **External (Consul/Etcd)**| **Highest** | High |

## 💼 Interview Q&A
**Q: What is the IP address 127.0.0.11 in a Docker container?**
**A**: It is the address of the **Docker Embedded DNS Resolver**. Docker intercepts all DNS traffic from the container and routes it to this internal service. It allows containers on the same user-defined network to resolve each other by name. It also handles forwarding external DNS requests to the host's DNS servers (like 8.8.8.8).

## 🧩 Practice Problems
1. Create a network and two containers. Delete one container and recreate it with the same name. Observe that the IP changes but the DNS name still works.
2. Inspect the `/etc/hosts` file of a container. Notice that Docker does NOT use this file for service discovery; it uses the 127.0.0.11 resolver instead.

---
Prev: [02_Overlay_Network.md](./02_Overlay_Network.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Port_Mapping_and_NAT.md](./04_Port_Mapping_and_NAT.md)
---
