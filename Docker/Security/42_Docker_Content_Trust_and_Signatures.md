# 📌 Topic: Docker Content Trust and Signatures

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are downloading a **Banking App**. 
- How do you know it's the real app and not a fake one made by a hacker to steal your password?
- You check the **Digital Signature**. 

**Docker Content Trust (DCT)** is a digital signature for images. 
When a developer "Signs" an image, they are saying: "I am the real author, and I guarantee this code hasn't been changed by anyone else." If the signature is missing or wrong, Docker will refuse to run the container.

🟡 **Practical Usage**
-----------------------------------
### 1. Enabling Content Trust
By default, it is turned off. You enable it with an environment variable.
```powershell
$env:DOCKER_CONTENT_TRUST=1
```
Now, if you try to `docker pull` an unsigned image, it will fail.

### 2. Signing an Image
When you `docker push`, Docker will ask you to create a "Passphrase" for your signing keys.
```powershell
docker push myrepo/my-app:v1.0
# You will be prompted to create 'Root' and 'Repository' keys.
```

### 3. Verifying an Image
```powershell
docker trust inspect --pretty nginx
```
This shows you who signed the image and when.

🔵 **Intermediate Understanding**
-----------------------------------
### Notary
Docker uses a separate server called **Notary** to store the signatures.
- **Image**: Stored in the Registry (e.g., Docker Hub).
- **Signature**: Stored in Notary.
When you pull, Docker talks to both to make sure they match.

### Key Hierarchy
1. **Root Key**: The "Master Key." Keep this offline in a safe!
2. **Repository Key**: Used to sign specific images.
3. **Delegation Key**: Allow other developers on your team to sign images without giving them the Master Key.

🔴 **Internals (Advanced)**
-----------------------------------
### TUF (The Update Framework)
DCT is based on **TUF**. It is designed to be secure even if the Registry server is hacked. 
- It prevents "Replay Attacks" (where a hacker sends you an old version of a "safe" image that has a bug they know how to use).
- It uses timestamps to ensure you are always getting the latest signed version.

### The `delegations` JSON
Inside the `~/.docker/trust` folder, Docker stores the metadata about who is allowed to sign what. If you lose this folder, you lose your ability to manage your signatures.

⚫ **Staff-Level Insights**
-----------------------------------
### Supply Chain Hardening
In a Staff-level CI/CD pipeline:
1. The code is built into an image.
2. The image is scanned for vulnerabilities (Chapter 31).
3. **ONLY IF** the scan passes, an automated "Signing Bot" uses a Delegation Key to sign the image.
4. The Production cluster is configured to **ONLY** run images signed by the "Signing Bot."
This ensures that **zero** un-scanned code ever touches production.

### Cosign (The Modern Alternative)
Many Staff Engineers are moving from Docker's built-in DCT to a newer tool called **Cosign** (part of the Sigstore project). It is easier to use, doesn't require a Notary server, and works perfectly with Kubernetes.

🏗️ **Mental Model**
Content Trust is a **Wax Seal** on a secret letter. If the seal is broken, don't read it.

⚡ **Actual Behavior**
When DCT is enabled, Docker pulls the image metadata from Notary *before* downloading any layers from the Registry.

🧠 **Resource Behavior**
- **Network**: Adds one extra API call to the Notary server during every pull.

💥 **Production Failures**
- **Lost Passphrase**: You forgot the passphrase for your Root Key. You can **never** sign a new version of that image again. You have to create a brand new repository.
- **Clock Skew**: If your server's clock is wrong, the "Timestamp" in the signature will look invalid, and Docker will refuse to pull the image.

🏢 **Best Practices**
- **Backup your keys** (`~/.docker/trust/private`).
- Use **Delegation keys** for CI/CD bots.
- Turn on DCT in your staging and production environments.

🧪 **Debugging**
```bash
# See the trust data for an image
docker trust inspect myrepo/my-app:v1.0
```

💼 **Interview Q&A**
- **Q**: What is Docker Content Trust?
- **A**: A feature that allows for digital signing and verification of Docker images to ensure their integrity and authenticity.
- **Q**: What happens if you try to pull an unsigned image with `DOCKER_CONTENT_TRUST=1`?
- **A**: The pull will fail with an error message stating that the image does not have trust data.

---
Prev: [41_Docker_Engine_API_and_SDKs.md](../Internals/41_Docker_Engine_API_and_SDKs.md) | Index: [00_Index.md](../00_Index.md) | Next: [43_Advanced_Dev_Workflows_Dev_Containers.md](../Ops/43_Advanced_Dev_Workflows_Dev_Containers.md)
---
