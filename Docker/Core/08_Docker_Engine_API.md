# 📌 Topic: Docker Engine API (The REST Surface)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: When you type `docker ps`, the CLI is just a messenger. It talks to the Docker Engine using a web-like API (REST) over a special file called a "Unix Socket."
**Expert**: The Docker Engine exposes a standard **RESTful API**. This API is the single point of entry for all Docker management. The `docker` CLI is simply an official client of this API. Staff-level engineers leverage this API directly for **Custom Orchestration**, **Dynamic Monitoring**, and **CI/CD Automation**. By communicating directly with `/var/run/docker.sock` (on Linux) or `npipe:////./pipe/docker_engine` (on Windows), you can programmatically control every aspect of the container lifecycle without relying on shell commands.

## 🏗️ Mental Model
- **Docker CLI**: The steering wheel of a car.
- **Docker Engine API**: The engine's computer (ECU). You can turn the wheel to steer, or you can plug a laptop into the ECU to send direct electrical signals to the tires.

## ⚡ Actual Behavior
- **Unix Socket**: By default, the API is not accessible over the network. It uses a local Unix domain socket which is faster and more secure than a TCP socket.
- **HTTP/HTTPS**: You can configure the daemon to listen on a TCP port (usually 2375 or 2376) for remote management, but this MUST be protected with mTLS.

## 🔬 Internal Mechanics (The Socket)
1. **The File**: `/var/run/docker.sock` is a special file type. When you write to it, you are sending data directly to the memory of the `dockerd` process.
2. **Permissions**: Only users in the `docker` group (or root) have permission to write to this socket.
3. **The Protocol**: It uses standard HTTP 1.1. You can literally use `curl` to talk to it.

## 🔁 Execution Flow
1. `docker ps`
2. CLI reads `/var/run/docker.sock`.
3. CLI sends `GET /v1.41/containers/json`.
4. `dockerd` processes the request, queries its internal state, and formats a JSON response.
5. CLI receives JSON and prints a pretty table.

## 🧠 Resource Behavior
- **API Overhead**: Rapid, thousands-per-second polling of the API can cause high CPU usage in `dockerd`. Use the `/events` endpoint for streaming updates instead of polling.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKER API ARCHITECTURE
       
[ docker-cli ]    [ Custom Node.js Script ]    [ Portainer ]
      |                      |                      |
      +-----------+----------+-----------+----------+
                  | (HTTP over Unix Socket)
                  v
       +----------------------------+
       |       Docker Daemon        |
       |  (REST API Server)         |
       +--------------|-------------+
                      v
            [ Container Runtime ]
```

## 🔍 Code (Direct API Interaction)
```bash
# 1. List containers via CURL (The CLI's "hidden" work)
sudo curl --unix-socket /var/run/docker.sock http://localhost/v1.41/containers/json

# 2. Get Engine Info
sudo curl --unix-socket /var/run/docker.sock http://localhost/v1.41/info | jq

# 3. Stream Events (Real-time monitoring)
sudo curl --unix-socket /var/run/docker.sock http://localhost/v1.41/events
```

## 💥 Production Failures
- **The "Socket Leak" Security Hole**: A developer mounts `/var/run/docker.sock` into a Jenkins container so it can build images. A hacker exploits the Jenkins app, talks to the socket, and starts a privileged container to gain root access on the entire host.
  *Fix*: Use **Docker-in-Docker (DinD)** or a dedicated build worker with restricted access.
- **Socket Permissions Reset**: After a system update, the permissions on `docker.sock` change to `600` (root only), causing all non-root scripts and CLI commands to fail.

## 🧪 Real-time Q&A
**Q: Why would I use the API instead of the CLI?**
**A**: When building automation tools. For example, if you are building a custom dashboard to show container health, it is much more efficient to parse JSON from the API than to scrape the output of `docker ps`.

## ⚠️ Edge Cases
- **Version Negotiation**: The CLI and Daemon might be on different versions. They "negotiate" the API version. If you hardcode a version like `v1.41` in a script, it might fail on older Docker versions.

## 🏢 Best Practices
- **Use Official SDKs**: Instead of raw `curl`, use the official Go or Python SDKs.
- **Secure the API**: Never expose the API over TCP without **mTLS (mutual TLS)** certificates. Without encryption, anyone on your network can take full control of your server.

## ⚖️ Trade-offs
| Method | Ease of Use | Automation Capability |
| :--- | :--- | :--- |
| **CLI** | High | Low (Shell parsing is brittle) |
| **SDK/API** | Medium | **Highest (JSON/Native objects)** |

## 💼 Interview Q&A
**Q: How does the Docker CLI communicate with the Docker Daemon?**
**A**: It uses a RESTful API over a Unix Domain Socket located at `/var/run/docker.sock`. It sends standard HTTP requests (GET, POST, DELETE) and receives responses in JSON format. This decoupled design allows the CLI to be on a different machine than the daemon, provided the connection is established over a network-secured TCP socket.

## 🧩 Practice Problems
1. Write a simple Node.js script using the `dockerode` library (or just raw `http` and a socket) to list the names of all running containers.
2. Use `tcpdump` or `socat` to sniff the traffic between the Docker CLI and the socket while running a `docker build`.

---
Prev: [07_BuildKit_Internals.md](./07_BuildKit_Internals.md) | Index: [00_Index.md](../00_Index.md) | Next: [09_System_Performance_Limits.md](./09_System_Performance_Limits.md)
---
