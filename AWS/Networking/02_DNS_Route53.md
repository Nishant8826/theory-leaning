# 🌐 DNS and Route 53

## 📌 Topic Name
Amazon Route 53: Scalable DNS and Domain Management

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Route 53 turns domain names (google.com) into IP addresses.
*   **Expert**: Route 53 is a **Highly Available, Global Authoritative DNS Service**. It is built on a network of **Anycast** edge locations worldwide. It provides not just name resolution, but also **Traffic Flow** management through sophisticated routing policies: Latency-based, Geo-location, Failover, and Multi-value answer. It is one of the few AWS services with a **100% Availability SLA**.

## 🏗️ Mental Model
Think of Route 53 as a **Global GPS for the Internet**.
- **The Map**: The Hosted Zone containing your records.
- **Anycast**: Multiple "Help Desks" around the world that all have the same phone number (IP). You are automatically routed to the one closest to you.
- **Routing Policy**: The logic that says "If you're in London, go to the Dublin data center. If Dublin is down, go to Frankfurt."

## ⚡ Actual Behavior
- **Authoritative**: Route 53 doesn't "ask" other servers for the answer; it *is* the source of truth for your domain.
- **Propagation**: Changes to Route 53 records usually propagate globally within 60 seconds, but external resolvers might cache the old record based on its **TTL (Time To Live)**.
- **Health Checks**: Route 53 can monitor your endpoints and automatically remove an IP from a DNS response if the endpoint is unhealthy.

## 🔬 Internal Mechanics
1.  **Anycast Routing**: Route 53 uses the same set of 4 IP addresses (Nameservers) for your hosted zone, but these IPs are announced via BGP from all 200+ AWS edge locations. This ensures that a DNS query from Tokyo is answered in Tokyo.
2.  **Health Check Data Plane**: A global fleet of "checkers" pings your IP. If the majority see a failure, they signal the DNS control plane to update the records.
3.  **Alias Records**: A special AWS-specific record type that points to an AWS resource (ALB, S3, CloudFront). Unlike a CNAME, an Alias record can be used for the **Zone Apex** (the naked domain like `myapp.com`).

## 🔁 Execution Flow (Recursive Query)
1.  **User**: Types `api.myapp.com`.
2.  **ISP Resolver**: Checks its cache. If empty, it asks the Root servers.
3.  **Root**: Points to the `.com` TLD servers.
4.  **TLD**: Points to the Route 53 Nameservers for `myapp.com`.
5.  **Route 53**: Receives the query at the nearest Anycast PoP and returns the IP (or Alias).
6.  **ISP Resolver**: Returns IP to User and caches it for the duration of the TTL.

## 🧠 Resource Behavior
- **Public Hosted Zone**: Visible to the whole internet.
- **Private Hosted Zone**: Only visible within specific VPCs (useful for internal microservices like `db.internal.prod`).

## 📐 ASCII Diagrams
```text
[ USER ] --(DNS Query)--> [ ROUTE 53 ANYCAST (Global) ]
                                |
      +-------------------------+-------------------------+
      |                         |                         |
 [ US-EAST-1 ]             [ AP-SOUTH-1 ]            [ EU-WEST-1 ]
 (IP: 1.1.1.1)             (IP: 1.1.1.1)             (IP: 1.1.1.1)
      |                         |                         |
[ HEALTH CHECK ] <--------- [ MONITORING ] ---------> [ HEALTH CHECK ]
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_route53_zone" "primary" {
  name = "example.com"
}

# Alias Record for ALB (Zone Apex)
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "example.com"
  type    = "A"

  alias {
    name                   = aws_lb.web_alb.dns_name
    zone_id                = aws_lb.web_alb.zone_id
    evaluate_target_health = true
  }
}

# Latency-based Routing
resource "aws_route53_record" "api_us" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "api.example.com"
  type    = "A"
  set_identifier = "us-api"
  latency_routing_policy {
    region = "us-east-1"
  }
  ttl = 60
  records = ["1.2.3.4"]
}
```

## 💥 Production Failures
1.  **TTL Too High**: You update your server IP, but set the TTL to 86400 (24 hours). Users are stuck hitting the old, dead IP for a full day.
2.  **Missing Health Checks**: You have two IPs for failover but no health check. One server dies, but Route 53 keeps sending 50% of traffic to the dead server.
3.  **Private DNS Conflict**: You name your internal domain `google.com` inside a Private Hosted Zone. Your EC2 instances will no longer be able to reach the *real* Google.

## 🧪 Real-time Q&A
*   **Q**: What is a "Zone Apex"?
*   **A**: It's the root of your domain (e.g., `example.com` with no `www`). Standard DNS doesn't allow a CNAME at the apex, which is why AWS created **Alias Records**.
*   **Q**: Does Route 53 support DNSSEC?
*   **A**: Yes, it provides a managed way to sign your DNS records to prevent spoofing.

## ⚠️ Edge Cases
*   **Weighted Routing**: Useful for **Canary Deployments** (send 5% of traffic to the new version).
*   **Split-Horizon DNS**: Having the same domain name (e.g., `dev.com`) return a public IP for external users and a private IP for internal VPC users.

## 🏢 Best Practices
1.  **Use Alias Records** whenever pointing to AWS resources.
2.  **Short TTLs** (60-300s) for dynamic records to allow for fast failover.
3.  **Monitor Health**: Every failover record MUST have a health check attached.

## ⚖️ Trade-offs
*   **Latency vs. Geo-location**: Latency-based routing sends users to the fastest region (measured by AWS). Geo-location sends users to a specific region based on their physical location (better for data residency).

## 💼 Interview Q&A
*   **Q**: How would you implement a Multi-Region Disaster Recovery plan using Route 53?
*   **A**: I would use a **Failover Routing Policy**. The Primary record points to Region A (ALB), and the Secondary points to Region B (Static S3 site or ALB). I would attach a health check to the Primary. If Region A goes down, Route 53 will automatically stop returning Region A's IP and start returning Region B's.

## 🧩 Practice Problems
1.  Set up a health check for an external website and configure an email notification for when it goes down.
2.  Create a "Multi-Value Answer" record set with 3 IPs and verify that DNS queries return a random subset of those IPs.

---
Prev: [01_ELB_ALB_NLB.md](../Networking/01_ELB_ALB_NLB.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [03_CDN_CloudFront.md](../Networking/03_CDN_CloudFront.md)
---
