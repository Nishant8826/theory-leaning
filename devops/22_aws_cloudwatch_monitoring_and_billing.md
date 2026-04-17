# 22 – AWS CloudWatch Monitoring & Billing Management

---

## Table of Contents

1. [What is AWS CloudWatch?](#1-what-is-aws-cloudwatch)
2. [EC2 Monitoring with CloudWatch](#2-ec2-monitoring-with-cloudwatch)
3. [CloudWatch Alarms](#3-cloudwatch-alarms)
4. [SNS – Simple Notification Service](#4-sns--simple-notification-service)
5. [CloudWatch Dashboards](#5-cloudwatch-dashboards)
6. [AWS Billing Management & Budget Alerts](#6-aws-billing-management--budget-alerts)
7. [Monitoring Best Practices](#7-monitoring-best-practices)
8. [Visual Diagrams](#8-visual-diagrams)
9. [Scenario-Based Q&A](#9-scenario-based-qa)
10. [Interview Q&A](#10-interview-qa)

---

## 1. What is AWS CloudWatch?

### What

AWS CloudWatch is AWS's built-in **observability and monitoring service**. Think of it as a CCTV system for your cloud infrastructure. It automatically collects **metrics** (numbers like CPU usage), **logs** (text records of what happened), and **events** from almost every AWS service.

### Why

Without monitoring, you are flying blind. You won't know:
- Why your application is slow
- When a server is about to crash
- How much money you are burning

CloudWatch solves this by giving you a single place to **watch, alert, and respond** to everything happening inside your AWS account.

### How (Step-by-Step)

1. **AWS services emit data automatically** – Every EC2 instance, RDS database, Lambda function, etc., sends metrics to CloudWatch without any setup.
2. **CloudWatch stores the data** – Metrics are kept for 15 months by default.
3. **You visualize data** – Using graphs and dashboards.
4. **You set alarms** – When a metric crosses a threshold, CloudWatch triggers an action (email, auto-scaling, etc.).
5. **You query logs** – Use CloudWatch Logs Insights to search and filter log data.

### Impact

| With CloudWatch | Without CloudWatch |
|---|---|
| Catch issues before users notice | Users report bugs before you know |
| Optimize cost by seeing idle resources | Pay for servers you don't need |
| Debug fast using centralized logs | Search through many scattered log files |
| Automate responses to incidents | Manual intervention every time |

---

## 2. EC2 Monitoring with CloudWatch

### What

When you launch an EC2 instance, CloudWatch automatically starts collecting basic metrics. You can upgrade to **Detailed Monitoring** for finer granularity.

### Why

By default, AWS gives you metrics every **5 minutes** (Basic Monitoring). If you enable **Detailed Monitoring**, you get metrics every **1 minute** — useful for catching short spikes that 5-minute averages would miss.

### How (Step-by-Step)

1. **Launch your EC2 instance** – During launch, under "Advanced Details", enable "Detailed CloudWatch monitoring".
2. **Navigate to the Monitoring tab** – Open your EC2 instance in the console → click the **Monitoring** tab.
3. **View auto-collected metrics:**
   - CPU Utilization (%)
   - Network In / Network Out (bytes)
   - Disk Read / Disk Write
   - Status Check metrics
4. **Graphs are pre-built** – CloudWatch automatically draws graphs for each metric with time-range selectors (1h, 3h, 12h, 1d, etc.).

### Key Metrics Explained

| Metric | What it tells you |
|---|---|
| **CPU Utilization** | How hard the processor is working (0–100%) |
| **Network In/Out** | How much data is being sent/received by the instance |
| **Disk Read/Write** | How much data the hard disk is reading or writing |
| **Status Checks** | Whether the VM is healthy (System check + Instance check) |

### Impact

- **Enabled:** You can see trends, spot anomalies, and respond before a crash.
- **Not enabled:** You are guessing when something goes wrong and have no historical data to debug with.

---

## 3. CloudWatch Alarms

### What

A CloudWatch Alarm **watches a single metric** and triggers an action when that metric crosses a threshold you define.

Example: "Alert me when CPU Utilization is above 80% for more than 5 minutes."

### Why

You cannot stare at a dashboard 24/7. Alarms automate the watching and notify the right people automatically.

### How (Step-by-Step)

1. Go to **CloudWatch → Alarms → Create Alarm**.
2. **Select a metric** (e.g., EC2 → Per-Instance Metrics → CPU Utilization).
3. **Set the threshold** (e.g., Greater than 80%).
4. **Set the period** – How long the condition must hold before alerting (e.g., 1 data point of 5 minutes = 5 min sustained breach).
5. **Configure actions** – Choose what happens:
   - Send a notification via **SNS**
   - Trigger an **Auto Scaling** action
   - Stop/Reboot/Terminate the instance
6. **Name the alarm** and save.

### Alarm States

```
OK  ──────────────────────────────────►  (Everything is normal)
                  │
                  │  threshold crossed
                  ▼
ALARM  ──────────────────────────────►  (Notification triggered)
                  │
                  │  metric drops below threshold
                  ▼
OK  ──────────────────────────────────►  (Back to normal)

INSUFFICIENT_DATA = not enough data points yet to evaluate
```

### Important Behaviour

- Alarms trigger **continuously** as long as the breach persists — not just once.
- A **single spike** that lasts less than the evaluation period will NOT trigger an alarm (by design — reduces false alerts).
- Configure evaluation periods wisely: too short = noisy; too long = slow to respond.

### Impact

- **With alarms:** Automated detection, faster response, sleeping engineers aren't woken up for false alarms.
- **Without alarms:** Reactive — you find out when a user complains or a service goes completely down.

---

## 4. SNS – Simple Notification Service

### What

SNS (Simple Notification Service) is a **messaging service** that CloudWatch uses to send notifications. CloudWatch doesn't email you directly — it sends a message to an SNS **Topic**, and SNS delivers it to subscribers.

### Why

SNS decouples the alert source from the destination. A single alarm can notify:
- Multiple email addresses
- SMS numbers
- Slack (via Lambda)
- PagerDuty, etc.

### How (Step-by-Step)

1. **Create an SNS Topic** – Name it (e.g., `cpu-alerts`).
2. **Subscribe to the topic** – Add your email address as a subscriber.
3. **Confirm the subscription** – AWS sends a confirmation email; click the link.
4. **Link the topic to your alarm** – When creating a CloudWatch Alarm, choose this SNS topic as the action.
5. **When the alarm fires** → CloudWatch sends to SNS → SNS emails you.

### Flow Diagram

```
EC2 Instance
    │  CPU > 80%
    ▼
CloudWatch Metric
    │  Alarm threshold crossed
    ▼
CloudWatch Alarm
    │  Publishes message
    ▼
SNS Topic  ──────► Email Subscriber 1
           ──────► Email Subscriber 2
           ──────► Lambda Function (Slack, PagerDuty, etc.)
```

---

## 5. CloudWatch Dashboards

### What

A CloudWatch Dashboard is a **custom visual page** where you pin graphs and widgets from multiple AWS services and multiple instances into one single view.

### Why

If you have 10 EC2 instances each in separate monitoring tabs, switching between them is slow and error-prone. A dashboard puts everything in one screen, making it easy for the whole team to see system health at a glance.

### How (Step-by-Step)

1. Go to **CloudWatch → Dashboards → Create Dashboard**.
2. **Name the dashboard** (e.g., `Avenger-Imran-Team`).
3. **Add widgets:**
   - Line chart, bar chart, number, text, alarm status, etc.
4. **Select the metric** to display in each widget (e.g., CPU for Instance-A).
5. **Add more instances to the same graph** – Multiple metrics on one line chart with different colored lines.
6. **Save the dashboard** – It auto-refreshes at configurable intervals.

### Best Practices

- Create **one dashboard per project or environment** (e.g., `prod-web-servers`, `dev-databases`), not one per VM.
- Use **different colors** for each instance on a combined graph to distinguish them easily.
- Pin **alarm status widgets** alongside metric graphs so you see both the data and its health status.

### Impact

- **With dashboards:** Instant situational awareness for the whole team; faster incident response.
- **Without dashboards:** Team members navigate individual service pages; slower to correlate issues across services.

---

## 6. AWS Billing Management & Budget Alerts

### What

AWS charges you for almost every resource you use. Billing Management tools help you understand your current spend, forecast future costs, and get alerted before you overspend.

### Key Tools

| Tool | Purpose |
|---|---|
| **Billing Dashboard** | Overview of total charges this month |
| **Current Bill** | Itemized breakdown (EC2 hours, data transfer, etc.) |
| **Free Tier Usage** | Shows how close you are to hitting free tier limits |
| **AWS Budgets** | Set a spend limit and get notified when you approach it |

### Why

Cloud costs can spiral quickly. Leaving a single EC2 instance running accidentally for a month can result in unexpected charges. Budget alerts are your financial safety net.

### How – Setting Up a Budget Alarm (Step-by-Step)

1. Go to **AWS Billing → Budgets → Create Budget**.
2. Choose **Cost Budget**.
3. Set the **budget amount** (e.g., ₹205 / month).
4. Set **alert thresholds** (e.g., alert at 80% = ₹164 spent).
5. **Add an SNS topic** or enter an email for notifications.
6. **Review and create**.

### Free Tier Tips

- Always check **Free Tier Usage** at the end of each lab.
- Common free tier services: EC2 (750 hrs/month t2.micro), S3 (5 GB), CloudWatch (10 custom metrics, 1M API calls).
- Going over free tier limits = **you get charged** — no automatic warning unless you set it up.

### Bill Forgiveness (Student Tip)

If you accidentally incur charges, AWS may forgive a one-time billing error for students. Contact **AWS Support** → create a billing support case → explain you are a student learning. This is a one-time courtesy, not a guarantee.

### Three Links to Check Every Session

```
1. Billing Dashboard  →  Are my total charges normal?
2. Current Bill       →  Which service is costing me money?
3. Free Tier Usage    →  Am I about to exceed free limits?
```

---

## 7. Monitoring Best Practices

### 1. Avoid Alert Fatigue
**False alerts** desensitize teams. If alarms trigger too often for non-issues, engineers start ignoring them — including real ones.

- Set meaningful thresholds (not too sensitive).
- Use evaluation periods to filter out momentary spikes.
- Tune alarms over time based on actual baselines.

### 2. Create Playbooks (Runbooks)
For **every alarm**, write a short runbook:
- What does this alarm mean?
- What are the first 3 things to check?
- Who to escalate to?

This ensures any team member can respond, not just the person who set up the alarm.

### 3. Consolidate Dashboards
- ❌ Bad: One dashboard per VM → 20 VMs = 20 dashboards
- ✅ Good: One dashboard per project/environment → 3 environments = 3 dashboards

### 4. Always Delete Unused Resources
After labs and testing:
- Terminate EC2 instances
- Delete unused Elastic IPs
- Remove NAT Gateways (they charge per hour)

Unused resources = **wasted money**.

---

## 8. Visual Diagrams

### CloudWatch Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Account                          │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │   EC2    │   │   RDS    │   │  Lambda  │  ...services  │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│       │              │              │                       │
│       └──────────────┴──────────────┘                       │
│                       │ Metrics & Logs                      │
│                       ▼                                     │
│              ┌─────────────────┐                            │
│              │   CloudWatch    │                            │
│              │  ┌───────────┐  │                            │
│              │  │  Metrics  │  │                            │
│              │  ├───────────┤  │                            │
│              │  │   Logs    │  │                            │
│              │  ├───────────┤  │                            │
│              │  │  Alarms   │──┼──► SNS ──► Email/SMS/Slack│
│              │  ├───────────┤  │                            │
│              │  │Dashboards │  │                            │
│              │  └───────────┘  │                            │
│              └─────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### CloudWatch Alarm Lifecycle

```
         Metric Value
              │
              │
    ┌─────────▼──────────┐
    │   Evaluation Period │   (e.g., 5 minutes)
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  Is value > 80%?   │
    └──────┬──────┬──────┘
           │ YES  │ NO
           │      └──────────► State: OK
           ▼
    ┌─────────────────────┐
    │   State: ALARM      │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │  Trigger SNS Topic  │
    └─────────┬───────────┘
              │
    ┌─────────▼───────────┐
    │  Email/SMS sent to  │
    │    Subscribers      │
    └─────────────────────┘
```

### Billing Alert Flow

```
AWS Resources Running
        │
        │ Usage data every hour
        ▼
  AWS Cost Explorer
        │
        │ Compares to budget
        ▼
  AWS Budgets Engine
        │
        │ Threshold reached (e.g., 80% of ₹205 = ₹164)
        ▼
   SNS Topic Triggered
        │
        ▼
   Your Email 📧
  "Warning: You have used 80% of your monthly budget"
```

### Dashboard Consolidation Pattern

```
❌ Per-VM approach (messy):
Dashboard-VM1  │  Dashboard-VM2  │  Dashboard-VM3  ...

✅ Per-Project approach (clean):
┌────────────────────────────────────────┐
│       Project: Avenger-Imran-Team      │
│  ┌──────────┐  ┌──────────┐           │
│  │ VM1 CPU  │  │ VM2 CPU  │  (same   │
│  │  ──────  │  │  ──────  │   graph) │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │VM1 NetIn │  │VM2 NetIn │           │
│  └──────────┘  └──────────┘           │
└────────────────────────────────────────┘
```

---

## 9. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your web application became very slow at 3 AM. By the time you woke up and checked at 8 AM, everything was back to normal. You have no idea what happened.

✅ **Answer:** CloudWatch Logs and Metrics would have captured the CPU, memory, and network data from 3 AM. You can go to CloudWatch → select your EC2 instance → set the time range to 2–4 AM and see exactly what spiked. If you had a CloudWatch Alarm set, you would also have received an email at 3 AM alerting you in real time.

---

🔍 **Scenario 2:** You are a student running multiple EC2 labs and suddenly get an AWS bill for $30. You didn't expect this.

✅ **Answer:** You likely left EC2 instances or Elastic IPs running after your lab. AWS charges for all running resources. Going forward: (1) Always set a Budget Alarm (e.g., ₹205 limit). (2) Check Free Tier Usage after every lab. (3) Terminate all instances when done. For the current charge, contact AWS Support and explain you are a student — they may offer one-time forgiveness.

---

🔍 **Scenario 3:** You manage 20 EC2 instances across 3 projects. You want your team to quickly see if anything is wrong without clicking through 20 different monitoring tabs.

✅ **Answer:** Create 3 CloudWatch Dashboards — one per project. Add all instance metrics for that project onto a single dashboard with different colored lines per instance. Your team now has a single URL per project to check system health instantly.

---

🔍 **Scenario 4:** You set a CloudWatch alarm for CPU > 50%. You are getting emails every 2 minutes even though the application is running fine. The team is starting to ignore alerts.

✅ **Answer:** Your threshold is too sensitive. Review the actual CPU baseline — if normal operation runs at 45–55%, then 50% is not a real problem. Adjust the threshold to 80% or above, and set the evaluation period to require 3 consecutive data points above the threshold before firing. This filters out normal fluctuations and reduces false alerts.

---

🔍 **Scenario 5:** A new team member joins and needs to respond to a CPU alarm at night, but they don't know what to do.

✅ **Answer:** This is where a **runbook** (playbook) helps. For every alarm, document: (1) What the alarm means, (2) First 3 steps to check (e.g., SSH into the instance, run `top`, check for runaway processes), (3) When and who to escalate to. The new team member follows the runbook and can handle incidents independently.

---

## 10. Interview Q&A

---

**Q1. What is Amazon CloudWatch and what are its main components?**

**A:** Amazon CloudWatch is AWS's monitoring and observability service. Its main components are:
- **Metrics** – Time-series numerical data (e.g., CPU utilization, request count)
- **Logs** – Text-based event records collected from applications and services
- **Alarms** – Rules that watch metrics and trigger actions when thresholds are breached
- **Dashboards** – Custom visual pages that display metrics and alarm status
- **Events/EventBridge** – Rules to react to changes in AWS resources automatically

---

**Q2. What is the difference between Basic Monitoring and Detailed Monitoring for EC2?**

**A:**
- **Basic Monitoring** (default, free): Metrics collected every **5 minutes**.
- **Detailed Monitoring** (paid): Metrics collected every **1 minute**.

Detailed monitoring is useful for applications that need faster detection of short-lived performance issues. Basic monitoring is sufficient for most general workloads.

---

**Q3. What are the three states of a CloudWatch Alarm?**

**A:**
1. **OK** – The metric is within the defined threshold.
2. **ALARM** – The metric has crossed the threshold for the configured evaluation period.
3. **INSUFFICIENT_DATA** – There isn't enough data yet to evaluate the alarm (e.g., alarm just created or metric stopped reporting).

---

**Q4. What is SNS and how does it work with CloudWatch Alarms?**

**A:** SNS (Simple Notification Service) is a pub/sub messaging service. CloudWatch Alarms do not send emails directly. Instead, when an alarm fires, it publishes a message to an **SNS Topic**. Any subscribers to that topic (email, SMS, Lambda, HTTP endpoints) receive the notification. This decouples the alerting mechanism from the notification delivery, allowing one alarm to notify multiple destinations simultaneously.

---

**Q5. How would you avoid alert fatigue in a production monitoring setup?**

**A:**
- Set **meaningful thresholds** based on actual performance baselines, not arbitrary numbers.
- Use **evaluation periods** to avoid triggering on momentary spikes (e.g., require 3 consecutive data points above threshold).
- Create **runbooks** so every alert has a defined response procedure.
- **Consolidate dashboards** by project rather than per-resource.
- Regularly **review and tune** alarms — disable or adjust ones that are consistently false positives.

---

**Q6. You accidentally left 5 EC2 instances running over the weekend. How could you have prevented unexpected charges?**

**A:**
- Set up an **AWS Budget Alarm** with a threshold (e.g., $10/month) to receive email warnings before costs escalate.
- Enable **Free Tier Usage Alerts** in the Billing preferences.
- Use **AWS Cost Explorer** to visualize daily spend.
- As a habit: always check the **Billing Dashboard**, **Current Bill**, and **Free Tier Usage** at the end of every lab session and terminate unused resources.

---

**Q7. What is a CloudWatch Dashboard and when would you use one?**

**A:** A CloudWatch Dashboard is a customizable page in the AWS Console that displays metrics and alarm statuses from multiple AWS services in a unified view. You would use it when:
- You manage **multiple instances** and want a consolidated view.
- You need **real-time situational awareness** for a team.
- You want to correlate metrics across services (e.g., EC2 CPU alongside RDS query latency).
- You want to share a health-check URL with your team without giving everyone full AWS console access (via read-only IAM).

---

**Q8. If a CloudWatch Alarm is set with a 5-minute period and threshold of CPU > 80%, and the CPU spikes to 95% for 3 minutes then drops — will the alarm fire?**

**A:** It depends on the evaluation configuration. With a **1-out-of-1 evaluation period of 5 minutes**, CloudWatch averages the data over 5 minutes. A 3-minute spike at 95% followed by normal levels might average below 80% over the full 5-minute window, so the alarm **may not fire**. This is actually a feature — it prevents false alarms from short, harmless spikes. To catch 3-minute spikes, you would need to enable Detailed Monitoring (1-minute intervals) and use shorter evaluation periods.

---

> 📌 **Key Reminder:** Always delete unused AWS resources after labs. Set up a budget alarm before every practice session. Monitor proactively — don't wait for users to report problems.


---
> ← Previous: [`21_NACL_CIDR_VPC_Peering_&_Transit_Gateway.md`](21_NACL_CIDR_VPC_Peering_&_Transit_Gateway.md) | Next: [`23_AWS_Lambda_&_Serverless_Architecture.md`](23_AWS_Lambda_&_Serverless_Architecture.md) →