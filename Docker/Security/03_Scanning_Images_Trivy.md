# 📌 Topic: Scanning Images (Trivy and Clair)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Image Scanning is like an antivirus for your Docker images. It looks at the libraries and software inside your image and checks them against a list of known "bugs" or security holes (CVEs).
**Expert**: Image Scanning is the implementation of **Vulnerability Management** in the CI/CD pipeline. It involves "Deep Packet Inspection" of the image layers and the application dependencies (e.g., `package.json` or `requirements.txt`). Staff-level engineering requires integrating scanners like **Trivy** or **Clair** into every build, setting **Severity Thresholds** (e.g., "Fail the build if a CRITICAL vulnerability is found"), and using **Ignore Lists** to manage "Unfixable" or "Low-risk" vulnerabilities to avoid developer fatigue.

## 🏗️ Mental Model
- **The Airport Scanner**: Your image is a suitcase. The scanner looks through the layers to see if you have any prohibited items (vulnerable software). If it finds a "bomb" (Critical CVE), it stops you from boarding the plane (deploying to production).

## ⚡ Actual Behavior
- **Database Driven**: Scanners download a local database of CVEs from sources like NVD (National Vulnerability Database).
- **Layer Analysis**: Scanners don't just look at the final image; they look at every layer to find hidden vulnerabilities that might have been "deleted" in a later layer but still exist in the image history.

## 🔬 Internal Mechanics (Trivy vs Clair)
1. **Trivy**: A "One-stop shop." It scans the OS packages (apt/apk) AND the application dependencies (npm/pip/go). It is fast, easy to use, and runs as a single binary.
2. **Clair**: A more "Enterprise" distributed system. It is usually built into registries (like Harbor or Quay). It requires a database (Postgres) and is designed for high-volume, continuous scanning of a whole registry.
3. **SCA (Software Composition Analysis)**: Both tools perform SCA by parsing lock files to identify exactly which version of a library you are using.

## 🔁 Execution Flow (Trivy in CI)
1. CI Builds image: `my-app:v1`.
2. CI runs `trivy image --severity HIGH,CRITICAL --exit-code 1 my-app:v1`.
3. Trivy identifies a vulnerable version of `openssl`.
4. Trivy returns a non-zero exit code.
5. The CI pipeline stops. The developer is notified.
6. Developer updates the base image or the library and pushes again.

## 🧠 Resource Behavior
- **Network**: The first time a scanner runs, it must download ~100MB of vulnerability data.
- **CPU/RAM**: Scanning large images with many dependencies (like a heavy Java app) can consume 2-4GB of RAM and significant CPU.

## 📐 ASCII Diagrams (REQUIRED)

```text
       VULNERABILITY SCANNING PIPELINE
       
[ Dockerfile ] -> [ Docker Build ] -> [ Image ]
                                         |
                                  +------v------+
                                  |    Trivy    | <--( CVE Database )
                                  +------|------+
                                         |
                       +-----------------+-----------------+
                       |                                   |
                [ No Criticals ]                    [ CRITICAL FOUND ]
                       |                                   |
                ( Deploy to Prod )                  ( Fail CI Build )
```

## 🔍 Code (Using Trivy)
```bash
# 1. Simple scan of a local image
trivy image nginx:latest

# 2. Scan a specific Dockerfile for best-practice violations
trivy config ./Dockerfile

# 3. Fail the build if CRITICAL vulnerabilities exist
trivy image --severity CRITICAL --exit-code 1 my-app:latest

# 4. Generate a JSON report for compliance teams
trivy image --format json --output report.json my-app:latest
```

## 💥 Production Failures
- **The "Day Zero" Panic**: An image was scanned and passed yesterday. Today, a new vulnerability is discovered in `log4j`. The image in production is now vulnerable, but no one knows because it's already "passed" the CI stage.
  *Fix*: Set up **Continuous Scanning** in your registry (ECR/Harbor) that rescans every 24 hours.
- **Developer Fatigue**: A scanner finds 500 "Medium" vulnerabilities that have no fix available. The developers start ignoring the scanner entirely.
  *Fix*: Only fail the build on "CRITICAL" or "HIGH" severities with a "FIX AVAILABLE" status.

## 🧪 Real-time Q&A
**Q: Can a scanner find "Zero-day" vulnerabilities (bugs no one knows about yet)?**
**A**: **No.** Scanners only find *known* vulnerabilities that have a CVE ID. To find unknown bugs, you need **Dynamic Analysis (DAST)** or **Pentesting**.

## ⚠️ Edge Cases
- **Secret Scanning**: Trivy can also look for hardcoded passwords, AWS keys, and certificates inside your image. This is a crucial second layer of defense.

## 🏢 Best Practices
- **Scan Base Images**: Scan your `node:alpine` before you even add your code.
- **Use `.trivyignore`**: To silence false positives or acknowledged risks.
- **Integrate into the IDE**: Use VS Code plugins to see vulnerabilities while you write your Dockerfile.

## ⚖️ Trade-offs
| Feature | Trivy | Clair |
| :--- | :--- | :--- |
| **Ease of Setup** | **Highest** | Low |
| **Scan Speed** | **Fast** | Medium |
| **Registry Integration**| Medium | **High** |

## 💼 Interview Q&A
**Q: How do you handle "Unfixable" vulnerabilities found by a Docker image scanner?**
**A**: First, I evaluate the **Exploitability**. If the vulnerability is in a library we don't actually use or if it requires a configuration we don't have, I might document it as a "Low Risk." Then, I use a `.trivyignore` file to suppress that specific CVE ID. This ensures the CI pipeline stays "Green" while maintaining a clear audit trail of why we chose to ignore that specific vulnerability. I also prioritize switching to a different base image (like Distroless) that doesn't contain the vulnerable package in the first place.

## 🧩 Practice Problems
1. Scan `python:3.9` vs `python:3.9-slim` vs `python:3.9-alpine`. Note the difference in the number of vulnerabilities.
2. Intentionally add a vulnerable library (like an old version of `express`) to a project and see if Trivy catches it.
3. Set up a GitHub Action that runs Trivy on every pull request.

---
Prev: [02_Kernel_Capabilities_and_seccomp.md](./02_Kernel_Capabilities_and_seccomp.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Network_Policies_and_mTLS.md](./04_Network_Policies_and_mTLS.md)
---
