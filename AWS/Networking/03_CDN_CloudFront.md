# 🌐 CDN and CloudFront

## 📌 Topic Name
Amazon CloudFront: Global Content Delivery and Edge Security

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Caches your images and videos at locations around the world so they load faster for users.
*   **Expert**: CloudFront is a **Programmable Global Content Delivery Network (CDN)**. It provides low-latency delivery of static and dynamic content by caching at the edge and optimizing the "Last Mile" connection to the user. Beyond caching, it serves as a **Global Security Perimeter** (integrating with AWS WAF) and a platform for **Edge Computing** (Lambda@Edge and CloudFront Functions).

## 🏗️ Mental Model
Think of CloudFront as a **Global Chain of Vending Machines**.
- **The Origin (S3/ALB)**: The main warehouse.
- **The Edge Location**: The vending machine in your local gym.
- **The Cache**: The snacks inside the machine.
- **Cache Miss**: The machine is empty; it has to call the warehouse to get a new snack.
- **Cache Hit**: You get the snack instantly from the machine.

## ⚡ Actual Behavior
- **Global Network**: 400+ PoPs (Points of Presence) connected to the AWS backbone.
- **SSL/TLS**: CloudFront terminates TLS at the edge, reducing the time for the handshake.
- **Protocol Optimization**: It uses a persistent connection to the Origin to speed up "Cache Misses."

## 🔬 Internal Mechanics
1.  **Cache Key**: A unique identifier for an object, usually consisting of the URL path but can include Query Strings, Headers, or Cookies.
2.  **Tiered Caching (Regional Edge Caches)**: Between the Edge PoP and the Origin, there is a middle layer of "Regional Edge Caches" (REC). This increases the cache hit ratio by pooling requests from multiple nearby Edge PoPs.
3.  **Origin Shield**: A centralized caching layer that further protects your origin from "traffic spikes" when many RECs all have a cache miss at the same time.

## 🔁 Execution Flow (Request)
1.  **Client**: Requests `https://static.com/logo.png`.
2.  **Route 53**: Directs user to the nearest Edge PoP via Anycast.
3.  **Edge PoP**: Checks local cache. If **Hit**, return data.
4.  **REC**: If Edge Miss, check Regional Edge Cache.
5.  **Origin**: If REC Miss, fetch from S3/ALB.
6.  **Response**: Data is streamed back to client and cached at REC and Edge PoP for future users.

## 🧠 Resource Behavior
- **TTLs (Time To Live)**: Minimum, Maximum, and Default. You can control these via the CloudFront console or the `Cache-Control` header from your origin.
- **Invalidation**: Manually forcing CloudFront to delete a cached object. (Costs money after 1000 invalidations per month).

## 📐 ASCII Diagrams
```text
[ USER ] --(SSL/TCP)--> [ EDGE PoP ] --(AWS Backbone)--> [ REGIONAL EDGE CACHE ]
                               |                               |
                        [ CACHE HIT? ]                  [ CACHE HIT? ]
                               |                               |
                        (If Miss, Go to REC)            (If Miss, Go to Origin)
                                                               |
                                                        [ S3 / ALB ORIGIN ]
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name              = aws_s3_bucket.b.bucket_regional_domain_name
    origin_id                = "myS3Origin"
    origin_access_control_id = aws_cloudfront_origin_access_control.default.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "myS3Origin"

    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

## 💥 Production Failures
1.  **The "Stale Content" Disaster**: You release a new version of your JS file but don't change the filename. CloudFront serves the old version for hours because the TTL hasn't expired. **Solution**: Use **Cache Busting** (e.g., `main.v2.js`).
2.  **Cache Poisoning**: An attacker sends a malicious header that gets cached by CloudFront. Subsequent users receive the malicious response.
3.  **Inadvertent Origin Overload**: You misconfigure the Cache Key to include a unique session ID. Every single user gets a "Cache Miss," and your Origin (ALB) crashes under the 100% traffic load.

## 🧪 Real-time Q&A
*   **Q**: Can CloudFront speed up dynamic content (API calls)?
*   **A**: Yes! Even if you don't cache the response, CloudFront optimizes the TCP handshake and uses the high-speed AWS backbone to talk to your Origin, which is faster than the public internet.
*   **Q**: What is Lambda@Edge?
*   **A**: It allows you to run Node.js/Python code *at the edge* to modify requests/responses (e.g., A/B testing, header manipulation).

## ⚠️ Edge Cases
*   **Price Classes**: You can choose to exclude expensive regions (like South America or Australia) from your distribution to save money.
*   **Signed URLs**: Used to provide time-limited access to private content (e.g., a paid video stream).

## 🏢 Best Practices
1.  **Use Origin Access Control (OAC)** to ensure users can only access S3 via CloudFront, not directly.
2.  **Version your assets**: `app.js?v=1` is good, but `app.v1.js` is better for CDN caching.
3.  **Enable Gzip/Brotli compression** to reduce data transfer costs and improve speed.

## ⚖️ Trade-offs
*   **High Cache Hit Ratio**: Faster for users, lower cost at origin, but risk of serving stale content.
*   **Low TTL / No Cache**: Always fresh content, but higher load on origin and higher latency.

## 💼 Interview Q&A
*   **Q**: How do you prevent users from bypassing CloudFront and hitting your S3 bucket directly?
*   **A**: I would use **Origin Access Control (OAC)**. I would update the S3 Bucket Policy to only allow `s3:GetObject` from the specific CloudFront Service Principal and then remove all other public access.

## 🧩 Practice Problems
1.  Create a CloudFront distribution for an S3 bucket and verify that the `X-Cache` header says `Hit from cloudfront`.
2.  Write a CloudFront Function that redirects users to a `/mobile` path if their `User-Agent` header indicates a smartphone.

---
Prev: [02_DNS_Route53.md](../Networking/02_DNS_Route53.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_API_Gateway_Internals.md](../Networking/04_API_Gateway_Internals.md)
---
