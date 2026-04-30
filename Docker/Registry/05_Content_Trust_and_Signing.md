# 📌 Topic: Content Trust and Signing (Notary)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Image Signing is like a digital verified badge. It proves that the image was built by your company and hasn't been changed by a hacker.
**Expert**: **Docker Content Trust (DCT)** is the implementation of **The Update Framework (TUF)** using **Notary**. It uses a hierarchy of keys (Root, Targets, Snapshot, Timestamp) to ensure the integrity and freshness of image data. Staff-level engineering requires understanding that signing is a **Defense Against Supply Chain Attacks**. If a hacker gains access to your registry and replaces your "Nginx" image with a malicious one, the signature will be missing or invalid, and a Docker client with DCT enabled will refuse to pull it.

## 🏗️ Mental Model
- **The Sealed Package**: You order a medication. It arrives in a box with a holographic seal. If the seal is broken or missing, you don't take the medicine. Image signing is that holographic seal.

## ⚡ Actual Behavior
- **Enforcement**: If you set `export DOCKER_CONTENT_TRUST=1`, your Docker client will **REFUSE** to pull any image that isn't signed.
- **The Warning**: If you try to push an unsigned image with DCT enabled, Docker will demand you create signing keys first.

## 🔬 Internal Mechanics (The Keys)
1. **Root Key**: The master key. Should be stored offline (Hardware Security Module or YubiKey).
2. **Targets Key**: Used to sign specific image tags.
3. **Snapshot Key**: Ensures that the collection of tags in a repository is consistent.
4. **Timestamp Key**: Prevents "Replay Attacks" where a hacker tries to feed you an old, signed version of an image with known bugs.

## 🔁 Execution Flow (The Signing Process)
1. Developer enables DCT: `export DOCKER_CONTENT_TRUST=1`.
2. Developer runs `docker push my-repo:v1`.
3. Docker prompts for a "Root Key" passphrase.
4. Docker generates keys and signs the manifest.
5. The signature (metadata) is pushed to the **Notary Server** (separate from the Registry).
6. When someone pulls the image, their Docker client checks the Notary Server to verify the signature.

## 🧠 Resource Behavior
- **Security**: Provides "Non-repudiation"—you can prove exactly who signed an image and when.
- **Complexity**: Managing passphrases and key backups is the hardest part of DCT. If you lose the Root Key, you can never sign that repository again.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DOCKER CONTENT TRUST (DCT)
       
[ Developer ] --( Push + Sign )--> [ Docker Registry ]
     |                                    |
( Signing Keys )                  [ Notary Server ]
     |                                    |
     +-----------------( Verify )---------+
                                          |
[ Prod Server ] <---( Pull Blocked if Unsigned )---
```

## 🔍 Code (Enabling and Signing)
```bash
# 1. Enable Content Trust in your shell
export DOCKER_CONTENT_TRUST=1

# 2. Push and Sign (Docker will ask for passphrases)
docker push myregistry.com/my-app:v1

# 3. View signatures for an image
docker trust inspect --pretty myregistry.com/my-app:v1

# 4. Revoke a signature (If an image is found to be vulnerable)
docker trust revoke myregistry.com/my-app:v1
```

## 💥 Production Failures
- **The "Lost Key" Lockout**: The person who set up image signing leaves the company. They took the passphrases with them. You can't push new versions of your app because the client requires a signature you can't provide.
  *Fix*: Use **Keyless Signing** (Cosign) or a centralized Key Management Service (KMS).
- **Notary Server Down**: Your registry is up, but the Notary server is down. Production servers can't pull signed images because they can't verify the signatures.

## 🧪 Real-time Q&A
**Q: Is Docker Content Trust (Notary v1) still the best way to sign images?**
**A**: It's being replaced. Notary v1 was very hard to manage. The industry is moving toward **Cosign (Notary v2)**. Cosign stores signatures as standard objects in the registry itself, making it much easier to use with modern tools like Kubernetes.

## ⚠️ Edge Cases
- **Delegation**: You can "delegate" signing power to other users or CI/CD systems without giving them the Root Key. This is essential for team-based development.

## 🏢 Best Practices
- **Sign in CI/CD**: Use a "Robot" targets key in your Jenkins pipeline.
- **Offline Root Key**: Never keep your Root Key on a networked computer.
- **Verify at Runtime**: Use an admission controller in Kubernetes (like Kyverno) to enforce that only signed images can be deployed.

## ⚖️ Trade-offs
| Feature | No Signing | Notary (DCT) | Cosign (Modern) |
| :--- | :--- | :--- | :--- |
| **Security** | Low | **High** | **High** |
| **Ease of Use** | **Highest** | Low | Medium |
| **Portability** | High | Low | **High** |

## 💼 Interview Q&A
**Q: What is a Replay Attack in the context of Docker images and how does signing prevent it?**
**A**: A Replay Attack is when an attacker intercepts a request for an image and provides an older, validly signed version of that image that has known security vulnerabilities. Docker Content Trust prevents this using a **Timestamp Key**. The Notary server generates a short-lived timestamp record for the image. If the timestamp is too old, the Docker client will refuse the pull, even if the image signature is technically valid, ensuring you only run the most recent and secure versions of your code.

## 🧩 Practice Problems
1. Enable `DOCKER_CONTENT_TRUST=1` and try to pull a popular unsigned image from a random registry. Observe the error.
2. Generate a key pair and sign a local image. Inspect the signature metadata.
3. Compare the UX of `docker trust` with the `cosign` CLI tool.

---
Prev: [04_Cloud_Registries_ECR_GCR.md](./04_Cloud_Registries_ECR_GCR.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Docker_Daemon_Security.md](../Security/01_Docker_Daemon_Security.md)
---
