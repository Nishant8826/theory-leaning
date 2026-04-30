# 📌 Topic: Pull-Through Caching (Performance)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: A Pull-Through Cache is like a proxy for Docker images. The first time you pull an image (like `alpine`), the cache downloads it and gives it to you. The second time anyone pulls it, the cache gives it to them instantly without going to the internet.
**Expert**: Pull-Through Caching is a **Network Optimization** that reduces external bandwidth usage and protects against registry rate limits (like Docker Hub's pull limits). It acts as a local mirror. Staff-level engineering requires configuring the Docker Daemon to use a **Registry Mirror** and understanding the difference between a simple cache (which only mirrors public images) and a full-blown internal registry (which stores your private images). It is essential for large-scale Kubernetes clusters or CI/CD farms where hundreds of nodes might try to pull the same `node:alpine` image simultaneously.

## 🏗️ Mental Model
- **The Water Tank**: Instead of every house in a village running a long pipe to the distant river (Docker Hub), the village builds one big water tank (Cache). The tank fills up from the river, and all the houses get their water from the tank. It's faster and the river doesn't get overwhelmed.

## ⚡ Actual Behavior
- **Speed**: Pulling a 500MB image from a local cache on a 10Gbps local network takes seconds. Pulling it from the internet takes minutes.
- **Reliability**: If Docker Hub goes down or is slow, your local builds and deployments can still proceed using the cached images.

## 🔬 Internal Mechanics (The Mirroring Flow)
1. **The Request**: Client runs `docker pull alpine`.
2. **The Redirection**: If `registry-mirrors` is set in `daemon.json`, the client sends the request to the local cache first.
3. **The Cache Miss**: If the cache doesn't have the image, it fetches it from the upstream registry (e.g., Docker Hub), saves a copy, and streams it to the client.
4. **The Cache Hit**: For all subsequent requests, the cache serves the blobs directly from its local storage.

## 🔁 Execution Flow
1. Client -> `GET /v2/library/alpine/manifests/latest` -> Cache.
2. Cache (Check local) -> Not found.
3. Cache -> `GET /v2/library/alpine/manifests/latest` -> Docker Hub.
4. Docker Hub -> Returns Manifest -> Cache.
5. Cache -> Saves Manifest -> Returns to Client.
6. Client -> Requests Blobs -> Cache.
7. Cache -> Downloads Blobs from Hub -> Saves to Disk -> Streams to Client.

## 🧠 Resource Behavior
- **Disk Space**: The cache can grow quickly. You need a **Retention Policy** to delete images that haven't been pulled in 30 days.
- **Bandwidth**: Dramatically reduced "Egress" (Outbound) traffic costs in cloud environments.

## 📐 ASCII Diagrams (REQUIRED)

```text
       PULL-THROUGH CACHE TOPOLOGY
       
[ Node A ] [ Node B ] [ Node C ]
    |          |          |
    +----------+----------+
               |
      [ Pull-Through Cache ] <---( High Speed Local Link )
               |
      ( External Network )
               |
        [ Docker Hub ]
```

## 🔍 Code (Configuring the Daemon)
```json
// /etc/docker/daemon.json
{
  "registry-mirrors": ["https://my-cache.internal.company.com"]
}
```
*After changing this, you must restart the Docker service: `systemctl restart docker`.*

## 💥 Production Failures
- **The "Stale Manifest"**: The cache has `alpine:latest` from 2 days ago. A new version is released on Docker Hub. The cache might continue to serve the old version until its "TTL" (Time To Live) expires.
  *Fix*: Configure a short TTL for manifests (e.g., 1 hour) but a long TTL for blobs (which never change).
- **Rate Limit Proxying**: You run a cache to avoid Docker Hub rate limits. However, the cache itself uses a single IP address to pull from the Hub. If 1,000 users pull 1,000 *different* images through the cache, the cache's IP will get blocked by Docker Hub.
  *Fix*: Log the cache into a "Pro" Docker Hub account.

## 🧪 Real-time Q&A
**Q: Can a pull-through cache store private images?**
**A**: Generally, no. Most simple pull-through caches (like the official `registry:2` in mirror mode) only work for public Docker Hub images. For private images, you should use a full registry like Harbor with **Proxy Cache** projects.

## ⚠️ Edge Cases
- **Authenticated Pulls**: If you need to pull from a private repository, the cache must have the credentials to that repository, or the client must pass them through the cache (which is complex to set up).

## 🏢 Best Practices
- **Centralize for the Office/Datacenter**: One cache per physical location.
- **Monitor Cache Hit Ratio**: If your hit ratio is < 50%, your cache is either too small or your images are too varied to benefit from caching.
- **Use for CI/CD**: Build runners should *always* use a mirror to prevent "Pull Limit" errors from breaking the build pipeline.

## ⚖️ Trade-offs
| Metric | No Cache | With Pull-Through Cache |
| :--- | :--- | :--- |
| **Pull Speed** | Variable (Internet) | **High (Local)** |
| **Internet Cost** | High | **Low** |
| **Complexity** | **None** | Medium (Requires server) |

## 💼 Interview Q&A
**Q: How do you handle Docker Hub's pull rate limits in a large engineering organization?**
**A**: I implement a **Pull-Through Cache** (Registry Mirror) inside the company's internal network. All developer machines and CI/CD runners are configured to use this mirror. When an image is requested, the cache serves it locally if it's already been pulled, avoiding an external request. For the initial pull, the cache is authenticated with a single **Docker Hub Pro/Business account**, which has much higher limits. This effectively shares the high limits of one account across the entire organization while drastically reducing external bandwidth usage.

## 🧩 Practice Problems
1. Start a `registry:2` container in mirror mode on your laptop.
2. Configure your Docker daemon to use `localhost:5000` as a mirror.
3. Pull `ubuntu:latest`, delete it locally, and pull it again. Compare the times using `time docker pull ubuntu:latest`.

---
Prev: [02_Self_Hosted_Harbor.md](./02_Self_Hosted_Harbor.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Cloud_Registries_ECR_GCR.md](./04_Cloud_Registries_ECR_GCR.md)
---
