# 📌 Topic: High Availability and Disaster Recovery

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are a **Bank**.
- **High Availability (HA)**: You have 10 tellers. If one teller gets sick, the bank stays open and customers don't even notice.
- **Disaster Recovery (DR)**: The bank building catches fire. You have a **Backup Building** in another city where all the money and records are safe, so you can reopen tomorrow.

In Docker, HA means having enough copies of your container so that if a server dies, the website stays up. DR means having a plan to restore your data if the entire cloud provider (like AWS) goes offline.

🟡 **Practical Usage**
-----------------------------------
### 1. High Availability (The "Redundancy" Rule)
**Rule**: Never run only 1 instance of a critical service.
```yaml
# docker-compose.yml for Swarm/K8s
services:
  web:
    image: my-app
    deploy:
      replicas: 3 # Run 3 copies
      update_config:
        parallelism: 1 # Update one at a time
        delay: 10s
```

### 2. Disaster Recovery (The "Backup" Rule)
Data in containers is temporary. Data in Volumes is local.
**Staff Strategy**: Use a script to backup your volumes to an external location (like S3) every night.
```bash
# Backup a volume to a compressed file
docker run --rm -v my-db-data:/data -v $(pwd):/backup alpine \
  tar cvf /backup/backup.tar /data
```

🔵 **Intermediate Understanding**
-----------------------------------
### Healthchecks & Self-Healing
If a container is "Running" but its app is "Frozen," Docker won't know.
**The Solution**: Add a **Healthcheck**. If the healthcheck fails, Docker (or Swarm/K8s) will automatically **Kill and Restart** the container.

### Multi-AZ (Availability Zones)
Don't put all your servers in the same data center.
- AWS has "Zones" (e.g., `us-east-1a` and `us-east-1b`).
- Staff Engineers spread their Docker hosts across at least 3 zones. If one zone loses power, the other two keep the site alive.

🔴 **Internals (Advanced)**
-----------------------------------
### Quorum and Consensus
In a cluster (Swarm or K8s), the "Managers" need to agree on what's happening.
- They use an algorithm called **Raft**.
- To have HA, you need an **Odd Number** of managers (3, 5, or 7). 
- If you have 2 managers and 1 dies, the other one doesn't have "Quorum" and will stop managing the cluster to prevent data corruption.

### State Persistence (Replicated Volumes)
Standard Docker volumes are stuck on one server. 
**The Advanced Solution**: Use **Distributed Storage** (like Ceph, GlusterFS, or Longhorn). These tools copy your volume data to 3 different servers simultaneously. If Server 1 explodes, Server 2 already has the data.

⚫ **Staff-Level Insights**
-----------------------------------
### Chaos Engineering
Don't wait for a disaster.
**Staff Strategy**: Use a tool like **Chaos Monkey**. It randomly kills production containers and servers during the day while everyone is at work.
**Why?** To prove that your HA and Self-healing systems actually work. If the site stays up when Monkey strikes, you can sleep soundly at night.

### The RTO and RPO
- **RTO (Recovery Time Objective)**: How long can the site be down? (e.g., "Back in 5 minutes").
- **RPO (Recovery Point Objective)**: How much data can we lose? (e.g., "Last 1 minute of transactions").
Staff Engineers design the Docker architecture to meet these business numbers.

🏗️ **Mental Model**
- **HA**: Surviving a **Flicker**.
- **DR**: Surviving a **Fire**.

⚡ **Actual Behavior**
Docker Compose does NOT handle HA. If your server dies, your containers stay dead. You need **Swarm** or **Kubernetes** for real HA.

🧠 **Resource Behavior**
- **Overhead**: HA costs 2x or 3x the money because you are running multiple copies of everything.

💥 **Production Failures**
- **The "Split Brain"**: Two halves of your cluster lose connection. Both think they are the leader. They both try to write to the same database, corrupting everything.
- **The "Backup that wasn't"**: You've been backing up your volumes for a year, but you never tried to **Restore** one. When a disaster happens, you find out the backup file is empty or corrupted.

🏢 **Best Practices**
- Always run at least **2 replicas**.
- Use **Healthchecks** in your YAML.
- Test your **Restoration process** once a month.
- Use **managed databases** (like AWS RDS) because they handle HA/DR for you.

🧪 **Debugging**
```bash
# Force a failover to test HA
docker node update --availability drain <manager-node-id>

# Check the health status of all replicas
docker service ps my-app
```

💼 **Interview Q&A**
- **Q**: What is the difference between HA and DR?
- **A**: HA is about keeping the system running during minor failures; DR is about recovering the system after a major catastrophe.
- **Q**: How many managers should a Docker Swarm have for High Availability?
- **A**: An odd number, usually 3 or 5, to maintain quorum.

---
Prev: [39_Cost_Optimization_and_Resource_Tuning.md](39_Cost_Optimization_and_Resource_Tuning.md) | Index: [00_Index.md](../00_Index.md) | Next: DONE
---
