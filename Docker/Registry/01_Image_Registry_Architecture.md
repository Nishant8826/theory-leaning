# 📌 Topic: Image Registry Architecture (Distribution)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: An Image Registry is like an App Store for Docker images. You "push" images to it and "pull" them down to other servers. Docker Hub is the most famous one.
**Expert**: An Image Registry is a **Content-Addressable Storage (CAS)** system compliant with the **OCI Distribution Specification**. It consists of two main parts: the **Registry API** (which handles authentication and manifest management) and the **Storage Backend** (where the actual binary layers are stored, like S3 or a local disk). Staff-level engineering requires understanding how registries handle **Deduplication** (only storing a shared layer once across thousands of images) and how **Pull-Through Caching** can drastically reduce the load on your external network.

## 🏗️ Mental Model
- **The Library**: The Registry is a library.
- **Manifest**: The library catalog card. It tells you which books (layers) belong to a specific image.
- **Layers**: The actual books. If 100 images use the same "Ubuntu" layer, the library only keeps one copy of that book on the shelf.

## ⚡ Actual Behavior
- **Deduplication**: When you push an image, the Docker client first sends the SHA256 hash of each layer. If the registry already has that hash, it responds with "Layer already exists," and the client skips the upload. This saves massive amounts of bandwidth.
- **Immutability**: Once a layer is pushed with a specific hash, it can never be changed. If you change 1 byte, the hash changes, and it's a new layer.

## 🔬 Internal Mechanics (OCI Spec)
1. **The Manifest**: A JSON file listing the image configuration and the layers (digests and sizes).
2. **Blobs**: The actual compressed tarballs of the layers, identified by their SHA256 digest.
3. **Tags**: Human-readable pointers (like `v1.0`) to a specific manifest. Tags are mutable; digests are not.
4. **Authentication**: Uses JWT (JSON Web Tokens) to verify that the client has permission to push/pull from a specific "Namespace" (Repository).

## 🔁 Execution Flow (The Pull)
1. Client: `GET /v2/my-app/manifests/v1`.
2. Registry: Returns the Manifest JSON.
3. Client: Parses manifest, identifies missing layers.
4. Client: `GET /v2/my-app/blobs/sha256:...` for each missing layer.
5. Registry: Streams the binary blobs.
6. Client: Extracts blobs to the local storage engine.

## 🧠 Resource Behavior
- **Bandwidth**: The biggest resource consumer. Public registries like Docker Hub often implement "Rate Limiting" to prevent abuse.
- **Storage**: Registries need high-durability storage (like S3) to ensure images aren't lost.

## 📐 ASCII Diagrams (REQUIRED)

```text
       REGISTRY ARCHITECTURE
       
[ Docker Client ] <--( HTTPS API )--> [ Registry API ]
                                          |
          +-------------------------------+-----------------------+
          |                               |                       |
 [ Manifest Store ]               [ Blob Store ]          [ Auth / Redis ]
 (Metadata / JSON)                (S3 / Layer Data)       (Permissions)
          |                               |
    (Deduplicated)                  (Deduplicated)
```

## 🔍 Code (Running a Private Registry)
```bash
# 1. Start a local registry
docker run -d -p 5000:5000 --name registry registry:2

# 2. Tag an image for the local registry
docker tag my-app:latest localhost:5000/my-app:v1

# 3. Push to local registry
docker push localhost:5000/my-app:v1

# 4. Inspect the registry catalog
curl http://localhost:5000/v2/_catalog
```

## 💥 Production Failures
- **The "Registry Outage"**: Your CI/CD pipeline pushes a new image, but the registry is down. Production deployments fail because the servers can't pull the image.
  *Fix*: Use a high-availability registry (ECR, GCR) or a local pull-through cache.
- **Layer Corruption**: A network blip during upload results in a corrupted blob. Docker pull fails with "digest mismatch."
  *Fix*: Registries perform checksum verification on every upload to prevent this.

## 🧪 Real-time Q&A
**Q: What is the difference between a Repository and a Registry?**
**A**: A **Registry** is the server (e.g., Docker Hub). A **Repository** is a collection of related images inside that registry (e.g., `nginx`). An **Image** is a specific version inside that repository identified by a tag or digest (e.g., `nginx:alpine`).

## ⚠️ Edge Cases
- **Insecure Registries**: By default, Docker only talks to registries over HTTPS. To use a local registry over HTTP, you must add it to `insecure-registries` in `daemon.json`.

## 🏢 Best Practices
- **Use Private Registries for Corporate Code**: Never push sensitive code to public Docker Hub.
- **Clean up old images**: Use a lifecycle policy to delete images older than 30 days that aren't tagged `prod`.
- **Scan on Push**: Use registries (like ECR or Harbor) that automatically scan images for vulnerabilities as soon as they are uploaded.

## ⚖️ Trade-offs
| Type | Speed | Security | Cost |
| :--- | :--- | :--- | :--- |
| **Public Hub** | Medium | Low | **Low** |
| **Self-Hosted** | **High** | High | Medium (Ops) |
| **Cloud Managed**| High | **Highest** | High |

## 💼 Interview Q&A
**Q: How does a Docker Registry save disk space when storing thousands of different images?**
**A**: It uses **Content-Addressable Storage** and **Layer Deduplication**. Every layer is identified by a unique SHA256 hash. If 500 different images are all based on the same `ubuntu:22.04` layer, the registry only stores that layer once. The image manifests for those 500 images all simply point to the same layer digest. This significantly reduces storage costs and speeds up uploads/downloads.

## 🧩 Practice Problems
1. Set up a private registry with basic authentication and TLS.
2. Push three different images that share the same base layer. Verify that the base layer was only uploaded once.
3. Use the Registry API (via `curl`) to list all tags for a repository.

---
Prev: [05_Scaling_with_Compose.md](../Compose/05_Scaling_with_Compose.md) | Index: [00_Index.md](../00_Index.md) | Next: [02_Self_Hosted_Harbor.md](./02_Self_Hosted_Harbor.md)
---
