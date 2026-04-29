# 🛡️ Network Security

## 📌 Topic Name
Defense in Depth: Layered Network Security in AWS

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Use firewalls and private subnets to protect your servers.
*   **Expert**: Network security is a **Layered Defense Strategy** that starts at the Edge and goes all the way to the Application. It involves **DDoS Protection (Shield)**, **Web Application Filtering (WAF)**, **Subnet Isolation**, **Security Groups/NACLs**, and **Traffic Inspection**. A Staff engineer doesn't just "block IPs"; they use **Managed Rules**, **Rate Limiting**, and **VPC Flow Logs** to detect and mitigate threats in real-time.

## 🏗️ Mental Model
Think of Network Security as a **Fortified Castle**.
- **The Moat**: AWS Shield (DDoS protection).
- **The Gatekeeper**: WAF (Inspects the "cargo" of the visitors).
- **The Outer Wall**: Public Subnets / IGW.
- **The Inner Wall**: Private Subnets / NACLs.
- **The Bodyguards**: Security Groups (Protecting specific people/instances).

## ⚡ Actual Behavior
- **AWS Shield Standard**: Automatically enabled for all customers at no cost. Protects against common Layer 3/4 DDoS attacks.
- **AWS WAF**: Inspects HTTP requests. Can block SQL injection, Cross-Site Scripting (XSS), and bot traffic.
- **Network Firewall**: A managed, stateful firewall for inspecting VPC traffic (including East-West traffic between subnets).

## 🔬 Internal Mechanics
1.  **WAF Web ACLs**: Consist of rules that evaluate properties like IP address, country, headers, and URI strings.
2.  **Traffic Mirroring**: Allows you to copy network traffic from an ENI and send it to an out-of-band security tool (like an IDS) for deep packet inspection without impacting the production path.
3.  **VPC Flow Logs**: Captures metadata about the IP traffic going to and from network interfaces in your VPC. Data is sent to CloudWatch Logs or S3.

## 🔁 Execution Flow (Security Stack)
1.  **Shield**: Absorbs Layer 3/4 flood.
2.  **WAF**: Inspects the HTTP payload. Blocks if "SQLi" detected.
3.  **ALB**: Terminates TLS and checks for valid certificate.
4.  **Security Group**: Only allows traffic from the ALB's security group on Port 8080.
5.  **EC2**: Receives the clean, authorized request.

## 🧠 Resource Behavior
- **Managed Rules**: AWS provides "pre-packaged" rules for WAF that cover the OWASP Top 10, so you don't have to write regex for every attack type.
- **VPC Ingress Routing**: Allows you to redirect all traffic entering a VPC through a security appliance (like a firewall) before it reaches its destination.

## 📐 ASCII Diagrams
```text
[ INTERNET ]
     |
[ AWS SHIELD (DDoS) ]
     |
[ AWS WAF (L7 Filter) ]
     |
[ PUBLIC SUBNET ] ----> [ ALB ]
                           |
[ PRIVATE SUBNET ] ----> [ SECURITY GROUP ] ----> [ EC2 ]
```

## 🔍 Code / IaC (WAF Rule)
```hcl
resource "aws_wafv2_web_acl" "main" {
  name        = "web-acl"
  scope       = "REGIONAL"
  description = "WAF with SQLi protection"

  default_action {
    allow {}
  }

  rule {
    name     = "SQLiRule"
    priority = 1
    action {
      block {}
    }
    statement {
      sqli_match_statement {
        field_to_match {
          all_query_arguments {}
        }
        text_transformation {
          priority = 0
          type     = "URL_DECODE"
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "sqli-rule"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "web-acl"
    sampled_requests_enabled   = true
  }
}
```

## 💥 Production Failures
1.  **False Positives**: A WAF rule is too aggressive and starts blocking valid user requests (e.g., a "search" query that looks like SQL). **Solution**: Use "Count" mode before "Block" mode.
2.  **Log Overload**: Enabling VPC Flow Logs for a high-traffic VPC and sending them to CloudWatch Logs. The cost of logging can exceed the cost of the compute. **Solution**: Send to S3 or use "Parquet" format.
3.  **Security Group "Any" Rule**: A developer opens port 22 to `0.0.0.0/0` "just for testing." The instance is compromised by a botnet within 15 minutes.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between Shield Standard and Shield Advanced?
*   **A**: Advanced ($3000/month) gives you 24/7 access to the DDoS Response Team (DRT), cost protection against scaling spikes during an attack, and advanced L7 protection.
*   **Q**: Can I use WAF with EC2 directly?
*   **A**: No. WAF must be attached to an ALB, API Gateway, AppSync, or CloudFront.

## ⚠️ Edge Cases
*   **Gateway Load Balancer (GWLB)**: The preferred way to scale 3rd party firewalls (like Palo Alto or Fortinet) in AWS.
*   **AWS Network Firewall**: Uses the Suricata rule engine for deep packet inspection.

## 🏢 Best Practices
1.  **Private Subnets for EVERYTHING**: Never put a DB or App server in a public subnet.
2.  **Use Managed Rulesets** for WAF to stay updated on new threats.
3.  **Enable VPC Flow Logs** for all production VPCs.

## ⚖️ Trade-offs
*   **Deep Packet Inspection (Firewall)**: Highest security but adds latency and cost.
*   **Security Groups**: Lowest latency and zero cost but limited to L4 (IP/Port).

## 💼 Interview Q&A
*   **Q**: How would you protect a web application from a Layer 7 DDoS attack (e.g., thousands of valid-looking HTTP requests)?
*   **A**: I would implement **AWS WAF with Rate Limiting**. I would set a rule that blocks any IP address that sends more than 2,000 requests in a 5-minute window. I would also use **CloudFront** to distribute the load and **Shield Advanced** for specialized DDoS support.

## 🧩 Practice Problems
1.  Identify the top 10 IP addresses hitting your web server by analyzing VPC Flow Logs in Athena.
2.  Configure a WAF rule that only allows traffic from a specific country.
