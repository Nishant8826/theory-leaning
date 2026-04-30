# 📌 Topic: Registry and Image Distribution

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are an **Author**. 
- You write a book (The Image) on your laptop. 
- To let the world read it, you upload it to a **Library** (The Registry).
- When a reader wants to read it, they go to the library and "Check out" (Pull) a copy.

**Docker Hub** is the world's biggest library. But you can also build your own **Private Library** if you don't want the world to see your secret books.

🟡 **Practical Usage**
-----------------------------------
### 1. Logging in
```powershell
docker login
```

### 2. Tagging for a Registry
Before you can push, you must "Label" the book for the correct library shelf.
```powershell
# Format: <registry_url>/<username>/<repository>:<tag>
docker tag my-app:latest myusername/my-app:v1.0
```

### 3. Pushing the Image
```powershell
docker push myusername/my-app:v1.0
```

### 4. Pulling on a server
```bash
docker pull myusername/my-app:v1.0
```

🔵 **Intermediate Understanding**
-----------------------------------
### Public vs. Private
- **Docker Hub**: Public and free for open source.
- **AWS ECR / GCP GCR / Azure ACR**: Private, secure, and integrated with your cloud provider.
- **Self-hosted (Harbor)**: Your own server inside your company.

### The "Latest" Tag Trap
If you use `image: my-app:latest`, you never know which version is running. 
**Best Practice**: Always use **Semantic Versioning** (v1.0.1) or the **Git Commit Hash** as your tag.

🔴 **Internals (Advanced)**
-----------------------------------
### The Registry API (V2)
When you run `docker pull`, Docker doesn't just download a single file. 
1. It asks the Registry for the **Manifest** (A JSON file listing all layers).
2. It checks its local cache: "Do I already have Layer A?".
3. It only downloads the layers it is missing.
This makes pushing and pulling extremely fast for small updates.

### Content-Addressable Storage (CAS)
If you push two different images that both use `ubuntu:22.04`, the Registry only stores the Ubuntu layers **once**. It uses the **SHA256 Hash** of the layer to identify it.

⚫ **Staff-Level Insights**
-----------------------------------
### Air-Gapped Environments
Some high-security companies (Banks, Military) have **No Internet**. 
**Staff Strategy**: Use a "Jump Server" to download images to a `.tar` file, physically move it on a USB drive, and use `docker load` on the private network.
```bash
# Save image to file
docker save my-app:v1.0 > my-app.tar
# Load on other side
docker load < my-app.tar
```

### Registry Mirrors and Caching
If you have 1000 servers pulling from Docker Hub at the same time, you might hit "Rate Limits."
**Staff Solution**: Set up a **Registry Mirror** (Pull-through cache) inside your network. Your servers pull from the mirror, and the mirror pulls from Docker Hub only once.

🏗️ **Mental Model**
A Registry is a **Warehouse** for your image snapshots.

⚡ **Actual Behavior**
Docker Hub has a **Rate Limit** for free users (e.g., 100 pulls every 6 hours). If you hit this limit, your production deployments will fail.

🧠 **Resource Behavior**
- **Bandwidth**: Pushing/Pulling uses massive amounts of network traffic. Keep your images small!

💥 **Production Failures**
- **"Image not found"**: You forgot to `docker login` on the new server.
- **"Manifest unknown"**: You tried to pull a tag that was deleted or never pushed.
- **Quota Exceeded**: Your CI/CD pipeline ran too many builds and hit the Docker Hub rate limit.

🏢 **Best Practices**
- Use **Immutable Tags** (don't overwrite `v1.0`).
- Clean up old tags in your registry to save money on storage.
- Use a **Private Registry** for anything that isn't open source.

🧪 **Debugging**
```bash
# See the layers being pushed/pulled
docker push my-app:v1.0 --verbose

# Check which registries you are logged into
cat ~/.docker/config.json
```

💼 **Interview Q&A**
- **Q**: What is the difference between a Repository and a Registry?
- **A**: A Registry is a collection of Repositories (like Docker Hub); a Repository is a collection of different versions (tags) of the same image.
- **Q**: Why is it dangerous to use the `latest` tag in production?
- **A**: Because it is not reproducible; the `latest` image today might be different from the `latest` image tomorrow.

---
Prev: [24_Compose_Profiles_and_Environment_Variables.md](../Orchestration/24_Compose_Profiles_and_Environment_Variables.md) | Index: [00_Index.md](../00_Index.md) | Next: [../Internals/25_Linux_Namespaces_The_Isolation_Engine.md](../Internals/25_Linux_Namespaces_The_Isolation_Engine.md)
---
