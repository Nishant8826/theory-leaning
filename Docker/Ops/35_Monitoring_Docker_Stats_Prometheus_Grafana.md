# 📌 Topic: Monitoring: Docker Stats, Prometheus, and Grafana

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are a **Nurse** in a hospital.
- **`docker stats`**: Is like checking a patient's pulse and temperature **manually**. You see it right now, but you don't know what it was an hour ago.
- **Prometheus**: Is like the **Heart Monitor** machine. It records the pulse every second and saves it in a database.
- **Grafana**: Is the **Big Screen** at the nurse's station that shows beautiful graphs and sounds an alarm if the heart stops.

Monitoring allows you to see how much CPU and RAM your containers are using over time, so you can catch problems before the app crashes.

🟡 **Practical Usage**
-----------------------------------
### 1. The built-in way (Live)
```powershell
docker stats
```
This shows: Container ID, CPU %, MEM Usage, NET I/O, BLOCK I/O.

### 2. The Professional way (Modern Stack)
Most engineers use the **Prometheus + cAdvisor + Grafana** stack.
- **cAdvisor**: A Google tool that runs as a container and "looks" at all your other containers to collect metrics.
- **Prometheus**: Pulls the data from cAdvisor every 15 seconds.
- **Grafana**: Connects to Prometheus to draw the graphs.

**A simple `docker-compose.yml` for monitoring:**
```yaml
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8080:8080"
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
```

🔵 **Intermediate Understanding**
-----------------------------------
### Metrics vs. Logs
- **Logs**: "The user clicked the button at 10:01 AM" (Event data).
- **Metrics**: "CPU is at 45%" (Numerical data).

### Pull vs. Push
- **Prometheus (Pull)**: The server goes to each container and asks "How are you doing?". This is the standard for Docker.
- **InfluxDB (Push)**: The containers send their own data to the server.

🔴 **Internals (Advanced)**
-----------------------------------
### Where does cAdvisor get data?
It reads the **Cgroup files** we talked about in Chapter 26!
- It looks at `/sys/fs/cgroup/memory/docker/<id>/memory.usage_in_bytes`.
- It converts those raw kernel numbers into a format Prometheus understands (Prometheus Exposition Format).

### Docker Engine Metrics
The Docker Engine itself can export metrics about its own health.
You have to enable it in `/etc/docker/daemon.json`:
```json
{
  "metrics-addr": "127.0.0.1:9323",
  "experimental": true
}
```

⚫ **Staff-Level Insights**
-----------------------------------
### Alerting Rules
Don't just watch graphs. 
**Staff Strategy**: Set up **Alertmanager**. 
- Rule: "If CPU > 90% for more than 5 minutes, send a message to Slack."
- Rule: "If a production container restarts more than 3 times in 1 hour, call the engineer on duty (PagerDuty)."

### High Cardinality
If you have 10,000 containers restarting every minute, your Prometheus database will explode because every container ID is a new "unique tag."
**Staff Tip**: Aggregate your metrics by **Image Name** or **Service Name** instead of individual Container IDs.

🏗️ **Mental Model**
Monitoring is the **Dashboard** of your car. You don't wait for the engine to smoke; you watch the oil gauge.

⚡ **Actual Behavior**
Monitoring tools usually add about **1-3% CPU overhead** to your server because they are constantly reading files and sending data over the network.

🧠 **Resource Behavior**
- **Prometheus Storage**: Metrics use very little disk space compared to logs. You can store years of metrics in just a few Gigabytes.

💥 **Production Failures**
- **"Metric Blindness"**: You are monitoring CPU but not **Disk I/O**. Your app is slow because the database can't read from the disk, but your dashboard looks "Green."
- **Prometheus OOM**: Prometheus tries to load too many metrics into RAM and crashes, leaving you blind right when your app is also crashing.

🏢 **Best Practices**
- Monitor the **4 Golden Signals**: Latency, Traffic, Errors, and Saturation (CPU/RAM).
- Use **Grafana Dashboards** from the community (e.g., Dashboard ID 142 for Docker).
- Keep your monitoring tools on a **separate server** from your app, so if the app server crashes, the monitor stays alive to tell you why.

🧪 **Debugging**
```bash
# See raw metrics from cAdvisor
curl localhost:8080/metrics

# Check if Prometheus can reach your containers
# Go to http://localhost:9090/targets
```

💼 **Interview Q&A**
- **Q**: What is the purpose of cAdvisor?
- **A**: To collect, aggregate, and export resource usage and performance data from running containers.
- **Q**: What is the difference between Prometheus and Grafana?
- **A**: Prometheus stores the data; Grafana visualizes it.

---
Prev: [34_Logging_Drivers_and_Aggregation.md](34_Logging_Drivers_and_Aggregation.md) | Index: [00_Index.md](../00_Index.md) | Next: [36_Debugging_Production_Incidents.md](36_Debugging_Production_Incidents.md)
---
