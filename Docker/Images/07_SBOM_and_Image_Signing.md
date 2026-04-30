# 📌 Topic: SBOM and Image Signing (Supply Chain Security)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Image Signing is like putting a wax seal on a letter. It proves the image really came from you and hasn't been tampered with. An SBOM (Software Bill of Materials) is like the ingredient list on a cereal box—it tells you exactly what libraries and versions are inside your image.
**Expert**: **Software Supply Chain Security** is about ensuring the integrity of the code from "commit to container." An **SBOM** is a machine-readable inventory (in SPDX or CycloneDX format) of every dependency in your image. **Image Signing** (using tools like **Cosign/Sigstore**) uses public-key cryptography to cryptographically sign the image manifest. Staff-level engineering involves enforcing **Admission Controllers** that prevent any unsigned image from running in your production cluster.

## 🏗️ Mental Model
- **SBOM**: The Manifest of a shipping container. It lists every box inside.
- **Image Signing**: The Digital Signature of the inspector who verified the manifest. If the signature is missing or broken, the ship isn't allowed to dock.

## ⚡ Actual Behavior
- **Transparency**: Anyone can run `cosign verify` on your image to confirm it was signed by your company's CI/CD pipeline.
- **Compliance**: Regulated industries (Finance/Healthcare) increasingly require an SBOM for every deployed artifact to prove they aren't running versions of libraries with known vulnerabilities (like Log4j).

## 🔬 Internal Mechanics (Sigstore/Cosign)
1. **The Signature**: Cosign generates a signature of the image's SHA256 digest.
2. **The Registry**: The signature is stored in the Docker Registry alongside the image as a separate OCI artifact.
3. **Keyless Signing**: Using Fulcio and Rekor (Sigstore), you can sign images using an OIDC identity (e.g., your GitHub/Google login) without ever managing private keys.
4. **SBOM Generation**: Tools like `Syft` or `Grype` scan the image layers and generate a JSON file listing every package, license, and version.

## 🔁 Execution Flow (The Secure Pipeline)
1. Developer pushes code.
2. CI builds the Docker image.
3. CI runs `syft <image> -o cyclonedx-json > sbom.json`.
4. CI attaches the SBOM to the image: `cosign attach sbom --sbom sbom.json <image>`.
5. CI signs the image: `cosign sign --key cosign.key <image>`.
6. Production Cluster (K8s) uses a policy (Kyverno/OPA) to verify the signature before pulling.

## 🧠 Resource Behavior
- **Storage**: SBOMs and signatures add a few kilobytes of metadata to your registry.
- **CPU**: Verification happens during the pull process and adds negligible latency (<100ms).

## 📐 ASCII Diagrams (REQUIRED)

```text
       SECURE SUPPLY CHAIN PIPELINE
       
[ BUILD ] -> [ SBOM GEN ] -> [ SIGNING ] -> [ REGISTRY ]
   |            |               |               |
(Docker)     (Syft)          (Cosign)        (Push)
                                                |
                                        [ VERIFICATION ]
                                                |
                                       (Admission Controller)
                                                |
                                        [ RUN CONTAINER ]
```

## 🔍 Code (Implementing Syft and Cosign)
```bash
# 1. Generate an SBOM for an image
syft node:18-alpine -o cyclonedx-json > node-sbom.json

# 2. Sign an image (Manual method)
# Generate keys first: cosign generate-key-pair
cosign sign --key cosign.key myregistry.com/my-app:latest

# 3. Verify the signature
cosign verify --key cosign.pub myregistry.com/my-app:latest

# 4. Attaching an SBOM to a container image
cosign attach sbom --sbom node-sbom.json myregistry.com/my-app:latest
```

## 💥 Production Failures
- **The "Stale Signature"**: You rotate your signing keys but forget to update the Admission Controller in your production cluster. All new deployments start failing because the "new" signatures are being verified against the "old" public key.
- **False Sense of Security**: Having an SBOM but never scanning it. An SBOM is just a list; you need a tool like **Grype** to continuously scan that list for newly discovered vulnerabilities.

## 🧪 Real-time Q&A
**Q: Is Image Signing the same as Docker Content Trust (DCT)?**
**A**: DCT (Notary v1) was the original attempt, but it was complex and hard to manage. **Cosign (Notary v2)** is the modern industry standard because it's simpler, works with standard registries, and supports "Keyless" signing via OIDC.

## ⚠️ Edge Cases
- **Base Image Trust**: If you sign your image but your base image (`FROM alpine`) is compromised, your signature only proves that *your* additions are yours; it doesn't guarantee the foundation. 
  *Fix*: Only use signed base images from trusted vendors (like Docker Official Images or Google).

## 🏢 Best Practices
- **Automate in CI**: Never sign images manually. Use GitHub Actions or Jenkins.
- **Store SBOMs as Artifacts**: Keep them accessible so security teams can query them during an incident.
- **Use Keyless Signing**: It eliminates the risk of "Leaked Private Keys."

## ⚖️ Trade-offs
| Tool | Ease of Integration | Security Depth |
| :--- | :--- | :--- |
| **Syft/SBOM** | **High** | Medium (Inventory only) |
| **Cosign (Keys)** | Medium | High (Auth integrity) |
| **Cosign (Keyless)**| **High** | **Highest (Identity-based)** |

## 💼 Interview Q&A
**Q: What is an SBOM and why is it important in container security?**
**A**: An SBOM is a Software Bill of Materials. It's a complete, machine-readable list of every component, library, and dependency inside a container image. It is critical because it provides **Visibility**. Without an SBOM, you are running a "black box." If a new vulnerability (like Log4Shell) is announced, an SBOM allows you to instantly search your entire fleet to see which images are affected, rather than having to manually rebuild and scan everything.

## 🧩 Practice Problems
1. Use `Syft` to generate an SBOM for one of your images and explore the JSON output.
2. Install `Cosign`, generate a key pair, and sign a local image. Verify it.

---
Prev: [06_Base_Images_and_Security.md](./06_Base_Images_and_Security.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Container_Lifecycle.md](../Containers/01_Container_Lifecycle.md)
---
