# 🛡️ Zero Trust on AWS

## 📌 Topic Name
Zero Trust Architecture: Identity as the New Perimeter

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Don't trust anyone, even if they are "inside" your network. Verify every request.
*   **Expert**: Zero Trust is a **Security Model** based on the principle of "Never Trust, Always Verify." In a traditional "Castle and Moat" model, once you are inside the VPC, you are trusted. In Zero Trust, we move away from **Network-based Trust** (IP addresses) to **Identity-based Trust** (IAM, JWTs, mTLS). Every request must be authenticated, authorized, and encrypted, regardless of where it originates.

## 🏗️ Mental Model
- **Castle and Moat (Traditional)**: Once you cross the bridge (VPN/Direct Connect), you can walk into any room (Service) in the castle.
- **Zero Trust (Modern)**: Every single room has a keypad. Even the employees living in the castle must scan their badge and provide a fingerprint (MFA) to enter every room, every time.

## ⚡ Actual Behavior
- **No Private IPs as Security**: An application doesn't trust a request just because it comes from a 10.x.x.x address.
- **Service-to-Service Auth**: Microservices use **IAM Roles** or **Mutual TLS (mTLS)** to identify each other.
- **Continuous Verification**: Permissions are checked for every single API call, and sessions are short-lived.

## 🔬 Internal Mechanics
1.  **IAM Everywhere**: Using **IAM Roles for Service Accounts (IRSA)** in EKS or **IAM Roles for EC2** to give every workload a unique cryptographic identity.
2.  **VPC Lattice**: A managed service that handles service-to-service communication, providing built-in auth/z and encryption without complex service meshes.
3.  **Verified Access**: Allows users to access internal applications without a VPN, by verifying their identity (via OIDC) and device posture (via CrowdStrike/Jamf) at the edge.

## 🔁 Execution Flow (Zero Trust Request)
1.  **Request**: App A calls App B.
2.  **Identity**: App A signs the request with its **IAM Credentials** (SigV4) or provides an **mTLS Certificate**.
3.  **Verification**: App B (or its proxy/Lattice) verifies the signature/cert.
4.  **Authorization**: IAM or a Policy Engine (like OPA) checks if App A is allowed to call `GET /data` on App B.
5.  **Encryption**: The entire data transfer is encrypted with **TLS**.
6.  **Response**: App B returns data only if all checks pass.

## 🧠 Resource Behavior
- **Least Privilege**: Policies are scoped to the specific action (e.g., `s3:GetObject` instead of `s3:*`).
- **Short-lived Credentials**: Using AWS STS to provide tokens that expire in 15 minutes to 1 hour.

## 📐 ASCII Diagrams
```text
[ WORKLOAD A ] --(Identity: IAM/mTLS)--> [ POLICY GATEKEEPER ]
                                               |
                   +---------------------------+---------------------------+
                   | (Verify Identity)         | (Check Policy)            |
                   V                           V                           V
          [ AUTHENTICATED ] ----------> [ AUTHORIZED ] ----------> [ WORKLOAD B ]
```

## 🔍 Code / IaC (VPC Lattice Service)
```hcl
# Example of a Lattice Service with Auth enabled
resource "aws_vpclattice_service" "my_service" {
  name      = "my-zero-trust-service"
  auth_type = "AWS_IAM" # Enforce IAM Auth for every call
}

resource "aws_vpclattice_auth_policy" "example" {
  resource_identifier = aws_vpclattice_service.my_service.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "vpc-lattice-svcs:Invoke"
      Effect    = "Allow"
      Principal = { "AWS": "arn:aws:iam::123456789012:role/AppARole" }
      Resource  = "*"
    }]
  })
}
```

## 💥 Production Failures
1.  **Certificate Expiry**: In an mTLS-based Zero Trust environment, if your certificate rotation script fails, the entire network goes dark as services stop trusting each other.
2.  **Identity Provider (IdP) Outage**: If your central IdP (e.g., Okta/Azure AD) is down, no one can get a token, and all access is blocked. Zero Trust increases dependency on the Identity plane.
3.  **Performance Overhead**: Performing a full IAM check or TLS handshake for every single packet can add latency to extremely chatty microservices. **Solution**: Use **VPC Lattice** or hardware-accelerated TLS.

## 🧪 Real-time Q&A
*   **Q**: Does Zero Trust mean I don't need a VPC?
*   **A**: No. VPC provides "Layer 3/4 Hygiene" and prevents accidental exposure, but it is no longer your *only* line of defense.
*   **Q**: What is the "Identity Plane"?
*   **A**: It's the infrastructure that manages Who can do What (IAM, Cognito, Active Directory).

## ⚠️ Edge Cases
*   **Legacy Apps**: Apps that don't support modern auth/z. You can use a "Sidecar" (like Envoy/App Mesh) to add the Zero Trust layer without changing the app code.
*   **Device Posture**: Denying access even to an authorized user if their laptop doesn't have the latest security patches.

## 🏢 Best Practices
1.  **Use IAM Roles for EVERYTHING**.
2.  **Encrypt in Transit**: Use TLS for all internal traffic.
3.  **Minimize Blast Radius**: Use micro-segmentation so that a compromise of one service doesn't lead to a total network takeover.

## ⚖️ Trade-offs
*   **Zero Trust**: Maximum security, highly resilient to insider threats, but higher complexity and operational overhead.
*   **Castle-and-Moat**: Simpler to manage and lower latency, but extremely vulnerable once the perimeter is breached.

## 💼 Interview Q&A
*   **Q**: How would you move an organization from a VPN-based model to a Zero Trust model on AWS?
*   **A**: 1. Implement **AWS Verified Access** for human-to-app traffic. 2. Use **VPC Lattice** for service-to-service traffic to enforce IAM authentication. 3. Ensure every workload has a unique **IAM Role**. 4. Gradually move security rules from NACLs/SGs (IP-based) to IAM Policies (Identity-based).

## 🧩 Practice Problems
1.  Configure an S3 bucket to only allow access if the request comes from an IAM role with a specific `SecurityLevel` tag.
2.  Set up VPC Lattice between two VPCs and enforce IAM authentication for a cross-VPC API call.

---
Prev: [04_Network_Security.md](../Security/04_Network_Security.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [06_Compliance_and_Auditing.md](../Security/06_Compliance_and_Auditing.md)
---
