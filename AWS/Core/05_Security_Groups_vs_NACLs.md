# 🛡️ Security Groups vs. NACLs

## 📌 Topic Name
Network Security: Stateful vs. Stateless Defense-in-Depth

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Security Groups (SGs) are for instances; Network ACLs (NACLs) are for subnets.
*   **Expert**: Security Groups are **Stateful, Distributed Firewalls** that operate at the ENI level. NACLs are **Stateless, Rule-based Firewalls** that operate at the Subnet boundary. SGs use **Connection Tracking**, while NACLs require explicit rules for both inbound and outbound traffic (including ephemeral ports).

## 🏗️ Mental Model
*   **Security Group**: Your personal bodyguard. If they let someone in, that person is automatically allowed to leave. They know exactly who you are talking to.
*   **NACL**: The security gate at the neighborhood entrance. They check IDs on the way in AND the way out. They don't remember you from 5 minutes ago.

## ⚡ Actual Behavior
- **Security Groups**: Default is "Allow all outbound, deny all inbound." If you allow Port 80 in, the response is automatically allowed out via connection tracking.
- **NACLs**: Default for the default VPC is "Allow all." Default for a *custom* NACL is "Deny all." Rules are processed in numerical order (lowest first).

## 🔬 Internal Mechanics
1.  **SG Connection Tracking**: AWS uses a "tracked connections" table in the host hypervisor. There is a limit to how many concurrent connections an instance can track. Once full, new connections are dropped (a common cause of "silent" network failures).
2.  **NACL Throughput**: NACLs are processed by the VPC router. They don't have the same "state" overhead as SGs, making them useful for blocking large-scale CIDRs (e.g., blocking an entire country or a known malicious botnet).
3.  **Distributed Enforcement**: SG rules are pushed to the physical host where the instance lives. NACL rules stay at the logical subnet boundary.

## 🔁 Execution Flow (Inbound Packet)
1.  **Subnet Boundary**: NACL evaluates the packet. If DENY, drop.
2.  **Instance ENI**: Security Group evaluates the packet. If DENY (not in allow list), drop.
3.  **Application**: OS receives the packet.

## 🧠 Resource Behavior
- **SGs are additive**: If you attach 5 SGs, the instance has the union of all ALLOW rules.
- **NACLs are first-match**: Once a rule matches (e.g., Rule 100), no further rules are evaluated.

## 📐 ASCII Diagrams
```text
[ INTERNET ]
     |
[ NACL (Stateless) ] --- Rule 100: Allow 80 In / Rule 200: Allow Ephemeral Out
     |
[ Security Group (Stateful) ] --- Rule: Allow 80 In (Auto-allows Out)
     |
[ EC2 INSTANCE ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# Security Group: Simple Allow HTTP
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# NACL: Must allow return traffic for ephemeral ports
resource "aws_network_acl_rule" "inbound_http" {
  network_acl_id = aws_network_acl.main.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 80
  to_port        = 80
}

resource "aws_network_acl_rule" "outbound_ephemeral" {
  network_acl_id = aws_network_acl.main.id
  rule_number    = 100
  egress         = true
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 1024
  to_port        = 65535 # Crucial for return traffic!
}
```

## 💥 Production Failures
1.  **Ephemeral Port Blockage**: Adding a NACL to block a specific IP but forgetting to allow outbound traffic for ports 1024-65535. Result: The server can receive requests but can't send responses back.
2.  **SG Tracked Connection Exhaustion**: High-traffic servers (Redis, Load Balancers) hitting the `conntrack` limit on smaller instance types, leading to packet loss despite low CPU/Memory.
3.  **Untracked Connections**: On some Nitro instances, certain types of traffic are "untracked" and don't count towards limits, but if you change a rule, it can drop existing connections.

## 🧪 Real-time Q&A
*   **Q**: Can I "Deny" an IP in a Security Group?
*   **A**: No. SGs are "Allow-only." To Deny, you must use a NACL.
*   **Q**: Why would I ever use a NACL?
*   **A**: For a "Broad Brush" security layer (e.g., blocking malicious subnets) or as a backup if an engineer accidentally opens an SG to `0.0.0.0/0`.

## ⚠️ Edge Cases
*   **SG Referencing**: You can allow traffic from "SG-A" to "SG-B." This is better than CIDRs because it follows the instances if their IPs change.
*   **Quota**: Default limit is 60 rules per Security Group.

## 🏢 Best Practices
1.  **Principle of Least Privilege**: SGs should be as tight as possible.
2.  **NACLs for Blacklisting**: Only use NACLs if you need to explicitly DENY traffic or create a DMZ.
3.  **Automation**: Use tools like AWS Firewall Manager to audit these at scale.

## ⚖️ Trade-offs
*   **SGs (Granular)**: Easy to manage but have state overhead.
*   **NACLs (Performant)**: No state overhead but very difficult to manage without breaking return traffic.

## 💼 Interview Q&A
*   **Q**: If a Security Group allows inbound traffic on port 22, do we need an outbound rule to respond to the SSH client?
*   **A**: No, because SGs are stateful. The response is tracked and allowed automatically.

## 🧩 Practice Problems
1.  A user reports they can ping a server but cannot SSH into it. Which firewall (SG or NACL) is most likely the culprit?
2.  Design a NACL rule set that allows a web server to receive traffic on port 443 and communicate with a database on port 5432.

---
Prev: [04_Subnets_Routing.md](../Core/04_Subnets_Routing.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [06_IAM_Deep_Dive.md](../Core/06_IAM_Deep_Dive.md)
---
