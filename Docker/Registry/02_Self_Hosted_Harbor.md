# 📌 Topic: Self-Hosted Harbor (Enterprise Registry)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Harbor is a high-end, self-hosted image registry. It's like having your own private Docker Hub with extra features like security scanning, role-based access, and image signing.
**Expert**: Harbor is a **Cloud Native Computing Foundation (CNCF)** graduated project that extends the standard Docker Registry with an enterprise-grade management layer. It provides **Multi-tenant Isolation**, **RBAC (Role-Based Access Control)**, **Vulnerability Scanning** (via Trivy), and **Image Replication** (syncing images between different data centers). Staff-level engineering requires mastering Harbor's **Garbage Collection** policies, **Robot Accounts** for CI/CD, and **P2P Distribution** (via Dragonfly) to handle massive pull bursts across thousands of nodes.

## 🏗️ Mental Model
- **Docker Registry**: A bare-bones file cabinet for images.
- **Harbor**: A high-security warehouse with armed guards (Auth), a medical inspector (Scanner), a digital notary (Cosign), and a logistics team (Replication).

## ⚡ Actual Behavior
- **Project-based Isolation**: Images are organized into "Projects." You can give the "Frontend Team" access to one project and the "Backend Team" access to another.
- **Immutable Tags**: Harbor can prevent users from overwriting tags (e.g., once `v1.0` is pushed, it can't be changed). This prevents accidental production breakages.

## 🔬 Internal Mechanics (The Harbor Stack)
1. **Nginx**: The entry point for all API and UI traffic.
2. **Core**: The main logic (Projects, Auth, Quotas).
3. **Job Service**: Handles long-running tasks like scanning, replication, and garbage collection.
4. **Registry (v2)**: The underlying standard Docker Distribution registry.
5. **Database (Postgres)**: Stores metadata, user info, and audit logs.
6. **Redis**: Used for caching and as a job queue.

## 🔁 Execution Flow (The "Secure Push")
1. Developer logs in via Harbor UI (OIDC/LDAP integration).
2. Developer pushes `my-app:v1`.
3. Harbor intercepts the push and stores the image.
4. Harbor triggers the **Trivy Scanner** automatically.
5. If critical vulnerabilities are found, Harbor can **block the pull** of that image.
6. Harbor signs the image using **Cosign/Notary**.

## 🧠 Resource Behavior
- **Disk Space**: Harbor can grow to petabytes. It requires regular **Garbage Collection** to delete unreferenced blobs (layers from deleted images).
- **CPU**: Vulnerability scanning is CPU-heavy. Large images can take minutes to scan.

## 📐 ASCII Diagrams (REQUIRED)

```text
       HARBOR ENTERPRISE ARCHITECTURE
       
[ Client ] --> [ Nginx ] --> [ Harbor Core ]
                                |
          +---------------------+-----------------------+
          |                     |                       |
 [ Database ]           [ Redis Queue ]        [ Docker Registry ]
 (Metadata)             (Scan Jobs)            (Binary Blobs)
                                |                       |
                        [ Trivy Scanner ]       [ S3 / Local Disk ]
```

## 🔍 Code (Harbor CLI and Robots)
```bash
# 1. Login with a Robot Account (Best practice for CI/CD)
# Robot accounts have long-lived tokens and limited scope
docker login myharbor.com -u 'robot$ci-builder' -p 'SECRET_TOKEN'

# 2. Push to a specific project
docker tag my-app:v1 myharbor.com/production/my-app:v1
docker push myharbor.com/production/my-app:v1

# 3. Trigger manual Garbage Collection (CLI/API)
# (Usually done via Harbor UI or Cron)
```

## 💥 Production Failures
- **The "Full Disk" Deadlock**: Harbor's database thinks an image exists, but the storage backend (S3) was accidentally cleared. Pulls fail with 404, and Harbor enters an inconsistent state.
- **OIDC Desync**: The connection between Harbor and your company's identity provider (Okta/AD) breaks. No one can push or pull, halting all deployments.
  *Fix*: Always have a local "admin" user as a backup.

## 🧪 Real-time Q&A
**Q: Why use Harbor instead of just ECR or GCR?**
**A**: 1. **Cost**: If you have petabytes of images, cloud transfer fees and storage can be astronomical. 2. **Privacy**: Some industries (Defense/Gov) cannot store code on public clouds. 3. **Governance**: Harbor provides more granular control over scanning policies and replication than basic cloud registries.

## ⚠️ Edge Cases
- **Garbage Collection (GC)**: By default, Harbor's GC is manual or scheduled. If you push 100 images a day and never run GC, your disk will fill up with "orphaned" layers from deleted tags.

## 🏢 Best Practices
- **Use Robot Accounts**: Never use personal credentials in Jenkins or GitHub Actions.
- **Enable Content Trust**: Only allow signed images to be pushed to production projects.
- **Automated Replication**: Use Harbor to mirror images from your Build region to your Deployment regions automatically.

## ⚖️ Trade-offs
| Feature | Docker Registry | Harbor |
| :--- | :--- | :--- |
| **Complexity** | **Low** | High |
| **Security Scanning**| None | **Built-in** |
| **RBAC** | Basic | **Advanced** |
| **Storage** | Local/S3 | Local/S3/Azure/GCS |

## 💼 Interview Q&A
**Q: How does Harbor's Garbage Collection work and why is it important?**
**A**: Harbor's storage driver uses a "soft delete" for images. When you delete a tag in the UI, the binary layers (blobs) remain on the disk. Garbage Collection is a two-phase process: 1. It identifies which blobs are no longer referenced by any manifest. 2. It physically deletes those blobs from the storage backend. It is critical for cost management and preventing disk exhaustion, especially in CI/CD environments where thousands of temporary "feature-branch" images are pushed and deleted every week.

## 🧩 Practice Problems
1. Install Harbor using the Helm chart or Docker Compose.
2. Create a "Project" and a "Robot Account". Push an image and verify it is scanned for vulnerabilities.
3. Configure a "Replication Rule" to pull an image from Docker Hub into your private Harbor project automatically.

---
Prev: [01_Image_Registry_Architecture.md](./01_Image_Registry_Architecture.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_Pull_Through_Caching.md](./03_Pull_Through_Caching.md)
---
