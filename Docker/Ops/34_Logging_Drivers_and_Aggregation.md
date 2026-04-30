# 📌 Topic: Logging Drivers and Aggregation

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you have 100 **Flashlights** (Containers) in a dark forest. 
- If you have to walk to each flashlight to see if it's still working, you will get tired (Checking `docker logs` one by one).
- Instead, you connect each flashlight with a fiber-optic cable to a **Central Screen** (Log Aggregator). Now you can see every light from your control room.

**Logging Drivers** are the "Cables." They decide where the text your app prints goes. 

🟡 **Practical Usage**
-----------------------------------
### 1. Default Driver: `json-file`
This is what you use locally.
```powershell
docker logs my-app
```

### 2. Sending logs to a Central Server (Syslog)
```powershell
docker run --log-driver syslog --log-opt syslog-address=tcp://192.168.1.10:514 nginx
```

### 3. Setting a Global Default
Change the settings for ALL containers on your server by editing `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

🔵 **Intermediate Understanding**
-----------------------------------
### The "Non-Blocking" Strategy
By default, if the log-aggregator is slow or down, Docker will make your app wait until the log is sent. This can **slow down your app**.
**Staff Fix**: Use `mode: non-blocking`. If the log server is busy, Docker will drop the logs instead of slowing down your app.
```json
"log-opts": {
  "mode": "non-blocking",
  "max-buffer-size": "4m"
}
```

### Common Log Aggregators
- **ELK Stack**: Elasticsearch, Logstash, Kibana.
- **EFK Stack**: Same, but with Fluentd.
- **Loki**: Grafana's lightweight logging system.
- **Splunk / Datadog**: Commercial options.

🔴 **Internals (Advanced)**
-----------------------------------
### The stdout/stderr redirection
Docker doesn't "watch" your app's files. It intercepts the **File Descriptors 1 (stdout)** and **2 (stderr)** of the container's PID 1 process. 
If your app writes to a file like `/app/logs/error.log` inside the container, `docker logs` will be **empty**!

### Log Rotation
The `json-file` driver writes to `/var/lib/docker/containers/<id>/<id>-json.log`. Without rotation, this file grows until the disk is full. When rotation is enabled, Docker keeps `max-file` number of files and deletes the oldest one when a new one is created.

⚫ **Staff-Level Insights**
-----------------------------------
### Sidecar Logging
If you have a legacy app that *must* write to a file, how do you get the logs out?
**Staff Strategy**: Use a **Sidecar container**. 
1. App writes to a shared volume (`/var/log/app`).
2. Sidecar container (like Fluent-bit) reads that file and sends it to the central log server.

### GELF (Graylog Extended Log Format)
For high-performance structured logging, use the `gelf` driver. It sends logs in a compressed format, saving network bandwidth compared to raw text.

🏗️ **Mental Model**
Logging is the **Nervous System** of your infrastructure.

⚡ **Actual Behavior**
If you use a non-default driver (like `syslog` or `awslogs`), the `docker logs` command will **stop working** locally! You must check the logs in your central dashboard instead.

🧠 **Resource Behavior**
- **CPU**: Processing and compressing logs for drivers like `fluentd` can use 2-5% of your CPU.
- **Network**: Sending millions of log lines can saturate your network card.

💥 **Production Failures**
- **The "Deadlock" Failure**: A log server goes down, the Docker buffer fills up, and every single container on the server freezes because they are waiting to write a log line.
  - **Fix**: Use `non-blocking` mode.
- **Disk Full**: You forgot to set `max-size`. A debug-heavy app fills the host's disk in 2 hours, crashing the OS.

🏢 **Best Practices**
- **Always set log rotation** in `daemon.json`.
- Log in **JSON format** from your app code (Structured Logging) to make searching easier in Kibana/Grafana.
- Use **Fluent-bit** on the host to collect logs; it's much lighter than Fluentd.

🧪 **Debugging**
```bash
# Check which driver a container is using
docker inspect <id> --format '{{.HostConfig.LogConfig.Type}}'

# See where the log file is on disk (Linux)
docker inspect <id> --format '{{.LogPath}}'
```

💼 **Interview Q&A**
- **Q**: Why would `docker logs` return nothing for a running container?
- **A**: 1. The app might be writing to a file instead of stdout/stderr. 2. A non-default logging driver (like syslog) might be in use.
- **Q**: What is log rotation?
- **A**: The process of limiting log file size and quantity to prevent disk exhaustion.

---
Prev: [33_Docker_in_Jenkins_Pipelines.md](33_Docker_in_Jenkins_Pipelines.md) | Index: [00_Index.md](../00_Index.md) | Next: [35_Monitoring_Docker_Stats_Prometheus_Grafana.md](35_Monitoring_Docker_Stats_Prometheus_Grafana.md)
---
