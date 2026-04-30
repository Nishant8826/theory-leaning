# 📌 Topic: Artifact Management (Versioning and Lifecycle)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Artifact Management is about how you name and store your Docker images. You use "Tags" to keep track of versions like `v1.0`, `v1.1`, or `latest`.
**Expert**: Artifact Management is the implementation of the **Immutable Infrastructure** principle. Once an image is pushed to the registry, it is a "Legal Document" of what was built. Staff-level engineering requires a strict **Versioning Policy** (Semantic Versioning), a **Promotion Workflow** (moving an image from `dev` -> `stage` -> `prod` without rebuilding), and an **Automated Lifecycle** (cleaning up thousands of temporary artifacts to control costs). You must also manage **Metadata** like build numbers, git commits, and license info attached to the image as labels.

## 🏗️ Mental Model
- **The Vineyard**: Every year, a vineyard produces a "Vintage" (Image). The bottle is sealed and labeled with the year and batch (Tag). You don't open the bottle and change the wine; if you want a different wine, you make a new batch. If the wine is good, it is "Promoted" from the basement (Dev) to the top shelf (Prod).

## ⚡ Actual Behavior
- **Immutability**: A tag like `v1.0` should never be deleted or overwritten. If you find a bug, you push `v1.0.1`.
- **Promotion**: Instead of rebuilding the image for production, you simply "Re-tag" the existing image: `docker tag my-app:dev-123 my-app:prod-1.0` and push it. This ensures that the *exact* bits you tested in Dev are what go to Prod.

## 🔬 Internal Mechanics (Labels and Digests)
1. **Labels**: Key-value pairs stored in the image configuration JSON. (e.g., `org.opencontainers.image.revision`).
2. **Digest (SHA256)**: The unique, mathematical fingerprint of the image content. Even if the tag `latest` changes, the digest `sha256:abcd...` will always point to the same binary.
3. **Registry Garbage Collection**: The process of deleting blobs that are no longer referenced by any tag.

## 🔁 Execution Flow (The Promotion)
1. CI builds `my-app:sha-abcdef` (The Git commit hash).
2. Image is deployed to Staging. Tests pass.
3. Release Manager: `docker pull my-app:sha-abcdef`.
4. Release Manager: `docker tag my-app:sha-abcdef my-app:v1.2.0`.
5. Release Manager: `docker push my-app:v1.2.0`.
6. Production pulls `v1.2.0`.

## 🧠 Resource Behavior
- **Storage**: Keeping every single build of every branch can cost thousands of dollars a month in S3 storage.
- **Registry Performance**: Large manifests with thousands of tags can slow down `docker search` and registry UI performance.

## 📐 ASCII Diagrams (REQUIRED)

```text
       ARTIFACT PROMOTION PIPELINE
       
[ BUILD ] -> [ DEV REGISTRY ] -> [ TEST ] -> [ PROD REGISTRY ]
   |                |              |                |
(Binary)       ( my-app:b1 )  ( PASS? )        ( my-app:v1 )
                                   |
                          +--------+--------+
                          |                 |
                   [ RE-TAG ONLY ]   [ NEVER RE-BUILD ]
```

## 🔍 Code (Labeling and Versioning)
```dockerfile
# Adding standard metadata to an image
FROM alpine:3.18
LABEL org.opencontainers.image.authors="engineering@mycompany.com"
LABEL org.opencontainers.image.source="https://github.com/myorg/myapp"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"

# CLI: Passing version at build time
# docker build --build-arg VERSION=1.2.0 --build-arg GIT_COMMIT=$(git rev-parse HEAD) .
```

## 💥 Production Failures
- **The "Latest" Trap**: You use `image: my-app:latest` in your production YAML. A developer pushes a broken experimental version to `latest`. Your production server restarts for a patch, pulls the "New" latest, and crashes.
  *Fix*: Never use `latest` in production. Always use specific versions.
- **Orphaned Images**: Your CI pushes a new image for every single commit. You have 5,000 images in ECR. You reach your storage limit, and the CI fails to push a critical security patch.

## 🧪 Real-time Q&A
**Q: What is the best tagging strategy?**
**A**: Use a combination: 1. **Git Hash** (`:sha-8826...`) for every build. 2. **Build Number** (`:build-456`) for CI tracking. 3. **Semantic Version** (`:v1.2.3`) for formal releases. This gives you traceability and stability.

## ⚠️ Edge Cases
- **Multi-Arch Manifests**: A single tag like `v1.0` can actually point to 5 different images (x86, ARM, etc.). When you re-tag, ensure you are re-tagging the **Manifest List**, not just one specific architecture image.

## 🏢 Best Practices
- **Standardize Labels**: Use the OCI Image Spec labels.
- **Automated Lifecycle**: Delete untagged images after 24 hours. Delete "Branch" images after 7 days.
- **Sign Your Artifacts**: Use Cosign to prove the artifact hasn't been tampered with since it was built.

## ⚖️ Trade-offs
| Tagging Style | Traceability | Stability | Cleanup Effort |
| :--- | :--- | :--- | :--- |
| **Latest** | **Lowest** | **Lowest** | Low |
| **Git SHA** | **Highest** | Medium | **Highest** |
| **SemVer** | Medium | **Highest** | Low |

## 💼 Interview Q&A
**Q: Why is image promotion (re-tagging) better than rebuilding an image for each environment?**
**A**: Rebuilding an image for each environment introduces the risk of **Non-Deterministic Artifacts**. Even if you use the same Dockerfile, a minor change in a base image or a third-party library (e.g., a package being updated on a repository) could result in a production image that is slightly different from the one you tested in staging. By re-tagging a single, verified image, you guarantee that the **Exact Same Bits** are deployed to production, eliminating an entire class of "it worked in staging" bugs.

## 🧩 Practice Problems
1. Write a script that takes an image from a `dev` repository and "Promotes" it to a `prod` repository.
2. Use `docker inspect` to view all the labels on an official image like `nginx`.
3. Set up an ECR Lifecycle Policy to keep only the last 5 images for each tag prefix.

---
Prev: [04_Blue_Green_and_Canary_Deploys.md](./04_Blue_Green_and_Canary_Deploys.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Docker_Swarm_Internals.md](../Orchestration/01_Docker_Swarm_Internals.md)
---
