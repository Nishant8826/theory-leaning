# Route53

## Why This Exists
Computers talk to each other using IP addresses like `198.51.100.24`. Humans are terrible at remembering numbers; we like names like `google.com`. AWS Route53 is a highly available Domain Name System (DNS) service. It acts as the translator that turns human-friendly domain names into computer IP addresses so your browser can find your servers.

## Real World Analogy
Think of a **Phonebook** or a **Contacts App**.
You don't memorize your plumber's phone number. When you need a pipe fixed, you open your contacts, search for "Plumber", and the phone dials the number `555-0199`. 
Route 53 is the internet's phonebook. Your browser asks "What is the number for `netflix.com`?" and Route53 replies "Go to IP `54.23.11.90`".

## Core Concepts
*   **Hosted Zone:** The container for all your DNS records for a specific domain (like a folder for `mywebsite.com`).
*   **A Record:** Maps a domain name directly to an IPv4 address.
*   **CNAME Record:** Maps a domain name to *another* domain name (like forwarding `www.app.com` to `app.com`).
*   **Alias Record:** A special AWS-only feature. It maps your domain to another AWS resource (like a Load Balancer or S3 bucket) directly, without incurring DNS query charges.
*   **TTL (Time To Live):** How long (in seconds) other servers on the internet should "remember" this IP before asking Route53 again.

## Architecture / Flow
1. User types `www.myapp.com` in Chrome.
2. The request hits a global DNS resolver, which eventually queries **Route53**.
3. Route53 checks the Hosted Zone for `myapp.com`.
4. It finds an Alias Record pointing to an AWS Application Load Balancer.
5. Route53 returns the IP address of that Load Balancer to the user's browser.
6. The browser connects to the Load Balancer.

## Practical Commands
*   *(Route53 is mostly managed via the AWS Console or Terraform. DNS changes are visual and structural).*
*   Terminal debugging: `nslookup myapp.com` or `dig myapp.com` to trace how the internet is resolving your domain.

## Hands-On Exercise
Buy a cheap domain (or use a free one). In AWS Route53, create a Hosted Zone. Copy the 4 "NS" (Name Server) records AWS gives you and paste them into your domain registrar's settings. Then, create an "A Record" in Route53 pointing `test.yourdomain.com` to the Public IP of an EC2 instance.

## Mini Project
**"Failover Routing"**
Route53 is smart. Set up a "Failover Routing Policy". Create a primary record pointing to an EC2 web server, and set up a Route53 Health Check on it. Create a secondary record pointing to a static S3 bucket hosting a "Sorry, we are down for maintenance" HTML page. Turn off the EC2 instance and watch Route53 automatically redirect traffic to the S3 bucket!

## Real Production Usage
Enterprise companies use Route53 to route traffic globally. If a user in Japan visits `myapp.com`, Route53's "Latency-Based Routing" detects their location and automatically sends them to the Tokyo AWS datacenter instead of the US datacenter, ensuring the fastest possible page load.

## Common Mistakes
*   **Impatience:** DNS caching is real. If you change an IP address in Route53, you might not see the change on your laptop for 10 minutes (or up to 24 hours depending on the TTL). Don't blindly make 5 changes thinking "it's not working".
*   **Using CNAME for Root Domains:** Standard DNS rules forbid using a CNAME on the root domain (`myapp.com`). You must use an AWS **Alias Record** to point your root domain to an AWS Load Balancer.

## Debugging Guide
*   **Site can't be reached?** Use a site like `whatsmydns.net` to see if your domain has propagated globally. If it hasn't, you either messed up your Name Servers at the registrar, or you just need to wait.

## Best Practices
*   **Use Alias Records:** Whenever you are pointing a domain to an AWS service (ALB, CloudFront, S3), always check the "Alias" toggle. It's faster, cheaper, and automatically updates if the underlying AWS service changes its internal IPs.

## Interview Questions
*   **Q: What is the purpose of TTL (Time To Live) in DNS?**
    *   *A: It tells intermediate DNS servers and browsers how long they should cache the DNS record. A low TTL (60s) is good during migrations so changes propagate quickly, while a high TTL (86400s) reduces traffic to the DNS server.*

## Summary
Route53 is the front door of your cloud architecture. It bridges the gap between human language and the complex network architecture running behind the scenes.

---
Prev: [04_load_balancer.md](./04_load_balancer.md) | Index: [Index](../00_index.md) | Next: [06_ssl_setup.md](./06_ssl_setup.md)
