# CloudFront Deep Dive

## What Is This Service?
Amazon CloudFront is a fast Content Delivery Network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds.

## Why This Service Exists
If your S3 bucket hosting your React app is located in Virginia (`us-east-1`), a user in Australia has to wait for data packets to travel across the globe, resulting in a slow, blank loading screen. CloudFront exists to aggressively cache your frontend files in Edge Locations around the world so the Australian user downloads the site from a data center in Sydney.

## Real World Analogy
CloudFront is like a **Global Delivery Franchise**.
Instead of shipping every pizza from one kitchen in New York (S3) to customers in London and Tokyo, you build local distribution hubs (Edge Locations) in those cities. When a customer orders, they get the pizza hot and fast from the local hub.

## How It Works
1. You configure a CloudFront "Distribution".
2. You set the "Origin"—the source of truth (e.g., your S3 bucket or your Application Load Balancer).
3. When User A in Paris requests `index.html`, CloudFront routes them to the Paris Edge Location.
4. If the Paris Edge doesn't have the file (a cache miss), it fetches it from the S3 Origin, sends it to the user, and caches it locally.
5. When User B in Paris requests the same file, it is served instantly from the local cache (a cache hit).

## Core Concepts
- **Origin**: The source of the content (S3 bucket, EC2 instance, ALB).
- **Edge Location**: The local data centers where content is cached (over 400 globally).
- **TTL (Time to Live)**: How long a file stays in the cache before CloudFront checks the origin for a newer version.
- **Invalidation**: Manually forcing CloudFront to delete a cached file so it pulls the fresh version from the origin immediately.

## MERN Stack Integration
- **React SPA**: CloudFront is mandatory. It sits in front of your S3 bucket, serving the compiled CSS/JS/HTML at lightning speed. It also provides free, automated SSL/TLS certificates for your custom domain.
- **Next.js**: CloudFront can cache SSR responses or static pages. AWS Amplify automatically provisions CloudFront for Next.js deployments to handle Edge routing.
- **Express APIs**: You can put CloudFront in front of your Application Load Balancer to cache frequent, read-only API requests (like fetching a list of public products), drastically reducing load on your Node.js backend.

## Production Impact
- **Latency**: Reduces load times from 800ms down to 20ms for global users, dramatically improving SEO and user experience.
- **Security**: CloudFront absorbs DDoS attacks. Since it sits in front of S3 or your ALB, massive traffic spikes hit the edge caches, not your actual infrastructure.

## Real Production Use Cases
- An e-commerce MERN application uses CloudFront to serve all product images. Because images rarely change, the TTL is set to 1 year. The Express backend never has to serve a single image, keeping compute costs near zero.

## Production Best Practices
- **Cache Invalidation is Slow**: Don't rely on manual invalidations for CI/CD. Instead, configure Webpack or Vite to inject content hashes into your React filenames (e.g., `main.a2b4c6.js`). Since the filename changes on every deployment, you never have to invalidate the cache—CloudFront just caches the new file.
- **Origin Access Control (OAC)**: Never leave your S3 bucket public. Restrict S3 bucket access so ONLY CloudFront can read from it using OAC.

## Security Best Practices
- **Geo-Restriction**: If your application is only legally allowed to operate in the US and Canada, you can configure CloudFront to instantly block requests from all other countries.
- **WAF Integration**: Attach AWS Web Application Firewall (WAF) to CloudFront to block SQL injections and malicious bots before they ever reach your Node.js servers.

## Cost Optimization Tips
- **Price Classes**: If you don't have users in South America or Australia (which have higher bandwidth costs), configure CloudFront to use `Price Class 100` (North America and Europe only) to save money.

## Common Mistakes
- **React Router 404s**: React SPAs handle routing internally. If a user directly visits `https://yourdomain.com/dashboard`, CloudFront will look for a file named `dashboard` in S3 and return a 403 or 404. You must configure CloudFront Custom Error Responses to catch 404s and return `/index.html` with a 200 OK.

## Debugging & Troubleshooting
- **Seeing old code after deployment**: The #1 CloudFront issue. Your browser or CloudFront is caching the old `index.html`. Trigger a cache invalidation for `/*` in the AWS console.

---
Prev : [./03_S3_Deep_Dive.md](./03_S3_Deep_Dive.md) | Index : [../00_Index.md](../00_Index.md) | Next : None
---
