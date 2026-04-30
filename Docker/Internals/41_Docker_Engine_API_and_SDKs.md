# 📌 Topic: Docker Engine API and SDKs

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine Docker is a **Self-Driving Car**.
- The `docker` commands you type are the **Steering Wheel**.
- But you can also control the car with a **Remote Control** from your phone.

The **Docker Engine API** is that remote control. 
It allows you to write your own computer programs (in Python, Go, or Javascript) that can start, stop, and build containers automatically. You don't have to type anything; your code does it for you.

🟡 **Practical Usage**
-----------------------------------
### 1. Talking to Docker with `curl`
Docker is just a web server listening on a hidden file (the socket).
```bash
# Ask the Docker Engine for a list of containers
sudo curl --unix-socket /var/run/docker.sock http://localhost/v1.41/containers/json
```

### 2. Using the Python SDK
```python
import docker
client = docker.from_env()

# Start a container from code
container = client.containers.run("nginx", detach=True)
print(f"Started container: {container.id}")
```

### 3. Using the Go SDK (The "Industry Standard")
Most big tools (like Kubernetes and Terraform) use the Go SDK to talk to Docker.

🔵 **Intermediate Understanding**
-----------------------------------
### The Unix Socket
On Linux, the API is exposed at `/var/run/docker.sock`. 
- It is a "Unix Domain Socket" (UDS).
- It is faster and more secure than a standard network port.
- **Security**: Only the `root` user or the `docker` group can talk to it.

### Versioning
The API is versioned (e.g., `v1.41`). This ensures that if you write a program today, it won't break when Docker updates to a new version next year.

🔴 **Internals (Advanced)**
-----------------------------------
### Exposing the API over TCP
You can make your Docker Engine reachable over the network (e.g., Port 2375).
**Staff Warning**: **Never do this without TLS/SSL!** 
If you expose the API over raw TCP, anyone on the internet can become `root` on your server by simply sending a `POST` request to start a privileged container.

### Hijacking and Streams
When you run `docker logs -f`, the API uses a technique called **HTTP Hijacking**. It keeps the connection open forever and "streams" the data directly from the container's stdout to your program.

⚫ **Staff-Level Insights**
-----------------------------------
### Building your own "Internal Heroku"
Staff engineers use the API to build custom deployment platforms for their companies. 
- A developer pushes code.
- A "Manager" app (written in Go) catches the code, calls the Docker API to build an image, and then calls the API to deploy it to a cluster.

### Monitoring with the Events API
The API has a special `/events` endpoint. It streams a message every time a container starts, dies, or crashes.
**Staff Tool**: Write a small "Watcher" app that listens to this stream and sends a Slack alert the exact millisecond a production container fails.

🏗️ **Mental Model**
The Docker API is the **Programmatic Interface** to the container world.

⚡ **Actual Behavior**
The `docker` CLI is actually a very small program. 99% of the work is done by the Daemon after receiving an API call from the CLI.

🧠 **Resource Behavior**
- **Concurrency**: The API can handle hundreds of simultaneous requests, but too many "Build" requests can overwhelm the CPU.

💥 **Production Failures**
- **The "Socket Leak"**: You gave a container access to the Docker Socket, and a bug in the container started 10,000 "Zombie" containers, crashing the server.
- **API Version Mismatch**: Your old Python script is using a version of the API that was removed in the latest Docker update.

🏢 **Best Practices**
- Use **Official SDKs** instead of raw `curl`.
- Use **TLS Certificates** if exposing the API over the network.
- Use **Read-only access** to the socket if possible.

🧪 **Debugging**
```bash
# See the exact API calls the CLI is making
docker --debug ps
```

💼 **Interview Q&A**
- **Q**: What is the Docker Engine API?
- **A**: A REST API used by the CLI and SDKs to communicate with the Docker Daemon.
- **Q**: How do you secure the Docker API over a network?
- **A**: By using HTTPS with Mutual TLS (mTLS) certificates.

---
Prev: [../Scaling/40_High_Availability_and_Disaster_Recovery.md](../Scaling/40_High_Availability_and_Disaster_Recovery.md) | Index: [00_Index.md](../00_Index.md) | Next: [42_Docker_Content_Trust_and_Signatures.md](../Security/42_Docker_Content_Trust_and_Signatures.md)
---
