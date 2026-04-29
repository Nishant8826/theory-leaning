# 📊 Service Quotas and Limits

## 📌 Topic Name
AWS Service Quotas: Managing the Boundaries of the Cloud

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: AWS has limits on how many resources you can create.
*   **Expert**: Service Quotas (formerly Limits) are the **Guardrails of the Multi-Tenant Substrate**. They exist to prevent a single customer from accidentally (or maliciously) consuming all physical capacity in a region and to protect the customer from runaway costs. There are **Soft Limits** (adjustable) and **Hard Limits** (unadjustable).

## 🏗️ Mental Model
Think of Quotas as **Credit Limits on a Credit Card**.
- **Soft Limit**: $5,000. You can call the bank and ask for $10,000.
- **Hard Limit**: Maximum withdrawal per day. The ATM physically cannot give more.

## ⚡ Actual Behavior
When you attempt to create a resource (e.g., `ec2:RunInstances`) and you are at the limit, the API returns a `ServiceQuotaExceededException` or `LimitExceeded`. Quotas are typically **Regional**. Having 1000 instances in `us-east-1` does not impact your limit in `us-west-2`.

## 🔬 Internal Mechanics
1.  **Quota Categories**:
    *   **Resource Quotas**: Max VPCs (5), Max EIPs (5).
    *   **Rate Quotas (API Throttling)**: Max `DescribeInstances` calls per second.
2.  **Service Quotas Dashboard**: A centralized service that allows you to view usage and request increases. It integrates with CloudWatch to alert you when you are at 80% capacity.
3.  **Bursting**: Some API limits allow "bursting"—you can go over the limit for a short period using a token-bucket algorithm.

## 🔁 Execution Flow (Limit Check)
1.  **Request**: `aws ec2 run-instances ...`
2.  **Control Plane**: Checks the internal "Quotas" database for the account/region.
3.  **Evaluation**: `CurrentUsage + Request <= QuotaLimit`.
4.  **Result**: If True, proceed to data plane. If False, return Error.

## 🧠 Resource Behavior
- **Default Limits**: New accounts often have lower limits than established accounts (to prevent fraud).
- **Propagation Time**: When a quota increase is approved, it can take 15-30 minutes for the change to propagate through the AWS control plane.

## 📐 ASCII Diagrams
```text
[ API Request ]
      |
[ Throttling Check (Rate) ] --- Token Bucket Empty? -> Return 429
      |
[ Resource Quota Check ] ------ Current + Req > Limit? -> Return 400
      |
[ Success: Resource Created ]
```

## 🔍 Code / IaC (Terraform)
```hcl
# Requesting a quota increase via Terraform (Self-service)
resource "aws_servicequotas_service_quota" "vpc_limit" {
  quota_code   = "L-F678F1CE" # Code for VPCs per Region
  service_code = "vpc"
  value        = 10 # Increase from default 5 to 10
}
```

## 💥 Production Failures
1.  **EIP Exhaustion**: A script creates new instances but forgets to release Elastic IPs. Soon, the ASG cannot launch new instances because the EIP quota is hit.
2.  **API Throttling during Outage**: During a regional issue, many automated scripts start calling `DescribeInstances` repeatedly, hitting the API rate limit and preventing engineers from seeing the status via the CLI.
3.  **Secondary Account Limits**: Developing in a sub-account but failing to request the same quota increases as the main account, leading to "works in dev, fails in staging" issues.

## 🧪 Real-time Q&A
*   **Q**: How long does it take for a limit increase to be approved?
*   **A**: Simple increases are automated and take minutes. Massive increases (e.g., 5000 GPU instances) require human review and can take days.
*   **Q**: Are there limits that cannot be increased?
*   **A**: Yes. Example: 100 S3 buckets per account (soft) can be increased, but the 10Gbps limit on a single NAT Gateway flow is a physical architectural limit.

## ⚠️ Edge Cases
*   **Throttling vs. Quota**: Throttling is about *speed* (API calls per second). Quota is about *quantity* (Total resources).
*   **Account Warming**: New accounts cannot immediately request massive quotas. You must build "trust" over time.

## 🏢 Best Practices
1.  **Monitor Quotas**: Use CloudWatch Alarms for Service Quotas.
2.  **Request in Advance**: If you are planning a migration or a "Black Friday" event, request increases weeks ahead of time.
3.  **Infrastructure as Code**: Manage quota requests in your IaC repo so they are documented.

## ⚖️ Trade-offs
*   **High Quotas vs. Blast Radius**: Higher quotas allow for more scale but increase the financial risk if a script goes into an infinite loop.

## 💼 Interview Q&A
*   **Q**: What do you do if your application receives a `RateExceeded` error from AWS?
*   **A**: Implement **Exponential Backoff and Jitter** in the client-side code and check if we can optimize the number of API calls (e.g., caching the results of `Describe` calls).

## 🧩 Practice Problems
1.  Identify the quota code for "Running On-Demand Standard instances" in your region.
2.  Calculate how many IP addresses you will need for an EKS cluster with 50 nodes, given the VPC CNI limits and your subnet size.
